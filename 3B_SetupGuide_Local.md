# Setup Guide — Mini Project 3B (Lokal + GitHub)
### Environment: Node v24 · npm 11 · Conda · Windows/Mac/Linux

---

## 📋 Status Awal Kamu

| Tool | Status | Versi |
|---|---|---|
| Node.js | ✅ Sudah ada | v24.14.1 |
| npm | ✅ Sudah ada | 11.11.0 |
| Conda | ✅ Sudah ada | — |
| Folder | ✅ Sudah ada | `gas_optimization/` |

Tidak perlu install Node sama sekali. Langsung ke setup project.

---

## 🗂️ Struktur Folder Target

```
gas_optimization/                  ← folder yang sudah kamu buat
├── .env                           ← API key (TIDAK di-commit ke GitHub)
├── .gitignore                     ← daftar file yang diabaikan git
├── environment.yml                ← definisi conda env (di-commit)
├── README.md                      ← dokumentasi project (di-commit)
│
├── hardhat_project/               ← project Node.js untuk ukur gas
│   ├── contracts/                 ← file .sol test
│   ├── scripts/                   ← script JS pengukur gas
│   ├── hardhat.config.js
│   └── package.json
│
├── contracts_dataset/             ← 50 kontrak dari Etherscan (di-gitignore)
├── contracts_metadata.json        ← metadata dataset (opsional di-commit)
│
├── notebooks/
│   └── pekan1_setup.ipynb         ← notebook utama (di-commit)
│
└── results/                       ← output analisis Pekan 2+
```

---

## 🚀 Setup Langkah demi Langkah

### Langkah 1 — Init Git Repository

```bash
cd gas_optimization

git init
git branch -M main
```

### Langkah 2 — Buat .gitignore

```bash
# Buat file .gitignore
```

Isi file `.gitignore`:

```
# Rahasia
.env

# Dataset besar (teman clone ulang sendiri via notebook)
contracts_dataset/

# Node.js
hardhat_project/node_modules/
hardhat_project/artifacts/
hardhat_project/cache/

# Python
__pycache__/
*.pyc
.ipynb_checkpoints/

# Hasil (opsional — hapus baris ini kalau mau share results)
results/
```

### Langkah 3 — Buat environment.yml

Isi file `environment.yml`:

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
  - pip:
      - py-solc-x
      - python-dotenv
```

> Node.js tidak masuk sini karena sudah ada di sistem kamu (v24).

### Langkah 4 — Buat Conda Environment

```bash
# Dari dalam folder gas_optimization/
conda env create -f environment.yml

# Aktifkan
conda activate gas_opt

# Verifikasi
python --version    # 3.11.x
pip show py-solc-x  # harus ada
```

### Langkah 5 — Install solc 0.8.20

```bash
# Pastikan gas_opt aktif
conda activate gas_opt

python -c "
import solcx
print('Installing solc 0.8.20...')
solcx.install_solc('0.8.20')
solcx.set_solc_version('0.8.20')
print('Done:', solcx.get_solc_version())
"
```

### Langkah 6 — Setup Hardhat

```bash
# Buat folder dan masuk
mkdir hardhat_project
cd hardhat_project

# Init npm project
npm init -y

# Install Hardhat
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox

# Verifikasi (harus muncul tanpa warning)
npx hardhat --version

# Kembali ke root
cd ..
```

Buat file `hardhat_project/hardhat.config.js`:

```javascript
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: false,  // WAJIB false — agar gas measurement konsisten
      },
    },
  },
  networks: {
    hardhat: {},
  },
};
```

### Langkah 7 — Buat folder notebooks dan results

```bash
mkdir notebooks
mkdir results
```

### Langkah 8 — Buat file .env

```bash
# Buat file .env (TIDAK di-commit ke GitHub)
```

Isi file `.env`:

```
ETHERSCAN_API_KEY=isi_api_key_kamu_di_sini
```

Cara dapat API key Etherscan:
1. Buka [etherscan.io](https://etherscan.io) → daftar akun gratis
2. Login → klik nama akun → **API Keys** → **Add**
3. Copy key → paste di `.env`

### Langkah 9 — Daftarkan Jupyter Kernel

```bash
conda activate gas_opt

python -m ipykernel install --user \
  --name gas_opt \
  --display-name "Gas Opt 3B"
```

### Langkah 10 — Buat README.md

Isi file `README.md`:

```markdown
# Mini Project 3B — Gas Optimization Framework

Gas Optimization Framework untuk Smart Contract Solidity menggunakan Static Analysis.

## Setup

### Prerequisites
- Conda
- Node.js >= 22

### Instalasi

1. Clone repository
   ```bash
   git clone https://github.com/USERNAME/gas_optimization.git
   cd gas_optimization
   ```

2. Buat conda environment
   ```bash
   conda env create -f environment.yml
   conda activate gas_opt
   ```

3. Install solc
   ```bash
   python -c "import solcx; solcx.install_solc('0.8.20'); solcx.set_solc_version('0.8.20')"
   ```

4. Setup Hardhat
   ```bash
   cd hardhat_project
   npm install
   cd ..
   ```

5. Buat file `.env` dan isi API key Etherscan
   ```
   ETHERSCAN_API_KEY=your_key_here
   ```

6. Jalankan notebook
   ```bash
   jupyter notebook notebooks/pekan1_setup.ipynb
   ```

## Struktur

- `notebooks/` — Jupyter notebooks per pekan
- `contracts_dataset/` — Dataset kontrak Solidity (download via notebook)
- `hardhat_project/` — Project Hardhat untuk pengukuran gas
- `results/` — Output analisis
```

### Langkah 11 — Push ke GitHub

```bash
# Dari dalam gas_optimization/

# Commit awal
git add .
git commit -m "Initial setup: environment, hardhat, notebooks"

# Buat repo di GitHub dulu di github.com, lalu:
git remote add origin https://github.com/USERNAME/gas_optimization.git
git push -u origin main
```

---

## 👥 Cara Teman Clone dan Run

Setelah repo ada di GitHub, teman cukup:

```bash
# 1. Clone
git clone https://github.com/USERNAME/gas_optimization.git
cd gas_optimization

# 2. Buat environment
conda env create -f environment.yml
conda activate gas_opt

# 3. Install solc
python -c "import solcx; solcx.install_solc('0.8.20'); solcx.set_solc_version('0.8.20')"

# 4. Install Hardhat dependencies
cd hardhat_project && npm install && cd ..

# 5. Buat .env dengan API key masing-masing
echo "ETHERSCAN_API_KEY=api_key_teman" > .env

# 6. Daftarkan kernel
python -m ipykernel install --user --name gas_opt --display-name "Gas Opt 3B"

# 7. Jalankan notebook
jupyter notebook notebooks/pekan1_setup.ipynb
```

> **Dataset tidak ikut di GitHub** (di-gitignore karena besar).  
> Setiap orang download ulang via notebook menggunakan API key masing-masing.

---

## ✅ Verifikasi Akhir

Jalankan ini untuk konfirmasi semua siap:

```bash
conda activate gas_opt
python -c "
import sys, subprocess, os
from dotenv import load_dotenv

load_dotenv()

checks = {
    'Python 3.11'  : sys.version.startswith('3.11'),
    'py-solc-x'    : __import__('solcx').get_solc_version() is not None,
    'API Key'      : bool(os.getenv('ETHERSCAN_API_KEY')),
}

node  = subprocess.run(['node',    '--version'], capture_output=True, text=True)
npx   = subprocess.run(['npx', 'hardhat', '--version'],
                        capture_output=True, text=True,
                        cwd='hardhat_project')

checks['Node.js 24']  = node.returncode == 0
checks['Hardhat']     = npx.returncode == 0

print('=== VERIFIKASI SETUP ===')
for label, ok in checks.items():
    print(f'  {\"✅\" if ok else \"❌\"} {label}')

all_ok = all(checks.values())
print()
print('Siap lanjut ke notebook!' if all_ok else 'Ada yang belum siap — cek tanda ❌')
"
```
