# CLAUDE.md — Mini Project 3B: Gas Optimization Framework

File ini adalah konteks project untuk Claude Code.
Baca ini sebelum melakukan apapun di project ini.

---

## 🎯 Tentang Project

**Nama:** Gas Optimization Framework untuk Smart Contract Solidity  
**Mata Kuliah:** Komputasi Berbasis Jaringan — S2 Tesis  
**Timeline:** Pekan 1 (Setup) → Pekan 2 (Detector) → Pekan 3 (Hardhat + Slither) → Pekan 4 (Eksperimen)

### Apa yang dibangun?
Tool analisis statik Python yang:
1. Membaca kode Solidity (`.sol`) dan men-generate AST
2. Mendeteksi 6 anti-pattern boros gas
3. Mengukur penghematan gas empiris via Hardhat
4. Membandingkan hasil dengan Slither

---

## 💻 Environment

| Tool | Versi | Catatan |
|---|---|---|
| Python | 3.11 | via conda env `gas_opt` |
| Node.js | v24.14.1 | sudah ada di sistem |
| npm | 11.11.0 | sudah ada di sistem |
| solc | 0.8.20 | **fixed, jangan ganti versi** |
| Hardhat | latest | di `hardhat_project/` |
| Conda env | `gas_opt` | aktifkan sebelum kerja |

### Aktivasi environment
```bash
conda activate gas_opt
```

### Key constraint yang tidak boleh diubah
- `solc` wajib versi **0.8.20** — sesuai variabel tetap eksperimen
- `optimizer: false` di Hardhat — agar gas measurement konsisten
- Seed tetap di setiap run eksperimen

---

## 📁 Struktur Project

```
gas_optimization/
├── CLAUDE.md                    ← file ini
├── .env                         ← ETHERSCAN_API_KEY (jangan di-commit)
├── .gitignore
├── environment.yml              ← definisi conda env
├── README.md
│
├── hardhat_project/             ← Node.js project untuk ukur gas
│   ├── contracts/               ← file .sol (test + kontrak yang dianalisis)
│   ├── scripts/                 ← script JS pengukur gas
│   ├── hardhat.config.js        ← optimizer: false, solc 0.8.20
│   └── package.json
│
├── contracts_dataset/           ← 50 kontrak .sol dari Etherscan
│   └── {Domain}_{No}_{Name}.sol ← contoh: DeFi_01_WETH.sol
│
├── contracts_metadata.json      ← metadata: LOC, domain, complexity, compile_ok
│
├── notebooks/
│   └── pekan1_setup.ipynb       ← notebook Pekan 1 (sudah selesai)
│
├── src/                         ← kode utama (dibuat mulai Pekan 2)
│   ├── ast_parser.py            ← generate_ast(), walk_ast(), find_nodes()
│   ├── detectors/               ← 6 modul detector anti-pattern
│   │   ├── redundant_sload.py
│   │   ├── unoptimized_loop.py
│   │   ├── string_vs_bytes32.py
│   │   ├── public_vs_external.py
│   │   ├── unchecked_arithmetic.py
│   │   └── dead_code.py
│   ├── gas_estimator.py         ← interface ke Hardhat
│   ├── refactorer.py            ← auto-refactoring (Pekan 3)
│   └── analyzer.py              ← entry point utama
│
└── results/                     ← output CSV/JSON dari eksperimen
```

---

## 🔧 Common Commands

### Jalankan Hardhat
```bash
# Dari root project
cd hardhat_project

# Compile kontrak
npx hardhat compile

# Ukur gas (script tertentu)
npx hardhat run scripts/ukur_gas.js --network hardhat

# Kembali ke root
cd ..
```

### Python / solcx
```python
import solcx
solcx.set_solc_version('0.8.20')   # selalu set ini di awal
```

### Baca API Key
```python
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv('ETHERSCAN_API_KEY')
```

### Baca metadata dataset
```python
import json
with open('contracts_metadata.json') as f:
    metadata = json.load(f)

# Filter yang bisa compile
valid = [m for m in metadata if m.get('compile_ok')]
```

---

## 🐛 6 Anti-Pattern yang Dideteksi

| No | Nama | Node AST | Penjelasan singkat |
|---|---|---|---|
| 1 | Redundant SLOAD | `Identifier` | State var dibaca dari storage >1x tanpa cache lokal |
| 2 | Unoptimized Loop | `ForStatement` | `.length` dibaca dari storage di setiap iterasi |
| 3 | String vs Bytes32 | `ElementaryTypeName` | Pakai `string` untuk teks pendek yang bisa pakai `bytes32` |
| 4 | Public vs External | `FunctionDefinition` | Fungsi `public` yang tidak pernah dipanggil internal |
| 5 | Unchecked Arithmetic | `BinaryOperation` | Operasi `+`/`-` di loop yang sudah pasti tidak overflow |
| 6 | Dead Code | `FunctionDefinition` | Fungsi yang tidak pernah dipanggil oleh siapapun |

---

## 📊 Dataset

- **50 kontrak** dari Etherscan (mainnet Ethereum, verified source)
- **5 domain**: DeFi (10), NFT (10), Token (10), Governance (10), Utility (10)
- **3 complexity level**: Simple (<100 LOC), Medium (100–500), Complex (500+)
- Tersimpan di `contracts_dataset/` dan metadata di `contracts_metadata.json`
- File `contracts_metadata.json` punya field: `alamat`, `domain`, `nama`, `file`, `loc`, `complexity`, `compile_ok`

---

## 📅 Status Per Pekan

### ✅ Pekan 1 — SELESAI
- solc 0.8.20 terinstall
- Hardhat project setup di `hardhat_project/`
- 50 kontrak didownload ke `contracts_dataset/`
- AST parser dasar: `generate_ast()`, `walk_ast()`, `find_nodes()`
- Inventarisasi node types selesai

### 🔄 Pekan 2 — IN PROGRESS / TODO
- Buat `src/ast_parser.py` (pindahkan fungsi dari notebook)
- Buat 6 modul detector di `src/detectors/`
- Buat `src/gas_estimator.py` untuk interface ke Hardhat
- Uji detector pada 50 kontrak
- Catat hasil ke `results/`

### ⏳ Pekan 3 — BELUM
- Auto-refactoring module
- Integrasi dengan Slither untuk comparison
- Head-to-head benchmarking

### ⏳ Pekan 4 — BELUM
- Full experiment run (50 kontrak)
- Isi tabel 4.4a–4.4e dari dokumen project
- Uji statistik (Wilcoxon, McNemar, dll)
- Laporan akhir

---

## ⚠️ Hal yang Perlu Diperhatikan

1. **Jangan ubah versi solc** — semua kontrak di dataset dikompilasi dengan 0.8.20. Ganti versi = hasil tidak konsisten.

2. **`optimizer: false` di hardhat.config.js** — jangan pernah set `true`, akan mengacaukan angka gas.

3. **Beberapa kontrak gagal compile** — ini normal. Selalu filter dengan `compile_ok: true` sebelum analisis.

4. **Rate limit Etherscan** — kalau download kontrak baru, selalu `time.sleep(0.25)` antar request.

5. **Dataset tidak di-commit ke GitHub** — ada di `.gitignore`. Setiap orang generate sendiri via notebook.

6. **`.env` tidak di-commit** — simpan API key di `.env`, jangan hardcode di kode.

---

## 🔗 Referensi

- Dokumen project: `03_Blockchain_Skenario.pdf`
- Panduan setup: `3B_SetupGuide_Local.md`
- Knowledge base: `3B_KnowledgeBase_Local.md`
- Penjelasan konsep: `3B_Penjelasan_Lengkap.md`