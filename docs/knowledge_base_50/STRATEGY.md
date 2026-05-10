# Strategi Eksperimen: Dataset 50 Kontrak (10/Domain)

**Branch**: `experiment/50-contracts`  
**Dataset**: `contracts_selection_50.json` — 50 kontrak, 10 per domain  
**Tujuan**: Replikasi eksperimen utama dengan dataset yang lebih seimbang dan bersih  
**Tanggal mulai**: 2026-05-10

---

## Latar Belakang & Motivasi

Dataset 75 kontrak (branch `main`) memiliki beberapa ketidakseimbangan:
- Domain NFT didominasi kontrak duplikat atau kontrak sangat modern dengan 0–2 findings
- Domain Token punya 2 `AdminUpgradeabilityProxy` yang hampir identik
- Domain Governance punya 3 `GovernorBravo*` yang saling overlapping
- Complexity Simple hanya 2 kontrak (keduanya Utility)

Dataset 50 kontrak ini dibuat dengan memilih secara purposive kontrak yang paling **representatif dan beragam** per domain — menghapus duplikat struktural dan kontrak trivial.

---

## Perubahan Dataset

| Domain | 75 → 50 | Yang Dihapus |
|---|---|---|
| DeFi | 15 → 10 | DaiJoin, ETHJoin, GemJoin (near-identical), AppProxyUpgradeable (0 findings), CErc20Delegator (duplikat) |
| NFT | 15 → 10 | Azuki, CloneX, Doodles, MutantApeYachtClub (2 findings modern), AdminUpgradeabilityProxy (generic proxy) |
| Token | 15 → 10 | ProxyERC20, SimpleToken/ApeCoin (2 findings), AdminUpgradeabilityProxy PAXG (duplikat BUSD), LQTYToken (1 finding), OwnedUpgradeabilityProxy |
| Governance | 15 → 10 | GovernorBravoDelegator ×2 (redundan), GovernorBravoDelegator Uniswap (0 findings), AdminUpgradeabilityProxy Aave, Tribe |
| Utility | 15 → 10 | Jug (3 findings, trivial), ReverseRegistrar (2 findings), NonfungiblePositionManager & SwapRouter02 (0 findings, ukuran raksasa) |

---

## Dependency Chain Notebook

```
contracts_selection_50.json
        │
        ▼
[STEP 1] pekan2_detectors.ipynb
        → results_50/pekan2_detector_results.json
        → results_50/pekan2_summary.csv
        │
        ├──────────────────────────────────────────────┐
        ▼                                              ▼
[STEP 2] pekan3_benchmark.ipynb              [STEP 3] pekan4_experiment.ipynb
  (TIDAK BERUBAH — benchmark sintetis)         reads: results_50/pekan2_detector_results.json
  results_50/ → salin dari results/                    results_50/pekan3_gas_benchmark.json
        │                                      → results_50/pekan4_statistical_tests.json
        │                                              │
        └──────────────────────────────────────────────┘
                                                       │
                                                       ▼
                                           [STEP 4] pekan4c_tabel_final.ipynb
                                             reads: results_50/pekan2_detector_results.json
                                                     results_50/pekan3_gas_benchmark.json
                                                     contracts_selection_50.json
                                             → results_50/tabel_4a_to_4e_final.json
                                             → results_50/tabel_4_4*.csv
```

**Catatan pekan3**: Gas benchmark mengukur kontrak sintetis (GasBenchmark.sol), bukan dataset kontrak. Hasilnya identik untuk dataset 50 maupun 75. Kita salin hasil pekan3 dari `results/` ke `results_50/` tanpa re-run.

---

## Rencana Eksekusi

### ✅ Selesai
- [x] Buat `contracts_selection_50.json` (10 per domain)
- [x] Buat branch `experiment/50-contracts`
- [x] Buat folder `docs/knowledge_base_50/`
- [x] Buat folder `results_50/`
- [x] Tulis `STRATEGY.md` ini

### 🔄 Akan Dikerjakan

**Fase 1 — Siapkan notebooks dan salin benchmark**
- [x] 1a. Patch `pekan2_detectors.ipynb`: SELECTION_FILE → `contracts_selection_50.json`, RESULTS_DIR → `results_50/`
- [x] 1b. Patch `pekan4_experiment.ipynb`: RESULTS_DIR → `results_50/`
- [x] 1c. Patch `pekan4c_tabel_final.ipynb`: SELECTION_FILE + RESULTS_DIR → `results_50/` (termasuk fix hardcoded OUT di Cell 7)
- [x] 1d. Salin `results/pekan3_gas_benchmark.json` → `results_50/`
- [x] 1e. Salin `results/pekan3_slither_results.json` → `results_50/`

**Fase 2 — Jalankan notebooks**
- [x] 2a. Jalankan `pekan2_detectors.ipynb` → 1.383 findings dari 50 kontrak
- [x] 2b. Jalankan `pekan4_experiment.ipynb` → Wilcoxon W=15 p=0.031, Spearman ρ=+0.329 p=0.020
- [x] 2c. Jalankan `pekan4c_tabel_final.ipynb` → semua tabel 4.4a–4.4e tersimpan di `results_50/`

**Fase 3 — Dokumentasi knowledge base**
- [x] 3a. Tulis `01_gambaran_umum.md`
- [x] 3b. Tulis `02_dataset.md`
- [x] 3c. Tulis `03_hasil_eksperimen.md`
- [x] 3d. Tulis `04_analisis_statistik.md`
- [x] 3e. Tulis `05_perbandingan_75_vs_50.md`

**Fase 4 — Commit**
- [x] 4a. Git add semua perubahan di branch ini
- [x] 4b. Push ke `origin/experiment/50-contracts`

---

## Hipotesis yang Diuji

Dataset 50 yang lebih bersih diharapkan menghasilkan:

1. **Total findings lebih rendah** — karena menghapus kontrak duplikat struktural
2. **Distribusi per-domain lebih merata** — tanpa outlier duplikat
3. **Statistik lebih stabil** — median dan mean lebih representatif per domain
4. **Spearman ρ lebih kuat** — dataset lebih clean → korelasi LOC-findings lebih konsisten
5. **KW per-domain tetap signifikan** — Token dan NFT era lama masih mendominasi

---

## Path Konfigurasi Eksperimen Ini

| Variable | Nilai |
|---|---|
| `SELECTION_FILE` | `contracts_selection_50.json` |
| `RESULTS_DIR` | `results_50/` |
| Branch | `experiment/50-contracts` |
| KB folder | `docs/knowledge_base_50/` |
| Solc version | 0.8.20 (tidak berubah) |
| Optimizer | false (tidak berubah) |
