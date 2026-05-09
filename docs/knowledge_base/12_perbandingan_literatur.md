# Perbandingan dengan Literatur Terkait

## Peta Literatur

Penelitian ini berada di persimpangan tiga bidang:
1. **Static analysis tools** untuk smart contract (Slither, SmartCheck, Oyente)
2. **Gas optimization research** (identifikasi anti-pattern, pengukuran empiris)
3. **Empirical software engineering** pada Ethereum (studi dataset kontrak mainnet)

---

## 1. Perbandingan dengan Tool Analisis Statik Sejenis

### Slither (Feist et al., 2019)

**Referensi**: Feist, J., Grieco, G., Groce, A. (2019). *Slither: A Static Analysis Framework For Smart Contracts*. IEEE/ACM WETSEB.

| Aspek | Slither | Framework Kita |
|---|---|---|
| Pendekatan | AST + taint analysis + data-flow | AST traversal (DFS) |
| Bahasa implementasi | Python | Python |
| Versi Solidity | ≥ 0.4.x (namun praktis 0.6.x+) | 0.4.x – 0.8.x (py-solcx multi-versi) |
| Gas-specific detectors | Beberapa (costly-loop, dll) | 6 detektor fokus gas |
| Kuantifikasi gas | Tidak (hanya flag) | Ya (gas diff per pattern, via Hardhat) |
| Kecepatan analisis | ~1.7s/kontrak (0.8.x) | ~0.20s/kontrak (rata-rata semua kompleksitas) |
| Dataset kontrak lama | Terbatas (0.4.x sering gagal) | ✅ Mendukung penuh |

**Perbedaan utama**: Slither dirancang untuk analisis keamanan umum (reentrancy, access control, dll) dengan gas sebagai fitur sekunder. Framework kita dirancang khusus untuk gas optimization dengan validasi kuantitatif empiris via benchmark Hardhat.

**Keterbatasan perbandingan**: Pada 10 kontrak sampel (semua 0.4.x era), Slither menghasilkan 0 temuan gas-related — bukan karena tidak ada anti-pattern, melainkan ketidakkompatibilan versi solc. Perbandingan head-to-head yang adil membutuhkan dataset kontrak 0.8.x.

---

### SmartCheck (Tikhomirov et al., 2018)

**Referensi**: Tikhomirov, S., et al. (2018). *SmartCheck: Static Analysis of Ethereum Smart Contracts*. IEEE WETSEB.

| Aspek | SmartCheck | Framework Kita |
|---|---|---|
| Pendekatan | XML parse tree pattern matching | AST JSON traversal |
| Target | Security + quality issues | Gas optimization khusus |
| Kuantifikasi gas | Tidak | Ya |
| Multi-versi solc | Tidak | Ya |

SmartCheck mendefinisikan pola sebagai XPath query atas XML tree — pendekatan yang lebih deklaratif tetapi kurang fleksibel untuk analisis alur data. Framework kita menggunakan traversal imperatif yang memungkinkan tracking konteks antar-node.

---

### Oyente (Luu et al., 2016)

**Referensi**: Luu, L., et al. (2016). *Making Smart Contracts Smarter*. ACM CCS.

Oyente menggunakan **symbolic execution** (bukan AST), yang lebih akurat untuk deteksi reentrancy dan integer overflow tetapi:
- Jauh lebih lambat (per-path analysis)
- Tidak dirancang untuk gas optimization
- Tidak menghasilkan estimasi gas savings

Pendekatan AST kita lebih cepat dan lebih cocok untuk analisis skala besar (50 kontrak) walaupun kehilangan presisi path-sensitive.

---

## 2. Perbandingan dengan Penelitian Gas Optimization

### Chen et al. (2017) — "Under-Optimized Smart Contracts Devour Your Money"

**Referensi**: Chen, T., Li, X., Luo, X., Zhang, X. (2017). *Under-Optimized Smart Contracts Devour Your Money*. IEEE SANER.

Ini adalah paper paling relevan dan paling dekat dengan penelitian kita.

| Aspek | Chen et al. (2017) | Penelitian Kita |
|---|---|---|
| Anti-pattern yang diteliti | 7 pola (frozen ether, gassy ERC20, costly loop, dll) | 6 pola (overlap di loop + storage access) |
| Metode deteksi | EVM bytecode analysis | Solidity AST analysis |
| Level analisis | Bytecode (post-compile) | Source code (pre-compile) |
| Dataset | ~5.000 kontrak Ethereum | 50 kontrak mainnet (purposive sampling) |
| Kuantifikasi gas | Teoritis (formula) | Empiris (benchmark Hardhat) |
| Validasi statistik | Tidak ada | Wilcoxon, KW, Chi-square, Spearman |
| Refactoring otomatis | Tidak | Ya (3 pola) |

**Keunggulan Chen et al.**: Dataset lebih besar, analisis bytecode lebih akurat (tidak terpengaruh source-level ambiguity).

**Keunggulan kita**: Analisis di level source code → lebih mudah diinterpretasi developer; kuantifikasi gas empiris (bukan teoritis); validasi statistik formal; refactoring otomatis; mendukung kontrak era lama.

**Overlap anti-pattern**:
- Chen: *costly loop* ↔ Kita: `unoptimized_loop` (konsep sama, implementasi berbeda)
- Chen: *gassy ERC20 token* (akses storage berulang) ↔ Kita: `redundant_sload`
- Chen: *dead code* ↔ Kita: `dead_code`

---

### Gasper / Gas Analysis Tools (Albert et al., 2018–2020)

**Referensi**: Albert, E., et al. (2018). *EthIR: A Framework for High-Level Analysis of Ethereum Bytecode*. ATVA. (dan karya lanjutan GASOL, 2020)

Pendekatan decompile bytecode → Rule-based IR → Gas upper bound analysis. Tujuan utama: membuktikan upper bound konsumsi gas (untuk verifikasi formal), bukan mengidentifikasi anti-pattern programmer.

| Aspek | Albert et al. / GASOL | Penelitian Kita |
|---|---|---|
| Fokus | Formal gas bound verification | Anti-pattern detection & quantification |
| Input | EVM bytecode | Solidity source code |
| Output | Gas upper bound (formula) | Findings list + estimated savings |
| Practical use | Verifikasi formal | Developer tooling |

---

## 3. Perbandingan Dataset & Metodologi

### Skala Dataset

| Penelitian | Jumlah Kontrak | Sumber | Metode Sampling |
|---|---|---|---|
| Chen et al. (2017) | ~5.000 | Ethereum mainnet | Random |
| Slither evaluation | ~24 (kasus uji) | Manual curated | Purposive |
| Penelitian kita | 50 | Ethereum mainnet (Etherscan) | Stratified purposive (5 domain × 10) |

Dataset 50 kontrak dengan stratifikasi domain memungkinkan analisis komparatif antar domain — sesuatu yang tidak dilakukan penelitian sebelumnya secara eksplisit.

### Validasi Empiris

Mayoritas penelitian gas optimization sebelumnya menggunakan **estimasi teoritis** (hitung opcode cost × frekuensi). Penelitian kita menggunakan **benchmark empiris** via Hardhat local EVM — lebih akurat karena:
- Mengukur gas consumption aktual pada EVM implementation nyata
- Optimizer dimatikan (`optimizer: false`) untuk isolasi efek keputusan programmer
- Setiap pattern diukur dalam kondisi identik (cold start, fixed state)

---

## 4. Posisi Kontribusi dalam Landscape Penelitian

```
                    ┌─────────────────────────────────────┐
                    │         LEVEL ANALISIS               │
                    │  Bytecode ◄─────────► Source Code   │
                    └─────────────────────────────────────┘
                          │                       │
              Chen et al. │                       │ SmartCheck
              Oyente       │                       │ Penelitian ini
              GASOL        │                       │ Slither (partial)
                          ▼                       ▼

┌─────────────────────────────────────────────────────────────┐
│                   TUJUAN ANALISIS                            │
│  Security ◄──────────────────────────────► Gas Efficiency   │
│                                                             │
│  Oyente, Mythril     SmartCheck     Slither    Chen et al.  │
│  (pure security)     (mixed)        (mixed)    Penelitian   │
│                                               ini (pure gas)│
└─────────────────────────────────────────────────────────────┘
```

**Celah yang diisi penelitian ini**:
1. Tidak ada tool yang mengkombinasikan: (a) source-level AST analysis, (b) multi-versi solc, (c) kuantifikasi gas empiris, dan (d) refactoring otomatis dalam satu framework Python
2. Validasi statistik formal (Wilcoxon, KW, Chi-square, Spearman) belum umum dilakukan pada penelitian gas optimization
3. Dataset terstrategifikasi per domain dengan analisis per-domain (KW per-domain) belum dilakukan sebelumnya

---

## 5. Tabel Ringkasan Perbandingan

| Fitur | Oyente | SmartCheck | Slither | Chen et al. | **Penelitian Ini** |
|---|---|---|---|---|---|
| Level analisis | Bytecode | Source | Source | Bytecode | Source |
| Fokus utama | Security | Quality | Security | Gas | Gas |
| Multi-versi solc | ✅ | Terbatas | Terbatas | ✅ | ✅ |
| Deteksi gas-specific | ❌ | Sebagian | Sebagian | ✅ | ✅ |
| Kuantifikasi gas | ❌ | ❌ | ❌ | Teoritis | **Empiris** |
| Validasi statistik | ❌ | ❌ | ❌ | ❌ | **✅** |
| Refactoring otomatis | ❌ | ❌ | ❌ | ❌ | **✅** |
| Open source Python | ❌ | ❌ | ✅ | ❌ | ✅ |
| Dataset kontrak lama | Terbatas | Terbatas | Terbatas | ✅ | ✅ |

---

## 6. Keterbatasan Dibanding Penelitian Terdahulu

1. **Skala dataset lebih kecil** (50 vs ~5.000 pada Chen et al.) — purposive sampling memungkinkan analisis mendalam per kontrak tetapi mengurangi generalisasi statistik

2. **False positive lebih tinggi** — analisis AST level source code tanpa data-flow analysis menghasilkan false positive (terutama `redundant_sload`) yang tidak dimiliki analisis bytecode

3. **Tidak ada path-sensitive analysis** — berbeda dengan Oyente/Mythril yang menggunakan symbolic execution, framework kita tidak dapat mendeteksi pola yang hanya muncul pada execution path tertentu

4. **Benchmark kondisi terkontrol** — pengukuran gas dilakukan pada kontrak benchmark sintetis, bukan pada kontrak nyata dengan kondisi state mainnet

---

## Referensi Utama

1. Feist, J., Grieco, G., Groce, A. (2019). Slither: A Static Analysis Framework For Smart Contracts. *IEEE/ACM WETSEB 2019*.
2. Chen, T., Li, X., Luo, X., Zhang, X. (2017). Under-Optimized Smart Contracts Devour Your Money. *IEEE SANER 2017*.
3. Tikhomirov, S., Voskresenskaya, E., Ivanitskiy, I., Takhaviev, R., Marchenko, E., Alexandrov, Y. (2018). SmartCheck: Static Analysis of Ethereum Smart Contracts. *IEEE WETSEB 2018*.
4. Luu, L., Chu, D.H., Olickel, H., Saxena, P., Hobor, A. (2016). Making Smart Contracts Smarter. *ACM CCS 2016*.
5. Albert, E., et al. (2018). EthIR: A Framework for High-Level Analysis of Ethereum Bytecode. *ATVA 2018*.
