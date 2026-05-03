# Per-Contract Findings: Data Lengkap 50 Kontrak

**Keterangan kolom**:
- `compile`: ✅ berhasil / ❌ gagal compile
- `rs` = redundant_sload | `ul` = unoptimized_loop | `sb` = string_vs_bytes32
- `pe` = public_vs_external | `ua` = unchecked_arithmetic | `dc` = dead_code
- `TOTAL` = jumlah semua findings

---

## Domain: DeFi (10 kontrak)

| No | Nama | LOC | compile | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | WETH9 | 1.511 | ✅ | 3 | 0 | 2 | 4 | 0 | 0 | **9** |
| 2 | UniswapV2Router02 | 1.559 | ✅ | 18 | 0 | 0 | 3 | 0 | 2 | **23** |
| 3 | Dai | 379 | ✅ | 7 | 0 | 3 | 0 | 0 | 0 | **10** |
| 4 | FiatTokenProxy | 657 | ✅ | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| 5 | Uni | 1.163 | ✅ | 14 | 0 | 11 | 3 | 0 | 0 | **28** |
| 6 | InitializableAdminUpgradeabilityProxy | 1.389 | ✅ | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| 7 | MiniMeToken | 1.199 | ✅ | 11 | 0 | 9 | 12 | 0 | 0 | **32** |
| 8 | AppProxyUpgradeable | 783 | ✅ | 0 | 0 | 0 | 8 | 0 | 3 | **11** |
| 9 | Comp | 301 | ✅ | 9 | 0 | 6 | 3 | 0 | 0 | **18** |
| 10 | DSToken | 947 | ✅ | 14 | 0 | 0 | 21 | 0 | 8 | **43** |
| | **DeFi Subtotal** | | | **76** | **0** | **31** | **54** | **0** | **13** | **174** |

**Catatan**:
- FiatTokenProxy dan InitializableAdminUpgradeabilityProxy (keduanya proxy pattern Aave/OpenZeppelin) menghasilkan 0 temuan karena arsitektur proxy yang meminimalkan storage access langsung
- UniswapV2Router02 memiliki 18 redundant_sload terbanyak di domain DeFi — contract stateless yang sering membaca state dari pasangan trading
- DSToken (Dai System Token era MakerDAO lama) sangat boros gas: 14 redundant SLOAD + 21 public functions + 8 dead code

---

## Domain: NFT (10 kontrak, 1 gagal compile)

| No | Nama | LOC | compile | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BoredApeYachtClub | 4.033 | ❌ | — | — | — | — | — | — | **—** |
| 2 | CryptoPunksMarket | 491 | ✅ | 20 | 0 | 4 | 11 | 0 | 0 | **35** |
| 3 | MutantApeYachtClub | 1.819 | ✅ | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| 4 | CloneX | 1.655 | ✅ | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| 5 | Moonbirds | 4.294 | ✅ | 0 | 0 | 2 | 2 | 2 | 1 | **7** |
| 6 | Azuki | 1.541 | ✅ | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| 7 | Doodles | 1.407 | ✅ | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| 8 | Meebits | 1.349 | ✅ | 21 | 0 | 3 | 3 | 0 | 0 | **27** |
| 9 | Toadz | 2.226 | ✅ | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| 10 | Land | 2.432 | ✅ | 0 | 0 | 3 | 0 | 8 | 2 | **13** |
| | **NFT Subtotal** | | | **41** | **0** | **12** | **26** | **10** | **3** | **92** |

**Catatan**:
- CryptoPunksMarket (2017, solc 0.4.x) memiliki 35 temuan — kontrak NFT pertama, ditulis tanpa mempertimbangkan gas optimization
- Meebits juga solc 0.4.x, dengan 21 redundant SLOAD
- Kontrak NFT modern (BAYC, MutantApe, Azuki, Doodles, Toadz) — semua menggunakan ERC-721 standar OpenZeppelin — hanya memiliki 2 temuan (public_vs_external minimal karena fungsi-fungsi override interface)
- Land (The Sandbox) memiliki 8 unchecked_arithmetic — solc 0.8.x dengan loop yang bisa dioptimasi
- BoredApeYachtClub gagal compile karena dependency/import yang tidak dapat diselesaikan dalam single-file analysis

---

## Domain: Token (10 kontrak, 1 gagal compile)

| No | Nama | LOC | compile | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | TetherToken | 893 | ✅ | 16 | 0 | 4 | 27 | 0 | 0 | **47** |
| 2 | WBTC | 1.317 | ✅ | 13 | 0 | 4 | 31 | 0 | 4 | **52** |
| 3 | LinkToken | 589 | ✅ | 5 | 0 | 2 | 19 | 0 | 2 | **28** |
| 4 | YFI | 449 | ✅ | 6 | 0 | 6 | 15 | 0 | 5 | **32** |
| 5 | OneInch | 2.235 | ✅ | 9 | 0 | 2 | 16 | 0 | 5 | **32** |
| 6 | GnosisToken | 301 | ❌ | — | — | — | — | — | — | **—** |
| 7 | BalancerGovernanceToken | 2.987 | ✅ | 6 | 0 | 5 | 20 | 0 | 10 | **41** |
| 8 | ProxyERC20 | 506 | ✅ | 5 | 0 | 0 | 18 | 0 | 0 | **23** |
| 9 | SimpleToken | 525 | ✅ | 0 | 0 | 2 | 0 | 0 | 0 | **2** |
| 10 | LQTYToken | 2.668 | ✅ | 0 | 0 | 0 | 0 | 0 | 1 | **1** |
| | **Token Subtotal** | | | **60** | **0** | **25** | **146** | **0** | **27** | **258** |

**Catatan**:
- Domain Token memiliki findings terbanyak (258) karena kontrak token ERC-20 era lama banyak mengekspos fungsi `public` yang seharusnya `external`
- WBTC (52) = kontrak tertinggi di seluruh dataset, terutama 31 public_vs_external
- TetherToken (Tether/USDT) yang lama memiliki 47 temuan — arsitektur manual tanpa library modern
- LQTYToken (Liquity, 2021) hanya 1 dead_code — kontrak modern sudah mengoptimasi
- SimpleToken (0 redundant, 0 loop, 0 unchecked) — kontrak sederhana, relatif bersih
- BalancerGovernanceToken (10 dead_code) — library Solidity yang tertanam memiliki banyak fungsi utilitas tidak terpakai

---

## Domain: Governance (10 kontrak, 1 gagal compile)

| No | Nama | LOC | compile | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GovernorBravoDelegator (v1) | 525 | ✅ | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| 2 | GovernorBravoDelegator (v2) | 266 | ✅ | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| 3 | FeiDAO | 3.516 | ❌ | — | — | — | — | — | — | **—** |
| 4 | AaveGovernanceV2 | 2.751 | ✅ | 4 | 0 | 2 | 4 | 0 | 3 | **13** |
| 5 | Governor (OpenZeppelin) | 1.011 | ✅ | 6 | 0 | 6 | 12 | 0 | 0 | **24** |
| 6 | GovernorAlpha (v1) | 323 | ✅ | 3 | 0 | 6 | 8 | 0 | 0 | **17** |
| 7 | GovernorAlpha (v2) | 604 | ✅ | 0 | 0 | 2 | 8 | 0 | 0 | **10** |
| 8 | ENSGovernor | 3.751 | ✅ | 0 | 0 | 0 | 4 | 0 | 2 | **6** |
| 9 | NounsDAOProxy | 402 | ✅ | 0 | 0 | 3 | 0 | 0 | 0 | **3** |
| 10 | GovernorAlpha (v3) | 348 | ✅ | 0 | 0 | 5 | 9 | 0 | 0 | **14** |
| | **Governance Subtotal** | | | **13** | **0** | **24** | **45** | **0** | **5** | **87** |

**Catatan**:
- GovernorBravoDelegator (Compound v1 dan v2) tidak menghasilkan temuan — kontrak delegator murni yang tidak mengandung logic
- Governor (OpenZeppelin) memiliki 24 temuan — library governance framework yang besar
- Domain Governance memiliki pola string_vs_bytes32 relatif banyak (24) karena kontrak governance sering menyimpan nama/deskripsi proposal sebagai `string`
- FeiDAO gagal compile karena import kompleks (Tribe/FEI ecosystem)

---

## Domain: Utility (10 kontrak, 1 gagal compile)

| No | Nama | LOC | compile | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DAO (The DAO) | 1.236 | ❌ | — | — | — | — | — | — | **—** |
| 2 | GnosisSafe | 1.132 | ✅ | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| 3 | MultiSigWallet | 731 | ✅ | 11 | 5 | 0 | 10 | 0 | 0 | **26** |
| 4 | Jug (MakerDAO) | 313 | ✅ | 3 | 0 | 0 | 0 | 0 | 0 | **3** |
| 5 | MultiSigWalletWithTimeLock | 6.783 | ✅ | 0 | 0 | 0 | 0 | 0 | 2 | **2** |
| 6 | Seaport (OpenSea) | 11.395 | ✅ | 0 | 0 | 0 | 0 | 0 | 2 | **2** |
| 7 | UniswapV3Factory | 3.383 | ✅ | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| 8 | SwapRouter | 2.096 | ✅ | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| 9 | SwapRouter02 | 3.878 | ✅ | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| 10 | NonfungiblePositionManager | 4.595 | ✅ | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| | **Utility Subtotal** | | | **14** | **5** | **0** | **12** | **0** | **4** | **35** |

**Catatan**:
- UniswapV3 contracts (Factory, SwapRouter, SwapRouter02, NonfungiblePositionManager) = **0 temuan** semua — kontrak modern (2021) yang sudah highly optimized untuk gas, ditulis oleh tim Uniswap Labs yang sangat sadar gas efficiency
- Seaport (OpenSea, 2022) = hanya 2 dead_code — kontrak yang diaudit ketat
- MultiSigWallet (Gnosis multisig lama, solc 0.4.x) = satu-satunya kontrak dengan `unoptimized_loop` (5 temuan)
- The DAO gagal compile — kontrak 2016 yang sangat lama (terkait dengan hack DAO yang terkenal)
- GnosisSafe modern = hanya 2 temuan minimal

---

## Kontrak dengan 0 Findings (Bersih)

8 kontrak dari 46 valid menghasilkan 0 findings:

| Kontrak | Domain | LOC | Keterangan |
|---|---|---|---|
| FiatTokenProxy | DeFi | 657 | Proxy pattern, no direct logic |
| InitializableAdminUpgradeabilityProxy | DeFi | 1.389 | Proxy pattern |
| UniswapV3Factory | Utility | 3.383 | Modern, highly optimized |
| SwapRouter | Utility | 2.096 | Modern, highly optimized |
| SwapRouter02 | Utility | 3.878 | Modern, highly optimized |
| NonfungiblePositionManager | Utility | 4.595 | Modern, highly optimized |
| GovernorBravoDelegator (v1) | Governance | 525 | Pure delegator, no logic |
| GovernorBravoDelegator (v2) | Governance | 266 | Pure delegator, no logic |

**Pola**: Kontrak modern (solc 0.8.x, post-2021) yang ditulis oleh tim berpengalaman dan sudah diaudit umumnya tidak memiliki anti-pattern yang terdeteksi. Proxy contracts juga bersih karena tidak mengandung application logic langsung.

---

## Rekap Total Keseluruhan

| Domain | n valid | Total Findings | Avg/kontrak | Kontrak dgn findings |
|---|---|---|---|---|
| DeFi | 10 | 174 | 17.4 | 8/10 (80%) |
| NFT | 9 | 92 | 10.2 | 7/9 (78%) |
| Token | 9 | 258 | 28.7 | 8/9 (89%) |
| Governance | 9 | 87 | 9.7 | 7/9 (78%) |
| Utility | 9 | 35 | 3.9 | 6/9 (67%) |
| **TOTAL** | **46** | **646** | **14.0** | **38/46 (83%)** |
