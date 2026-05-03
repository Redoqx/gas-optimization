# Hasil Eksperimen: Tabel 4.4a–4.4e

## Tabel 4.4a — Gas Savings per Anti-Pattern

*Sumber: Hardhat estimateGas, kontrak benchmark GasBenchmark.sol, solc 0.8.20, optimizer: false*

| No | Anti-Pattern | Gas Boros | Gas Hemat | Selisih | Hemat (%) |
|---|---|---|---|---|---|
| 1 | redundant_sload | 24.208 | 24.022 | 186 | 0.77% |
| 2 | unoptimized_loop | 51.187 | 50.156 | 1.031 | 2.01% |
| 3 | string_vs_bytes32 | 24.540 | 23.590 | 950 | 3.87% |
| 4 | public_vs_external | 52.544 | 49.871 | 2.673 | 5.09% |
| 5 | unchecked_arithmetic | 59.105 | 47.060 | 12.045 | 20.38% |
| 6 | dead_code | 123.985 | 123.985 | 0 | 0.00% |
| | **Rata-rata** | | | | **5.35%** |

**Catatan kondisi pengukuran**:
- `redundant_sload`: 3x read vs 1x cache + 2x akses lokal
- `unoptimized_loop`: array 10 elemen, `.length` per iterasi vs cache sekali
- `string_vs_bytes32`: read string "Token" (5 char) vs bytes32 "Token"
- `public_vs_external`: array 10 elemen, `memory` copy vs `calldata` langsung
- `unchecked_arithmetic`: loop 100 iterasi dengan counter `i`
- `dead_code`: deployment cost, 3 fungsi internal mati vs tanpa dead func

---

## Tabel 4.4b — Distribusi Findings per Domain

*Sumber: hasil deteksi 46 kontrak valid, pekan2_detector_results.json*

| Domain | n | redund_sload | unopt_loop | str_bytes32 | pub_ext | unchk_arith | dead_code | TOTAL |
|---|---|---|---|---|---|---|---|---|
| DeFi | 10 | 76 | 0 | 31 | 54 | 0 | 13 | **174** |
| NFT | 9 | 41 | 0 | 12 | 26 | 10 | 3 | **92** |
| Token | 9 | 60 | 0 | 25 | 146 | 0 | 27 | **258** |
| Governance | 9 | 13 | 0 | 24 | 45 | 0 | 5 | **87** |
| Utility | 9 | 14 | 5 | 0 | 12 | 0 | 4 | **35** |
| **TOTAL** | **46** | **204** | **5** | **72** | **283** | **10** | **52** | **646** |

**Observasi penting**:
- Token domain mendominasi karena kontrak token ERC-20 era lama sangat banyak fungsi `public` (menghasilkan 146 findings `public_vs_external`)
- `unoptimized_loop` hanya ditemukan di Utility (MultiSigWallet) — kontrak lain tidak memiliki pola loop dengan state variable `.length`
- `unchecked_arithmetic` hanya relevan pada kontrak solc ≥ 0.8.0, yang mayoritas ada di domain NFT (era 2021–2022)
- DeFi memiliki `redundant_sload` terbanyak karena kontrak DeFi sering membaca state variable (balances, allowances) berulang kali dalam satu fungsi

---

## Tabel 4.4c — Top 10 Kontrak dengan Findings Terbanyak

| No | Nama | Domain | LOC | redund | unopt | str_b32 | pub_ext | unchk | dead | TOTAL |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | WBTC | Token | 1.317 | 13 | 0 | 4 | 31 | 0 | 4 | **52** |
| 2 | TetherToken | Token | 893 | 16 | 0 | 4 | 27 | 0 | 0 | **47** |
| 3 | DSToken | DeFi | 947 | 14 | 0 | 0 | 21 | 0 | 8 | **43** |
| 4 | BalancerGovernanceToken | Token | 2.987 | 6 | 0 | 5 | 20 | 0 | 10 | **41** |
| 5 | CryptoPunksMarket | NFT | 491 | 20 | 0 | 4 | 11 | 0 | 0 | **35** |
| 6 | MiniMeToken | DeFi | 1.199 | 11 | 0 | 9 | 12 | 0 | 0 | **32** |
| 7 | YFI | Token | 449 | 6 | 0 | 6 | 15 | 0 | 5 | **32** |
| 8 | OneInch | Token | 2.235 | 9 | 0 | 2 | 16 | 0 | 5 | **32** |
| 9 | Uni | DeFi | 1.163 | 14 | 0 | 11 | 3 | 0 | 0 | **28** |
| 10 | LinkToken | Token | 589 | 5 | 0 | 2 | 19 | 0 | 2 | **28** |

**Pola yang terlihat**: Kontrak-kontrak dengan findings tinggi umumnya adalah kontrak era **Solidity 0.4.x–0.5.x** (TetherToken, WETH9, WBTC, DSToken, MiniMeToken, CryptoPunksMarket). Kontrak era lama belum menggunakan best practice modern seperti `external` visibility, `bytes32` untuk teks pendek, dan belum menerapkan pattern cache SLOAD.

---

## Tabel 4.4d — Analisis per Complexity Level

| Complexity | Kriteria LOC | n | Avg LOC | Avg Findings | Density (findings/LOC×100) |
|---|---|---|---|---|---|
| Simple | < 100 | 0 | — | — | — |
| Medium | 100–500 | 9 | 363.6 | 14.7 | 4.034% |
| Complex | > 500 | 37 | 2.169.9 | 13.9 | 0.640% |

**Catatan**: Density findings/LOC lebih tinggi pada kontrak Medium — kontrak ukuran menengah ternyata lebih padat pola boros dibandingkan kontrak besar. Kontrak Complex umumnya lebih baru (era 0.8.x) atau lebih modern dalam praktik penulisannya.

### Korelasi Spearman: LOC vs Total Findings

| Statistik | Nilai |
|---|---|
| Spearman rho | **-0.261** |
| p-value | 0.079 |
| Signifikan (α=0.05) | Tidak |

**Interpretasi**: Korelasi negatif lemah — kontrak lebih panjang *cenderung sedikit lebih sedikit* findings relatif terhadap ukurannya. Ini counter-intuitive namun dapat dijelaskan: kontrak besar cenderung ditulis lebih baru (era 0.8.x) atau oleh tim yang lebih berpengalaman dengan gas optimization. Hubungan tidak signifikan secara statistik (p=0.079).

---

## Tabel 4.4e — Perbandingan Detektor Kita vs Slither

*Sumber: Slither 0.11.5, 10 kontrak sampel*

| No | Kontrak | Kita (total findings) | Slither (gas-related) | Status |
|---|---|---|---|---|
| 1 | WETH9 | 9 | 0 | Hanya kita |
| 2 | UniswapV2Router02 | 23 | 0 | Hanya kita |
| 3 | Dai | 10 | 0 | Hanya kita |
| 4 | FiatTokenProxy | 0 | 0 | Nihil |
| 5 | Uni | 28 | 0 | Hanya kita |
| 6 | InitializableAdminUpgradeabilityProxy | 0 | 0 | Nihil |
| 7 | MiniMeToken | 32 | 0 | Hanya kita |
| 8 | AppProxyUpgradeable | 11 | 0 | Hanya kita |
| 9 | Comp | 18 | 0 | Hanya kita |
| 10 | DSToken | 43 | 0 | Hanya kita |

**Kontingen McNemar 2×2**:

| | Slither menemukan | Slither tidak menemukan |
|---|---|---|
| **Kita menemukan** | 0 | 8 |
| **Kita tidak menemukan** | 0 | 2 |

**b=8, c=0** → McNemar tidak dapat dihitung (b+c harus mengandung perbedaan dua arah)

**Interpretasi**: Slither 0.11.5 tidak dapat menganalisis kontrak-kontrak dengan pragma solidity 0.4.x (mayoritas sampel ini). Hal ini bukan berarti Slither lebih buruk secara fundamental, melainkan **keterbatasan kompatibilitas versi solc**. Framework kita (berbasis py-solcx multi-versi) berhasil menganalisis semua kontrak terlepas dari versi solc.

---

## Ringkasan Statistik Deskriptif (46 Kontrak Valid)

| Statistik | Nilai |
|---|---|
| Total findings | 646 |
| Kontrak dengan setidaknya 1 finding | 38 (82.6%) |
| Kontrak tanpa findings | 8 (17.4%) |
| Rata-rata findings per kontrak | 14.0 |
| Median findings per kontrak | 3.0 |
| Std deviation | 16.1 |
| Min findings | 0 |
| Max findings | 52 (WBTC) |
