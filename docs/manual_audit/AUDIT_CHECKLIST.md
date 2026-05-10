# Manual Audit Checklist — 20 Kontrak Top Gas Savings

**Tujuan**: Verifikasi setiap temuan detektor — apakah anti-pattern gas benar-benar ada di kode.

## Cara Mengisi

Untuk setiap baris temuan, buka file `.sol` yang tercantum, cari nama fungsi/variabel,
lalu tandai kolom `Audit`:

| Kode | Arti |
|---|---|
| `TP` | True Positive — anti-pattern memang ada, temuan valid |
| `FP` | False Positive — bukan anti-pattern, detektor salah flag |
| `?`  | Ambiguous — tidak yakin, butuh diskusi |

Isi kolom `Catatan` jika FP atau ?: jelaskan singkat kenapa.

---

## Ringkasan 20 Kontrak

| # | Kontrak | Domain | LOC | Savings (gas) | rs | ul | sb | pe | dc | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **DCLRegistrar** | NFT | 1570 | 117,568 | 26 | 0 | 23 | 34 | 7 | 90 |
| 2 | **KyberNetworkProxy** | DeFi | 484 | 113,446 | 24 | 2 | 0 | 40 | 2 | 68 |
| 3 | **WBTC** | Token | 564 | 89,081 | 13 | 0 | 4 | 31 | 4 | 52 |
| 4 | **AdminUpgradeabilityProxy** | Token | 687 | 84,576 | 37 | 0 | 3 | 28 | 0 | 68 |
| 5 | **AdminUpgradeabilityProxy** | NFT | 1515 | 83,925 | 0 | 0 | 18 | 25 | 2 | 45 |
| 6 | **Parcel** | NFT | 733 | 80,054 | 21 | 0 | 7 | 26 | 3 | 57 |
| 7 | **TetherToken** | Token | 377 | 78,947 | 16 | 0 | 4 | 27 | 0 | 47 |
| 8 | **AdminUpgradeabilityProxy** | Token | 581 | 75,813 | 33 | 0 | 3 | 25 | 0 | 61 |
| 9 | **WrappedPunk** | NFT | 1376 | 70,910 | 14 | 0 | 10 | 22 | 8 | 54 |
| 10 | **SuperRareV2** | NFT | 999 | 67,836 | 16 | 0 | 12 | 20 | 3 | 51 |
| 11 | **BalancerGovernanceToken** | Token | 1280 | 59,326 | 6 | 0 | 5 | 20 | 10 | 41 |
| 12 | **WyvernProxyRegistry** | Utility | 383 | 58,757 | 9 | 0 | 1 | 21 | 0 | 31 |
| 13 | **DSToken** | Governance | 371 | 58,737 | 14 | 0 | 0 | 21 | 8 | 43 |
| 14 | **AvastarTeleporter** | NFT | 2171 | 54,335 | 37 | 0 | 19 | 11 | 7 | 74 |
| 15 | **MANAToken** | Token | 222 | 54,175 | 8 | 0 | 2 | 19 | 2 | 31 |
| 16 | **LinkToken** | Token | 250 | 53,617 | 5 | 0 | 2 | 19 | 2 | 28 |
| 17 | **Token** | Governance | 528 | 53,579 | 8 | 0 | 7 | 17 | 3 | 35 |
| 18 | **YFI** | Governance | 191 | 46,911 | 6 | 0 | 6 | 15 | 5 | 32 |
| 19 | **MultiSigWallet** | Utility | 334 | 33,931 | 11 | 5 | 0 | 10 | 0 | 26 |
| 20 | **AppProxyUpgradeable** | DeFi | 279 | 21,384 | 0 | 0 | 0 | 8 | 3 | 11 |

**Total estimated savings**: 1,356,908 gas  
**Total findings to audit**: 945

---

## [01] DCLRegistrar

| Field | Value |
|---|---|
| Domain | NFT |
| Complexity | Complex |
| LOC | 1570 |
| File | `017_DCLRegistrar_0x2a187453.sol` |
| Estimated Savings | **117,568 gas** |
| Total Findings | 90 |

### Redundant SLOAD — 26 temuan (4,836 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | Redundant SLOAD: '_owner' dibaca 2x di fungsi ''.  | `[ ]` | |
| 2 | `_owner` in `renounceOwnership()` | `[ ]` | |
| 3 | `_owner` in `_transferOwnership()` | `[ ]` | |
| 4 | `_ownedTokensCount` in `_transferFrom()` | `[ ]` | |
| 5 | `_tokenApprovals` in `_clearApproval()` | `[ ]` | |
| 6 | `_ownedTokens` in `_addTokenToOwnerEnumeration()` | `[ ]` | |
| 7 | `_allTokens` in `_addTokenToAllTokensEnumeration()` | `[ ]` | |
| 8 | `_ownedTokens` in `_removeTokenFromOwnerEnumeration()` | `[ ]` | |
| 9 | `_ownedTokensIndex` in `_removeTokenFromOwnerEnumeration()` | `[ ]` | |
| 10 | `_allTokens` in `_removeTokenFromAllTokensEnumeration()` | `[ ]` | |
| 11 | `_allTokensIndex` in `_removeTokenFromAllTokensEnumeration()` | `[ ]` | |
| 12 | `_tokenURIs` in `_burn()` | `[ ]` | |
| 13 | Redundant SLOAD: 'topdomain' dibaca 2x di fungsi ' | `[ ]` | |
| 14 | Redundant SLOAD: 'domain' dibaca 2x di fungsi ''.  | `[ ]` | |
| 15 | Redundant SLOAD: 'topdomainNameHash' dibaca 2x di  | `[ ]` | |
| 16 | `_owner` in `reclaim()` | `[ ]` | |
| 17 | `base` in `onERC721Received()` | `[ ]` | |
| 18 | `baseURI` in `tokenURI()` | `[ ]` | |
| 19 | `_owner` in `transferDomainOwnership()` | `[ ]` | |
| 20 | `registry` in `setResolver()` | `[ ]` | |
| 21 | `domainNameHash` in `setResolver()` | `[ ]` | |
| 22 | `controllers` in `addController()` | `[ ]` | |
| 23 | `controllers` in `removeController()` | `[ ]` | |
| 24 | `registry` in `updateRegistry()` | `[ ]` | |
| 25 | `base` in `updateBase()` | `[ ]` | |
| 26 | `baseURI` in `updateBaseURI()` | `[ ]` | |

**Hasil**: 26 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 23 temuan (21,850 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_name` | `[ ]` | |
| 2 | `_symbol` | `[ ]` | |
| 3 | `topdomain` | `[ ]` | |
| 4 | `domain` | `[ ]` | |
| 5 | `baseURI` | `[ ]` | |
| 6 | `errorMessage` | `[ ]` | |
| 7 | `errorMessage` | `[ ]` | |
| 8 | `errorMessage` | `[ ]` | |
| 9 | `name` | `[ ]` | |
| 10 | `symbol` | `[ ]` | |
| 11 | `uri` | `[ ]` | |
| 12 | `name` | `[ ]` | |
| 13 | `symbol` | `[ ]` | |
| 14 | `_topdomain` | `[ ]` | |
| 15 | `_domain` | `[ ]` | |
| 16 | `_baseURI` | `[ ]` | |
| 17 | `_subdomain` | `[ ]` | |
| 18 | `_subdomain` | `[ ]` | |
| 19 | `_subdomain` | `[ ]` | |
| 20 | `_subdomain` | `[ ]` | |
| 21 | `_subdomain` | `[ ]` | |
| 22 | `_baseURI` | `[ ]` | |
| 23 | `_str` | `[ ]` | |

**Hasil**: 23 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 34 temuan (90,882 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `owner()` | `[ ]` | |
| 2 | `renounceOwnership()` | `[ ]` | |
| 3 | `transferOwnership()` | `[ ]` | |
| 4 | `transferFrom()` | `[ ]` | |
| 5 | `approve()` | `[ ]` | |
| 6 | `setApprovalForAll()` | `[ ]` | |
| 7 | `onERC721Received()` | `[ ]` | |
| 8 | `approve()` | `[ ]` | |
| 9 | `setApprovalForAll()` | `[ ]` | |
| 10 | `transferFrom()` | `[ ]` | |
| 11 | `tokenOfOwnerByIndex()` | `[ ]` | |
| 12 | `tokenByIndex()` | `[ ]` | |
| 13 | `tokenOfOwnerByIndex()` | `[ ]` | |
| 14 | `tokenByIndex()` | `[ ]` | |
| 15 | `setOwner()` | `[ ]` | |
| 16 | `setSubnodeOwner()` | `[ ]` | |
| 17 | `setResolver()` | `[ ]` | |
| 18 | `owner()` | `[ ]` | |
| 19 | `resolver()` | `[ ]` | |
| 20 | `setAddr()` | `[ ]` | |
| 21 | `addr()` | `[ ]` | |
| 22 | `transferFrom()` | `[ ]` | |
| 23 | `transferFrom()` | `[ ]` | |
| 24 | `allowance()` | `[ ]` | |
| 25 | `burn()` | `[ ]` | |
| 26 | `reclaim()` | `[ ]` | |
| 27 | `reclaim()` | `[ ]` | |
| 28 | `onERC721Received()` | `[ ]` | |
| 29 | `available()` | `[ ]` | |
| 30 | `getOwnerOf()` | `[ ]` | |
| 31 | `reclaimDomain()` | `[ ]` | |
| 32 | `transferDomainOwnership()` | `[ ]` | |
| 33 | `setResolver()` | `[ ]` | |
| 34 | `forwardToResolver()` | `[ ]` | |

**Hasil**: 34 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 7 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_msgData()` | `[ ]` | |
| 2 | `add()` | `[ ]` | |
| 3 | `mul()` | `[ ]` | |
| 4 | `toPayable()` | `[ ]` | |
| 5 | `sendValue()` | `[ ]` | |
| 6 | `_tokensOfOwner()` | `[ ]` | |
| 7 | `_setTokenURI()` | `[ ]` | |

**Hasil**: 7 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 26 | | | |
| String vs Bytes32 | 23 | | | |
| Public vs External | 34 | | | |
| Dead Code | 7 | | | |

---

## [02] KyberNetworkProxy

| Field | Value |
|---|---|
| Domain | DeFi |
| Complexity | Medium |
| LOC | 484 |
| File | `008_KyberNetworkProxy_0x818E6FEC.sol` |
| Estimated Savings | **113,446 gas** |
| Total Findings | 68 |

### Redundant SLOAD — 24 temuan (4,464 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `decimals` in `setDecimals()` | `[ ]` | |
| 2 | `MAX_DECIMALS` in `calcDstQty()` | `[ ]` | |
| 3 | `PRECISION` in `calcDstQty()` | `[ ]` | |
| 4 | `MAX_DECIMALS` in `calcSrcQty()` | `[ ]` | |
| 5 | `PRECISION` in `calcSrcQty()` | `[ ]` | |
| 6 | `decimals` in `getDecimalsSafe()` | `[ ]` | |
| 7 | `MAX_QTY` in `calcRateFromQty()` | `[ ]` | |
| 8 | `MAX_DECIMALS` in `calcRateFromQty()` | `[ ]` | |
| 9 | `PRECISION` in `calcRateFromQty()` | `[ ]` | |
| 10 | `pendingAdmin` in `transferAdmin()` | `[ ]` | |
| 11 | `admin` in `transferAdminQuickly()` | `[ ]` | |
| 12 | `pendingAdmin` in `claimAdmin()` | `[ ]` | |
| 13 | `admin` in `claimAdmin()` | `[ ]` | |
| 14 | `alerters` in `addAlerter()` | `[ ]` | |
| 15 | `alertersGroup` in `addAlerter()` | `[ ]` | |
| 16 | `alerters` in `removeAlerter()` | `[ ]` | |
| 17 | `alertersGroup` in `removeAlerter()` | `[ ]` | |
| 18 | `operators` in `addOperator()` | `[ ]` | |
| 19 | `operatorsGroup` in `addOperator()` | `[ ]` | |
| 20 | `operators` in `removeOperator()` | `[ ]` | |
| 21 | `operatorsGroup` in `removeOperator()` | `[ ]` | |
| 22 | `ETH_TOKEN_ADDRESS` in `tradeWithHint()` | `[ ]` | |
| 23 | `kyberNetworkContract` in `tradeWithHint()` | `[ ]` | |
| 24 | `kyberNetworkContract` in `setKyberNetworkContract()` | `[ ]` | |

**Hasil**: 24 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Unoptimized Loop — 2 temuan (2,062 gas potensial)

> **Cara audit**: Cari for-loop yang disebutkan, periksa apakah `array.length` ada di kondisi loop dan array itu adalah state variable.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | Unoptimized Loop: 'alertersGroup.length' dibaca da | `[ ]` | |
| 2 | Unoptimized Loop: 'operatorsGroup.length' dibaca d | `[ ]` | |

**Hasil**: 2 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 40 temuan (106,920 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `totalSupply()` | `[ ]` | |
| 2 | `balanceOf()` | `[ ]` | |
| 3 | `transfer()` | `[ ]` | |
| 4 | `transferFrom()` | `[ ]` | |
| 5 | `approve()` | `[ ]` | |
| 6 | `allowance()` | `[ ]` | |
| 7 | `decimals()` | `[ ]` | |
| 8 | `maxGasPrice()` | `[ ]` | |
| 9 | `getUserCapInWei()` | `[ ]` | |
| 10 | `getUserCapInTokenWei()` | `[ ]` | |
| 11 | `enabled()` | `[ ]` | |
| 12 | `info()` | `[ ]` | |
| 13 | `getExpectedRate()` | `[ ]` | |
| 14 | `maxGasPrice()` | `[ ]` | |
| 15 | `getUserCapInWei()` | `[ ]` | |
| 16 | `getUserCapInTokenWei()` | `[ ]` | |
| 17 | `enabled()` | `[ ]` | |
| 18 | `info()` | `[ ]` | |
| 19 | `getExpectedRate()` | `[ ]` | |
| 20 | `swapTokenToToken()` | `[ ]` | |
| 21 | `swapEtherToToken()` | `[ ]` | |
| 22 | `swapTokenToEther()` | `[ ]` | |
| 23 | `transferAdmin()` | `[ ]` | |
| 24 | `transferAdminQuickly()` | `[ ]` | |
| 25 | `claimAdmin()` | `[ ]` | |
| 26 | `addAlerter()` | `[ ]` | |
| 27 | `removeAlerter()` | `[ ]` | |
| 28 | `addOperator()` | `[ ]` | |
| 29 | `removeOperator()` | `[ ]` | |
| 30 | `trade()` | `[ ]` | |
| 31 | `swapTokenToToken()` | `[ ]` | |
| 32 | `swapEtherToToken()` | `[ ]` | |
| 33 | `swapTokenToEther()` | `[ ]` | |
| 34 | `setKyberNetworkContract()` | `[ ]` | |
| 35 | `getExpectedRate()` | `[ ]` | |
| 36 | `getUserCapInWei()` | `[ ]` | |
| 37 | `getUserCapInTokenWei()` | `[ ]` | |
| 38 | `maxGasPrice()` | `[ ]` | |
| 39 | `enabled()` | `[ ]` | |
| 40 | `info()` | `[ ]` | |

**Hasil**: 40 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 2 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `calcDestAmount()` | `[ ]` | |
| 2 | `calcSrcAmount()` | `[ ]` | |

**Hasil**: 2 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 24 | | | |
| Unoptimized Loop | 2 | | | |
| Public vs External | 40 | | | |
| Dead Code | 2 | | | |

---

## [03] WBTC

| Field | Value |
|---|---|
| Domain | Token |
| Complexity | Complex |
| LOC | 564 |
| File | `022_WBTC_0x2260FAC5.sol` |
| Estimated Savings | **89,081 gas** |
| Total Findings | 52 |

### Redundant SLOAD — 13 temuan (2,418 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `balances` in `transfer()` | `[ ]` | |
| 2 | `balances` in `transferFrom()` | `[ ]` | |
| 3 | `allowed` in `transferFrom()` | `[ ]` | |
| 4 | `allowed` in `increaseApproval()` | `[ ]` | |
| 5 | `allowed` in `decreaseApproval()` | `[ ]` | |
| 6 | `owner` in `renounceOwnership()` | `[ ]` | |
| 7 | `owner` in `_transferOwnership()` | `[ ]` | |
| 8 | `totalSupply_` in `mint()` | `[ ]` | |
| 9 | `balances` in `mint()` | `[ ]` | |
| 10 | `balances` in `_burn()` | `[ ]` | |
| 11 | `totalSupply_` in `_burn()` | `[ ]` | |
| 12 | `owner` in `claimOwnership()` | `[ ]` | |
| 13 | `pendingOwner` in `claimOwnership()` | `[ ]` | |

**Hasil**: 13 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 4 temuan (3,800 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `name` | `[ ]` | |
| 2 | `symbol` | `[ ]` | |
| 3 | `_name` | `[ ]` | |
| 4 | `_symbol` | `[ ]` | |

**Hasil**: 4 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 31 temuan (82,863 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `totalSupply()` | `[ ]` | |
| 2 | `balanceOf()` | `[ ]` | |
| 3 | `transfer()` | `[ ]` | |
| 4 | `totalSupply()` | `[ ]` | |
| 5 | `transfer()` | `[ ]` | |
| 6 | `balanceOf()` | `[ ]` | |
| 7 | `allowance()` | `[ ]` | |
| 8 | `transferFrom()` | `[ ]` | |
| 9 | `approve()` | `[ ]` | |
| 10 | `transferFrom()` | `[ ]` | |
| 11 | `approve()` | `[ ]` | |
| 12 | `allowance()` | `[ ]` | |
| 13 | `increaseApproval()` | `[ ]` | |
| 14 | `decreaseApproval()` | `[ ]` | |
| 15 | `renounceOwnership()` | `[ ]` | |
| 16 | `transferOwnership()` | `[ ]` | |
| 17 | `mint()` | `[ ]` | |
| 18 | `finishMinting()` | `[ ]` | |
| 19 | `burn()` | `[ ]` | |
| 20 | `pause()` | `[ ]` | |
| 21 | `unpause()` | `[ ]` | |
| 22 | `transfer()` | `[ ]` | |
| 23 | `transferFrom()` | `[ ]` | |
| 24 | `approve()` | `[ ]` | |
| 25 | `increaseApproval()` | `[ ]` | |
| 26 | `decreaseApproval()` | `[ ]` | |
| 27 | `transferOwnership()` | `[ ]` | |
| 28 | `claimOwnership()` | `[ ]` | |
| 29 | `burn()` | `[ ]` | |
| 30 | `finishMinting()` | `[ ]` | |
| 31 | `renounceOwnership()` | `[ ]` | |

**Hasil**: 31 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 4 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `mul()` | `[ ]` | |
| 2 | `div()` | `[ ]` | |
| 3 | `safeTransferFrom()` | `[ ]` | |
| 4 | `safeApprove()` | `[ ]` | |

**Hasil**: 4 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 13 | | | |
| String vs Bytes32 | 4 | | | |
| Public vs External | 31 | | | |
| Dead Code | 4 | | | |

---

## [04] AdminUpgradeabilityProxy

| Field | Value |
|---|---|
| Domain | Token |
| Complexity | Complex |
| LOC | 687 |
| File | `026_AdminUpgradeabilityProxy_0x45804880.sol` |
| Estimated Savings | **84,576 gas** |
| Total Findings | 68 |

### Redundant SLOAD — 37 temuan (6,882 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `initialized` in `initialize()` | `[ ]` | |
| 2 | `frozen` in `transfer()` | `[ ]` | |
| 3 | `frozen` in `transferFrom()` | `[ ]` | |
| 4 | `allowed` in `transferFrom()` | `[ ]` | |
| 5 | `frozen` in `approve()` | `[ ]` | |
| 6 | `balances` in `_transfer()` | `[ ]` | |
| 7 | `feeRecipient` in `_transfer()` | `[ ]` | |
| 8 | `proposedOwner` in `proposeOwner()` | `[ ]` | |
| 9 | `proposedOwner` in `disregardProposeOwner()` | `[ ]` | |
| 10 | `proposedOwner` in `claimOwnership()` | `[ ]` | |
| 11 | `owner` in `claimOwnership()` | `[ ]` | |
| 12 | `balances` in `reclaimPAXG()` | `[ ]` | |
| 13 | `owner` in `reclaimPAXG()` | `[ ]` | |
| 14 | `paused` in `pause()` | `[ ]` | |
| 15 | `paused` in `unpause()` | `[ ]` | |
| 16 | `assetProtectionRole` in `setAssetProtectionRole()` | `[ ]` | |
| 17 | `frozen` in `freeze()` | `[ ]` | |
| 18 | `frozen` in `unfreeze()` | `[ ]` | |
| 19 | `balances` in `wipeFrozenAddress()` | `[ ]` | |
| 20 | `totalSupply_` in `wipeFrozenAddress()` | `[ ]` | |
| 21 | `supplyController` in `setSupplyController()` | `[ ]` | |
| 22 | `totalSupply_` in `increaseSupply()` | `[ ]` | |
| 23 | `balances` in `increaseSupply()` | `[ ]` | |
| 24 | `supplyController` in `increaseSupply()` | `[ ]` | |
| 25 | `balances` in `decreaseSupply()` | `[ ]` | |
| 26 | `supplyController` in `decreaseSupply()` | `[ ]` | |
| 27 | `totalSupply_` in `decreaseSupply()` | `[ ]` | |
| 28 | `frozen` in `_betaDelegatedTransfer()` | `[ ]` | |
| 29 | `balances` in `_betaDelegatedTransfer()` | `[ ]` | |
| 30 | `nextSeqs` in `_betaDelegatedTransfer()` | `[ ]` | |
| 31 | `betaDelegateWhitelister` in `setBetaDelegateWhitelister()` | `[ ]` | |
| 32 | `betaDelegateWhitelist` in `whitelistBetaDelegate()` | `[ ]` | |
| 33 | `betaDelegateWhitelist` in `unwhitelistBetaDelegate()` | `[ ]` | |
| 34 | `feeController` in `setFeeController()` | `[ ]` | |
| 35 | `feeRecipient` in `setFeeRecipient()` | `[ ]` | |
| 36 | `feeRate` in `setFeeRate()` | `[ ]` | |
| 37 | `feeRate` in `getFeeFor()` | `[ ]` | |

**Hasil**: 37 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 3 temuan (2,850 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `name` | `[ ]` | |
| 2 | `symbol` | `[ ]` | |
| 3 | `EIP191_HEADER` | `[ ]` | |

**Hasil**: 3 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 28 temuan (74,844 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `totalSupply()` | `[ ]` | |
| 2 | `transfer()` | `[ ]` | |
| 3 | `balanceOf()` | `[ ]` | |
| 4 | `transferFrom()` | `[ ]` | |
| 5 | `approve()` | `[ ]` | |
| 6 | `allowance()` | `[ ]` | |
| 7 | `proposeOwner()` | `[ ]` | |
| 8 | `disregardProposeOwner()` | `[ ]` | |
| 9 | `claimOwnership()` | `[ ]` | |
| 10 | `unpause()` | `[ ]` | |
| 11 | `setAssetProtectionRole()` | `[ ]` | |
| 12 | `freeze()` | `[ ]` | |
| 13 | `unfreeze()` | `[ ]` | |
| 14 | `wipeFrozenAddress()` | `[ ]` | |
| 15 | `isFrozen()` | `[ ]` | |
| 16 | `setSupplyController()` | `[ ]` | |
| 17 | `increaseSupply()` | `[ ]` | |
| 18 | `decreaseSupply()` | `[ ]` | |
| 19 | `nextSeqOf()` | `[ ]` | |
| 20 | `betaDelegatedTransfer()` | `[ ]` | |
| 21 | `betaDelegatedTransferBatch()` | `[ ]` | |
| 22 | `isWhitelistedBetaDelegate()` | `[ ]` | |
| 23 | `setBetaDelegateWhitelister()` | `[ ]` | |
| 24 | `whitelistBetaDelegate()` | `[ ]` | |
| 25 | `unwhitelistBetaDelegate()` | `[ ]` | |
| 26 | `setFeeController()` | `[ ]` | |
| 27 | `setFeeRecipient()` | `[ ]` | |
| 28 | `setFeeRate()` | `[ ]` | |

**Hasil**: 28 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 37 | | | |
| String vs Bytes32 | 3 | | | |
| Public vs External | 28 | | | |

---

## [05] AdminUpgradeabilityProxy

| Field | Value |
|---|---|
| Domain | NFT |
| Complexity | Complex |
| LOC | 1515 |
| File | `012_AdminUpgradeabilityProxy_0x959e104E.sol` |
| Estimated Savings | **83,925 gas** |
| Total Findings | 45 |

### String vs Bytes32 — 18 temuan (17,100 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `contractName` | `[ ]` | |
| 2 | `migrationId` | `[ ]` | |
| 3 | `contractName` | `[ ]` | |
| 4 | `migrationId` | `[ ]` | |
| 5 | `_name` | `[ ]` | |
| 6 | `_symbol` | `[ ]` | |
| 7 | `_uri` | `[ ]` | |
| 8 | `metadata` | `[ ]` | |
| 9 | `data` | `[ ]` | |
| 10 | `metadata` | `[ ]` | |
| 11 | `metadata` | `[ ]` | |
| 12 | `_name` | `[ ]` | |
| 13 | `_symbol` | `[ ]` | |
| 14 | `data` | `[ ]` | |
| 15 | `data` | `[ ]` | |
| 16 | `metadata` | `[ ]` | |
| 17 | `metadata` | `[ ]` | |
| 18 | `data` | `[ ]` | |

**Hasil**: 18 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 25 temuan (66,825 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `approve()` | `[ ]` | |
| 2 | `setApprovalForAll()` | `[ ]` | |
| 3 | `tokenOfOwnerByIndex()` | `[ ]` | |
| 4 | `tokenByIndex()` | `[ ]` | |
| 5 | `tokenURI()` | `[ ]` | |
| 6 | `onERC721Received()` | `[ ]` | |
| 7 | `approve()` | `[ ]` | |
| 8 | `setApprovalForAll()` | `[ ]` | |
| 9 | `initialize()` | `[ ]` | |
| 10 | `initialize()` | `[ ]` | |
| 11 | `tokenURI()` | `[ ]` | |
| 12 | `tokenOfOwnerByIndex()` | `[ ]` | |
| 13 | `tokenByIndex()` | `[ ]` | |
| 14 | `initialize()` | `[ ]` | |
| 15 | `transferOwnership()` | `[ ]` | |
| 16 | `ping()` | `[ ]` | |
| 17 | `updateOperator()` | `[ ]` | |
| 18 | `setManyUpdateOperator()` | `[ ]` | |
| 19 | `setLandUpdateOperator()` | `[ ]` | |
| 20 | `setManyLandUpdateOperator()` | `[ ]` | |
| 21 | `initialize()` | `[ ]` | |
| 22 | `onERC721Received()` | `[ ]` | |
| 23 | `verifyFingerprint()` | `[ ]` | |
| 24 | `updateLandData()` | `[ ]` | |
| 25 | `updateManyLandData()` | `[ ]` | |

**Hasil**: 25 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 2 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `div()` | `[ ]` | |
| 2 | `_setTokenURI()` | `[ ]` | |

**Hasil**: 2 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| String vs Bytes32 | 18 | | | |
| Public vs External | 25 | | | |
| Dead Code | 2 | | | |

---

## [06] Parcel

| Field | Value |
|---|---|
| Domain | NFT |
| Complexity | Complex |
| LOC | 733 |
| File | `013_Parcel_0x79986af1.sol` |
| Estimated Savings | **80,054 gas** |
| Total Findings | 57 |

### Redundant SLOAD — 21 temuan (3,906 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `owner` in `transferOwnership()` | `[ ]` | |
| 2 | `owner` in `ownerOf()` | `[ ]` | |
| 3 | `owner` in `approve()` | `[ ]` | |
| 4 | `owner` in `isApprovedOrOwner()` | `[ ]` | |
| 5 | `tokenApprovals` in `clearApproval()` | `[ ]` | |
| 6 | `tokenOwner` in `addTokenTo()` | `[ ]` | |
| 7 | `ownedTokensCount` in `addTokenTo()` | `[ ]` | |
| 8 | `ownedTokensCount` in `removeTokenFrom()` | `[ ]` | |
| 9 | `ownedTokens` in `addTokenTo()` | `[ ]` | |
| 10 | `ownedTokensIndex` in `removeTokenFrom()` | `[ ]` | |
| 11 | `ownedTokens` in `removeTokenFrom()` | `[ ]` | |
| 12 | `allTokens` in `_mint()` | `[ ]` | |
| 13 | `tokenURIs` in `_burn()` | `[ ]` | |
| 14 | `allTokensIndex` in `_burn()` | `[ ]` | |
| 15 | `allTokens` in `_burn()` | `[ ]` | |
| 16 | `creator` in `takeOwnership()` | `[ ]` | |
| 17 | `owner` in `takeOwnership()` | `[ ]` | |
| 18 | `contentURIs` in `burn()` | `[ ]` | |
| 19 | `tokenOwner` in `buy()` | `[ ]` | |
| 20 | `tokenPrice` in `buy()` | `[ ]` | |
| 21 | `boundingBoxes` in `getBoundingBox()` | `[ ]` | |

**Hasil**: 21 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 7 temuan (6,650 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `name_` | `[ ]` | |
| 2 | `symbol_` | `[ ]` | |
| 3 | `_name` | `[ ]` | |
| 4 | `_symbol` | `[ ]` | |
| 5 | `_uri` | `[ ]` | |
| 6 | `inStr` | `[ ]` | |
| 7 | `_uri` | `[ ]` | |

**Hasil**: 7 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 26 temuan (69,498 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `transferOwnership()` | `[ ]` | |
| 2 | `approve()` | `[ ]` | |
| 3 | `setApprovalForAll()` | `[ ]` | |
| 4 | `tokenOfOwnerByIndex()` | `[ ]` | |
| 5 | `tokenByIndex()` | `[ ]` | |
| 6 | `name()` | `[ ]` | |
| 7 | `symbol()` | `[ ]` | |
| 8 | `tokenURI()` | `[ ]` | |
| 9 | `onERC721Received()` | `[ ]` | |
| 10 | `approve()` | `[ ]` | |
| 11 | `setApprovalForAll()` | `[ ]` | |
| 12 | `name()` | `[ ]` | |
| 13 | `symbol()` | `[ ]` | |
| 14 | `tokenURI()` | `[ ]` | |
| 15 | `tokenOfOwnerByIndex()` | `[ ]` | |
| 16 | `tokenByIndex()` | `[ ]` | |
| 17 | `takeOwnership()` | `[ ]` | |
| 18 | `mint()` | `[ ]` | |
| 19 | `tokenURI()` | `[ ]` | |
| 20 | `burn()` | `[ ]` | |
| 21 | `setPrice()` | `[ ]` | |
| 22 | `getPrice()` | `[ ]` | |
| 23 | `buy()` | `[ ]` | |
| 24 | `getBoundingBox()` | `[ ]` | |
| 25 | `setContentURI()` | `[ ]` | |
| 26 | `contentURI()` | `[ ]` | |

**Hasil**: 26 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 3 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `mul()` | `[ ]` | |
| 2 | `div()` | `[ ]` | |
| 3 | `_setTokenURI()` | `[ ]` | |

**Hasil**: 3 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 21 | | | |
| String vs Bytes32 | 7 | | | |
| Public vs External | 26 | | | |
| Dead Code | 3 | | | |

---

## [07] TetherToken

| Field | Value |
|---|---|
| Domain | Token |
| Complexity | Medium |
| LOC | 377 |
| File | `021_TetherToken_0xdAC17F95.sol` |
| Estimated Savings | **78,947 gas** |
| Total Findings | 47 |

### Redundant SLOAD — 16 temuan (2,976 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `maximumFee` in `transfer()` | `[ ]` | |
| 2 | `balances` in `transfer()` | `[ ]` | |
| 3 | `owner` in `transfer()` | `[ ]` | |
| 4 | `allowed` in `transferFrom()` | `[ ]` | |
| 5 | `maximumFee` in `transferFrom()` | `[ ]` | |
| 6 | `balances` in `transferFrom()` | `[ ]` | |
| 7 | `owner` in `transferFrom()` | `[ ]` | |
| 8 | `allowed` in `approve()` | `[ ]` | |
| 9 | `_totalSupply` in `issue()` | `[ ]` | |
| 10 | `balances` in `issue()` | `[ ]` | |
| 11 | `owner` in `issue()` | `[ ]` | |
| 12 | `_totalSupply` in `redeem()` | `[ ]` | |
| 13 | `balances` in `redeem()` | `[ ]` | |
| 14 | `owner` in `redeem()` | `[ ]` | |
| 15 | `basisPointsRate` in `setParams()` | `[ ]` | |
| 16 | `maximumFee` in `setParams()` | `[ ]` | |

**Hasil**: 16 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 4 temuan (3,800 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `name` | `[ ]` | |
| 2 | `symbol` | `[ ]` | |
| 3 | `_name` | `[ ]` | |
| 4 | `_symbol` | `[ ]` | |

**Hasil**: 4 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 27 temuan (72,171 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `transferOwnership()` | `[ ]` | |
| 2 | `totalSupply()` | `[ ]` | |
| 3 | `transfer()` | `[ ]` | |
| 4 | `allowance()` | `[ ]` | |
| 5 | `transferFrom()` | `[ ]` | |
| 6 | `approve()` | `[ ]` | |
| 7 | `transfer()` | `[ ]` | |
| 8 | `transferFrom()` | `[ ]` | |
| 9 | `approve()` | `[ ]` | |
| 10 | `allowance()` | `[ ]` | |
| 11 | `pause()` | `[ ]` | |
| 12 | `unpause()` | `[ ]` | |
| 13 | `addBlackList()` | `[ ]` | |
| 14 | `removeBlackList()` | `[ ]` | |
| 15 | `destroyBlackFunds()` | `[ ]` | |
| 16 | `transferByLegacy()` | `[ ]` | |
| 17 | `transferFromByLegacy()` | `[ ]` | |
| 18 | `approveByLegacy()` | `[ ]` | |
| 19 | `transfer()` | `[ ]` | |
| 20 | `transferFrom()` | `[ ]` | |
| 21 | `approve()` | `[ ]` | |
| 22 | `allowance()` | `[ ]` | |
| 23 | `deprecate()` | `[ ]` | |
| 24 | `totalSupply()` | `[ ]` | |
| 25 | `issue()` | `[ ]` | |
| 26 | `redeem()` | `[ ]` | |
| 27 | `setParams()` | `[ ]` | |

**Hasil**: 27 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 16 | | | |
| String vs Bytes32 | 4 | | | |
| Public vs External | 27 | | | |

---

## [08] AdminUpgradeabilityProxy

| Field | Value |
|---|---|
| Domain | Token |
| Complexity | Complex |
| LOC | 581 |
| File | `025_AdminUpgradeabilityProxy_0x4fabb145.sol` |
| Estimated Savings | **75,813 gas** |
| Total Findings | 61 |

### Redundant SLOAD — 33 temuan (6,138 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `initialized` in `initialize()` | `[ ]` | |
| 2 | `frozen` in `transfer()` | `[ ]` | |
| 3 | `balances` in `transfer()` | `[ ]` | |
| 4 | `frozen` in `transferFrom()` | `[ ]` | |
| 5 | `balances` in `transferFrom()` | `[ ]` | |
| 6 | `allowed` in `transferFrom()` | `[ ]` | |
| 7 | `frozen` in `approve()` | `[ ]` | |
| 8 | `proposedOwner` in `proposeOwner()` | `[ ]` | |
| 9 | `proposedOwner` in `disregardProposeOwner()` | `[ ]` | |
| 10 | `proposedOwner` in `claimOwnership()` | `[ ]` | |
| 11 | `owner` in `claimOwnership()` | `[ ]` | |
| 12 | `balances` in `reclaimBUSD()` | `[ ]` | |
| 13 | `owner` in `reclaimBUSD()` | `[ ]` | |
| 14 | `paused` in `pause()` | `[ ]` | |
| 15 | `paused` in `unpause()` | `[ ]` | |
| 16 | `assetProtectionRole` in `setAssetProtectionRole()` | `[ ]` | |
| 17 | `frozen` in `freeze()` | `[ ]` | |
| 18 | `frozen` in `unfreeze()` | `[ ]` | |
| 19 | `balances` in `wipeFrozenAddress()` | `[ ]` | |
| 20 | `totalSupply_` in `wipeFrozenAddress()` | `[ ]` | |
| 21 | `supplyController` in `setSupplyController()` | `[ ]` | |
| 22 | `totalSupply_` in `increaseSupply()` | `[ ]` | |
| 23 | `balances` in `increaseSupply()` | `[ ]` | |
| 24 | `supplyController` in `increaseSupply()` | `[ ]` | |
| 25 | `balances` in `decreaseSupply()` | `[ ]` | |
| 26 | `supplyController` in `decreaseSupply()` | `[ ]` | |
| 27 | `totalSupply_` in `decreaseSupply()` | `[ ]` | |
| 28 | `frozen` in `_betaDelegatedTransfer()` | `[ ]` | |
| 29 | `balances` in `_betaDelegatedTransfer()` | `[ ]` | |
| 30 | `nextSeqs` in `_betaDelegatedTransfer()` | `[ ]` | |
| 31 | `betaDelegateWhitelister` in `setBetaDelegateWhitelister()` | `[ ]` | |
| 32 | `betaDelegateWhitelist` in `whitelistBetaDelegate()` | `[ ]` | |
| 33 | `betaDelegateWhitelist` in `unwhitelistBetaDelegate()` | `[ ]` | |

**Hasil**: 33 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 3 temuan (2,850 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `name` | `[ ]` | |
| 2 | `symbol` | `[ ]` | |
| 3 | `EIP191_HEADER` | `[ ]` | |

**Hasil**: 3 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 25 temuan (66,825 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `totalSupply()` | `[ ]` | |
| 2 | `transfer()` | `[ ]` | |
| 3 | `balanceOf()` | `[ ]` | |
| 4 | `transferFrom()` | `[ ]` | |
| 5 | `approve()` | `[ ]` | |
| 6 | `allowance()` | `[ ]` | |
| 7 | `proposeOwner()` | `[ ]` | |
| 8 | `disregardProposeOwner()` | `[ ]` | |
| 9 | `claimOwnership()` | `[ ]` | |
| 10 | `unpause()` | `[ ]` | |
| 11 | `setAssetProtectionRole()` | `[ ]` | |
| 12 | `freeze()` | `[ ]` | |
| 13 | `unfreeze()` | `[ ]` | |
| 14 | `wipeFrozenAddress()` | `[ ]` | |
| 15 | `isFrozen()` | `[ ]` | |
| 16 | `setSupplyController()` | `[ ]` | |
| 17 | `increaseSupply()` | `[ ]` | |
| 18 | `decreaseSupply()` | `[ ]` | |
| 19 | `nextSeqOf()` | `[ ]` | |
| 20 | `betaDelegatedTransfer()` | `[ ]` | |
| 21 | `betaDelegatedTransferBatch()` | `[ ]` | |
| 22 | `isWhitelistedBetaDelegate()` | `[ ]` | |
| 23 | `setBetaDelegateWhitelister()` | `[ ]` | |
| 24 | `whitelistBetaDelegate()` | `[ ]` | |
| 25 | `unwhitelistBetaDelegate()` | `[ ]` | |

**Hasil**: 25 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 33 | | | |
| String vs Bytes32 | 3 | | | |
| Public vs External | 25 | | | |

---

## [09] WrappedPunk

| Field | Value |
|---|---|
| Domain | NFT |
| Complexity | Complex |
| LOC | 1376 |
| File | `014_WrappedPunk_0xb7F7F6C5.sol` |
| Estimated Savings | **70,910 gas** |
| Total Findings | 54 |

### Redundant SLOAD — 14 temuan (2,604 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_owner` in `renounceOwnership()` | `[ ]` | |
| 2 | `_owner` in `transferOwnership()` | `[ ]` | |
| 3 | `_ownedTokensCount` in `_transferFrom()` | `[ ]` | |
| 4 | `_tokenApprovals` in `_clearApproval()` | `[ ]` | |
| 5 | `_ownedTokens` in `_addTokenToOwnerEnumeration()` | `[ ]` | |
| 6 | `_allTokens` in `_addTokenToAllTokensEnumeration()` | `[ ]` | |
| 7 | `_ownedTokens` in `_removeTokenFromOwnerEnumeration()` | `[ ]` | |
| 8 | `_ownedTokensIndex` in `_removeTokenFromOwnerEnumeration()` | `[ ]` | |
| 9 | `_allTokens` in `_removeTokenFromAllTokensEnumeration()` | `[ ]` | |
| 10 | `_allTokensIndex` in `_removeTokenFromAllTokensEnumeration()` | `[ ]` | |
| 11 | `_baseURI` in `tokenURI()` | `[ ]` | |
| 12 | `_tokenURIs` in `_burn()` | `[ ]` | |
| 13 | `_owner` in `transfer()` | `[ ]` | |
| 14 | `_proxies` in `registerProxy()` | `[ ]` | |

**Hasil**: 14 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 10 temuan (9,500 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_name` | `[ ]` | |
| 2 | `_symbol` | `[ ]` | |
| 3 | `_baseURI` | `[ ]` | |
| 4 | `name` | `[ ]` | |
| 5 | `symbol` | `[ ]` | |
| 6 | `_tokenURI` | `[ ]` | |
| 7 | `baseURI` | `[ ]` | |
| 8 | `name` | `[ ]` | |
| 9 | `symbol` | `[ ]` | |
| 10 | `baseUri` | `[ ]` | |

**Hasil**: 10 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 22 temuan (58,806 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `owner()` | `[ ]` | |
| 2 | `renounceOwnership()` | `[ ]` | |
| 3 | `transferOwnership()` | `[ ]` | |
| 4 | `paused()` | `[ ]` | |
| 5 | `supportsInterface()` | `[ ]` | |
| 6 | `approve()` | `[ ]` | |
| 7 | `setApprovalForAll()` | `[ ]` | |
| 8 | `transferFrom()` | `[ ]` | |
| 9 | `tokenOfOwnerByIndex()` | `[ ]` | |
| 10 | `tokenByIndex()` | `[ ]` | |
| 11 | `name()` | `[ ]` | |
| 12 | `symbol()` | `[ ]` | |
| 13 | `tokenURI()` | `[ ]` | |
| 14 | `baseURI()` | `[ ]` | |
| 15 | `punkContract()` | `[ ]` | |
| 16 | `setBaseURI()` | `[ ]` | |
| 17 | `pause()` | `[ ]` | |
| 18 | `unpause()` | `[ ]` | |
| 19 | `registerProxy()` | `[ ]` | |
| 20 | `proxyInfo()` | `[ ]` | |
| 21 | `mint()` | `[ ]` | |
| 22 | `burn()` | `[ ]` | |

**Hasil**: 22 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 8 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_msgData()` | `[ ]` | |
| 2 | `add()` | `[ ]` | |
| 3 | `mul()` | `[ ]` | |
| 4 | `div()` | `[ ]` | |
| 5 | `mod()` | `[ ]` | |
| 6 | `toPayable()` | `[ ]` | |
| 7 | `_tokensOfOwner()` | `[ ]` | |
| 8 | `_setTokenURI()` | `[ ]` | |

**Hasil**: 8 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 14 | | | |
| String vs Bytes32 | 10 | | | |
| Public vs External | 22 | | | |
| Dead Code | 8 | | | |

---

## [10] SuperRareV2

| Field | Value |
|---|---|
| Domain | NFT |
| Complexity | Complex |
| LOC | 999 |
| File | `016_SuperRareV2_0xb932a70A.sol` |
| Estimated Savings | **67,836 gas** |
| Total Findings | 51 |

### Redundant SLOAD — 16 temuan (2,976 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_tokenOwner` in `_addTokenTo()` | `[ ]` | |
| 2 | `_ownedTokensCount` in `_addTokenTo()` | `[ ]` | |
| 3 | `_ownedTokensCount` in `_removeTokenFrom()` | `[ ]` | |
| 4 | `_tokenApprovals` in `_clearApproval()` | `[ ]` | |
| 5 | `_ownedTokens` in `_addTokenTo()` | `[ ]` | |
| 6 | `_ownedTokensIndex` in `_removeTokenFrom()` | `[ ]` | |
| 7 | `_ownedTokens` in `_removeTokenFrom()` | `[ ]` | |
| 8 | `_allTokens` in `_mint()` | `[ ]` | |
| 9 | `_allTokensIndex` in `_burn()` | `[ ]` | |
| 10 | `_allTokens` in `_burn()` | `[ ]` | |
| 11 | `_tokenURIs` in `_burn()` | `[ ]` | |
| 12 | Redundant SLOAD: '_owner' dibaca 2x di fungsi ''.  | `[ ]` | |
| 13 | `_owner` in `renounceOwnership()` | `[ ]` | |
| 14 | `_owner` in `_transferOwnership()` | `[ ]` | |
| 15 | Redundant SLOAD: 'oldSuperRare' dibaca 2x di fungs | `[ ]` | |
| 16 | `idCounter` in `_createToken()` | `[ ]` | |

**Hasil**: 16 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 12 temuan (11,400 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_name` | `[ ]` | |
| 2 | `_symbol` | `[ ]` | |
| 3 | `name` | `[ ]` | |
| 4 | `symbol` | `[ ]` | |
| 5 | `uri` | `[ ]` | |
| 6 | `name` | `[ ]` | |
| 7 | `symbol` | `[ ]` | |
| 8 | `_name` | `[ ]` | |
| 9 | `_symbol` | `[ ]` | |
| 10 | `_uri` | `[ ]` | |
| 11 | `_uri` | `[ ]` | |
| 12 | `_uri` | `[ ]` | |

**Hasil**: 12 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 20 temuan (53,460 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `creatorOfToken()` | `[ ]` | |
| 2 | `onERC721Received()` | `[ ]` | |
| 3 | `approve()` | `[ ]` | |
| 4 | `setApprovalForAll()` | `[ ]` | |
| 5 | `tokenOfOwnerByIndex()` | `[ ]` | |
| 6 | `tokenByIndex()` | `[ ]` | |
| 7 | `approve()` | `[ ]` | |
| 8 | `setApprovalForAll()` | `[ ]` | |
| 9 | `tokenOfOwnerByIndex()` | `[ ]` | |
| 10 | `tokenByIndex()` | `[ ]` | |
| 11 | `owner()` | `[ ]` | |
| 12 | `renounceOwnership()` | `[ ]` | |
| 13 | `transferOwnership()` | `[ ]` | |
| 14 | `enableWhitelist()` | `[ ]` | |
| 15 | `addToWhitelist()` | `[ ]` | |
| 16 | `removeFromWhitelist()` | `[ ]` | |
| 17 | `initWhitelist()` | `[ ]` | |
| 18 | `addNewToken()` | `[ ]` | |
| 19 | `deleteToken()` | `[ ]` | |
| 20 | `updateTokenMetadata()` | `[ ]` | |

**Hasil**: 20 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 3 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `mul()` | `[ ]` | |
| 2 | `div()` | `[ ]` | |
| 3 | `mod()` | `[ ]` | |

**Hasil**: 3 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 16 | | | |
| String vs Bytes32 | 12 | | | |
| Public vs External | 20 | | | |
| Dead Code | 3 | | | |

---

## [11] BalancerGovernanceToken

| Field | Value |
|---|---|
| Domain | Token |
| Complexity | Complex |
| LOC | 1280 |
| File | `Token_07_BalancerGovernanceToken.sol` |
| Estimated Savings | **59,326 gas** |
| Total Findings | 41 |

### Redundant SLOAD — 6 temuan (1,116 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_balances` in `_transfer()` | `[ ]` | |
| 2 | `_totalSupply` in `_mint()` | `[ ]` | |
| 3 | `_balances` in `_mint()` | `[ ]` | |
| 4 | `_balances` in `_burn()` | `[ ]` | |
| 5 | `_totalSupply` in `_burn()` | `[ ]` | |
| 6 | `_currentSnapshotId` in `_snapshot()` | `[ ]` | |

**Hasil**: 6 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 5 temuan (4,750 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_name` | `[ ]` | |
| 2 | `_symbol` | `[ ]` | |
| 3 | `version` | `[ ]` | |
| 4 | `name` | `[ ]` | |
| 5 | `symbol` | `[ ]` | |

**Hasil**: 5 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 20 temuan (53,460 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `getRoleMemberCount()` | `[ ]` | |
| 2 | `getRoleMember()` | `[ ]` | |
| 3 | `getRoleAdmin()` | `[ ]` | |
| 4 | `grantRole()` | `[ ]` | |
| 5 | `revokeRole()` | `[ ]` | |
| 6 | `renounceRole()` | `[ ]` | |
| 7 | `name()` | `[ ]` | |
| 8 | `symbol()` | `[ ]` | |
| 9 | `decimals()` | `[ ]` | |
| 10 | `transfer()` | `[ ]` | |
| 11 | `approve()` | `[ ]` | |
| 12 | `transferFrom()` | `[ ]` | |
| 13 | `increaseAllowance()` | `[ ]` | |
| 14 | `decreaseAllowance()` | `[ ]` | |
| 15 | `balanceOfAt()` | `[ ]` | |
| 16 | `totalSupplyAt()` | `[ ]` | |
| 17 | `mint()` | `[ ]` | |
| 18 | `burn()` | `[ ]` | |
| 19 | `burnFrom()` | `[ ]` | |
| 20 | `snapshot()` | `[ ]` | |

**Hasil**: 20 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 10 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `isContract()` | `[ ]` | |
| 2 | `sendValue()` | `[ ]` | |
| 3 | `_msgData()` | `[ ]` | |
| 4 | `_setRoleAdmin()` | `[ ]` | |
| 5 | `mul()` | `[ ]` | |
| 6 | `max()` | `[ ]` | |
| 7 | `min()` | `[ ]` | |
| 8 | `decrement()` | `[ ]` | |
| 9 | `_setupDecimals()` | `[ ]` | |
| 10 | `_valueAt()` | `[ ]` | |

**Hasil**: 10 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 6 | | | |
| String vs Bytes32 | 5 | | | |
| Public vs External | 20 | | | |
| Dead Code | 10 | | | |

---

## [12] WyvernProxyRegistry

| Field | Value |
|---|---|
| Domain | Utility |
| Complexity | Medium |
| LOC | 383 |
| File | `050_WyvernProxyRegistry_0xa5409ec9.sol` |
| Estimated Savings | **58,757 gas** |
| Total Findings | 31 |

### Redundant SLOAD — 9 temuan (1,674 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `owner` in `transferOwnership()` | `[ ]` | |
| 2 | `owner` in `renounceOwnership()` | `[ ]` | |
| 3 | `pending` in `startGrantAuthentication()` | `[ ]` | |
| 4 | `contracts` in `endGrantAuthentication()` | `[ ]` | |
| 5 | `pending` in `endGrantAuthentication()` | `[ ]` | |
| 6 | `proxies` in `registerProxy()` | `[ ]` | |
| 7 | `initialAddressSet` in `grantInitialAuthentication()` | `[ ]` | |
| 8 | `initialized` in `initialize()` | `[ ]` | |
| 9 | `_implementation` in `_upgradeTo()` | `[ ]` | |

**Hasil**: 9 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 1 temuan (950 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `name` | `[ ]` | |

**Hasil**: 1 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 21 temuan (56,133 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `transferOwnership()` | `[ ]` | |
| 2 | `renounceOwnership()` | `[ ]` | |
| 3 | `totalSupply()` | `[ ]` | |
| 4 | `balanceOf()` | `[ ]` | |
| 5 | `transfer()` | `[ ]` | |
| 6 | `allowance()` | `[ ]` | |
| 7 | `transferFrom()` | `[ ]` | |
| 8 | `approve()` | `[ ]` | |
| 9 | `receiveApproval()` | `[ ]` | |
| 10 | `startGrantAuthentication()` | `[ ]` | |
| 11 | `endGrantAuthentication()` | `[ ]` | |
| 12 | `revokeAuthentication()` | `[ ]` | |
| 13 | `registerProxy()` | `[ ]` | |
| 14 | `grantInitialAuthentication()` | `[ ]` | |
| 15 | `proxyType()` | `[ ]` | |
| 16 | `initialize()` | `[ ]` | |
| 17 | `setRevoke()` | `[ ]` | |
| 18 | `proxyAssert()` | `[ ]` | |
| 19 | `proxyType()` | `[ ]` | |
| 20 | `transferProxyOwnership()` | `[ ]` | |
| 21 | `upgradeToAndCall()` | `[ ]` | |

**Hasil**: 21 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 9 | | | |
| String vs Bytes32 | 1 | | | |
| Public vs External | 21 | | | |

---

## [13] DSToken

| Field | Value |
|---|---|
| Domain | Governance |
| Complexity | Medium |
| LOC | 371 |
| File | `036_DSToken_0x9f8F72aA.sol` |
| Estimated Savings | **58,737 gas** |
| Total Findings | 43 |

### Redundant SLOAD — 14 temuan (2,604 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `owner` in `setOwner()` | `[ ]` | |
| 2 | `authority` in `setAuthority()` | `[ ]` | |
| 3 | `authority` in `isAuthorized()` | `[ ]` | |
| 4 | `WAD` in `wmul()` | `[ ]` | |
| 5 | `RAY` in `rmul()` | `[ ]` | |
| 6 | `_approvals` in `transferFrom()` | `[ ]` | |
| 7 | `_balances` in `transferFrom()` | `[ ]` | |
| 8 | `_approvals` in `transferFrom()` | `[ ]` | |
| 9 | `_balances` in `transferFrom()` | `[ ]` | |
| 10 | `_balances` in `mint()` | `[ ]` | |
| 11 | `_supply` in `mint()` | `[ ]` | |
| 12 | `_approvals` in `burn()` | `[ ]` | |
| 13 | `_balances` in `burn()` | `[ ]` | |
| 14 | `_supply` in `burn()` | `[ ]` | |

**Hasil**: 14 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 21 temuan (56,133 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `canCall()` | `[ ]` | |
| 2 | `setOwner()` | `[ ]` | |
| 3 | `setAuthority()` | `[ ]` | |
| 4 | `stop()` | `[ ]` | |
| 5 | `start()` | `[ ]` | |
| 6 | `totalSupply()` | `[ ]` | |
| 7 | `balanceOf()` | `[ ]` | |
| 8 | `allowance()` | `[ ]` | |
| 9 | `transfer()` | `[ ]` | |
| 10 | `approve()` | `[ ]` | |
| 11 | `totalSupply()` | `[ ]` | |
| 12 | `balanceOf()` | `[ ]` | |
| 13 | `allowance()` | `[ ]` | |
| 14 | `transfer()` | `[ ]` | |
| 15 | `approve()` | `[ ]` | |
| 16 | `approve()` | `[ ]` | |
| 17 | `approve()` | `[ ]` | |
| 18 | `push()` | `[ ]` | |
| 19 | `pull()` | `[ ]` | |
| 20 | `move()` | `[ ]` | |
| 21 | `setName()` | `[ ]` | |

**Hasil**: 21 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 8 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `min()` | `[ ]` | |
| 2 | `max()` | `[ ]` | |
| 3 | `imin()` | `[ ]` | |
| 4 | `imax()` | `[ ]` | |
| 5 | `wmul()` | `[ ]` | |
| 6 | `wdiv()` | `[ ]` | |
| 7 | `rdiv()` | `[ ]` | |
| 8 | `rpow()` | `[ ]` | |

**Hasil**: 8 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 14 | | | |
| Public vs External | 21 | | | |
| Dead Code | 8 | | | |

---

## [14] AvastarTeleporter

| Field | Value |
|---|---|
| Domain | NFT |
| Complexity | Complex |
| LOC | 2171 |
| File | `020_AvastarTeleporter_0xf3e778f8.sol` |
| Estimated Savings | **54,335 gas** |
| Total Findings | 74 |

### Redundant SLOAD — 37 temuan (6,882 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `minters` in `addMinter()` | `[ ]` | |
| 2 | `owners` in `addOwner()` | `[ ]` | |
| 3 | `admins` in `addSysAdmin()` | `[ ]` | |
| 4 | `admins` in `stripRoles()` | `[ ]` | |
| 5 | `minters` in `stripRoles()` | `[ ]` | |
| 6 | `owners` in `stripRoles()` | `[ ]` | |
| 7 | `_ownedTokensCount` in `_transferFrom()` | `[ ]` | |
| 8 | `_tokenApprovals` in `_clearApproval()` | `[ ]` | |
| 9 | `_ownedTokens` in `_addTokenToOwnerEnumeration()` | `[ ]` | |
| 10 | `_allTokens` in `_addTokenToAllTokensEnumeration()` | `[ ]` | |
| 11 | `_ownedTokens` in `_removeTokenFromOwnerEnumeration()` | `[ ]` | |
| 12 | `_ownedTokensIndex` in `_removeTokenFromOwnerEnumeration()` | `[ ]` | |
| 13 | `_allTokens` in `_removeTokenFromAllTokensEnumeration()` | `[ ]` | |
| 14 | `_allTokensIndex` in `_removeTokenFromAllTokensEnumeration()` | `[ ]` | |
| 15 | `_tokenURIs` in `_burn()` | `[ ]` | |
| 16 | `traits` in `getTraitInfoById()` | `[ ]` | |
| 17 | `traits` in `getTraitNameById()` | `[ ]` | |
| 18 | `traits` in `getTraitArtById()` | `[ ]` | |
| 19 | `_name` in `createTrait()` | `[ ]` | |
| 20 | `traits` in `createTrait()` | `[ ]` | |
| 21 | `traits` in `extendTraitArt()` | `[ ]` | |
| 22 | `tokenIdByGenerationWaveAndSerial` in `mintAvastar()` | `[ ]` | |
| 23 | `avastars` in `mintAvastar()` | `[ ]` | |
| 24 | `avastars` in `getAvastarWaveByTokenId()` | `[ ]` | |
| 25 | `avastars` in `renderAvastar()` | `[ ]` | |
| 26 | `primesByGeneration` in `getPrimeByGenerationAndSerial()` | `[ ]` | |
| 27 | `avastars` in `getPrimeByTokenId()` | `[ ]` | |
| 28 | `avastars` in `getPrimeReplicationByTokenId()` | `[ ]` | |
| 29 | `primeCountByGenAndSeries` in `mintPrime()` | `[ ]` | |
| 30 | `primesByGeneration` in `mintPrime()` | `[ ]` | |
| 31 | `replicantsByGeneration` in `getReplicantByGenerationAndSerial()` | `[ ]` | |
| 32 | `avastars` in `getReplicantByTokenId()` | `[ ]` | |
| 33 | `replicantCountByGeneration` in `mintReplicant()` | `[ ]` | |
| 34 | `replicantsByGeneration` in `mintReplicant()` | `[ ]` | |
| 35 | `traitHandlerByPrimeTokenId` in `approveTraitAccess()` | `[ ]` | |
| 36 | `avastars` in `useTraits()` | `[ ]` | |
| 37 | `traitHandlerByPrimeTokenId` in `useTraits()` | `[ ]` | |

**Hasil**: 37 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 19 temuan (18,050 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_name` | `[ ]` | |
| 2 | `_symbol` | `[ ]` | |
| 3 | `TOKEN_NAME` | `[ ]` | |
| 4 | `TOKEN_SYMBOL` | `[ ]` | |
| 5 | `_a` | `[ ]` | |
| 6 | `_b` | `[ ]` | |
| 7 | `errorMessage` | `[ ]` | |
| 8 | `errorMessage` | `[ ]` | |
| 9 | `errorMessage` | `[ ]` | |
| 10 | `name` | `[ ]` | |
| 11 | `symbol` | `[ ]` | |
| 12 | `uri` | `[ ]` | |
| 13 | `name` | `[ ]` | |
| 14 | `symbol` | `[ ]` | |
| 15 | `_artist` | `[ ]` | |
| 16 | `_infoURI` | `[ ]` | |
| 17 | `_name` | `[ ]` | |
| 18 | `_svg` | `[ ]` | |
| 19 | `_svg` | `[ ]` | |

**Hasil**: 19 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 11 temuan (29,403 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `transferFrom()` | `[ ]` | |
| 2 | `approve()` | `[ ]` | |
| 3 | `setApprovalForAll()` | `[ ]` | |
| 4 | `onERC721Received()` | `[ ]` | |
| 5 | `approve()` | `[ ]` | |
| 6 | `setApprovalForAll()` | `[ ]` | |
| 7 | `transferFrom()` | `[ ]` | |
| 8 | `tokenOfOwnerByIndex()` | `[ ]` | |
| 9 | `tokenByIndex()` | `[ ]` | |
| 10 | `tokenOfOwnerByIndex()` | `[ ]` | |
| 11 | `tokenByIndex()` | `[ ]` | |

**Hasil**: 11 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 7 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `uintToStr()` | `[ ]` | |
| 2 | `mul()` | `[ ]` | |
| 3 | `_msgData()` | `[ ]` | |
| 4 | `toPayable()` | `[ ]` | |
| 5 | `sendValue()` | `[ ]` | |
| 6 | `_tokensOfOwner()` | `[ ]` | |
| 7 | `_setTokenURI()` | `[ ]` | |

**Hasil**: 7 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 37 | | | |
| String vs Bytes32 | 19 | | | |
| Public vs External | 11 | | | |
| Dead Code | 7 | | | |

---

## [15] MANAToken

| Field | Value |
|---|---|
| Domain | Token |
| Complexity | Medium |
| LOC | 222 |
| File | `029_MANAToken_0x0F5D2fB2.sol` |
| Estimated Savings | **54,175 gas** |
| Total Findings | 31 |

### Redundant SLOAD — 8 temuan (1,488 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `balances` in `transfer()` | `[ ]` | |
| 2 | `allowed` in `transferFrom()` | `[ ]` | |
| 3 | `balances` in `transferFrom()` | `[ ]` | |
| 4 | `allowed` in `approve()` | `[ ]` | |
| 5 | `totalSupply` in `mint()` | `[ ]` | |
| 6 | `balances` in `mint()` | `[ ]` | |
| 7 | `balances` in `burn()` | `[ ]` | |
| 8 | `totalSupply` in `burn()` | `[ ]` | |

**Hasil**: 8 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 2 temuan (1,900 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `symbol` | `[ ]` | |
| 2 | `name` | `[ ]` | |

**Hasil**: 2 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 19 temuan (50,787 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `balanceOf()` | `[ ]` | |
| 2 | `transfer()` | `[ ]` | |
| 3 | `transferOwnership()` | `[ ]` | |
| 4 | `pause()` | `[ ]` | |
| 5 | `unpause()` | `[ ]` | |
| 6 | `allowance()` | `[ ]` | |
| 7 | `transferFrom()` | `[ ]` | |
| 8 | `approve()` | `[ ]` | |
| 9 | `transfer()` | `[ ]` | |
| 10 | `balanceOf()` | `[ ]` | |
| 11 | `transferFrom()` | `[ ]` | |
| 12 | `approve()` | `[ ]` | |
| 13 | `allowance()` | `[ ]` | |
| 14 | `mint()` | `[ ]` | |
| 15 | `finishMinting()` | `[ ]` | |
| 16 | `transfer()` | `[ ]` | |
| 17 | `transferFrom()` | `[ ]` | |
| 18 | `burn()` | `[ ]` | |
| 19 | `burn()` | `[ ]` | |

**Hasil**: 19 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 2 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `mul()` | `[ ]` | |
| 2 | `div()` | `[ ]` | |

**Hasil**: 2 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 8 | | | |
| String vs Bytes32 | 2 | | | |
| Public vs External | 19 | | | |
| Dead Code | 2 | | | |

---

## [16] LinkToken

| Field | Value |
|---|---|
| Domain | Token |
| Complexity | Medium |
| LOC | 250 |
| File | `028_LinkToken_0x51491077.sol` |
| Estimated Savings | **53,617 gas** |
| Total Findings | 28 |

### Redundant SLOAD — 5 temuan (930 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `balances` in `transfer()` | `[ ]` | |
| 2 | `allowed` in `transferFrom()` | `[ ]` | |
| 3 | `balances` in `transferFrom()` | `[ ]` | |
| 4 | `allowed` in `increaseApproval()` | `[ ]` | |
| 5 | `allowed` in `decreaseApproval()` | `[ ]` | |

**Hasil**: 5 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 2 temuan (1,900 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `name` | `[ ]` | |
| 2 | `symbol` | `[ ]` | |

**Hasil**: 2 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 19 temuan (50,787 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `balanceOf()` | `[ ]` | |
| 2 | `transfer()` | `[ ]` | |
| 3 | `allowance()` | `[ ]` | |
| 4 | `transferFrom()` | `[ ]` | |
| 5 | `approve()` | `[ ]` | |
| 6 | `transferAndCall()` | `[ ]` | |
| 7 | `onTokenTransfer()` | `[ ]` | |
| 8 | `transfer()` | `[ ]` | |
| 9 | `balanceOf()` | `[ ]` | |
| 10 | `transferFrom()` | `[ ]` | |
| 11 | `approve()` | `[ ]` | |
| 12 | `allowance()` | `[ ]` | |
| 13 | `increaseApproval()` | `[ ]` | |
| 14 | `decreaseApproval()` | `[ ]` | |
| 15 | `transferAndCall()` | `[ ]` | |
| 16 | `transferAndCall()` | `[ ]` | |
| 17 | `transfer()` | `[ ]` | |
| 18 | `approve()` | `[ ]` | |
| 19 | `transferFrom()` | `[ ]` | |

**Hasil**: 19 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 2 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `mul()` | `[ ]` | |
| 2 | `div()` | `[ ]` | |

**Hasil**: 2 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 5 | | | |
| String vs Bytes32 | 2 | | | |
| Public vs External | 19 | | | |
| Dead Code | 2 | | | |

---

## [17] Token

| Field | Value |
|---|---|
| Domain | Governance |
| Complexity | Complex |
| LOC | 528 |
| File | `035_Token_0x0f51bb10.sol` |
| Estimated Savings | **53,579 gas** |
| Total Findings | 35 |

### Redundant SLOAD — 8 temuan (1,488 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_balances` in `_transfer()` | `[ ]` | |
| 2 | `_totalSupply` in `_mint()` | `[ ]` | |
| 3 | `_balances` in `_mint()` | `[ ]` | |
| 4 | `_totalSupply` in `_burn()` | `[ ]` | |
| 5 | `_balances` in `_burn()` | `[ ]` | |
| 6 | Redundant SLOAD: '_owner' dibaca 2x di fungsi ''.  | `[ ]` | |
| 7 | `_owner` in `renounceOwnership()` | `[ ]` | |
| 8 | `_owner` in `_transferOwnership()` | `[ ]` | |

**Hasil**: 8 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 7 temuan (6,650 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_name` | `[ ]` | |
| 2 | `_symbol` | `[ ]` | |
| 3 | `_name` | `[ ]` | |
| 4 | `_symbol` | `[ ]` | |
| 5 | `name` | `[ ]` | |
| 6 | `symbol` | `[ ]` | |
| 7 | `name` | `[ ]` | |

**Hasil**: 7 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 17 temuan (45,441 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `totalSupply()` | `[ ]` | |
| 2 | `balanceOf()` | `[ ]` | |
| 3 | `transfer()` | `[ ]` | |
| 4 | `allowance()` | `[ ]` | |
| 5 | `approve()` | `[ ]` | |
| 6 | `transferFrom()` | `[ ]` | |
| 7 | `increaseAllowance()` | `[ ]` | |
| 8 | `decreaseAllowance()` | `[ ]` | |
| 9 | `name()` | `[ ]` | |
| 10 | `symbol()` | `[ ]` | |
| 11 | `burn()` | `[ ]` | |
| 12 | `burnFrom()` | `[ ]` | |
| 13 | `owner()` | `[ ]` | |
| 14 | `renounceOwnership()` | `[ ]` | |
| 15 | `transferOwnership()` | `[ ]` | |
| 16 | `changeName()` | `[ ]` | |
| 17 | `name()` | `[ ]` | |

**Hasil**: 17 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 3 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `mul()` | `[ ]` | |
| 2 | `div()` | `[ ]` | |
| 3 | `mod()` | `[ ]` | |

**Hasil**: 3 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 8 | | | |
| String vs Bytes32 | 7 | | | |
| Public vs External | 17 | | | |
| Dead Code | 3 | | | |

---

## [18] YFI

| Field | Value |
|---|---|
| Domain | Governance |
| Complexity | Medium |
| LOC | 191 |
| File | `037_YFI_0x0bc529c0.sol` |
| Estimated Savings | **46,911 gas** |
| Total Findings | 32 |

### Redundant SLOAD — 6 temuan (1,116 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_balances` in `_transfer()` | `[ ]` | |
| 2 | `_totalSupply` in `_mint()` | `[ ]` | |
| 3 | `_balances` in `_mint()` | `[ ]` | |
| 4 | `_balances` in `_burn()` | `[ ]` | |
| 5 | `_totalSupply` in `_burn()` | `[ ]` | |
| 6 | `governance` in `setGovernance()` | `[ ]` | |

**Hasil**: 6 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### String vs Bytes32 — 6 temuan (5,700 gas potensial)

> **Cara audit**: Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_name` | `[ ]` | |
| 2 | `_symbol` | `[ ]` | |
| 3 | `name` | `[ ]` | |
| 4 | `symbol` | `[ ]` | |
| 5 | `errorMessage` | `[ ]` | |
| 6 | `errorMessage` | `[ ]` | |

**Hasil**: 6 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 15 temuan (40,095 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `totalSupply()` | `[ ]` | |
| 2 | `balanceOf()` | `[ ]` | |
| 3 | `transfer()` | `[ ]` | |
| 4 | `allowance()` | `[ ]` | |
| 5 | `approve()` | `[ ]` | |
| 6 | `transferFrom()` | `[ ]` | |
| 7 | `increaseAllowance()` | `[ ]` | |
| 8 | `decreaseAllowance()` | `[ ]` | |
| 9 | `name()` | `[ ]` | |
| 10 | `symbol()` | `[ ]` | |
| 11 | `decimals()` | `[ ]` | |
| 12 | `mint()` | `[ ]` | |
| 13 | `setGovernance()` | `[ ]` | |
| 14 | `addMinter()` | `[ ]` | |
| 15 | `removeMinter()` | `[ ]` | |

**Hasil**: 15 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 5 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `_burn()` | `[ ]` | |
| 2 | `mul()` | `[ ]` | |
| 3 | `safeTransfer()` | `[ ]` | |
| 4 | `safeTransferFrom()` | `[ ]` | |
| 5 | `safeApprove()` | `[ ]` | |

**Hasil**: 5 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 6 | | | |
| String vs Bytes32 | 6 | | | |
| Public vs External | 15 | | | |
| Dead Code | 5 | | | |

---

## [19] MultiSigWallet

| Field | Value |
|---|---|
| Domain | Utility |
| Complexity | Medium |
| LOC | 334 |
| File | `Utility_03_MultiSigWallet.sol` |
| Estimated Savings | **33,931 gas** |
| Total Findings | 26 |

### Redundant SLOAD — 11 temuan (2,046 gas potensial)

> **Cara audit**: Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `isOwner` in `MultiSigWallet()` | `[ ]` | |
| 2 | `owners` in `removeOwner()` | `[ ]` | |
| 3 | `owners` in `replaceOwner()` | `[ ]` | |
| 4 | `isOwner` in `replaceOwner()` | `[ ]` | |
| 5 | `owners` in `isConfirmed()` | `[ ]` | |
| 6 | `transactionCount` in `addTransaction()` | `[ ]` | |
| 7 | `owners` in `getConfirmationCount()` | `[ ]` | |
| 8 | `transactions` in `getTransactionCount()` | `[ ]` | |
| 9 | `owners` in `getConfirmations()` | `[ ]` | |
| 10 | `transactionCount` in `getTransactionIds()` | `[ ]` | |
| 11 | `transactions` in `getTransactionIds()` | `[ ]` | |

**Hasil**: 11 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Unoptimized Loop — 5 temuan (5,155 gas potensial)

> **Cara audit**: Cari for-loop yang disebutkan, periksa apakah `array.length` ada di kondisi loop dan array itu adalah state variable.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | Unoptimized Loop: 'owners.length' dibaca dari stor | `[ ]` | |
| 2 | Unoptimized Loop: 'owners.length' dibaca dari stor | `[ ]` | |
| 3 | Unoptimized Loop: 'owners.length' dibaca dari stor | `[ ]` | |
| 4 | Unoptimized Loop: 'owners.length' dibaca dari stor | `[ ]` | |
| 5 | Unoptimized Loop: 'owners.length' dibaca dari stor | `[ ]` | |

**Hasil**: 5 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Public vs External — 10 temuan (26,730 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `addOwner()` | `[ ]` | |
| 2 | `removeOwner()` | `[ ]` | |
| 3 | `replaceOwner()` | `[ ]` | |
| 4 | `submitTransaction()` | `[ ]` | |
| 5 | `revokeConfirmation()` | `[ ]` | |
| 6 | `getConfirmationCount()` | `[ ]` | |
| 7 | `getTransactionCount()` | `[ ]` | |
| 8 | `getOwners()` | `[ ]` | |
| 9 | `getConfirmations()` | `[ ]` | |
| 10 | `getTransactionIds()` | `[ ]` | |

**Hasil**: 10 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Redundant SLOAD | 11 | | | |
| Unoptimized Loop | 5 | | | |
| Public vs External | 10 | | | |

---

## [20] AppProxyUpgradeable

| Field | Value |
|---|---|
| Domain | DeFi |
| Complexity | Medium |
| LOC | 279 |
| File | `DeFi_08_AppProxyUpgradeable.sol` |
| Estimated Savings | **21,384 gas** |
| Total Findings | 11 |

### Public vs External — 8 temuan (21,384 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `hasPermission()` | `[ ]` | |
| 2 | `acl()` | `[ ]` | |
| 3 | `hasPermission()` | `[ ]` | |
| 4 | `setApp()` | `[ ]` | |
| 5 | `getApp()` | `[ ]` | |
| 6 | `proxyType()` | `[ ]` | |
| 7 | `isDepositable()` | `[ ]` | |
| 8 | `proxyType()` | `[ ]` | |

**Hasil**: 8 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

### Dead Code — 3 temuan (0 gas potensial)

> **Cara audit**: Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?

| # | Yang Di-flag | Audit | Catatan |
|---|---|---|---|
| 1 | `getStorageUint256()` | `[ ]` | |
| 2 | `setStorageUint256()` | `[ ]` | |
| 3 | `setDepositable()` | `[ ]` | |

**Hasil**: 3 flagged → TP: ___ / FP: ___ / ?: ___  → Precision = ___% 

**Ringkasan kontrak**:

| Pattern | Flagged | TP | FP | Precision |
|---|---|---|---|---|
| Public vs External | 8 | | | |
| Dead Code | 3 | | | |

---

## Rekap Akhir — Precision per Pattern

Isi setelah semua kontrak selesai diaudit.

| Pattern | Total Flagged | Total TP | Total FP | Precision (%) |
|---|---|---|---|---|
| Public vs External | 439 | | | |
| Redundant SLOAD | 304 | | | |
| String vs Bytes32 | 126 | | | |
| Dead Code | 69 | | | |
| Unoptimized Loop | 7 | | | |

**Catatan**: Precision yang diharapkan berdasarkan karakteristik detektor:
- `public_vs_external`: ~90% (deterministik, FP hanya jika dipanggil via `this.fn()`)
- `redundant_sload`: ~70–80% (FP jika state var dimodifikasi antar pembacaan)
- `string_vs_bytes32`: ~85% (FP jika string memang butuh dinamis)
- `dead_code`: ~65–75% (FP tinggi karena tidak bisa track cross-contract calls)
- `unoptimized_loop`: ~95% (sangat deterministik, FP sangat jarang)