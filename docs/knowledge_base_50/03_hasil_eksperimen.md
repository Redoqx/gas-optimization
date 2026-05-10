# Hasil Eksperimen — Tabel 4.4a sampai 4.4e (Dataset 50 Kontrak)

Semua hasil tersimpan di `results_50/`. Benchmark gas (pekan3) identik dengan dataset 75 karena menggunakan kontrak sintetis.

---

## Tabel 4.4a — Detection Accuracy (20-Contract Sample)

*(Diambil dari subset 20 kontrak yang sama dengan eksperimen 75-kontrak — nilai precision/recall tidak berubah karena ground truth identik)*

| Anti-Pattern | True Positive | False Positive | False Negative | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| redundant_sload | — | — | — | ~72% | ~91% | ~80% |
| unoptimized_loop | — | — | — | ~100% | ~100% | ~100% |
| string_vs_bytes32 | — | — | — | ~88% | ~85% | ~86% |
| public_vs_external | — | — | — | ~79% | ~83% | ~81% |
| unchecked_arithmetic | N/A | N/A | N/A | N/A | N/A | N/A |
| dead_code | — | — | — | ~62% | ~80% | ~70% |

*Catatan: Precision/recall tidak di-rerun untuk 50-contract experiment karena ground truth labeling tidak berubah.*

---

## Tabel 4.4b — Gas Savings per Anti-Pattern

*(Benchmark sintetis — sama dengan eksperimen 75 karena tidak bergantung dataset)*

| Anti-Pattern | Contracts w/ Pattern | Gas Boros | Gas Hemat | Saved (%) | Refactor |
|---|---|---|---|---|---|
| Redundant SLOAD | 39/50 | 24.208 | 24.022 | **0.77%** | 0% |
| Unoptimized Loop | 2/50 | 51.187 | 50.156 | **2.01%** | 85% |
| String vs Bytes32 | 35/50 | 24.540 | 23.590 | **3.87%** | 0% |
| Public vs External | 41/50 | 52.544 | 49.871 | **5.09%** | 100% |
| Unchecked Arithmetic | 0/50 | 59.105 | 47.060 | **20.38%** | 0% |
| Dead Code | 20/50 | 123.985 | 123.985 | **0.00%** | 0% |

**Avg savings (5 efektif pola)**: 5.35%

---

## Tabel 4.4c — Cross-Domain Pattern Distribution

| Anti-Pattern | DeFi (10) | NFT (10) | Token (10) | Gov (10) | Util (10) | TOTAL |
|---|---|---|---|---|---|---|
| redundant_sload | 148 | 208 | 110 | 67 | 28 | **561** |
| unoptimized_loop | 2 | 0 | 0 | 0 | 5 | **7** |
| string_vs_bytes32 | 22 | 94 | 27 | 52 | 2 | **197** |
| public_vs_external | 45 | 150 | 179 | 80 | 64 | **518** |
| unchecked_arithmetic | 0 | 0 | 0 | 0 | 0 | **0** |
| dead_code | 23 | 34 | 27 | 16 | 0 | **100** |
| **TOTAL** | **240** | **486** | **343** | **215** | **99** | **1.383** |
| **Avg/contract** | 24.0 | 48.6 | 34.3 | 21.5 | 9.9 | 27.7 |

**Observasi**:
- NFT masih domain tertinggi (486, 35.1%) — kini tanpa kontrak modern 2-findings, angka lebih solid
- Token kedua (343, 24.8%) — dominasi public_vs_external dari token ERC-20 era lama
- Utility terendah (99, 7.2%) — menghapus NonfungiblePositionManager & SwapRouter02 tidak mengubah angka (keduanya 0 findings)
- `public_vs_external` tetap #2 (37.5%) vs `redundant_sload` #1 (40.6%) — urutan sedikit berbeda dari dataset 75

---

## Tabel 4.4d — Complexity Analysis

| Complexity | n | Avg Findings | Median | Std | Precision* | Recall* | Waktu (s/kontrak) |
|---|---|---|---|---|---|---|---|
| Simple (<100 SLOC) | 2 | 9.0 | 9.0 | 1.41 | 88.9% | 100% | ~0.079 |
| Medium (100–500 SLOC) | 28 | 22.0 | 19.0 | 16.8 | 80.2% | 88.6% | ~0.130 |
| Complex (500+ SLOC) | 20 | 35.5 | 36.5 | 25.2 | 80.2% | 88.6% | ~0.310 |

*Precision/recall dari 75-contract experiment (tidak di-rerun)

**Kruskal-Wallis**: H=5.606, p=0.061 — **tidak signifikan** pada α=0.05 (namun borderline, p mendekati 0.05)

*Dataset 75: H=2.857, p=0.240 → dataset 50 lebih kuat menunjukkan perbedaan complexity walaupun masih tidak signifikan*

---

## Tabel 4.4e — Head-to-Head vs Slither

*(Sample 10 kontrak untuk Slither — reused dari eksperimen 75 karena Slither limitation sama)*

| Metrik | Our Tool | Slither | Overlap |
|---|---|---|---|
| Total Patterns Detected | 136 | 0* | 0 |
| Unique to Our Tool | 5 | — | — |
| Unique to Slither | — | 0 | — |
| Precision (shared patterns) | N/A† | N/A† | — |
| Gas Quantification | Ya (per pattern) | Tidak | — |
| Avg Analysis Time | ~0.20 s/kontrak | ~1.7 s (0.8x+) | — |

*Slither 0 = parse failure pada solc 0.4.x (bukan false negative)  
†Tidak dapat dihitung karena Slither menghasilkan 0 deteksi

**Catatan**: Tabel 4.4e tidak berubah dari eksperimen 75 karena Slither sample (10 kontrak) adalah fixed sample dari dataset dan keterbatasan Slither bersifat teknis (versi solc), bukan dataset-dependent.

---

## Per-Contract Findings Lengkap

### DeFi
| Nama | SLOC | Cx | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| Dai | 169 | M | 7 | 0 | 3 | 0 | 0 | 0 | **10** |
| KyberNetworkProxy | 484 | M | 24 | 2 | 0 | 40 | 0 | 2 | **68** |
| Spotter | 129 | M | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| UniswapV2Factory | 414 | M | 17 | 0 | 2 | 1 | 0 | 0 | **20** |
| UniswapV2Pair | 396 | M | 11 | 0 | 2 | 1 | 0 | 0 | **14** |
| Vat | 238 | M | 24 | 0 | 0 | 0 | 0 | 0 | **24** |
| CErc20 | 2.178 | C | 33 | 0 | 6 | 1 | 0 | 9 | **49** |
| CErc20Delegator | 1.901 | C | 0 | 0 | 2 | 1 | 0 | 3 | **6** |
| CEther | 2.138 | C | 32 | 0 | 7 | 1 | 0 | 9 | **49** |
| InitializableAdminUpgradeabilityProxy | 1.185 | C | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **Subtotal** | | | **148** | **2** | **22** | **45** | **0** | **23** | **240** |

### NFT
| Nama | SLOC | Cx | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| CryptoPunksMarket | 212 | M | 20 | 0 | 4 | 11 | 0 | 0 | **35** |
| AvastarTeleporter | 2.171 | C | 37 | 0 | 19 | 11 | 0 | 7 | **74** |
| BaseRegistrarImplementation | 664 | C | 10 | 0 | 0 | 10 | 0 | 3 | **23** |
| DCLRegistrar | 1.570 | C | 26 | 0 | 23 | 34 | 0 | 7 | **90** |
| KittyCore | 1.685 | C | 19 | 0 | 4 | 9 | 0 | 0 | **32** |
| LANDProxy | 1.256 | C | 24 | 0 | 12 | 4 | 0 | 3 | **43** |
| Meebits | 567 | C | 21 | 0 | 3 | 3 | 0 | 0 | **27** |
| Parcel | 733 | C | 21 | 0 | 7 | 26 | 0 | 3 | **57** |
| SuperRareV2 | 999 | C | 16 | 0 | 12 | 20 | 0 | 3 | **51** |
| WrappedPunk | 1.376 | C | 14 | 0 | 10 | 22 | 0 | 8 | **54** |
| **Subtotal** | | | **208** | **0** | **94** | **150** | **0** | **34** | **486** |

### Token
| Nama | SLOC | Cx | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| BAToken | 146 | M | 11 | 0 | 3 | 10 | 0 | 0 | **24** |
| LinkToken | 250 | M | 5 | 0 | 2 | 19 | 0 | 2 | **28** |
| MANAToken | 222 | M | 8 | 0 | 2 | 19 | 0 | 2 | **31** |
| TetherToken | 377 | M | 16 | 0 | 4 | 27 | 0 | 0 | **47** |
| AdminUpgradeabilityProxy (BUSD) | 581 | C | 33 | 0 | 3 | 25 | 0 | 0 | **61** |
| BalancerGovernanceToken | 1.280 | C | 6 | 0 | 5 | 20 | 0 | 10 | **41** |
| FiatTokenProxy (USDC) | 2.715 | C | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| GraphToken | 832 | C | 9 | 0 | 2 | 12 | 0 | 4 | **27** |
| OneInch | 964 | C | 9 | 0 | 2 | 16 | 0 | 5 | **32** |
| WBTC | 564 | C | 13 | 0 | 4 | 31 | 0 | 4 | **52** |
| **Subtotal** | | | **110** | **0** | **27** | **179** | **0** | **27** | **343** |

### Governance
| Nama | SLOC | Cx | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| Comp | 249 | M | 9 | 0 | 6 | 3 | 0 | 0 | **18** |
| DSToken (MKR) | 371 | M | 14 | 0 | 0 | 21 | 0 | 8 | **43** |
| Governor (ENS) | 443 | M | 6 | 0 | 6 | 12 | 0 | 0 | **24** |
| GovernorAlpha | 252 | M | 3 | 0 | 6 | 8 | 0 | 0 | **17** |
| GovernorBravoDelegate | 465 | M | 0 | 0 | 3 | 2 | 0 | 0 | **5** |
| NounsDAOProxy | 336 | M | 0 | 0 | 3 | 0 | 0 | 0 | **3** |
| Uni (UNI) | 493 | M | 14 | 0 | 11 | 3 | 0 | 0 | **28** |
| YFI | 191 | M | 6 | 0 | 6 | 15 | 0 | 5 | **32** |
| AaveGovernanceV2 | 1.234 | C | 4 | 0 | 2 | 4 | 0 | 3 | **13** |
| MiniMeToken (LDO) | 516 | C | 11 | 0 | 9 | 12 | 0 | 0 | **32** |
| **Subtotal** | | | **67** | **0** | **52** | **80** | **0** | **16** | **215** |

### Utility
| Nama | SLOC | Cx | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| Multicall | 43 | S | 0 | 0 | 0 | 8 | 0 | 0 | **8** |
| Multicall2 | 70 | S | 0 | 0 | 0 | 10 | 0 | 0 | **10** |
| DSProxyFactory | 183 | M | 6 | 0 | 0 | 5 | 0 | 0 | **11** |
| ENSRegistryWithFallback | 236 | M | 1 | 0 | 0 | 8 | 0 | 0 | **9** |
| ERC1820Registry | 194 | M | 1 | 0 | 1 | 0 | 0 | 0 | **2** |
| GnosisSafeProxyFactory | 152 | M | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| MultiSigWallet | 334 | M | 11 | 5 | 0 | 10 | 0 | 0 | **26** |
| WyvernProxyRegistry | 383 | M | 9 | 0 | 1 | 21 | 0 | 0 | **31** |
| GnosisSafe | 1.008 | C | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| UniswapV3Factory | 2.970 | C | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **Subtotal** | | | **28** | **5** | **2** | **64** | **0** | **0** | **99** |
