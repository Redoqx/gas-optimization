# Mini Project 3B — Gas Optimization Framework

Gas Optimization Framework untuk Smart Contract Solidity menggunakan Static Analysis.

## Setup

### Prerequisites
- Conda
- Node.js >= 22

### Instalasi

1. Clone repository
   ```bash
   git clone https://github.com/Redoqx/gas_optimization.git
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
