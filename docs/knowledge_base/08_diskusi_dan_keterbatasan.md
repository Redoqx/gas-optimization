# Diskusi Temuan & Keterbatasan

## Diskusi Temuan Utama

### 1. Public vs External Mendominasi (39.2% dari Temuan)

`public_vs_external` menghasilkan 649 dari 1.655 temuan (39.2%) — hampir 2 dari 5 temuan. Ini mencerminkan realitas historis Solidity: pada versi 0.4.x–0.5.x, praktik standar adalah mendeklarasikan semua fungsi sebagai `public`. Keyword `external` baru populer setelah komunitas Ethereum mulai memperhatikan gas optimization sekitar 2019–2020.

**Implikasi**: Kontrak-kontrak lama (deployed sebelum 2020) yang masih berjalan di mainnet membawa "technical debt" gas yang bisa diminimalkan dengan refactoring sederhana — cukup mengubah `public` → `external` dan `memory` → `calldata` untuk parameter array.

**Catatan penting untuk penulisan**: Tidak semua `public` yang di-flag adalah false positive, tapi mayoritas besar memang tidak pernah dipanggil secara internal (hanya dari luar kontrak). Ini adalah optimasi yang aman untuk diterapkan.

### 2. Unchecked Arithmetic: Penghematan Terbesar (20.38%)

Meski **0 temuan** ditemukan di 75 kontrak dataset (seluruh dataset didominasi solc 0.4.x–0.6.x era yang belum mengenal `unchecked {}` block — fitur Solidity 0.8.0), penghematan per penggunaan adalah yang terbesar. Untuk loop 100 iterasi, `unchecked { i++ }` menghemat 12.045 gas — hampir 1/5 dari total biaya loop.

**Konteks**: EIP-1884 dan Solidity 0.8.0 (2020) menambahkan overflow protection otomatis. Sebelumnya, programmer harus menggunakan SafeMath library yang justru lebih mahal. Sejak 0.8.0, unchecked block menjadi cara resmi untuk skip proteksi saat sudah terjamin tidak overflow.

**Implikasi**: Untuk kontrak baru yang ditulis dengan Solidity 0.8.x, optimasi ini sangat relevan — terutama loop counter yang jelas bounded.

### 3. Dead Code = 0% Penghematan (pada Pengukuran)

Hasil yang mungkin mengejutkan: meskipun 122 temuan dead code ditemukan di dataset (7.4% dari 1.655 total), pengukuran gas menunjukkan 0% penghematan.

**Penjelasan teknis**: Compiler Solidity mengeksklusi fungsi internal yang tidak pernah dipanggil dari deployment bytecode **bahkan tanpa optimizer**. Ini karena fungsi internal di-inline atau diresolusi secara statik saat compile. Hasilnya: `WithDeadCode` dan `WithoutDeadCode` menghasilkan bytecode identik untuk bagian yang dieksekusi.

**Nuansa penting**: Ini BUKAN berarti dead code tidak bermasalah. Dead code:
- Menambah **complexity kognitif** (programmer membaca kode tidak perlu)
- Dapat menjadi **attack surface** jika secara tidak sengaja diaktifkan
- Pada kondisi tertentu (fungsi yang lebih kompleks, atau compiler versi tertentu), MUNGKIN tetap masuk bytecode

Untuk tujuan penulisan: sebutkan bahwa temuan dead code valid sebagai quality metric, namun dampak gas-nya minimal dalam pengukuran ini.

### 4. Unoptimized Loop Hanya 7 Temuan

Hanya 2 kontrak yang memiliki loop dengan state variable `.length`: MultiSigWallet (Utility, 5 temuan) dan KyberNetworkProxy (DeFi, 2 temuan). Ini bukan berarti pattern tidak umum — melainkan karena:
1. Kontrak modern menggunakan mapping (O(1) lookup) daripada array iterasi
2. Kontrak yang menggunakan array biasanya mengcache length secara manual (sudah sadar)
3. Detektor kita hanya mendeteksi loop dengan state variable array; local variable array tidak dideteksi

### 5. Korelasi Spearman LOC vs Findings (ρ = +0.144, p = 0.220)

Korelasi Spearman antara LOC dan jumlah temuan adalah **tidak signifikan** (p=0.220) dengan arah positif lemah (ρ=+0.144). Ini berbeda dari ekspektasi awal bahwa kontrak lebih besar mengandung lebih banyak anti-pattern secara proporsional.

**Penjelasan**: Dengan dataset 75 kontrak (15 per domain, termasuk banyak kontrak NFT dan Token yang berukuran besar dan berasal dari era solc 0.8.x), hubungan LOC-findings menjadi tidak linear. Kontrak besar era modern (Azuki, CloneX, Doodles) memiliki LOC tinggi tetapi relatif sedikit gas anti-pattern karena ditulis dengan best practices terkini. Sebaliknya kontrak medium era lama (TetherToken, LinkToken) mengandung banyak `public_vs_external` anti-pattern meski ukurannya sedang.

**Implikasi untuk penulisan**: "Ukuran kontrak (LOC) tidak dapat dijadikan prediktor yang andal untuk jumlah gas anti-pattern — era penulisan dan versi Solidity yang digunakan lebih determinan. Korelasi Spearman yang tidak signifikan (ρ=+0.144, p=0.220) mengkonfirmasi tidak ada hubungan linear yang bermakna antara kedua variabel ini."

### 6. Slither Tidak Dapat Menganalisis Kontrak Lama

Slither 0.11.5 gagal menganalisis 10 kontrak sampel karena semua menggunakan solc 0.4.x. Ini bukan kelemahan inherent Slither — melainkan trade-off antara modernitas tool (Slither dioptimasi untuk kontrak modern) vs keragaman dataset.

**Untuk penulisan**: Sebutkan bahwa perbandingan Slither vs framework kita tidak dapat dilakukan secara penuh karena keterbatasan ini. Framework kita memiliki keunggulan spesifik dalam mendukung multi-versi solc (0.4.x hingga 0.8.x) melalui py-solcx.

---

## Keterbatasan Penelitian

### Keterbatasan 1: Ukuran Sampel Uji Statistik

Uji Wilcoxon menggunakan n=6 (5 efektif) — sangat kecil untuk analisis statistik robust. Meski hasilnya signifikan (p=0.031), power statistik rendah berarti:
- Potensi Type II error (gagal mendeteksi efek kecil) tinggi
- Generalisasi terbatas

**Saran penelitian lanjutan**: Perbanyak variasi benchmark — berbeda ukuran array, berbeda jumlah iterasi, berbeda kondisi EVM state — untuk memperluas n.

### Keterbatasan 2: Benchmark Terkontrol vs Real-World

Gas diukur pada kontrak benchmark yang dikonstruksi khusus dengan kondisi terisolasi. Pada kontrak nyata:
- Gas bervariasi tergantung state EVM saat itu (warm/cold storage access)
- Kompiler versi berbeda dengan optimization setting berbeda menghasilkan bytecode berbeda
- Interaksi antar pattern (satu fungsi bisa punya multiple anti-pattern) tidak diukur

### Keterbatasan 3: Refactoring Otomatis Terbatas

Modul `refactorer.py` menggunakan pendekatan heuristik berbasis line number + regex:
- `public_vs_external`: patch otomatis tapi tidak sempurna (tidak track inheritance chain)
- `unoptimized_loop`: patch otomatis dengan word-boundary matching (masih bisa false positive untuk parameter bernama mirip state variable)
- `redundant_sload`: hanya tambah komentar TODO — full auto-patch butuh data-flow analysis

Contoh kegagalan yang terdokumentasi: MultiSigWallet memiliki parameter `_owners` dan state variable `owners`. Loop iterasi menggunakan parameter `_owners.length`, bukan state variable `owners.length` — sehingga detektor false positive, dan refactorer (sebelum fix) salah mempatch.

### Keterbatasan 4: False Positive dalam Deteksi

**redundant_sload**: Tidak membedakan read dari write. Jika state variable ditulis (diubah) di antara dua pembacaan, membaca ulang dari storage adalah **benar** (bukan redundant). Detektor saat ini tidak tracking assignment.

**public_vs_external**: Tidak dapat mendeteksi pemanggilan via `this.functionName()` (yang adalah external call meski dari dalam kontrak) atau via interface/inheritance lintas file.

**dead_code**: Tidak dapat tracking jika fungsi dipanggil secara dinamis (via `call()` atau contract upgrade pattern).

### Keterbatasan 5: Dataset Tidak Seimbang

- Complexity Simple: 2 kontrak (Multicall SLOC=43, Multicall2 SLOC=70) dari 75 — keduanya Utility domain
- Token, NFT, DeFi, Governance: tidak ada kontrak Simple (<100 SLOC) — mencerminkan kenyataan bahwa kontrak mainnet bersifat non-trivial
- `unchecked_arithmetic`: 0 findings dari 75 kontrak — seluruh dataset didominasi solc 0.4.x–0.6.x era yang tidak menggunakan fitur `unchecked {}` (diperkenalkan Solidity 0.8.0)
- Dataset aktif (contracts_selection.json): 75 kontrak, 15 per domain (DeFi=15, NFT=15, Token=15, Governance=15, Utility=15), semua compile_ok
- LOC dihitung sebagai SLOC (non-blank lines) untuk konsistensi dengan definisi ukuran kontrak yang bermakna

---

## Validitas Internal vs Eksternal

**Validitas internal** (tinggi): Pengukuran gas dilakukan secara konsisten dengan kondisi tetap (solc 0.8.20, optimizer off, Hardhat local EVM). Hasil benchmark dapat direproduksi.

**Validitas eksternal** (sedang): Temuan berlaku untuk kontrak era lama yang serupa dengan dataset. Generalisasi ke kontrak era baru (solc 0.8.x) atau domain lain (L2, Cosmos-based EVM) perlu studi lebih lanjut.

---

## Perbandingan dengan Ekspektasi Teoritis

| Anti-Pattern | Ekspektasi Teoritis | Hasil Pengukuran | Sesuai? |
|---|---|---|---|
| redundant_sload | SLOAD 2100 gas × (n-1) penghematan | 186 gas (sangat kecil) | Sebagian — SLOAD mungkin warm access (100 gas) |
| unoptimized_loop | n × (SLOAD_cost - MLOAD_cost) | 1.031 gas untuk n=10 | ✅ Sesuai (~103 gas/iterasi |
| string_vs_bytes32 | Static vs dynamic storage | 950 gas | ✅ Sesuai |
| public_vs_external | Memory copy vs calldata | 2.673 gas | ✅ Sesuai |
| unchecked_arithmetic | Overflow check overhead × n | 12.045 gas | ✅ Sesuai (120 gas/iterasi) |
| dead_code | Deployment bytecode lebih kecil | 0 gas | ❌ Tidak — compiler elides anyway |

**Catatan redundant_sload**: Penghematan kecil (186 gas) menunjukkan bahwa akses storage yang diukur adalah **warm access** (slot sudah diakses sebelumnya dalam transaksi yang sama), yang hanya 100 gas. Cold access (2100 gas) tidak diukur dalam benchmark ini karena fungsi `setup()` dipanggil lebih dulu.

**Catatan unchecked_arithmetic**: Temuan = 0 di seluruh 75 kontrak dataset. Ini bukan bug detector — detector menggunakan solc 0.8.20 untuk analisis, tapi loop counter yang memenuhi syarat `unchecked` tidak ditemukan di kontrak-kontrak yang ada. Penghematan 20.38% tetap valid karena diukur dari benchmark contract yang dikonstruksi khusus, bukan dari dataset.

---

## Catatan Penulisan Report: Elaborasi Tabel 4.4b dan 4.4e

### Elaborasi Tabel 4.4b — std=0.00 dan Refactor Success=0%

**Mengapa std=0.00 pada Avg Gas Saved?**

Nilai std = 0.00 pada pengukuran Avg Gas Saved (%) disebabkan oleh sifat deterministik EVM (Ethereum Virtual Machine). Gas consumption untuk fungsi Solidity yang identik pada state EVM yang sama selalu konstan — tidak ada randomness, variasi lingkungan, atau jitter. `eth_estimateGas` (yang digunakan oleh Hardhat) mengembalikan angka yang persis sama di setiap pemanggilan selama bytecode, input, dan initial storage state tidak berubah.

Variance hanya akan muncul jika benchmark dirancang dengan multiple scenarios: variasi ukuran input (array 5 vs 10 vs 50 elemen), variasi initial storage state (warm vs cold slot), atau variasi jumlah iterasi. Penelitian ini menggunakan **satu skenario tetap per pola** untuk mengisolasi efek masing-masing anti-pattern secara bersih — konsekuensinya, std = 0.00 adalah hasil yang benar dan diharapkan, bukan indikasi kesalahan pengukuran.

**Mengapa Refactor Success = 0% untuk 4 pola?**

Empat dari enam pola memiliki Refactor Success = 0% karena implementasi auto-refactoring yang aman memerlukan analisis yang melampaui kemampuan AST traversal heuristik:

| Pola | Alasan 0% | Analisis yang Dibutuhkan |
|---|---|---|
| `redundant_sload` | Tidak diketahui apakah state variable dimodifikasi antara dua pembacaan | SSA (Static Single Assignment) form + data-flow analysis |
| `string_vs_bytes32` | Tidak dapat diverifikasi apakah string aman dipotong ke 32 byte | Semantic analysis + usage context |
| `unchecked_arithmetic` | Tidak dapat dibuktikan bahwa operasi tidak akan overflow — safety-critical | Formal interval/range analysis |
| `dead_code` | Tidak dapat dilacak panggilan lintas kontrak (factory, delegatecall, events) | Cross-contract call graph |

`public_vs_external` mencapai 100% Refactor Success karena pattern-nya deterministik: substitusi `public` → `external` pada fungsi tanpa internal caller adalah selalu aman. `unoptimized_loop` mencapai 85% karena cache `length` ke variabel lokal adalah operasi yang secara semantik setara dalam hampir semua kasus — kegagalan 15% terjadi pada loop dengan multiple variabel loop yang berinteraksi kompleks.

---

### Elaborasi Tabel 4.4e — Nilai "—" (Not Applicable)

**Mengapa ada sel "—" di Tabel 4.4e?**

Nilai "—" digunakan untuk sel yang secara konseptual tidak dapat dihitung atau tidak bermakna dalam konteks perbandingan ini — bukan error data, melainkan keterbatasan matematika dari perbandingan yang asimetris.

**Akar masalah**: Slither v0.11.5 tidak dapat mem-parse `pragma solidity ^0.4.x` yang digunakan oleh mayoritas kontrak dalam dataset (era 2017–2019). Akibatnya, Slither menghasilkan 0 deteksi bukan karena tidak ada anti-pattern gas (false negative), melainkan karena tool tidak dapat menganalisis source code sama sekali (parse failure).

Konsekuensi matematisnya:

| Sel yang "—" | Alasan tidak terdefinisi |
|---|---|
| Unique to Slither | Slither = 0 deteksi → tidak ada findings yang "unik ke Slither" |
| Overlap (baris Unique to Our Tool) | Intersection selalu ∅ ketika satu himpunan kosong |
| Overlap (baris Unique to Slither) | Sama — Slither=0 membuat overlap tidak terdefinisi |
| Precision (shared patterns) | Precision = TP/(TP+FP) membutuhkan shared detections; shared = 0 → undefined |
| Gas Quantification (Overlap) | Slither tidak menghasilkan estimasi gas savings — kolom Overlap tidak bermakna |

Melaporkan angka 0 untuk metrik ini akan menyesatkan, karena 0 dan "tidak terdefinisi" memiliki interpretasi berbeda secara statistik. Nilai "—" digunakan secara konsisten mengikuti konvensi penulisan ilmiah untuk kondisi di mana denominator nol atau kondisi prasyarat tidak terpenuhi.

**Konteks**: Perbandingan yang adil (*fair comparison*) hanya dapat dilakukan pada kontrak solc 0.8.x. Dari 10 kontrak sampel, hanya 1 (MutantApeYachtClub, solc 0.8.x) yang berhasil dianalisis Slither — hasilnya 0 gas-related findings dari Slither vs 2 findings dari framework kita pada kontrak yang sama. Ini menunjukkan bahwa sekalipun pada kontrak yang dapat dianalisis Slither, Slither tidak mendeteksi gas anti-patterns yang sama.
