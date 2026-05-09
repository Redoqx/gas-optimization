# Kesimpulan & Saran

## Kesimpulan per Rumusan Masalah

### RQ1: Pola anti-pattern gas apa yang umum ditemukan di smart contract nyata?

**Jawaban**: Dari 6 anti-pattern yang diteliti, **`public_vs_external`** adalah yang paling umum (649 dari 1.655 temuan, 39.2%), diikuti sangat dekat oleh `redundant_sload` (634, 38.3%). Dominasi keduanya mencerminkan era penulisan kontrak yang berbeda:

- **public_vs_external**: mayoritas kontrak era 0.4.x–0.6.x menggunakan `public` sebagai default; `external`/`calldata` baru dipopulerkan pasca 2019
- **redundant_sload**: storage access berulang tanpa caching lokal adalah pola yang meluas di hampir semua domain

Urutan frekuensi: public_vs_external (39.2%) ≈ redundant_sload (38.3%) > string_vs_bytes32 (14.7%) > dead_code (7.4%) > unoptimized_loop (0.4%) > unchecked_arithmetic (0.0%)

Anti-pattern ditemukan di **89.2% dari 74 kontrak valid** (66 kontrak), menunjukkan bahwa pola boros gas adalah hal yang sangat umum di smart contract real-world.

**Catatan khusus unchecked_arithmetic**: 0 findings pada 74 kontrak dataset bukan berarti pola tidak ada di mainnet — melainkan karena dataset didominasi era solc 0.4.x–0.6.x sebelum Solidity 0.8.0 yang memperkenalkan `unchecked {}` block. Gas benchmark untuk pola ini tetap valid (20.38% savings) karena diukur menggunakan kontrak sintetis solc 0.8.20.

### RQ2: Seberapa besar penghematan gas yang dapat dicapai?

**Jawaban**: Penghematan gas bervariasi signifikan per pola:

| Anti-Pattern | Penghematan |
|---|---|
| unchecked_arithmetic | **20.38%** (tertinggi — benchmark synthetic) |
| public_vs_external | 5.09% |
| string_vs_bytes32 | 3.87% |
| unoptimized_loop | 2.01% |
| redundant_sload | 0.77% |
| dead_code | 0% (pada runtime; compiler elides dead functions) |

Rata-rata penghematan (6 pola): **5.35%**. Jika diterapkan pada kontrak yang sering dipanggil (ribuan transaksi/hari), penghematan ini signifikan dalam nilai ETH. Token domain memiliki potensi penghematan terbesar (median estimated savings 49.044 gas/contract).

### RQ3: Apakah framework deteksi statik berbasis AST efektif?

**Jawaban**: Ya, efektif. Framework berhasil mendeteksi 1.655 temuan pada 74 kontrak real-world dari berbagai domain dan era Solidity. Keunggulan utama:
- Mendukung multi-versi solc (0.4.x hingga 0.8.x) via py-solcx
- Berhasil menormalisasi dua format AST Solidity (legacy compact/new expanded)
- Menemukan temuan pada kontrak yang bahkan tidak bisa dianalisis Slither (0.4.x era)
- Presisi rata-rata 80.2% dan recall 88.6% (pada 4 pola aktif dalam 20-contract sample)
- Analysis time: ~0.08s (Simple), ~0.13s (Medium), ~0.31s (Complex) — sangat cepat

### RQ4: Apakah penghematan gas signifikan secara statistik?

**Jawaban**: **Ya**, signifikan secara statistik — dikonfirmasi oleh dua uji Wilcoxon independen:

1. **Wilcoxon per-pattern** (n=5 efektif): **W=15.0, p=0.031** — semua 5 pola menunjukkan penghematan positif (W=15 adalah nilai maksimum untuk n=5).

2. **Wilcoxon per-contract** (n=65): **W=2145.0, p<0.001** — W=2145 adalah nilai maksimum untuk n=65; semua 65 kontrak yang memiliki findings menunjukkan estimated savings positif.

Uji tambahan **Kruskal-Wallis per-domain** (H=18.409, p=0.001) menunjukkan bahwa besarnya potensi penghematan berbeda signifikan antar domain — Token dan NFT era lama memiliki potensi penghematan gas terbesar.

---

## Kesimpulan Umum

1. **Framework gas optimization berbasis AST terbukti feasible** dan dapat diimplementasikan dalam Python menggunakan py-solcx. Analisis statik menghasilkan 1.655 findings yang relevan dan terstruktur dari 74 kontrak mainnet.

2. **Pola boros gas sangat umum** di smart contract mainnet Ethereum, khususnya pada kontrak era 2017–2019. Mayoritas kontrak (89.2%) memiliki setidaknya satu temuan. Dua pola mendominasi hampir setara: `public_vs_external` (39.2%) dan `redundant_sload` (38.3%).

3. **Penghematan gas empiris terbukti nyata dan signifikan secara statistik** untuk 5 dari 6 pola yang diuji. `unchecked_arithmetic` memberikan penghematan terbesar (20.38%) yang sangat relevan untuk kontrak modern.

4. **Keberadaan anti-pattern tidak bergantung pada domain atau ukuran kontrak** (Chi-square p=0.134, KW-complexity p=0.240, Spearman ρ=+0.144). Anti-pattern boros gas adalah masalah universal lintas domain. Namun **besarnya potensi penghematan berbeda signifikan per domain** (KW-domain H=18.409, p=0.001) — Token dan NFT era lama memiliki potensi penghematan terbesar.

5. **Perbandingan dengan Slither terbatas** karena ketidakkompatibilan versi solc, namun framework kita unggul dalam mendukung kontrak era lama (solc 0.4.x). Pada 10 kontrak sampel: Our Tool = 152 findings vs Slither = 0 (parse failure).

---

## Kontribusi Ilmiah

| No | Kontribusi | Wujud |
|---|---|---|
| 1 | Tool analisis statik Python untuk 6 anti-pattern gas | `src/detectors/`, `src/ast_parser.py` |
| 2 | Normalizer AST multi-versi Solidity | `_normalize_compact()` di ast_parser.py |
| 3 | Dataset hasil analisis 75 kontrak mainnet (74 valid) | `results/pekan2_detector_results.json` |
| 4 | Benchmark gas empiris 6 pola | `results/pekan3_gas_benchmark.json` |
| 5 | Validasi statistik (4 uji utama + 3 tambahan) | `results/pekan4_statistical_tests.json` |
| 6 | Modul auto-refactoring (2 pola efektif) | `src/refactorer.py` |
| 7 | Dataset konfigurasi terstruktur | `contracts_selection.json` (75 kontrak, 15/domain) |
| 8 | Independent experiment subset | `contracts_experiment_independent.json` (38 kontrak) |

---

## Saran Penelitian Lanjutan

### Saran Teknis

1. **Perluas cakupan anti-pattern**: Tambahkan deteksi untuk `SSTORE` berulang, penggunaan `uint8` vs `uint256` (padding overhead), `keccak256` berulang, dan pola proxy yang tidak optimal.

2. **Tingkatkan akurasi deteksi**: Implementasikan data-flow analysis untuk `redundant_sload` agar tidak false positive ketika state variable diubah di antara pembacaan. Gunakan SSA (Static Single Assignment) form.

3. **Support unchecked_arithmetic pada solc 0.8.x**: Detektor perlu diuji dan dikalibrasi pada dataset kontrak era solc 0.8.x untuk memvalidasi precision/recall pada pola ini.

4. **Integrasi CI/CD**: Buat plugin untuk Hardhat atau Foundry yang menjalankan analisis otomatis saat `compile`.

5. **Benchmark lebih komprehensif**: Variasikan kondisi pengukuran (array size, iterasi, cold vs warm access) untuk mendapatkan n lebih besar untuk uji statistik.

### Saran Metodologis

1. **Dataset solc 0.8.x**: Tambahkan dataset kontrak era 2022–2024 (solc 0.8.x) untuk perbandingan Slither yang adil dan untuk menguji `unchecked_arithmetic` pada data real.

2. **Studi longitudinal**: Bandingkan kontrak yang di-deploy sebelum dan sesudah best practice dipopulerkan.

3. **Ground truth validation**: Buat kontrak dengan anti-pattern yang sengaja dibuat untuk mengukur precision/recall detektor secara eksak.

4. **L2 analysis**: Analisis apakah pola yang sama muncul di kontrak Polygon, Optimism, Arbitrum — gas model L2 berbeda.

---

## Implikasi Praktis

- Untuk **developer smart contract**: Gunakan `external` dan `calldata` untuk fungsi yang tidak dipanggil internal; cache state variable yang dibaca berulang; gunakan `unchecked` untuk loop counter yang terbatas (solc 0.8.x+).

- Untuk **auditor**: Tool ini dapat mempercepat identifikasi gas inefficiency, terutama pada kontrak era lama yang belum dioptimasi.

- Untuk **platform/protocol**: Kontrak yang sering dipanggil (DEX, lending protocol, NFT marketplace) dapat menghemat biaya yang signifikan bagi pengguna jika anti-pattern dieliminasi. Domain Token dan NFT era lama memiliki potensi terbesar.
