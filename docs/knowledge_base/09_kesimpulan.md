# Kesimpulan & Saran

## Kesimpulan per Rumusan Masalah

### RQ1: Pola anti-pattern gas apa yang umum ditemukan di smart contract nyata?

**Jawaban**: Dari 6 anti-pattern yang diteliti, **`public_vs_external`** adalah yang paling umum ditemukan (283 dari 646 temuan, 43.8%). Anti-pattern ini dominan karena mayoritas kontrak dalam dataset ditulis di era Solidity 0.4.x–0.6.x ketika `public` adalah default dan best practice `external`/`calldata` belum dipopulerkan.

Urutan frekuensi: public_vs_external (43.8%) > redundant_sload (31.6%) > string_vs_bytes32 (11.1%) > dead_code (8.1%) > unchecked_arithmetic (1.5%) > unoptimized_loop (0.8%)

Anti-pattern ditemukan di **82.6% dari 46 kontrak valid** (38 kontrak), menunjukkan bahwa pola boros gas adalah hal yang umum dan meluas di smart contract real-world.

### RQ2: Seberapa besar penghematan gas yang dapat dicapai?

**Jawaban**: Penghematan gas bervariasi signifikan per pola:

| Anti-Pattern | Penghematan |
|---|---|
| unchecked_arithmetic | 20.38% (tertinggi) |
| public_vs_external | 5.09% |
| string_vs_bytes32 | 3.87% |
| unoptimized_loop | 2.01% |
| redundant_sload | 0.77% |
| dead_code | 0% (pada runtime, deployment tidak terukur) |

Rata-rata penghematan (6 pola): **5.35%**. Jika diterapkan pada kontrak yang sering dipanggil (ribuan transaksi/hari), penghematan ini signifikan dalam nilai ETH.

### RQ3: Apakah framework deteksi statik berbasis AST efektif?

**Jawaban**: Ya, efektif. Framework berhasil mendeteksi 646 temuan pada 46 kontrak real-world dari berbagai domain dan era. Keunggulan utama:
- Mendukung multi-versi solc (0.4.x hingga 0.8.x) melalui py-solcx
- Berhasil menormalisasi dua format AST Solidity (lama/baru)
- Menemukan temuan pada kontrak yang bahkan tidak bisa dianalisis Slither (0.4.x era)

### RQ4: Apakah penghematan gas signifikan secara statistik?

**Jawaban**: **Ya**, signifikan secara statistik — dikonfirmasi oleh dua uji Wilcoxon independen:

1. **Wilcoxon per-pattern** (n=5 efektif): **W=15.0, p=0.031** — semua 5 pola menunjukkan penghematan positif (W=15 adalah nilai maksimum untuk n=5).

2. **Wilcoxon per-contract** (n=35): **W=630.0, p<0.001** — menggunakan kontrak sebagai unit observasi dengan estimated savings `Σ(findings × avg_diff_gas)`. Hasil sangat kuat: W=630 adalah nilai maksimum untuk n=35, semua kontrak yang dioptimasi menunjukkan savings positif.

Uji tambahan **Kruskal-Wallis per-domain** (H=14.015, p=0.007) menunjukkan bahwa besarnya potensi penghematan berbeda signifikan antar domain — kontrak Token dan DeFi era lama memiliki potensi penghematan gas terbesar.

---

## Kesimpulan Umum

1. **Framework gas optimization berbasis AST terbukti feasible** dan dapat diimplementasikan dalam Python menggunakan py-solcx. Analisis statik menghasilkan findings yang relevan dan dapat diinterpretasi.

2. **Pola boros gas sangat umum** di smart contract mainnet Ethereum, khususnya pada kontrak era 2017–2019. Sebagian besar kontrak (82.6%) memiliki setidaknya satu temuan.

3. **Penghematan gas empiris terbukti nyata dan signifikan secara statistik** untuk 5 dari 6 pola yang diuji. `unchecked_arithmetic` memberikan penghematan terbesar (20.38%) yang sangat relevan untuk kontrak modern.

4. **Keberadaan anti-pattern tidak bergantung pada domain atau ukuran kontrak** (Chi-square p=0.073, KW-complexity p=0.427, Spearman ρ=-0.261). Anti-pattern boros gas adalah masalah universal lintas domain. Namun **besarnya potensi penghematan berbeda signifikan per domain** (KW-domain H=14.015, p=0.007) — domain Token dan DeFi era lama memiliki potensi penghematan terbesar karena dominasi `public_vs_external`.

5. **Perbandingan dengan Slither terbatas** karena ketidakkompatibilan versi solc, namun framework kita unggul dalam mendukung kontrak era lama (solc 0.4.x).

---

## Kontribusi Ilmiah

| No | Kontribusi | Wujud |
|---|---|---|
| 1 | Tool analisis statik Python untuk 6 anti-pattern gas | `src/detectors/`, `src/ast_parser.py` |
| 2 | Normalizer AST multi-versi Solidity | `_normalize_compact()` di ast_parser.py |
| 3 | Dataset hasil analisis 50 kontrak mainnet | `results/pekan2_detector_results.json` |
| 4 | Benchmark gas empiris 6 pola | `results/pekan3_gas_benchmark.json` |
| 5 | Validasi statistik (4 uji) | `results/pekan4_statistical_tests.json` |
| 6 | Modul auto-refactoring (3 pola) | `src/refactorer.py` |

---

## Saran Penelitian Lanjutan

### Saran Teknis

1. **Perluas cakupan anti-pattern**: Tambahkan deteksi untuk `SSTORE` berulang, penggunaan `uint8` vs `uint256` (padding overhead), `keccak256` berulang, dan pola proxy yang tidak optimal.

2. **Tingkatkan akurasi deteksi**: Implementasikan data-flow analysis untuk `redundant_sload` agar tidak false positive ketika state variable diubah di antara pembacaan. Gunakan SSA (Static Single Assignment) form.

3. **Integrasi CI/CD**: Buat plugin untuk Hardhat atau Foundry yang menjalankan analisis otomatis saat `compile` — sehingga feedback diberikan real-time ke developer.

4. **Benchmark lebih komprehensif**: Variasikan kondisi pengukuran (array size, iterasi, cold vs warm access) untuk mendapatkan n lebih besar untuk uji statistik.

5. **Refactoring otomatis penuh**: Untuk `redundant_sload`, implementasikan full data-flow analysis berbasis SSA untuk patch otomatis yang aman.

### Saran Metodologis

1. **Gunakan kontrak L2**: Analisis apakah pola yang sama muncul di kontrak Polygon, Optimism, Arbitrum — gas model L2 berbeda, beberapa optimasi mungkin lebih/kurang relevan.

2. **Studi longitudinal**: Bandingkan kontrak yang di-deploy sebelum dan sesudah best practice dipopulerkan (misal: sebelum/sesudah EIP-1559, sebelum/sesudah solcx 0.8).

3. **Ground truth validation**: Buat kontrak dengan anti-pattern yang sengaja dibuat (synthetic benchmark) untuk mengukur precision/recall detektor secara eksak.

4. **User study**: Evaluasi apakah findings yang dihasilkan framework benar-benar digunakan developer — apakah meningkatkan efisiensi proses review kode.

---

## Implikasi Praktis

- Untuk **developer smart contract**: Gunakan `external` dan `calldata` untuk fungsi yang tidak dipanggil internal; gunakan `unchecked` untuk loop counter yang terbatas; cache state variable yang dibaca berulang ke variabel lokal.

- Untuk **auditor**: Tool ini dapat mempercepat identifikasi gas inefficiency, terutama pada kontrak era lama yang belum dioptimasi.

- Untuk **platform/protocol**: Kontrak yang sering dipanggil (DEX, lending protocol) dapat menghemat biaya yang signifikan bagi pengguna jika anti-pattern dieliminasi.
