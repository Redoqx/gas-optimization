# Dataset: 75 Smart Contract dari Etherscan Mainnet

## Komposisi Dataset

| Atribut | Detail |
|---|---|
| Sumber | Etherscan.io — Ethereum Mainnet, verified source code |
| Jumlah kontrak | 75 (15 per domain) |
| Domain | DeFi, NFT, Token, Governance, Utility |
| Complexity level | Simple (<100 SLOC), Medium (100–500 SLOC), Complex (>500 SLOC) |
| Berhasil compile | 74 kontrak (98.7%) |
| Gagal compile | 1 kontrak (1.3%) |
| File konfigurasi | `contracts_selection.json` (active dataset) |

## Alasan Pemilihan Dataset Ini

1. **Real-world contracts**: Kontrak yang sudah deployed dan diverifikasi di mainnet, bukan dummy/contoh tutorial
2. **Diversity of domains**: 5 domain berbeda memastikan representasi use-case beragam
3. **Verified source**: Etherscan menyediakan source code yang sudah diverifikasi sesuai deployed bytecode
4. **Range of complexity**: Dari Multicall (43 SLOC) hingga NonfungiblePositionManager (3.957 SLOC)
5. **Historical breadth**: Kontrak dari era Solidity 0.4.x (2017) hingga 0.8.x (2022+)
6. **Stratified sampling**: 15 kontrak per domain, memaksimalkan jumlah kontrak Simple yang tersedia

---

## Distribusi per Complexity Level (74 kontrak valid)

| Complexity | Kriteria | Jumlah | Rata-rata SLOC | Rata-rata Findings |
|---|---|---|---|---|
| Simple | < 100 SLOC | **2** | 56.5 | 9.0 |
| Medium | 100–500 SLOC | **36** | 305 | 16.8 |
| Complex | > 500 SLOC | **36** | 1.472 | 24.6 |

**Catatan Simple**: Hanya 2 kontrak Simple tersedia di seluruh dataset 75 kontrak (keduanya Utility domain: Multicall dan Multicall2). Ini mencerminkan kenyataan bahwa kontrak mainnet yang verified di Etherscan umumnya berukuran non-trivial. Token, NFT, DeFi, dan Governance tidak memiliki kontrak <100 SLOC dalam dataset ini.

---

## Distribusi per Domain

### DeFi (Decentralized Finance) — 15 kontrak, 15 compile-ok

| Nama | SLOC | Complexity | Solc Era |
|---|---|---|---|
| AppProxyUpgradeable | 279 | Medium | 0.4.x |
| Dai | 169 | Medium | 0.5.x |
| DaiJoin | 192 | Medium | 0.5.x |
| ETHJoin | 192 | Medium | 0.5.x |
| GemJoin | 162 | Medium | 0.5.x |
| KyberNetworkProxy | 484 | Medium | 0.6.x |
| Spotter | 129 | Medium | 0.5.x |
| UniswapV2Factory | 414 | Medium | 0.5.x |
| UniswapV2Pair | 396 | Medium | 0.5.x |
| Vat | 238 | Medium | 0.5.x |
| CErc20 | 2.178 | Complex | 0.5.x |
| CErc20Delegator (cDAI) | 1.901 | Complex | 0.5.x |
| CErc20Delegator (cCOMP) | 1.901 | Complex | 0.5.x |
| CEther | 2.138 | Complex | 0.5.x |
| InitializableAdminUpgradeabilityProxy | 1.185 | Complex | 0.6.x |

### NFT (Non-Fungible Token) — 15 kontrak, 15 compile-ok

| Nama | SLOC | Complexity | Solc Era |
|---|---|---|---|
| CryptoPunksMarket | 212 | Medium | 0.4.x |
| AdminUpgradeabilityProxy | 1.515 | Complex | 0.5.x |
| AvastarTeleporter | 2.171 | Complex | 0.5.x |
| Azuki | 1.335 | Complex | 0.8.x |
| BaseRegistrarImplementation (ENS) | 664 | Complex | 0.5.x |
| CloneX | 1.308 | Complex | 0.8.x |
| DCLRegistrar | 1.570 | Complex | 0.5.x |
| Doodles | 1.206 | Complex | 0.8.x |
| KittyCore (CryptoKitties) | 1.685 | Complex | 0.4.x |
| LANDProxy (Decentraland) | 1.256 | Complex | 0.4.x |
| Meebits | 567 | Complex | 0.8.x |
| MutantApeYachtClub | 1.550 | Complex | 0.8.x |
| Parcel | 733 | Complex | 0.5.x |
| SuperRareV2 | 999 | Complex | 0.5.x |
| WrappedPunk | 1.376 | Complex | 0.5.x |

### Token (ERC-20 & Derivatif) — 15 kontrak, 15 compile-ok

| Nama | SLOC | Complexity | Solc Era |
|---|---|---|---|
| BAToken | 146 | Medium | 0.4.x |
| LinkToken | 250 | Medium | 0.4.x |
| MANAToken | 222 | Medium | 0.4.x |
| ProxyERC20 | 408 | Medium | 0.5.x |
| SimpleToken (ApeCoin) | 451 | Medium | 0.8.x |
| TetherToken | 377 | Medium | 0.4.x |
| AdminUpgradeabilityProxy (BUSD) | 581 | Complex | 0.6.x |
| AdminUpgradeabilityProxy (PAXG) | 687 | Complex | 0.6.x |
| BalancerGovernanceToken | 1.280 | Complex | 0.7.x |
| FiatTokenProxy (USDC) | 2.715 | Complex | 0.6.x |
| GraphToken | 832 | Complex | 0.7.x |
| LQTYToken | 2.135 | Complex | 0.6.x |
| OneInch | 964 | Complex | 0.6.x |
| OwnedUpgradeabilityProxy (TUSD) | 1.291 | Complex | 0.5.x |
| WBTC | 564 | Complex | 0.4.x |

### Governance (DAO & Voting) — 15 kontrak, 15 compile-ok

| Nama | SLOC | Complexity | Solc Era |
|---|---|---|---|
| Comp | 249 | Medium | 0.5.x |
| DSToken (MKR) | 371 | Medium | 0.5.x |
| Governor (ENS) | 443 | Medium | 0.8.x |
| GovernorAlpha (Compound) | 252 | Medium | 0.5.x |
| GovernorBravoDelegate | 465 | Medium | 0.5.x |
| GovernorBravoDelegator (Compound) | 465 | Medium | 0.5.x |
| GovernorBravoDelegator (Uniswap) | 200 | Medium | 0.7.x |
| NounsDAOProxy | 336 | Medium | 0.8.x |
| Tribe (FEI) | 322 | Medium | 0.8.x |
| Uni (UNI) | 493 | Medium | 0.6.x |
| YFI | 191 | Medium | 0.5.x |
| AaveGovernanceV2 | 1.234 | Complex | 0.7.x |
| AdminUpgradeabilityProxy (Aave) | 1.117 | Complex | 0.6.x |
| MiniMeToken (LDO) | 516 | Complex | 0.4.x |
| Token (ANT) | 528 | Complex | 0.4.x |

### Utility (General Purpose) — 15 kontrak, 14 compile-ok

| Nama | SLOC | Complexity | Solc Era | Compile |
|---|---|---|---|---|
| Multicall | 43 | **Simple** | 0.5.x | ✅ |
| Multicall2 | 70 | **Simple** | 0.5.x | ✅ |
| DSProxyFactory | 183 | Medium | 0.5.x | ✅ |
| ENSRegistryWithFallback | 236 | Medium | 0.5.x | ✅ |
| ERC1820Registry | 194 | Medium | 0.5.x | ✅ |
| GnosisSafeProxyFactory | 152 | Medium | 0.8.x | ✅ |
| Jug (MakerDAO) | 141 | Medium | 0.5.x | ✅ |
| MultiSigWallet (Gnosis) | 334 | Medium | 0.4.x | ✅ |
| ReverseRegistrar (ENS) | 354 | Medium | 0.5.x | ✅ |
| WyvernProxyRegistry | 383 | Medium | 0.4.x | ✅ |
| GnosisSafe | 1.008 | Complex | 0.7.x | ✅ |
| NonfungiblePositionManager | 3.957 | Complex | 0.7.x | ✅ |
| SwapRouter02 | 3.276 | Complex | 0.7.x | ✅ |
| UniswapV3Factory | 2.970 | Complex | 0.6.x | ✅ |
| PublicResolver (ENS) | 342 | Medium | 0.8.x | ❌ (compile fail) |

---

## Statistik Dataset Keseluruhan (74 compile-ok)

| Statistik | Nilai |
|---|---|
| SLOC terkecil | 43 (Multicall) |
| SLOC terbesar | 3.957 (NonfungiblePositionManager) |
| Rata-rata SLOC | ~889 |
| Range solc | 0.4.x – 0.8.x |
| Dominan era | 0.4.x–0.6.x (kontrak lama sebelum Solidity 0.8.0) |
| Kontrak solc 0.8.x | ~15 kontrak |

---

## Catatan Metodologi

- **SLOC** (Source Lines of Code = non-blank lines): digunakan sebagai ukuran kontrak, bukan raw LOC, karena Etherscan menambahkan blank lines dalam download yang menggelembungkan hitungan ~2×.
- **Flattening effect**: Beberapa kontrak kecil di source aslinya (misal MakerDAO GemJoin ~40 baris) berukuran 129–192 SLOC setelah Etherscan meratakan import — diklasifikasikan Medium bukan Simple.
- **contracts_selection.json** adalah file konfigurasi aktif yang menentukan dataset eksperimen. Semua notebook membaca dari file ini.
