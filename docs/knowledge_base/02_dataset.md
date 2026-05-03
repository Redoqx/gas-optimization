# Dataset: 50 Smart Contract dari Etherscan Mainnet

## Komposisi Dataset

| Atribut | Detail |
|---|---|
| Sumber | Etherscan.io — Ethereum Mainnet, verified source code |
| Jumlah kontrak | 50 (10 per domain) |
| Domain | DeFi, NFT, Token, Governance, Utility |
| Complexity level | Simple (<100 LOC), Medium (100–500 LOC), Complex (>500 LOC) |
| Berhasil compile | 46 kontrak (92%) |
| Gagal compile | 4 kontrak (8%) |

## Alasan Pemilihan Dataset Ini

1. **Real-world contracts**: Kontrak yang sudah deployed dan diverifikasi di mainnet, bukan dummy/contoh tutorial
2. **Diversity of domains**: 5 domain berbeda memastikan representasi use-case beragam
3. **Verified source**: Etherscan menyediakan source code yang sudah diverifikasi sesuai deployed bytecode
4. **Range of complexity**: Kontrak simple hingga complex (Seaport: 11.395 LOC)
5. **Historical breadth**: Kontrak dari era Solidity 0.4.x hingga 0.8.x

---

## Distribusi per Domain

### DeFi (Decentralized Finance) — 10 kontrak

| File | Nama | LOC | Complexity | Compile | Solc Era |
|---|---|---|---|---|---|
| DeFi_01_WETH9.sol | WETH9 | 1.511 | Complex | ✅ | 0.4.x |
| DeFi_02_UniswapV2Router02.sol | UniswapV2Router02 | 1.559 | Complex | ✅ | 0.6.x |
| DeFi_03_Dai.sol | Dai | 379 | Medium | ✅ | 0.5.x |
| DeFi_04_FiatTokenProxy.sol | FiatTokenProxy | 657 | Complex | ✅ | 0.6.x |
| DeFi_05_Uni.sol | Uni | 1.163 | Complex | ✅ | 0.6.x |
| DeFi_06_InitializableAdminUpgradeabilityProxy.sol | InitializableAdminUpgradeabilityProxy | 1.389 | Complex | ✅ | 0.5.x |
| DeFi_07_MiniMeToken.sol | MiniMeToken | 1.199 | Complex | ✅ | 0.4.x |
| DeFi_08_AppProxyUpgradeable.sol | AppProxyUpgradeable | 783 | Complex | ✅ | 0.5.x |
| DeFi_09_Comp.sol | Comp | 301 | Medium | ✅ | 0.5.x |
| DeFi_10_DSToken.sol | DSToken | 947 | Complex | ✅ | 0.5.x |

### NFT (Non-Fungible Token) — 10 kontrak

| File | Nama | LOC | Complexity | Compile |
|---|---|---|---|---|
| NFT_01_BoredApeYachtClub.sol | BoredApeYachtClub | 4.033 | Complex | ❌ |
| NFT_02_CryptoPunksMarket.sol | CryptoPunksMarket | 491 | Medium | ✅ |
| NFT_03_MutantApeYachtClub.sol | MutantApeYachtClub | 1.819 | Complex | ✅ |
| NFT_04_CloneX.sol | CloneX | 1.655 | Complex | ✅ |
| NFT_05_Moonbirds.sol | Moonbirds | 4.294 | Complex | ✅ |
| NFT_06_Azuki.sol | Azuki | 1.541 | Complex | ✅ |
| NFT_07_Doodles.sol | Doodles | 1.407 | Complex | ✅ |
| NFT_08_Meebits.sol | Meebits | 1.349 | Complex | ✅ |
| NFT_09_Toadz.sol | Toadz | 2.226 | Complex | ✅ |
| NFT_10_Land.sol | Land | 2.432 | Complex | ✅ |

### Token (ERC-20 & Derivatif) — 10 kontrak

| File | Nama | LOC | Complexity | Compile |
|---|---|---|---|---|
| Token_01_TetherToken.sol | TetherToken | 893 | Complex | ✅ |
| Token_02_WBTC.sol | WBTC | 1.317 | Complex | ✅ |
| Token_03_LinkToken.sol | LinkToken | 589 | Complex | ✅ |
| Token_04_YFI.sol | YFI | 449 | Medium | ✅ |
| Token_05_OneInch.sol | OneInch | 2.235 | Complex | ✅ |
| Token_06_GnosisToken.sol | GnosisToken | 301 | Medium | ❌ |
| Token_07_BalancerGovernanceToken.sol | BalancerGovernanceToken | 2.987 | Complex | ✅ |
| Token_08_ProxyERC20.sol | ProxyERC20 | 506 | Complex | ✅ |
| Token_09_SimpleToken.sol | SimpleToken | 525 | Complex | ✅ |
| Token_10_LQTYToken.sol | LQTYToken | 2.668 | Complex | ✅ |

### Governance (DAO & Voting) — 10 kontrak

| File | Nama | LOC | Complexity | Compile |
|---|---|---|---|---|
| Governance_01_GovernorBravoDelegator.sol | GovernorBravoDelegator | 525 | Complex | ✅ |
| Governance_02_GovernorBravoDelegator.sol | GovernorBravoDelegator | 266 | Medium | ✅ |
| Governance_03_FeiDAO.sol | FeiDAO | 3.516 | Complex | ❌ |
| Governance_04_AaveGovernanceV2.sol | AaveGovernanceV2 | 2.751 | Complex | ✅ |
| Governance_05_Governor.sol | Governor | 1.011 | Complex | ✅ |
| Governance_06_GovernorAlpha.sol | GovernorAlpha | 323 | Medium | ✅ |
| Governance_07_GovernorAlpha.sol | GovernorAlpha | 604 | Complex | ✅ |
| Governance_08_ENSGovernor.sol | ENSGovernor | 3.751 | Complex | ✅ |
| Governance_09_NounsDAOProxy.sol | NounsDAOProxy | 402 | Medium | ✅ |
| Governance_10_GovernorAlpha.sol | GovernorAlpha | 348 | Medium | ✅ |

### Utility (General Purpose) — 10 kontrak

| File | Nama | LOC | Complexity | Compile |
|---|---|---|---|---|
| Utility_01_DAO.sol | DAO | 1.236 | Complex | ❌ |
| Utility_02_GnosisSafe.sol | GnosisSafe | 1.132 | Complex | ✅ |
| Utility_03_MultiSigWallet.sol | MultiSigWallet | 731 | Complex | ✅ |
| Utility_04_Jug.sol | Jug | 313 | Medium | ✅ |
| Utility_05_MultiSigWalletWithTimeLock.sol | MultiSigWalletWithTimeLock | 6.783 | Complex | ✅ |
| Utility_06_Seaport.sol | Seaport | 11.395 | Complex | ✅ |
| Utility_07_UniswapV3Factory.sol | UniswapV3Factory | 3.383 | Complex | ✅ |
| Utility_08_SwapRouter.sol | SwapRouter | 2.096 | Complex | ✅ |
| Utility_09_SwapRouter02.sol | SwapRouter02 | 3.878 | Complex | ✅ |
| Utility_10_NonfungiblePositionManager.sol | NonfungiblePositionManager | 4.595 | Complex | ✅ |

---

## Kontrak yang Gagal Compile (4 dari 50)

| Kontrak | Penyebab Perkiraan |
|---|---|
| BoredApeYachtClub | Dependency/import tidak terpenuhi dalam single-file compile |
| GnosisToken | Versi solc tidak kompatibel atau import issue |
| FeiDAO | Import kompleks atau versi pragma tidak terdukung |
| DAO | Versi solc sangat lama (The DAO, 2016) |

Keempat kontrak ini **dikecualikan dari analisis** — hanya 46 kontrak valid yang dianalisis.

---

## Distribusi Complexity Level (46 kontrak valid)

| Complexity | Kriteria | Jumlah | Avg LOC | Avg Findings |
|---|---|---|---|---|
| Simple | < 100 LOC | 0 | — | — |
| Medium | 100–500 LOC | 9 | 364 | 14.7 |
| Complex | > 500 LOC | 37 | 2.170 | 13.9 |

**Catatan**: Tidak ada kontrak Simple dalam dataset — wajar karena kontrak mainnet yang verified umumnya cukup kompleks.

---

## Statistik Dataset Keseluruhan

- Total LOC (46 valid): ~90.000 baris
- LOC terkecil: 266 (GovernorBravoDelegator)
- LOC terbesar: 11.395 (Seaport)
- Range solc: 0.4.18 s/d 0.8.18
- Sebagian besar kontrak menggunakan solc 0.4.x–0.6.x (era sebelum Solidity 0.8)
