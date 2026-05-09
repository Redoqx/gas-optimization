# Per-Contract Findings: Data Lengkap 74 Kontrak

**Dataset aktif**: `contracts_selection.json` (75 kontrak, 74 compile-ok)

**Keterangan kolom**:
- `rs` = redundant_sload | `ul` = unoptimized_loop | `sb` = string_vs_bytes32
- `pe` = public_vs_external | `ua` = unchecked_arithmetic | `dc` = dead_code
- `TOTAL` = jumlah semua findings

---

## Domain: DeFi (15 kontrak, 15 compile-ok)

| Nama | SLOC | Cx | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| AppProxyUpgradeable | 279 | M | 0 | 0 | 0 | 8 | 0 | 3 | **11** |
| Dai | 169 | M | 7 | 0 | 3 | 0 | 0 | 0 | **10** |
| DaiJoin | 192 | M | 1 | 0 | 0 | 1 | 0 | 0 | **2** |
| ETHJoin | 192 | M | 1 | 0 | 0 | 1 | 0 | 0 | **2** |
| GemJoin | 162 | M | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
| KyberNetworkProxy | 484 | M | 24 | 2 | 0 | 40 | 0 | 2 | **68** |
| Spotter | 129 | M | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| UniswapV2Factory | 414 | M | 17 | 0 | 2 | 1 | 0 | 0 | **20** |
| UniswapV2Pair | 396 | M | 11 | 0 | 2 | 1 | 0 | 0 | **14** |
| Vat | 238 | M | 24 | 0 | 0 | 0 | 0 | 0 | **24** |
| CErc20 | 2.178 | C | 33 | 0 | 6 | 1 | 0 | 9 | **49** |
| CErc20Delegator (cDAI) | 1.901 | C | 0 | 0 | 2 | 1 | 0 | 3 | **6** |
| CErc20Delegator (cCOMP) | 1.901 | C | 0 | 0 | 2 | 1 | 0 | 3 | **6** |
| CEther | 2.138 | C | 32 | 0 | 7 | 1 | 0 | 9 | **49** |
| InitializableAdminUpgradeabilityProxy | 1.185 | C | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **DeFi Subtotal** | | | **151** | **2** | **24** | **56** | **0** | **29** | **262** |

**Catatan**:
- KyberNetworkProxy (68 temuan) — kontrak era 0.6.x dengan banyak fungsi `public` dan storage reads berulang
- Vat (24 rs) — MakerDAO CDP engine, banyak akses ke mapping storage tanpa caching
- Spotter & InitializableAdminUpgradeabilityProxy: 0 findings (proxy pattern minimal / modern design)
- CErc20 dan CEther hampir identik strukturnya — masing-masing 49 findings

---

## Domain: NFT (15 kontrak, 15 compile-ok)

| Nama | SLOC | Cx | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| CryptoPunksMarket | 212 | M | 20 | 0 | 4 | 11 | 0 | 0 | **35** |
| AdminUpgradeabilityProxy | 1.515 | C | 0 | 0 | 18 | 25 | 0 | 2 | **45** |
| AvastarTeleporter | 2.171 | C | 37 | 0 | 19 | 11 | 0 | 7 | **74** |
| Azuki | 1.335 | C | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| BaseRegistrarImplementation | 664 | C | 10 | 0 | 0 | 10 | 0 | 3 | **23** |
| CloneX | 1.308 | C | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| DCLRegistrar | 1.570 | C | 26 | 0 | 23 | 34 | 0 | 7 | **90** |
| Doodles | 1.206 | C | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| KittyCore (CryptoKitties) | 1.685 | C | 19 | 0 | 4 | 9 | 0 | 0 | **32** |
| LANDProxy (Decentraland) | 1.256 | C | 24 | 0 | 12 | 4 | 0 | 3 | **43** |
| Meebits | 567 | C | 21 | 0 | 3 | 3 | 0 | 0 | **27** |
| MutantApeYachtClub | 1.550 | C | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| Parcel | 733 | C | 21 | 0 | 7 | 26 | 0 | 3 | **57** |
| SuperRareV2 | 999 | C | 16 | 0 | 12 | 20 | 0 | 3 | **51** |
| WrappedPunk | 1.376 | C | 14 | 0 | 10 | 22 | 0 | 8 | **54** |
| **NFT Subtotal** | | | **208** | **0** | **112** | **183** | **0** | **36** | **539** |

**Catatan**:
- **DCLRegistrar memiliki temuan terbanyak** (90) — kontrak era 0.5.x Decentraland dengan banyak string dan storage reads
- **AvastarTeleporter**: 37 redundant_sload tertinggi di NFT
- Kontrak modern (Azuki, CloneX, Doodles, MutantApeYachtClub, Meebits) era 0.8.x: masing-masing hanya 2 findings (public_vs_external pada fungsi override)
- String vs Bytes32 tinggi di NFT (112) karena banyak kontrak menyimpan metadata sebagai string

---

## Domain: Token (15 kontrak, 15 compile-ok)

| Nama | SLOC | Cx | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| BAToken | 146 | M | 11 | 0 | 3 | 10 | 0 | 0 | **24** |
| LinkToken | 250 | M | 5 | 0 | 2 | 19 | 0 | 2 | **28** |
| MANAToken | 222 | M | 8 | 0 | 2 | 19 | 0 | 2 | **31** |
| ProxyERC20 | 408 | M | 5 | 0 | 0 | 18 | 0 | 0 | **23** |
| SimpleToken (ApeCoin) | 451 | M | 0 | 0 | 2 | 0 | 0 | 0 | **2** |
| TetherToken | 377 | M | 16 | 0 | 4 | 27 | 0 | 0 | **47** |
| AdminUpgradeabilityProxy (BUSD) | 581 | C | 33 | 0 | 3 | 25 | 0 | 0 | **61** |
| AdminUpgradeabilityProxy (PAXG) | 687 | C | 37 | 0 | 3 | 28 | 0 | 0 | **68** |
| BalancerGovernanceToken | 1.280 | C | 6 | 0 | 5 | 20 | 0 | 10 | **41** |
| FiatTokenProxy (USDC) | 2.715 | C | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| GraphToken | 832 | C | 9 | 0 | 2 | 12 | 0 | 4 | **27** |
| LQTYToken | 2.135 | C | 0 | 0 | 0 | 0 | 0 | 1 | **1** |
| OneInch | 964 | C | 9 | 0 | 2 | 16 | 0 | 5 | **32** |
| OwnedUpgradeabilityProxy (TUSD) | 1.291 | C | 17 | 0 | 3 | 11 | 0 | 10 | **41** |
| WBTC | 564 | C | 13 | 0 | 4 | 31 | 0 | 4 | **52** |
| **Token Subtotal** | | | **169** | **0** | **35** | **236** | **0** | **38** | **478** |

**Catatan**:
- **Public_vs_external dominasi** (236 findings) — token ERC-20 era lama menggunakan `public` secara masif
- TetherToken: 16+27=43 findings (rs+pe) — kontrak USDT 2017 era 0.4.x
- FiatTokenProxy (USDC) & LQTYToken: hampir 0 findings — kontrak modern yang sudah dioptimasi
- Dua AdminUpgradeabilityProxy (BUSD/PAXG) memiliki struktur mirip tapi berbeda ukuran

---

## Domain: Governance (15 kontrak, 15 compile-ok)

| Nama | SLOC | Cx | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| Comp | 249 | M | 9 | 0 | 6 | 3 | 0 | 0 | **18** |
| DSToken (MKR) | 371 | M | 14 | 0 | 0 | 21 | 0 | 8 | **43** |
| Governor (ENS) | 443 | M | 6 | 0 | 6 | 12 | 0 | 0 | **24** |
| GovernorAlpha (Compound) | 252 | M | 3 | 0 | 6 | 8 | 0 | 0 | **17** |
| GovernorBravoDelegate | 465 | M | 0 | 0 | 3 | 2 | 0 | 0 | **5** |
| GovernorBravoDelegator (Compound) | 465 | M | 0 | 0 | 3 | 2 | 0 | 0 | **5** |
| GovernorBravoDelegator (Uniswap) | 200 | M | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| NounsDAOProxy | 336 | M | 0 | 0 | 3 | 0 | 0 | 0 | **3** |
| Tribe (FEI) | 322 | M | 0 | 0 | 4 | 3 | 0 | 0 | **7** |
| Uni (UNI) | 493 | M | 14 | 0 | 11 | 3 | 0 | 0 | **28** |
| YFI | 191 | M | 6 | 0 | 6 | 15 | 0 | 5 | **32** |
| AaveGovernanceV2 | 1.234 | C | 4 | 0 | 2 | 4 | 0 | 3 | **13** |
| AdminUpgradeabilityProxy (Aave) | 1.117 | C | 0 | 0 | 4 | 6 | 0 | 0 | **10** |
| MiniMeToken (LDO) | 516 | C | 11 | 0 | 9 | 12 | 0 | 0 | **32** |
| Token (ANT) | 528 | C | 8 | 0 | 7 | 17 | 0 | 3 | **35** |
| **Governance Subtotal** | | | **75** | **0** | **70** | **108** | **0** | **19** | **272** |

**Catatan**:
- DSToken (MKR): 43 findings — kontrak governance MakerDAO era lama
- GovernorBravoDelegator (Uniswap, LOC=200): 0 findings — versi lebih modern
- String_vs_bytes32 tinggi (70) di Governance — kontrak governance banyak menyimpan string untuk deskripsi proposal

---

## Domain: Utility (14 compile-ok dari 15)

| Nama | SLOC | Cx | rs | ul | sb | pe | ua | dc | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| Multicall | 43 | **S** | 0 | 0 | 0 | 8 | 0 | 0 | **8** |
| Multicall2 | 70 | **S** | 0 | 0 | 0 | 10 | 0 | 0 | **10** |
| DSProxyFactory | 183 | M | 6 | 0 | 0 | 5 | 0 | 0 | **11** |
| ENSRegistryWithFallback | 236 | M | 1 | 0 | 0 | 8 | 0 | 0 | **9** |
| ERC1820Registry | 194 | M | 1 | 0 | 1 | 0 | 0 | 0 | **2** |
| GnosisSafeProxyFactory | 152 | M | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Jug (MakerDAO) | 141 | M | 3 | 0 | 0 | 0 | 0 | 0 | **3** |
| MultiSigWallet | 334 | M | 11 | 5 | 0 | 10 | 0 | 0 | **26** |
| ReverseRegistrar | 354 | M | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| WyvernProxyRegistry | 383 | M | 9 | 0 | 1 | 21 | 0 | 0 | **31** |
| GnosisSafe | 1.008 | C | 0 | 0 | 0 | 2 | 0 | 0 | **2** |
| NonfungiblePositionManager | 3.957 | C | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| SwapRouter02 | 3.276 | C | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| UniswapV3Factory | 2.970 | C | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| *(PublicResolver — compile fail)* | 342 | M | — | — | — | — | — | — | **—** |
| **Utility Subtotal** | | | **31** | **5** | **2** | **66** | **0** | **0** | **104** |

**Catatan**:
- **MultiSigWallet**: satu-satunya kontrak dengan unoptimized_loop (5 findings, loop dengan `.owners.length`)
- **Multicall & Multicall2**: kontrak Simple — hanya public_vs_external (semua fungsi bisa external)
- Empat kontrak Uniswap v3/Gnosis Safe era modern: 0 findings — dikembangkan dengan gas optimization sebagai prioritas utama
- **WyvernProxyRegistry** (31 findings): kontrak OpenSea era lama dengan banyak fungsi public

---

## Ringkasan Cross-Domain

| Domain | n compile-ok | Total Findings | Avg/Contract | Max | % dari Total |
|---|---|---|---|---|---|
| DeFi | 15 | 262 | 17.5 | 68 (KyberNetworkProxy) | 15.8% |
| NFT | 15 | 539 | 35.9 | 90 (DCLRegistrar) | 32.6% |
| Token | 15 | 478 | 31.9 | 68 (AdminUpgradeabilityProxy PAXG) | 28.9% |
| Governance | 15 | 272 | 18.1 | 43 (DSToken) | 16.4% |
| Utility | 14 | 104 | 7.4 | 31 (WyvernProxyRegistry) | 6.3% |
| **TOTAL** | **74** | **1.655** | **22.4** | **90** | **100%** |

**Legend**: Cx = Complexity (S=Simple, M=Medium, C=Complex)
