# Alur Penelitian: Kronologi Pekan 1–4

## Pekan 1 — Setup & Fondasi

**Tujuan**: Menyiapkan seluruh environment dan mengumpulkan dataset 50 kontrak.

### Langkah-langkah

1. **Setup conda environment** `gas_opt` dengan Python 3.11
2. **Install py-solcx** dan download solc multi-versi (0.4.26, 0.5.17, 0.6.12, 0.7.6, 0.8.20)
3. **Setup Hardhat project** di `hardhat_project/` — Node.js, hardhat.config.js dengan `optimizer: false` dan solc 0.8.20
4. **Download 50 kontrak** dari Etherscan via API (rate-limit: 0.25s antar request), simpan ke `contracts_dataset/`
5. **Build AST parser dasar**: `generate_ast()`, `walk_ast()`, `find_nodes()`
6. **Inventarisasi node types**: Eksplor 50 kontrak untuk mengetahui nodeType apa yang umum muncul
7. **Update `contracts_metadata.json`**: Catat LOC, domain, complexity, dan `compile_ok` untuk tiap kontrak

### Output Pekan 1
- `contracts_dataset/` — 50 file `.sol`
- `contracts_metadata.json` — metadata 50 kontrak
- `notebooks/pekan1_setup.ipynb` — notebook setup
- `src/ast_parser.py` versi awal

### Keputusan Teknis Penting

**Solc versi 0.8.20 sebagai fixed version untuk benchmark**: Semua benchmark contract dikompilasi dengan versi ini agar perbandingan gas konsisten (variabel tetap eksperimen).

**Optimizer: false di Hardhat**: Jika diaktifkan, kompiler akan mengoptimasi sendiri → mengaburkan perbedaan antara kode boros dan hemat. Untuk mengukur efek keputusan programmer, optimizer harus mati.

---

## Pekan 2 — Membangun 6 Detektor

**Tujuan**: Implementasi 6 modul detektor anti-pattern dan uji pada dataset.

### Tantangan Utama: Dua Format AST

Solidity <0.6 menghasilkan format AST "compact JSON" yang berbeda dari format modern. Ini ditemukan saat semua detektor mengembalikan 0 findings pada kontrak-kontrak tua (WETH9, TetherToken, MultiSigWallet yang menggunakan solc 0.4.x).

**Solusi**: Tambahkan normalizer `_normalize_compact()` di `ast_parser.py` yang secara rekursif mengkonversi format lama (`name`/`children`/`attributes`) ke format modern (`nodeType`/named-fields). Normalizer ini menangani ~25 jenis node berbeda.

### Bug Signifikan yang Ditemukan & Diperbaiki

**Bug `find_nodes()`**: Fungsi asli hanya mengecek `nodeType`, padahal node format lama tidak punya `nodeType`. Diperbaiki dengan `n.get('nodeType') or n.get('name')`.

**Bug `unchecked_arithmetic`**: `PragmaDirective.value` tidak ada di format AST modern — versi harus dibaca dari `PragmaDirective.literals` (array). Diperbaiki dengan `' '.join(literals)` sebelum parsing versi.

**Bug loop increment detection**: Deteksi awal hanya mencari `BinaryOperation` (+/-). Diperluas ke `Assignment` (+=/-=) dan `UnaryOperation` (++/--) yang lebih umum.

### Langkah-langkah

1. Buat `src/detectors/__init__.py` — export `ALL_DETECTORS` list
2. Implementasi 6 modul detektor (satu per anti-pattern)
3. Uji smoke test pada 3 kontrak representatif
4. Temukan masalah format AST lama → implementasi normalizer
5. Re-run semua detektor → 646 findings terdeteksi
6. Jalankan batch pada 50 kontrak, simpan ke `results/pekan2_detector_results.json`
7. Buat `notebooks/pekan2_detectors.ipynb`

### Output Pekan 2
- `src/detectors/` — 6 modul + `__init__.py`
- `src/ast_parser.py` — versi lengkap dengan normalizer
- `results/pekan2_detector_results.json` — 646 findings dari 46 kontrak
- `notebooks/pekan2_detectors.ipynb`

---

## Pekan 3 — Benchmark Gas & Refactoring

**Tujuan**: Mengukur penghematan gas empiris dan membangun modul auto-refactoring.

### Komponen yang Dibangun

**`src/gas_estimator.py`**:
- Berisi source code `GasBenchmark.sol` sebagai string Python
- Berisi Hardhat script `run_benchmarks.js` sebagai string Python  
- `write_benchmarks()`: tulis file ke `hardhat_project/`, compile
- `measure_all()`: jalankan script, parse output JSON, kembalikan hasil

**`src/refactorer.py`**:
- `refactor_public_to_external()`: ubah `public` → `external` pada fungsi yang di-flag
- `refactor_cache_loop_length()`: insert `uint256 _xLen = x.length;` sebelum loop
- `refactor_sload_add_comments()`: tambah komentar TODO untuk redundant_sload

### Bug yang Ditemukan & Diperbaiki

**Bug `UnicodeEncodeError` di gas_estimator**: Windows menggunakan encoding cp1252 sebagai default. File `.sol` yang ditulis berisi karakter `─` (U+2500) dari komentar dekoratif. Diperbaiki dengan `encoding='utf-8'` pada semua `write_text()` calls.

**Bug word-boundary di refactorer**: Substring matching `owners.length in line` juga cocok dengan `_owners.length` karena Python `in` operator tidak tahu word boundary. Kontrak MultiSigWallet punya parameter bernama `_owners` dan state variable bernama `owners`. Refactorer salah me-replace `_owners.length` menjadi `__ownersLen` (double underscore). Diperbaiki dengan `re.compile(r'\b' + re.escape(arr_name) + r'\.length\b')`.

**Bug Slither di Windows**: `2>/dev/null` adalah bash syntax yang tidak berjalan di Windows cmd.exe. `slither {sol_file}` dengan `shell=True` gagal dengan "The system cannot find the path specified." Diperbaiki dengan `shutil.which('slither')` untuk path, list args (tanpa shell=True), dan temp file untuk output JSON.

### Hasil Benchmark Gas

| Anti-Pattern | Gas Boros | Gas Hemat | Selisih | Hemat (%) |
|---|---|---|---|---|
| redundant_sload | 24.208 | 24.022 | 186 | 0.77% |
| unoptimized_loop | 51.187 | 50.156 | 1.031 | 2.01% |
| string_vs_bytes32 | 24.540 | 23.590 | 950 | 3.87% |
| public_vs_external | 52.544 | 49.871 | 2.673 | 5.09% |
| unchecked_arithmetic | 59.105 | 47.060 | 12.045 | 20.38% |
| dead_code | 123.985 | 123.985 | 0 | 0.00% |

### Mengapa dead_code = 0%?

Compiler Solidity mengeliminasi fungsi internal yang tidak pernah dipanggil **bahkan tanpa optimizer**. Fungsi-fungsi dead tersebut tidak masuk ke deployment bytecode, sehingga `estimateGas` untuk deployment menunjukkan nilai identik. Ini adalah keterbatasan pengukuran, bukan berarti dead code tidak berdampak — di kontrak produksi dengan optimizer ON, dampaknya bisa berbeda.

### Output Pekan 3
- `src/gas_estimator.py`
- `src/refactorer.py`
- `results/pekan3_gas_benchmark.json`
- `results/pekan3_slither_results.json` (10 kontrak, semua Slither=0)
- `results/refactored_MultiSigWallet.sol`
- `notebooks/pekan3_benchmark.ipynb`

---

## Pekan 4 — Full Experiment & Analisis Statistik

**Tujuan**: Agregasi semua hasil, uji statistik, export untuk laporan.

### Langkah-langkah

1. Load semua hasil Pekan 2 & 3
2. Reproduce Tabel 4.4a–4.4d dengan format thesis-ready
3. Tabel 4.4e: perbandingan dengan Slither
4. Uji Wilcoxon signed-rank (gas savings)
5. Uji Chi-square (domain vs findings)
6. Uji Kruskal-Wallis (complexity vs findings)
7. Korelasi Spearman (LOC vs findings)
8. Export semua tabel ke CSV
9. Export `pekan4_statistical_tests.json`

### Masalah Minor

**numpy tidak ada di environment**: Install via `pip install numpy` (sudah ditambahkan ke `environment.yml` setelah itu).

### Output Pekan 4
- `results/tabel_4_4a_gas_savings.csv`
- `results/tabel_4_4b_domain.csv`
- `results/tabel_4_4c_top10.csv`
- `results/tabel_4_4d_complexity.csv`
- `results/tabel_4_4e_slither.csv`
- `results/pekan4_all_findings.csv`
- `results/pekan4_statistical_tests.json`
- `notebooks/pekan4_experiment.ipynb`

---

## Ringkasan Timeline

| Pekan | Fokus | Deliverable Utama | Status |
|---|---|---|---|
| 1 | Setup & dataset collection | 50 kontrak + metadata | ✅ Selesai |
| 2 | 6 detektor anti-pattern | 646 findings + notebook | ✅ Selesai |
| 3 | Gas benchmark + refactoring | Tabel gas + refactored code | ✅ Selesai |
| 4 | Statistik + export | 4 uji + 6 CSV + JSON | ✅ Selesai |
