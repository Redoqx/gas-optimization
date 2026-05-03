# Detail Implementasi Teknis

## Struktur Direktori

```
gas_optimization/
├── src/
│   ├── ast_parser.py          ← Core: compile + walk AST
│   ├── analyzer.py            ← Entry point: jalankan semua detektor
│   ├── gas_estimator.py       ← Interface ke Hardhat
│   ├── refactorer.py          ← Auto-patch source code
│   └── detectors/
│       ├── __init__.py        ← Export ALL_DETECTORS list
│       ├── redundant_sload.py
│       ├── unoptimized_loop.py
│       ├── string_vs_bytes32.py
│       ├── public_vs_external.py
│       ├── unchecked_arithmetic.py
│       └── dead_code.py
│
├── hardhat_project/
│   ├── contracts/             ← GasBenchmark.sol (generated)
│   ├── scripts/               ← run_benchmarks.js (generated)
│   └── hardhat.config.js      ← solc 0.8.20, optimizer: false
│
├── contracts_dataset/         ← 50 file .sol
├── contracts_metadata.json    ← metadata tiap kontrak
├── results/                   ← output CSV/JSON
├── notebooks/                 ← Jupyter notebooks
│   ├── pekan1_setup.ipynb
│   ├── pekan2_detectors.ipynb
│   ├── pekan3_benchmark.ipynb
│   └── pekan4_experiment.ipynb
└── docs/knowledge_base/       ← file ini
```

---

## Modul: `src/ast_parser.py`

### Fungsi Utama

```python
generate_ast(filepath) → dict | None
```
Entry point utama. Memanggil `smart_compile_ast()` yang:
1. Baca source file
2. Auto-detect versi pragma (`detect_solc_ver()`)
3. Install solc versi yang dibutuhkan jika belum ada
4. Handle multifile (jika source berisi banyak file, split dulu)
5. Compile dengan py-solcx
6. Normalisasi AST jika format lama (`_maybe_normalize()`)

```python
walk_ast(node, callback, depth=0) → None
```
Traversal DFS seluruh AST. Callback dipanggil dengan (node, depth) untuk setiap node.

```python
find_nodes(ast, target_type) → list[dict]
```
Kumpulkan semua node dengan nodeType tertentu. Handles both modern (`nodeType`) and old format (`name`).

### Normalizer Compact AST

`_normalize_compact(node)` adalah fungsi rekursif yang mengkonversi format lama ke modern:

| Node Lama | Konversi ke |
|---|---|
| `ForStatement` | Set `initializationExpression`, `conditionExpression`, `loopExpression`, `body` dari children[0..3] |
| `ContractDefinition` | `nodes` = _wrap_state_vars(children) |
| `FunctionDefinition` | Extract `name`, `visibility`, `parameters`, `body` dari attributes & children |
| `Identifier` | `name` dari `attributes.value` |
| `MemberAccess` | `memberName` dari `attributes.member_name` |
| `PragmaDirective` | `literals` dari `attributes.literals` |
| `BinaryOperation` | `operator`, `leftExpression`, `rightExpression` |
| `Assignment` | `operator`, `leftHandSide`, `rightHandSide` |
| State VariableDeclaration | Dibungkus dalam `StateVariableDeclaration` container |

### Version Detection Map

```python
SOLC_MAP = {
    '0.4': '0.4.26',
    '0.5': '0.5.17',
    '0.6': '0.6.12',
    '0.7': '0.7.6',
    '0.8': '0.8.20',
}
```

Untuk solc <0.4.11 (The DAO, kontrak sangat lama), di-fallback ke 0.4.26 karena py-solcx tidak support versi lebih lama.

---

## Modul: `src/detectors/__init__.py`

Mengeksport list `ALL_DETECTORS` yang digunakan oleh `analyzer.py` dan notebook:

```python
from src.detectors.redundant_sload     import detect as detect_redundant_sload
from src.detectors.unoptimized_loop    import detect as detect_unoptimized_loop
from src.detectors.string_vs_bytes32   import detect as detect_string_vs_bytes32
from src.detectors.public_vs_external  import detect as detect_public_vs_external
from src.detectors.unchecked_arithmetic import detect as detect_unchecked
from src.detectors.dead_code           import detect as detect_dead_code

ALL_DETECTORS = [
    ('redundant_sload',      detect_redundant_sload),
    ('unoptimized_loop',     detect_unoptimized_loop),
    ('string_vs_bytes32',    detect_string_vs_bytes32),
    ('public_vs_external',   detect_public_vs_external),
    ('unchecked_arithmetic', detect_unchecked),
    ('dead_code',            detect_dead_code),
]
```

---

## Modul: `src/gas_estimator.py`

### Arsitektur

Gas estimator menyimpan source code kontrak benchmark dan script Hardhat **sebagai string Python** (tidak di-hardcode ke file terpisah). Saat dijalankan:

1. `write_benchmarks()`: tulis ke `hardhat_project/contracts/GasBenchmark.sol` dan `hardhat_project/scripts/run_benchmarks.js`, lalu compile
2. `measure_all()`: jalankan script via `subprocess`, parse output JSON dari stdout

### Protokol Output

Script JS menggunakan sentinel markers untuk parsing:
```
GAS_RESULTS_BEGIN
{"pattern": "...", "boros": "...", "hemat": "...", "diff": "...", "pct_save": "..."}
...
GAS_RESULTS_END
```
Python hanya parse baris yang berada di antara kedua marker.

### Keputusan Implementasi Penting

- **`encoding='utf-8'`** wajib pada `write_text()` — Windows default cp1252 tidak support karakter Unicode di komentar Solidity
- **Ethers v6 API**: `waitForDeployment()` bukan `deployed()`, BigInt arithmetic untuk gas estimation
- **CJS format**: script menggunakan `require()` bukan `import` karena `hardhat.config.js` adalah CommonJS

---

## Modul: `src/refactorer.py`

### Tiga Fungsi Refactoring

**`refactor_public_to_external(source, findings)`**:
- Input: source code string + list findings dari detektor public_vs_external
- Proses: untuk setiap fungsi yang di-flag, cari baris deklarasi dan ganti `public` → `external`
- Pattern regex: `r'(\bfunction\s+' + re.escape(func_name) + r'\b[^{]*?)\bpublic\b'`
- Jika finding tidak punya line number (format AST lama): scan seluruh file

**`refactor_cache_loop_length(source, findings)`**:
- Untuk setiap loop yang di-flag, insert `uint256 _xLen = x.length;` sebelum loop dan ganti `.length` dengan cache variable
- Patch dilakukan **bottom-up** (dari baris terbesar ke terkecil) agar nomor baris tidak bergeser saat insert
- Pattern word-boundary: `re.compile(r'\b' + re.escape(arr_name) + r'\.length\b')` — penting untuk tidak cocok dengan `_owners.length` saat mencari `owners.length`

**`refactor_sload_add_comments(source, findings)`**:
- Tambah komentar `// TODO: cache {var} ke local var untuk hemat SLOAD` di baris fungsi yang di-flag
- Safe fallback: tidak mengubah logic kode, hanya menambah petunjuk

### `apply_all_refactors(filepath, findings_by_type)`

Entry point yang memanggil ketiga fungsi di atas secara berurutan dan mengembalikan `(refactored_source, summary_dict)`.

---

## Hardhat Configuration

```javascript
// hardhat_project/hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: { enabled: false }  // JANGAN DIUBAH
    }
  },
  networks: {
    hardhat: {}
  }
};
```

**Kenapa `optimizer: false` dikunci**: Gas measurement bertujuan mengukur efek keputusan programmer. Dengan optimizer ON, compiler sendiri yang mengoptimasi — misalnya menghapus dead code atau menggabungkan SLOAD berulang. Ini akan menghilangkan perbedaan yang ingin kita ukur.

---

## Alur Data Lengkap

```
contracts_dataset/*.sol
    │
    ▼
src/ast_parser.py::generate_ast()
    │ AST dict (normalized)
    ▼
src/detectors/*.py::detect(ast)
    │ list of findings
    ▼
results/pekan2_detector_results.json
    │
    ├── ▼ Visualisasi di notebooks/pekan2_detectors.ipynb
    │
    └── ▼ src/refactorer.py::apply_all_refactors()
             │ refactored source .sol
             ▼
           results/refactored_*.sol

hardhat_project/contracts/GasBenchmark.sol (generated)
    │
    ▼
Hardhat EVM: npx hardhat run scripts/run_benchmarks.js
    │ JSON per pattern
    ▼
results/pekan3_gas_benchmark.json
    │
    ▼
notebooks/pekan4_experiment.ipynb
    │ scipy stats
    ▼
results/pekan4_statistical_tests.json
results/tabel_4_4*.csv
```

---

## Environment & Dependencies

### `environment.yml`
```yaml
name: gas_opt
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pip
  - jupyter
  - notebook
  - ipykernel
  - requests
  - numpy
  - scipy
  - pip:
      - py-solc-x
      - python-dotenv
      - slither-analyzer
      - packaging
```

### Cara Aktivasi
```bash
conda activate gas_opt
jupyter notebook
```

### Cara Install Ulang dari Scratch
```bash
conda env create -f environment.yml
conda activate gas_opt
cd hardhat_project && npm install && cd ..
```

---

## Catatan Kompatibilitas Windows

Beberapa masalah yang ditemukan saat development di Windows:

| Masalah | Penyebab | Solusi |
|---|---|---|
| `UnicodeEncodeError` saat tulis .sol | Windows default encoding cp1252 | Selalu pakai `encoding='utf-8'` |
| Slither `The system cannot find the path specified` | `2>/dev/null` adalah bash syntax | Gunakan `shutil.which()` + list args + temp file |
| `conda run -c "python -c ..."` gagal | Conda Windows tidak support multiline -c | Tulis ke .py file dulu, lalu jalankan |
| numpy `ModuleNotFoundError` | Tidak di-include di environment.yml awal | Install manual + tambah ke environment.yml |
