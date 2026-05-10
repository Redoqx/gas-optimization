# Metodologi Penelitian

## Pendekatan Umum

Penelitian ini menggunakan pendekatan **analisis statik berbasis AST (Abstract Syntax Tree)** yang dikombinasikan dengan **pengukuran gas empiris** melalui eksekusi di EVM lokal. Ada tiga fase utama:

```
Fase 1: Deteksi Statik
   File .sol → Compile ke AST → Traversal AST → Deteksi Anti-Pattern → Findings

Fase 2: Pengukuran Gas Empiris
   Kontrak Benchmark → Deploy di Hardhat EVM → estimateGas() → Tabel Penghematan

Fase 3: Validasi Statistik
   Findings + Gas Data → Uji Wilcoxon / Chi-square / Kruskal-Wallis / Spearman → Signifikansi
```

---

## Fase 1: Analisis Statik Berbasis AST

### Mengapa AST?

AST (Abstract Syntax Tree) merepresentasikan struktur logis kode, bukan teks mentah. Keunggulan:
- **Presisi**: Membedakan `owners.length` (state variable) vs `_owners.length` (parameter lokal) berdasarkan posisi struktural
- **Context-aware**: Dapat mendeteksi bahwa identifier berada di dalam loop, bukan di luar
- **Tidak sensitif whitespace/formatting**: Kode yang ditulis berbeda namun semantik sama tetap terdeteksi

Alternatif yang ditolak:
- **Regex/text search**: Tidak tahu apakah `.length` berada di dalam loop atau di kondisi lain
- **Bytecode analysis**: Sulit di-trace kembali ke baris source code

### Pipeline Analisis Statik

```
File .sol
    ↓ detect_solc_ver()       ← auto-detect versi pragma
    ↓ solcx.compile_source()  ← compile dengan py-solcx
    ↓ AST JSON                ← format modern: nodeType/named-fields
    ↓ _normalize_compact()    ← jika solc lama (0.4.x), normalisasi ke format modern
    ↓ walk_ast() + find_nodes()
    ↓ Detector modules (6 modul)
    ↓ List of findings {detector, description, line, severity}
```

### Penanganan Dua Format AST Solidity

Solidity memiliki dua format AST yang berbeda:

| Format | Versi Solidity | Struktur | Contoh Node |
|---|---|---|---|
| **Compact JSON** (lama) | < 0.6 | `name`/`children`/`attributes` | `{"name": "ForStatement", "children": [...]}` |
| **Modern JSON** | ≥ 0.6 | `nodeType`/named-fields | `{"nodeType": "ForStatement", "body": {...}}` |

Solusi: fungsi `_normalize_compact()` secara rekursif mengkonversi format lama ke format modern, sehingga semua detektor hanya perlu handle satu format.

### Seleksi Versi Solc Otomatis

```
SOLC_MAP = {
  '0.4': '0.4.26',   # versi patch terbaru di setiap minor
  '0.5': '0.5.17',
  '0.6': '0.6.12',
  '0.7': '0.7.6',
  '0.8': '0.8.20',   # ← FIXED untuk benchmark
}
```

Parser membaca `pragma solidity` dari source, menentukan major.minor, lalu menggunakan versi patch tertinggi yang tersedia. Ini memaksimalkan keberhasilan compile.

---

## Fase 2: Pengukuran Gas Empiris (Hardhat)

### Mengapa Hardhat?

Hardhat menyediakan EVM in-process (berbasis `@nomicfoundation/hardhat-network`) yang:
- Deterministik: gas tidak bergantung pada congestion mainnet
- Cepat: tidak perlu mining time
- `estimateGas()`: menghitung gas tepat untuk panggilan fungsi tanpa mengirim transaksi

### Kontrak Benchmark

Kontrak khusus `GasBenchmark.sol` ditulis di Solidity 0.8.20 dengan pasangan fungsi **boros** vs **hemat** untuk setiap anti-pattern:

| Anti-Pattern | Fungsi Boros | Fungsi Hemat | Perbedaan Kunci |
|---|---|---|---|
| redundant_sload | `sload_boros()` — baca `counter` 3x | `sload_hemat()` — cache ke `c`, pakai 3x | 1x SLOAD vs 3x SLOAD |
| unoptimized_loop | `loop_boros()` — `items.length` per iter | `loop_hemat()` — cache `n = items.length` | SLOAD per iterasi vs 1x |
| string_vs_bytes32 | `str_boros()` returns `string` | `str_hemat()` returns `bytes32` | dynamic vs fixed size |
| public_vs_external | `pub_boros(uint256[] memory)` | `ext_hemat(uint256[] calldata)` | memory copy vs calldata |
| unchecked_arithmetic | `arith_boros(n)` — checked `i++` | `arith_hemat(n)` — `unchecked { i++ }` | overflow check overhead |
| dead_code | `WithDeadCode` deployment | `WithoutDeadCode` deployment | 3 dead internal funcs |

### Konfigurasi Hardhat (Variabel Tetap)

```javascript
// hardhat.config.js
solidity: {
  version: "0.8.20",        // FIXED — tidak pernah diubah
  settings: {
    optimizer: { enabled: false }  // FIXED — tidak pernah diaktifkan
  }
}
```

**Alasan optimizer: false**: Jika optimizer diaktifkan, kompiler akan menghapus dead code dan mengoptimasi SLOAD secara otomatis — sehingga perbedaan antara kode boros dan hemat menjadi artifisial. Penelitian ini mengukur efek **keputusan programmer**, bukan efek kompiler.

---

## Fase 3: Validasi Statistik

### Pemilihan Uji Statistik

| Uji | Digunakan Untuk | Alasan Pemilihan |
|---|---|---|
| **Wilcoxon Signed-Rank** | Gas boros vs hemat (6 pasang) | Non-parametrik, data gas tidak terdistribusi normal, sampel berpasangan |
| **Chi-square** | Domain vs keberadaan findings (binary) | Uji independensi kategorik |
| **Kruskal-Wallis** | Complexity level vs jumlah findings | Non-parametrik versi ANOVA untuk 2+ grup |
| **Spearman Rank Correlation** | LOC vs total findings | Non-parametrik, tidak asumsikan linearitas |

### Mengapa Non-Parametrik?

Distribusi gas consumption dan findings count **tidak mengikuti distribusi normal** (skewed right, outlier tinggi). Uji non-parametrik (Wilcoxon, Kruskal-Wallis, Spearman) tidak mengasumsikan normalitas sehingga lebih tepat untuk data ini.

### Hipotesis yang Diuji

**H1 (Wilcoxon)**: Median penghematan gas > 0 (optimasi memberi efek positif yang nyata)
- H0: Median boros − hemat = 0
- H1: Median boros − hemat > 0 (one-sided)

**H2 (Chi-square)**: Distribusi findings bergantung pada domain kontrak
- H0: Domain tidak mempengaruhi keberadaan findings
- H1: Ada perbedaan signifikan antar domain

**H3 (Kruskal-Wallis)**: Complexity level mempengaruhi jumlah findings
- H0: Distribusi findings sama di semua complexity level

**H4 (Spearman)**: Ada korelasi antara LOC dan jumlah findings
- H0: rho = 0

---

## Fase 4: Verifikasi Manual (Audit Precision)

Untuk mengukur precision detector secara nyata (bukan pseudo-estimate), dilakukan **manual audit** terhadap 20 kontrak dengan estimated gas savings tertinggi (*purposive sampling by impact*). Sampling ini mencakup 64.9% dari total potensi penghematan dataset.

### Pipeline Audit

```
results/pekan2_detector_results.json
    ↓ scripts/generate_audit_checklist.py
    ↓ docs/manual_audit/audit_findings_raw.json  ← findings per kontrak
    ↓ scripts/run_manual_audit.py
    ↓ docs/manual_audit/AUDIT_RESULTS.md         ← verdict per finding
```

### Metode Verifikasi per Pattern

| Pattern | Cara Verifikasi |
|---|---|
| `public_vs_external` | Cari pemanggilan `funcName(` di dalam file, kecualikan baris deklarasi dan `this.`/`super.` |
| `redundant_sload` | Ekstrak function body via brace-depth tracking; hitung read vs assignment positions |
| `string_vs_bytes32` | Cari deklarasi state variable; periksa panjang literal string initializer |
| `dead_code` | Cari semua pemanggilan nama fungsi; cek virtual/override |
| `unoptimized_loop` | Cari for-loop dengan `.length` di kondisi iterasi |

### Klasifikasi Verdict

- **TP** (True Positive): anti-pattern terbukti ada di kode
- **FP** (False Positive): anti-pattern tidak ada, detektor salah flag
- **?** (Ambiguous): tidak dapat diverifikasi — umumnya karena function body parser gagal mengekstrak scope pada kontrak >2000 LOC, nested contracts, atau inline assembly

### Keterbatasan Pendekatan Ini

- **Recall tidak diukur**: audit hanya menilai findings yang di-flag (precision), bukan yang terlewat (FN)
- **233 kasus ambiguous di redundant_sload**: brace-depth parser kadang gagal pada kontrak yang sangat besar; kasus ini dikecualikan dari perhitungan precision
- **20 dari 74 kontrak**: audit mencakup kontrak dengan dampak terbesar, bukan coverage penuh

---

## Tools & Environment

| Komponen | Versi | Fungsi |
|---|---|---|
| Python | 3.11 | Bahasa utama pipeline analisis |
| py-solcx | latest | Interface ke solc compiler dari Python |
| solc | 0.4.26 – 0.8.20 | Compiler Solidity (multi-versi) |
| Node.js | v24.14.1 | Runtime Hardhat |
| Hardhat | latest | Local EVM untuk gas measurement |
| scipy | latest | Uji statistik |
| numpy | latest | Operasi array |
| slither-analyzer | 0.11.5 | Tool perbandingan (Slither) |
| Conda env | `gas_opt` | Isolasi environment Python |

---

## Keterbatasan Metodologi

1. **n=6 untuk Wilcoxon**: Unit observasi adalah pattern (bukan kontrak individual), sehingga n kecil. Hasil tetap signifikan (W+=15, p=0.031) namun power statistik terbatas.

2. **Benchmark terisolasi**: Gas diukur pada kontrak benchmark yang dikonstruksi khusus, bukan pada kontrak dataset asli. Angka penghematan bersifat ilustratif.

3. **Slither keterbatasan solc lama**: Slither 0.11.5 tidak dapat menganalisis kontrak dengan pragma solidity 0.4.x (mayoritas dataset), sehingga perbandingan head-to-head tidak dapat dilakukan secara penuh.

4. **Refactoring hanya heuristik**: Modul refactorer menggunakan regex berbasis line number, bukan full data-flow analysis, sehingga patch untuk `redundant_sload` hanya berupa komentar TODO.
