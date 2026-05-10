# Dataset 50 Kontrak — Deskripsi Lengkap

**File konfigurasi**: `contracts_selection_50.json`  
**Total**: 50 kontrak, 10 per domain, semua compile_ok  
**Complexity**: Simple=2, Medium=28, Complex=20

---

## Domain: DeFi (10 kontrak)

| Nama | SLOC | Cx | Temuan |
|---|---|---|---|
| Dai | 169 | M | 10 |
| KyberNetworkProxy | 484 | M | 68 |
| Spotter | 129 | M | 0 |
| UniswapV2Factory | 414 | M | 20 |
| UniswapV2Pair | 396 | M | 14 |
| Vat | 238 | M | 24 |
| CErc20 | 2.178 | C | 49 |
| CErc20Delegator (cDAI) | 1.901 | C | 6 |
| CEther | 2.138 | C | 49 |
| InitializableAdminUpgradeabilityProxy | 1.185 | C | 0 |
| **DeFi Subtotal** | | | **240** |

**Yang dihapus dari 15→10**: DaiJoin, ETHJoin, GemJoin (tiga kontrak MakerDAO join yang hampir identik strukturnya), AppProxyUpgradeable (proxy pattern, 0 findings yang unik), satu duplikat CErc20Delegator (cCOMP identik dengan cDAI secara struktur).

---

## Domain: NFT (10 kontrak)

| Nama | SLOC | Cx | Temuan |
|---|---|---|---|
| CryptoPunksMarket | 212 | M | 35 |
| AvastarTeleporter | 2.171 | C | 74 |
| BaseRegistrarImplementation | 664 | C | 23 |
| DCLRegistrar | 1.570 | C | 90 |
| KittyCore (CryptoKitties) | 1.685 | C | 32 |
| LANDProxy (Decentraland) | 1.256 | C | 43 |
| Meebits | 567 | C | 27 |
| Parcel | 733 | C | 57 |
| SuperRareV2 | 999 | C | 51 |
| WrappedPunk | 1.376 | C | 54 |
| **NFT Subtotal** | | | **486** |

**Yang dihapus dari 15→10**: Azuki, CloneX, Doodles, MutantApeYachtClub (keempat kontrak modern solc 0.8.x, masing-masing hanya 2 findings — menambah bias negatif pada korelasi LOC), AdminUpgradeabilityProxy (generic proxy, bukan NFT-specific).

---

## Domain: Token (10 kontrak)

| Nama | SLOC | Cx | Temuan |
|---|---|---|---|
| BAToken | 146 | M | 24 |
| LinkToken | 250 | M | 28 |
| MANAToken | 222 | M | 31 |
| TetherToken | 377 | M | 47 |
| AdminUpgradeabilityProxy (BUSD) | 581 | C | 61 |
| BalancerGovernanceToken | 1.280 | C | 41 |
| FiatTokenProxy (USDC) | 2.715 | C | 0 |
| GraphToken | 832 | C | 27 |
| OneInch | 964 | C | 32 |
| WBTC | 564 | C | 52 |
| **Token Subtotal** | | | **343** |

**Yang dihapus dari 15→10**: ProxyERC20, SimpleToken/ApeCoin (2 findings, bukan token kontrak asli), AdminUpgradeabilityProxy PAXG (duplikat struktural dari BUSD), LQTYToken (1 finding — modern design), OwnedUpgradeabilityProxy/TUSD (overlap dengan BUSD pattern).

---

## Domain: Governance (10 kontrak)

| Nama | SLOC | Cx | Temuan |
|---|---|---|---|
| Comp | 249 | M | 18 |
| DSToken (MKR) | 371 | M | 43 |
| Governor (ENS) | 443 | M | 24 |
| GovernorAlpha (Compound) | 252 | M | 17 |
| GovernorBravoDelegate | 465 | M | 5 |
| NounsDAOProxy | 336 | M | 3 |
| Uni (UNI) | 493 | M | 28 |
| YFI | 191 | M | 32 |
| AaveGovernanceV2 | 1.234 | C | 13 |
| MiniMeToken (LDO) | 516 | C | 32 |
| **Governance Subtotal** | | | **215** |

**Yang dihapus dari 15→10**: GovernorBravoDelegator ×2 (Compound & Uniswap, keduanya redundan dengan GovernorBravoDelegate yang sudah ada), GovernorBravoDelegator Uniswap (versi 200 LOC, 0 findings), AdminUpgradeabilityProxy Aave (generic proxy), Tribe/FEI (7 findings, governance minor).

---

## Domain: Utility (10 kontrak)

| Nama | SLOC | Cx | Temuan |
|---|---|---|---|
| Multicall | 43 | S | 8 |
| Multicall2 | 70 | S | 10 |
| DSProxyFactory | 183 | M | 11 |
| ENSRegistryWithFallback | 236 | M | 9 |
| ERC1820Registry | 194 | M | 2 |
| GnosisSafeProxyFactory | 152 | M | 0 |
| MultiSigWallet | 334 | M | 26 |
| WyvernProxyRegistry | 383 | M | 31 |
| GnosisSafe | 1.008 | C | 2 |
| UniswapV3Factory | 2.970 | C | 0 |
| **Utility Subtotal** | | | **99** |

**Yang dihapus dari 15→10**: Jug (3 findings, trivial MakerDAO), ReverseRegistrar (2 findings, minimal), NonfungiblePositionManager (0 findings, 3.957 LOC — outlier raksasa), SwapRouter02 (0 findings, 3.276 LOC — outlier raksasa). PublicResolver sudah gagal compile sejak awal.

---

## Ringkasan Complexity

| Complexity | n | Range SLOC | Avg Findings |
|---|---|---|---|
| Simple (<100 SLOC) | 2 | 43–70 | 9.0 |
| Medium (100–500 SLOC) | 28 | 129–493 | 22.0 |
| Complex (500+ SLOC) | 20 | 516–2.970 | 35.5 |

**Catatan**: Dua kontrak Simple masih hanya Multicall & Multicall2 (Utility) — ini mencerminkan realitas mainnet Ethereum, bukan keterbatasan sampling.
