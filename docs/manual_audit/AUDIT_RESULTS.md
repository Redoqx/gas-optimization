# Hasil Manual Audit — 20 Kontrak Top Gas Savings

Dihasilkan otomatis oleh `scripts/run_manual_audit.py`.
Setiap finding diverifikasi dengan membaca file `.sol` langsung.

---

## Ringkasan Precision per Pattern

| Pattern | Total | TP | FP | ? | Precision |
|---|---|---|---|---|---|
| Public vs External | 439 | 322 | 114 | 3 | **73.9%** |
| Redundant SLOAD | 304 | 49 | 22 | 233 | **69.0%** |
| String vs Bytes32 | 126 | 99 | 0 | 27 | **100.0%** |
| Dead Code | 69 | 64 | 3 | 2 | **95.5%** |
| Unoptimized Loop | 7 | 7 | 0 | 0 | **100.0%** |
| **TOTAL** | **945** | **541** | **139** | **265** | **79.6%** |

---

## [01] DCLRegistrar (NFT)

LOC: 1570 | Est. Savings: 117,568 gas

### Redundant SLOAD — 26 temuan → TP=7 FP=6 ?=13 (precision≈54%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_owner` | ❌ FP | assignment to `_owner` at body-line 104 between reads |
| 2 | `_owner` in `renounceOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 3 | `_owner` in `_transferOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 4 | `_ownedTokensCount` in `_transferFrom()` | ✅ TP | 2 reads, no assignment between them |
| 5 | `_tokenApprovals` in `_clearApproval()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 6 | `_ownedTokens` in `_addTokenToOwnerEnumeration()` | ✅ TP | 2 reads, no assignment between them |
| 7 | `_allTokens` in `_addTokenToAllTokensEnumeration()` | ✅ TP | 2 reads, no assignment between them |
| 8 | `_ownedTokens` in `_removeTokenFromOwnerEnumeration()` | ❌ FP | assignment to `_ownedTokens` at body-line 22 between reads |
| 9 | `_ownedTokensIndex` in `_removeTokenFromOwnerEnumeration()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 10 | `_allTokens` in `_removeTokenFromAllTokensEnumeration()` | ❌ FP | assignment to `_allTokens` at body-line 24 between reads |
| 11 | `_allTokensIndex` in `_removeTokenFromAllTokensEnumeration()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 12 | `_tokenURIs` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 13 | `topdomain` | ❌ FP | assignment to `topdomain` at body-line 2964 between reads |
| 14 | `domain` | ❌ FP | assignment to `domain` at body-line 2972 between reads |
| 15 | `topdomainNameHash` | ❌ FP | assignment to `topdomainNameHash` at body-line 2978 between reads |
| 16 | `_owner` in `reclaim()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 17 | `base` in `onERC721Received()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 18 | `baseURI` in `tokenURI()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 19 | `_owner` in `transferDomainOwnership()` | ✅ TP | 3 reads, no assignment between them |
| 20 | `registry` in `setResolver()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 21 | `domainNameHash` in `setResolver()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 22 | `controllers` in `addController()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 23 | `controllers` in `removeController()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 24 | `registry` in `updateRegistry()` | ✅ TP | 3 reads, no assignment between them |
| 25 | `base` in `updateBase()` | ✅ TP | 3 reads, no assignment between them |
| 26 | `baseURI` in `updateBaseURI()` | ✅ TP | 2 reads, no assignment between them |

### String vs Bytes32 — 23 temuan → TP=18 FP=0 ?=5 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 2 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 3 | `topdomain` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 4 | `domain` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 5 | `baseURI` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 6 | `errorMessage` | ⚠️ ? | `errorMessage` not found as top-level state variable — may be inherited or local |
| 7 | `errorMessage` | ⚠️ ? | `errorMessage` not found as top-level state variable — may be inherited or local |
| 8 | `errorMessage` | ⚠️ ? | `errorMessage` not found as top-level state variable — may be inherited or local |
| 9 | `name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 10 | `symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 11 | `uri` | ⚠️ ? | `uri` not found as top-level state variable — may be inherited or local |
| 12 | `name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 13 | `symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 14 | `_topdomain` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 15 | `_domain` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 16 | `_baseURI` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 17 | `_subdomain` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 18 | `_subdomain` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 19 | `_subdomain` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 20 | `_subdomain` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 21 | `_subdomain` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 22 | `_baseURI` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 23 | `_str` | ⚠️ ? | `_str` not found as top-level state variable — may be inherited or local |

### Public vs External — 34 temuan → TP=20 FP=14 ?=0 (precision≈59%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `owner()` | ❌ FP | called internally at lines [3285, 3637] |
| 2 | `renounceOwnership()` | ✅ TP |  |
| 3 | `transferOwnership()` | ✅ TP |  |
| 4 | `transferFrom()` | ❌ FP | called internally at lines [3417] |
| 5 | `approve()` | ✅ TP |  |
| 6 | `setApprovalForAll()` | ✅ TP |  |
| 7 | `onERC721Received()` | ❌ FP | called internally at lines [1747] |
| 8 | `approve()` | ✅ TP |  |
| 9 | `setApprovalForAll()` | ✅ TP |  |
| 10 | `transferFrom()` | ❌ FP | called internally at lines [3417] |
| 11 | `tokenOfOwnerByIndex()` | ✅ TP |  |
| 12 | `tokenByIndex()` | ✅ TP |  |
| 13 | `tokenOfOwnerByIndex()` | ✅ TP |  |
| 14 | `tokenByIndex()` | ✅ TP |  |
| 15 | `setOwner()` | ✅ TP |  |
| 16 | `setSubnodeOwner()` | ❌ FP | called internally at lines [3103, 3141, 3181] |
| 17 | `setResolver()` | ❌ FP | called internally at lines [3449] |
| 18 | `owner()` | ❌ FP | called internally at lines [3285, 3637] |
| 19 | `resolver()` | ❌ FP | called internally at lines [3435, 3469] |
| 20 | `setAddr()` | ✅ TP |  |
| 21 | `addr()` | ✅ TP |  |
| 22 | `transferFrom()` | ❌ FP | called internally at lines [3417] |
| 23 | `transferFrom()` | ❌ FP | called internally at lines [3417] |
| 24 | `allowance()` | ✅ TP |  |
| 25 | `burn()` | ✅ TP |  |
| 26 | `reclaim()` | ❌ FP | called internally at lines [3235, 3395] |
| 27 | `reclaim()` | ❌ FP | called internally at lines [3235, 3395] |
| 28 | `onERC721Received()` | ❌ FP | called internally at lines [1747] |
| 29 | `available()` | ✅ TP |  |
| 30 | `getOwnerOf()` | ✅ TP |  |
| 31 | `reclaimDomain()` | ✅ TP |  |
| 32 | `transferDomainOwnership()` | ✅ TP |  |
| 33 | `setResolver()` | ❌ FP | called internally at lines [3449] |
| 34 | `forwardToResolver()` | ✅ TP |  |

### Dead Code — 7 temuan → TP=6 FP=1 ?=0 (precision≈86%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_msgData()` | ✅ TP | no callers found in file |
| 2 | `add()` | ❌ FP | called at lines [3701] |
| 3 | `mul()` | ✅ TP | no callers found in file |
| 4 | `toPayable()` | ✅ TP | no callers found in file |
| 5 | `sendValue()` | ✅ TP | no callers found in file |
| 6 | `_tokensOfOwner()` | ✅ TP | no callers found in file |
| 7 | `_setTokenURI()` | ✅ TP | no callers found in file |

---

## [02] KyberNetworkProxy (DeFi)

LOC: 484 | Est. Savings: 113,446 gas

### Redundant SLOAD — 24 temuan → TP=7 FP=2 ?=15 (precision≈78%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `decimals` in `setDecimals()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 2 | `MAX_DECIMALS` in `calcDstQty()` | ✅ TP | 2 reads, no assignment between them |
| 3 | `PRECISION` in `calcDstQty()` | ✅ TP | 2 reads, no assignment between them |
| 4 | `MAX_DECIMALS` in `calcSrcQty()` | ✅ TP | 2 reads, no assignment between them |
| 5 | `PRECISION` in `calcSrcQty()` | ✅ TP | 2 reads, no assignment between them |
| 6 | `decimals` in `getDecimalsSafe()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 7 | `MAX_QTY` in `calcRateFromQty()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 8 | `MAX_DECIMALS` in `calcRateFromQty()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 9 | `PRECISION` in `calcRateFromQty()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 10 | `pendingAdmin` in `transferAdmin()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 11 | `admin` in `transferAdminQuickly()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 12 | `pendingAdmin` in `claimAdmin()` | ✅ TP | 2 reads, no assignment between them |
| 13 | `admin` in `claimAdmin()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 14 | `alerters` in `addAlerter()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 15 | `alertersGroup` in `addAlerter()` | ✅ TP | 2 reads, no assignment between them |
| 16 | `alerters` in `removeAlerter()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 17 | `alertersGroup` in `removeAlerter()` | ❌ FP | assignment to `alertersGroup` at body-line 10 between reads |
| 18 | `operators` in `addOperator()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 19 | `operatorsGroup` in `addOperator()` | ✅ TP | 2 reads, no assignment between them |
| 20 | `operators` in `removeOperator()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 21 | `operatorsGroup` in `removeOperator()` | ❌ FP | assignment to `operatorsGroup` at body-line 10 between reads |
| 22 | `ETH_TOKEN_ADDRESS` in `tradeWithHint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 23 | `kyberNetworkContract` in `tradeWithHint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 24 | `kyberNetworkContract` in `setKyberNetworkContract()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |

### Unoptimized Loop — 2 temuan → TP=2 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `alertersGroup.length` | ✅ TP | state array `.length` in for-loop at line 515 |
| 2 | `operatorsGroup.length` | ✅ TP | state array `.length` in for-loop at line 565 |

### Public vs External — 40 temuan → TP=18 FP=22 ?=0 (precision≈45%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `totalSupply()` | ✅ TP |  |
| 2 | `balanceOf()` | ❌ FP | called internally at lines [265] |
| 3 | `transfer()` | ❌ FP | called internally at lines [621, 641] |
| 4 | `transferFrom()` | ❌ FP | called internally at lines [971] |
| 5 | `approve()` | ✅ TP |  |
| 6 | `allowance()` | ✅ TP |  |
| 7 | `decimals()` | ❌ FP | called internally at lines [149, 167] |
| 8 | `maxGasPrice()` | ❌ FP | called internally at lines [1087] |
| 9 | `getUserCapInWei()` | ❌ FP | called internally at lines [1071] |
| 10 | `getUserCapInTokenWei()` | ❌ FP | called internally at lines [1079] |
| 11 | `enabled()` | ❌ FP | called internally at lines [1095] |
| 12 | `info()` | ❌ FP | called internally at lines [1103] |
| 13 | `getExpectedRate()` | ❌ FP | called internally at lines [1063] |
| 14 | `maxGasPrice()` | ❌ FP | called internally at lines [1087] |
| 15 | `getUserCapInWei()` | ❌ FP | called internally at lines [1071] |
| 16 | `getUserCapInTokenWei()` | ❌ FP | called internally at lines [1079] |
| 17 | `enabled()` | ❌ FP | called internally at lines [1095] |
| 18 | `info()` | ❌ FP | called internally at lines [1103] |
| 19 | `getExpectedRate()` | ❌ FP | called internally at lines [1063] |
| 20 | `swapTokenToToken()` | ✅ TP |  |
| 21 | `swapEtherToToken()` | ✅ TP |  |
| 22 | `swapTokenToEther()` | ✅ TP |  |
| 23 | `transferAdmin()` | ✅ TP |  |
| 24 | `transferAdminQuickly()` | ✅ TP |  |
| 25 | `claimAdmin()` | ✅ TP |  |
| 26 | `addAlerter()` | ✅ TP |  |
| 27 | `removeAlerter()` | ✅ TP |  |
| 28 | `addOperator()` | ✅ TP |  |
| 29 | `removeOperator()` | ✅ TP |  |
| 30 | `trade()` | ✅ TP |  |
| 31 | `swapTokenToToken()` | ✅ TP |  |
| 32 | `swapEtherToToken()` | ✅ TP |  |
| 33 | `swapTokenToEther()` | ✅ TP |  |
| 34 | `setKyberNetworkContract()` | ✅ TP |  |
| 35 | `getExpectedRate()` | ❌ FP | called internally at lines [1063] |
| 36 | `getUserCapInWei()` | ❌ FP | called internally at lines [1071] |
| 37 | `getUserCapInTokenWei()` | ❌ FP | called internally at lines [1079] |
| 38 | `maxGasPrice()` | ❌ FP | called internally at lines [1087] |
| 39 | `enabled()` | ❌ FP | called internally at lines [1095] |
| 40 | `info()` | ❌ FP | called internally at lines [1103] |

### Dead Code — 2 temuan → TP=2 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `calcDestAmount()` | ✅ TP | no callers found in file |
| 2 | `calcSrcAmount()` | ✅ TP | no callers found in file |

---

## [03] WBTC (Token)

LOC: 564 | Est. Savings: 89,081 gas

### Redundant SLOAD — 13 temuan → TP=1 FP=0 ?=12 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `balances` in `transfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 2 | `balances` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 3 | `allowed` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `allowed` in `increaseApproval()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 5 | `allowed` in `decreaseApproval()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 6 | `owner` in `renounceOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 7 | `owner` in `_transferOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 8 | `totalSupply_` in `mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 9 | `balances` in `mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 10 | `balances` in `_burn()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 11 | `totalSupply_` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 12 | `owner` in `claimOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 13 | `pendingOwner` in `claimOwnership()` | ✅ TP | 2 reads, no assignment between them |

### String vs Bytes32 — 4 temuan → TP=2 FP=0 ?=2 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 2 | `symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 3 | `_name` | ⚠️ ? | `_name` not found as top-level state variable — may be inherited or local |
| 4 | `_symbol` | ⚠️ ? | `_symbol` not found as top-level state variable — may be inherited or local |

### Public vs External — 31 temuan → TP=14 FP=17 ?=0 (precision≈45%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `totalSupply()` | ✅ TP |  |
| 2 | `balanceOf()` | ❌ FP | called internally at lines [1263] |
| 3 | `transfer()` | ❌ FP | called internally at lines [1181] |
| 4 | `totalSupply()` | ✅ TP |  |
| 5 | `transfer()` | ❌ FP | called internally at lines [1181] |
| 6 | `balanceOf()` | ❌ FP | called internally at lines [1263] |
| 7 | `allowance()` | ✅ TP |  |
| 8 | `transferFrom()` | ❌ FP | called internally at lines [1203] |
| 9 | `approve()` | ❌ FP | called internally at lines [1223] |
| 10 | `transferFrom()` | ❌ FP | called internally at lines [1203] |
| 11 | `approve()` | ❌ FP | called internally at lines [1223] |
| 12 | `allowance()` | ✅ TP |  |
| 13 | `increaseApproval()` | ❌ FP | called via super.increaseApproval() at lines [1047] |
| 14 | `decreaseApproval()` | ❌ FP | called via super.decreaseApproval() at lines [1069] |
| 15 | `renounceOwnership()` | ✅ TP |  |
| 16 | `transferOwnership()` | ✅ TP |  |
| 17 | `mint()` | ✅ TP |  |
| 18 | `finishMinting()` | ✅ TP |  |
| 19 | `burn()` | ❌ FP | called via super.burn() at lines [1297] |
| 20 | `pause()` | ✅ TP |  |
| 21 | `unpause()` | ✅ TP |  |
| 22 | `transfer()` | ❌ FP | called internally at lines [1181] |
| 23 | `transferFrom()` | ❌ FP | called internally at lines [1203] |
| 24 | `approve()` | ❌ FP | called internally at lines [1223] |
| 25 | `increaseApproval()` | ❌ FP | called via super.increaseApproval() at lines [1047] |
| 26 | `decreaseApproval()` | ❌ FP | called via super.decreaseApproval() at lines [1069] |
| 27 | `transferOwnership()` | ✅ TP |  |
| 28 | `claimOwnership()` | ✅ TP |  |
| 29 | `burn()` | ❌ FP | called via super.burn() at lines [1297] |
| 30 | `finishMinting()` | ✅ TP |  |
| 31 | `renounceOwnership()` | ✅ TP |  |

### Dead Code — 4 temuan → TP=4 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `mul()` | ✅ TP | no callers found in file |
| 2 | `div()` | ✅ TP | no callers found in file |
| 3 | `safeTransferFrom()` | ✅ TP | no callers found in file |
| 4 | `safeApprove()` | ✅ TP | no callers found in file |

---

## [04] AdminUpgradeabilityProxy (Token)

LOC: 687 | Est. Savings: 84,576 gas

### Redundant SLOAD — 37 temuan → TP=8 FP=5 ?=24 (precision≈62%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `initialized` in `initialize()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 2 | `frozen` in `transfer()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 3 | `frozen` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `allowed` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 5 | `frozen` in `approve()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 6 | `balances` in `_transfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 7 | `feeRecipient` in `_transfer()` | ✅ TP | 3 reads, no assignment between them |
| 8 | `proposedOwner` in `proposeOwner()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 9 | `proposedOwner` in `disregardProposeOwner()` | ✅ TP | 3 reads, no assignment between them |
| 10 | `proposedOwner` in `claimOwnership()` | ✅ TP | 2 reads, no assignment between them |
| 11 | `owner` in `claimOwnership()` | ❌ FP | assignment to `owner` at body-line 6 between reads |
| 12 | `balances` in `reclaimPAXG()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 13 | `owner` in `reclaimPAXG()` | ✅ TP | 2 reads, no assignment between them |
| 14 | `paused` in `pause()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 15 | `paused` in `unpause()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 16 | `assetProtectionRole` in `setAssetProtectionRole()` | ✅ TP | 2 reads, no assignment between them |
| 17 | `frozen` in `freeze()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 18 | `frozen` in `unfreeze()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 19 | `balances` in `wipeFrozenAddress()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 20 | `totalSupply_` in `wipeFrozenAddress()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 21 | `supplyController` in `setSupplyController()` | ✅ TP | 2 reads, no assignment between them |
| 22 | `totalSupply_` in `increaseSupply()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 23 | `balances` in `increaseSupply()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 24 | `supplyController` in `increaseSupply()` | ✅ TP | 3 reads, no assignment between them |
| 25 | `balances` in `decreaseSupply()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 26 | `supplyController` in `decreaseSupply()` | ✅ TP | 4 reads, no assignment between them |
| 27 | `totalSupply_` in `decreaseSupply()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 28 | `frozen` in `_betaDelegatedTransfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 29 | `balances` in `_betaDelegatedTransfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 30 | `nextSeqs` in `_betaDelegatedTransfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 31 | `betaDelegateWhitelister` in `setBetaDelegateWhitelister()` | ❌ FP | assignment to `betaDelegateWhitelister` at body-line 4 between reads |
| 32 | `betaDelegateWhitelist` in `whitelistBetaDelegate()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 33 | `betaDelegateWhitelist` in `unwhitelistBetaDelegate()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 34 | `feeController` in `setFeeController()` | ❌ FP | assignment to `feeController` at body-line 8 between reads |
| 35 | `feeRecipient` in `setFeeRecipient()` | ❌ FP | assignment to `feeRecipient` at body-line 6 between reads |
| 36 | `feeRate` in `setFeeRate()` | ❌ FP | assignment to `feeRate` at body-line 6 between reads |
| 37 | `feeRate` in `getFeeFor()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |

### String vs Bytes32 — 3 temuan → TP=3 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `name` | ✅ TP | value="Paxos Gold" (10 chars ≤ 32) |
| 2 | `symbol` | ✅ TP | value="PAXG" (4 chars ≤ 32) |
| 3 | `EIP191_HEADER` | ✅ TP | value="\x19\x01" (8 chars ≤ 32) |

### Public vs External — 28 temuan → TP=28 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `totalSupply()` | ✅ TP |  |
| 2 | `transfer()` | ✅ TP |  |
| 3 | `balanceOf()` | ✅ TP |  |
| 4 | `transferFrom()` | ✅ TP |  |
| 5 | `approve()` | ✅ TP |  |
| 6 | `allowance()` | ✅ TP |  |
| 7 | `proposeOwner()` | ✅ TP |  |
| 8 | `disregardProposeOwner()` | ✅ TP |  |
| 9 | `claimOwnership()` | ✅ TP |  |
| 10 | `unpause()` | ✅ TP |  |
| 11 | `setAssetProtectionRole()` | ✅ TP |  |
| 12 | `freeze()` | ✅ TP |  |
| 13 | `unfreeze()` | ✅ TP |  |
| 14 | `wipeFrozenAddress()` | ✅ TP |  |
| 15 | `isFrozen()` | ✅ TP |  |
| 16 | `setSupplyController()` | ✅ TP |  |
| 17 | `increaseSupply()` | ✅ TP |  |
| 18 | `decreaseSupply()` | ✅ TP |  |
| 19 | `nextSeqOf()` | ✅ TP |  |
| 20 | `betaDelegatedTransfer()` | ✅ TP |  |
| 21 | `betaDelegatedTransferBatch()` | ✅ TP |  |
| 22 | `isWhitelistedBetaDelegate()` | ✅ TP |  |
| 23 | `setBetaDelegateWhitelister()` | ✅ TP |  |
| 24 | `whitelistBetaDelegate()` | ✅ TP |  |
| 25 | `unwhitelistBetaDelegate()` | ✅ TP |  |
| 26 | `setFeeController()` | ✅ TP |  |
| 27 | `setFeeRecipient()` | ✅ TP |  |
| 28 | `setFeeRate()` | ✅ TP |  |

---

## [05] AdminUpgradeabilityProxy (NFT)

LOC: 1515 | Est. Savings: 83,925 gas

### String vs Bytes32 — 18 temuan → TP=17 FP=0 ?=1 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `contractName` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 2 | `migrationId` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 3 | `contractName` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 4 | `migrationId` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 5 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 6 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 7 | `_uri` | ⚠️ ? | `_uri` not found as top-level state variable — may be inherited or local |
| 8 | `metadata` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 9 | `data` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 10 | `metadata` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 11 | `metadata` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 12 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 13 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 14 | `data` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 15 | `data` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 16 | `metadata` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 17 | `metadata` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 18 | `data` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |

### Public vs External — 25 temuan → TP=14 FP=11 ?=0 (precision≈56%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `approve()` | ✅ TP |  |
| 2 | `setApprovalForAll()` | ✅ TP |  |
| 3 | `tokenOfOwnerByIndex()` | ✅ TP |  |
| 4 | `tokenByIndex()` | ✅ TP |  |
| 5 | `tokenURI()` | ✅ TP |  |
| 6 | `onERC721Received()` | ❌ FP | called internally at lines [597] |
| 7 | `approve()` | ✅ TP |  |
| 8 | `setApprovalForAll()` | ✅ TP |  |
| 9 | `initialize()` | ❌ FP | called internally at lines [1350, 1351] |
| 10 | `initialize()` | ❌ FP | called internally at lines [1350, 1351] |
| 11 | `tokenURI()` | ✅ TP |  |
| 12 | `tokenOfOwnerByIndex()` | ✅ TP |  |
| 13 | `tokenByIndex()` | ✅ TP |  |
| 14 | `initialize()` | ❌ FP | called internally at lines [1350, 1351] |
| 15 | `transferOwnership()` | ✅ TP |  |
| 16 | `ping()` | ❌ FP | called internally at lines [1187] |
| 17 | `updateOperator()` | ❌ FP | called internally at lines [1632] |
| 18 | `setManyUpdateOperator()` | ❌ FP | called internally at lines [1337] |
| 19 | `setLandUpdateOperator()` | ✅ TP |  |
| 20 | `setManyLandUpdateOperator()` | ✅ TP |  |
| 21 | `initialize()` | ❌ FP | called internally at lines [1350, 1351] |
| 22 | `onERC721Received()` | ❌ FP | called internally at lines [597] |
| 23 | `verifyFingerprint()` | ❌ FP | called internally at lines [1050] |
| 24 | `updateLandData()` | ❌ FP | called internally at lines [1661] |
| 25 | `updateManyLandData()` | ✅ TP |  |

### Dead Code — 2 temuan → TP=2 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `div()` | ✅ TP | no callers found in file |
| 2 | `_setTokenURI()` | ✅ TP | no callers found in file |

---

## [06] Parcel (NFT)

LOC: 733 | Est. Savings: 80,054 gas

### Redundant SLOAD — 21 temuan → TP=4 FP=0 ?=17 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `owner` in `transferOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 2 | `owner` in `ownerOf()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 3 | `owner` in `approve()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `owner` in `isApprovedOrOwner()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 5 | `tokenApprovals` in `clearApproval()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 6 | `tokenOwner` in `addTokenTo()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 7 | `ownedTokensCount` in `addTokenTo()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 8 | `ownedTokensCount` in `removeTokenFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 9 | `ownedTokens` in `addTokenTo()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 10 | `ownedTokensIndex` in `removeTokenFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 11 | `ownedTokens` in `removeTokenFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 12 | `allTokens` in `_mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 13 | `tokenURIs` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 14 | `allTokensIndex` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 15 | `allTokens` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 16 | `creator` in `takeOwnership()` | ✅ TP | 3 reads, no assignment between them |
| 17 | `owner` in `takeOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 18 | `contentURIs` in `burn()` | ✅ TP | 2 reads, no assignment between them |
| 19 | `tokenOwner` in `buy()` | ✅ TP | 2 reads, no assignment between them |
| 20 | `tokenPrice` in `buy()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 21 | `boundingBoxes` in `getBoundingBox()` | ✅ TP | 6 reads, no assignment between them |

### String vs Bytes32 — 7 temuan → TP=4 FP=0 ?=3 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `name_` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 2 | `symbol_` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 3 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 4 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 5 | `_uri` | ⚠️ ? | `_uri` not found as top-level state variable — may be inherited or local |
| 6 | `inStr` | ⚠️ ? | `inStr` not found as top-level state variable — may be inherited or local |
| 7 | `_uri` | ⚠️ ? | `_uri` not found as top-level state variable — may be inherited or local |

### Public vs External — 26 temuan → TP=25 FP=1 ?=0 (precision≈96%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `transferOwnership()` | ✅ TP |  |
| 2 | `approve()` | ✅ TP |  |
| 3 | `setApprovalForAll()` | ✅ TP |  |
| 4 | `tokenOfOwnerByIndex()` | ✅ TP |  |
| 5 | `tokenByIndex()` | ✅ TP |  |
| 6 | `name()` | ✅ TP |  |
| 7 | `symbol()` | ✅ TP |  |
| 8 | `tokenURI()` | ✅ TP |  |
| 9 | `onERC721Received()` | ❌ FP | called internally at lines [997] |
| 10 | `approve()` | ✅ TP |  |
| 11 | `setApprovalForAll()` | ✅ TP |  |
| 12 | `name()` | ✅ TP |  |
| 13 | `symbol()` | ✅ TP |  |
| 14 | `tokenURI()` | ✅ TP |  |
| 15 | `tokenOfOwnerByIndex()` | ✅ TP |  |
| 16 | `tokenByIndex()` | ✅ TP |  |
| 17 | `takeOwnership()` | ✅ TP |  |
| 18 | `mint()` | ✅ TP |  |
| 19 | `tokenURI()` | ✅ TP |  |
| 20 | `burn()` | ✅ TP |  |
| 21 | `setPrice()` | ✅ TP |  |
| 22 | `getPrice()` | ✅ TP |  |
| 23 | `buy()` | ✅ TP |  |
| 24 | `getBoundingBox()` | ✅ TP |  |
| 25 | `setContentURI()` | ✅ TP |  |
| 26 | `contentURI()` | ✅ TP |  |

### Dead Code — 3 temuan → TP=3 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `mul()` | ✅ TP | no callers found in file |
| 2 | `div()` | ✅ TP | no callers found in file |
| 3 | `_setTokenURI()` | ✅ TP | no callers found in file |

---

## [07] TetherToken (Token)

LOC: 377 | Est. Savings: 78,947 gas

### Redundant SLOAD — 16 temuan → TP=2 FP=0 ?=14 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `maximumFee` in `transfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 2 | `balances` in `transfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 3 | `owner` in `transfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `allowed` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 5 | `maximumFee` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 6 | `balances` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 7 | `owner` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 8 | `allowed` in `approve()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 9 | `_totalSupply` in `issue()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 10 | `balances` in `issue()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 11 | `owner` in `issue()` | ✅ TP | 2 reads, no assignment between them |
| 12 | `_totalSupply` in `redeem()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 13 | `balances` in `redeem()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 14 | `owner` in `redeem()` | ✅ TP | 2 reads, no assignment between them |
| 15 | `basisPointsRate` in `setParams()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 16 | `maximumFee` in `setParams()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |

### String vs Bytes32 — 4 temuan → TP=2 FP=0 ?=2 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 2 | `symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 3 | `_name` | ⚠️ ? | `_name` not found as top-level state variable — may be inherited or local |
| 4 | `_symbol` | ⚠️ ? | `_symbol` not found as top-level state variable — may be inherited or local |

### Public vs External — 27 temuan → TP=10 FP=17 ?=0 (precision≈37%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `transferOwnership()` | ✅ TP |  |
| 2 | `totalSupply()` | ❌ FP | called internally at lines [783] |
| 3 | `transfer()` | ❌ FP | called via super.transfer() at lines [681] |
| 4 | `allowance()` | ❌ FP | called internally at lines [751] |
| 5 | `transferFrom()` | ❌ FP | called via super.transferFrom() at lines [701] |
| 6 | `approve()` | ❌ FP | called via super.approve() at lines [737] |
| 7 | `transfer()` | ❌ FP | called via super.transfer() at lines [681] |
| 8 | `transferFrom()` | ❌ FP | called via super.transferFrom() at lines [701] |
| 9 | `approve()` | ❌ FP | called via super.approve() at lines [737] |
| 10 | `allowance()` | ❌ FP | called internally at lines [751] |
| 11 | `pause()` | ✅ TP |  |
| 12 | `unpause()` | ✅ TP |  |
| 13 | `addBlackList()` | ✅ TP |  |
| 14 | `removeBlackList()` | ✅ TP |  |
| 15 | `destroyBlackFunds()` | ✅ TP |  |
| 16 | `transferByLegacy()` | ❌ FP | called internally at lines [677] |
| 17 | `transferFromByLegacy()` | ❌ FP | called internally at lines [697] |
| 18 | `approveByLegacy()` | ❌ FP | called internally at lines [733] |
| 19 | `transfer()` | ❌ FP | called via super.transfer() at lines [681] |
| 20 | `transferFrom()` | ❌ FP | called via super.transferFrom() at lines [701] |
| 21 | `approve()` | ❌ FP | called via super.approve() at lines [737] |
| 22 | `allowance()` | ❌ FP | called internally at lines [751] |
| 23 | `deprecate()` | ✅ TP |  |
| 24 | `totalSupply()` | ❌ FP | called internally at lines [783] |
| 25 | `issue()` | ✅ TP |  |
| 26 | `redeem()` | ✅ TP |  |
| 27 | `setParams()` | ✅ TP |  |

---

## [08] AdminUpgradeabilityProxy (Token)

LOC: 581 | Est. Savings: 75,813 gas

### Redundant SLOAD — 33 temuan → TP=7 FP=2 ?=24 (precision≈78%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `initialized` in `initialize()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 2 | `frozen` in `transfer()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 3 | `balances` in `transfer()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 4 | `frozen` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 5 | `balances` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 6 | `allowed` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 7 | `frozen` in `approve()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 8 | `proposedOwner` in `proposeOwner()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 9 | `proposedOwner` in `disregardProposeOwner()` | ✅ TP | 3 reads, no assignment between them |
| 10 | `proposedOwner` in `claimOwnership()` | ✅ TP | 2 reads, no assignment between them |
| 11 | `owner` in `claimOwnership()` | ❌ FP | assignment to `owner` at body-line 6 between reads |
| 12 | `balances` in `reclaimBUSD()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 13 | `owner` in `reclaimBUSD()` | ✅ TP | 2 reads, no assignment between them |
| 14 | `paused` in `pause()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 15 | `paused` in `unpause()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 16 | `assetProtectionRole` in `setAssetProtectionRole()` | ✅ TP | 2 reads, no assignment between them |
| 17 | `frozen` in `freeze()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 18 | `frozen` in `unfreeze()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 19 | `balances` in `wipeFrozenAddress()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 20 | `totalSupply_` in `wipeFrozenAddress()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 21 | `supplyController` in `setSupplyController()` | ✅ TP | 2 reads, no assignment between them |
| 22 | `totalSupply_` in `increaseSupply()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 23 | `balances` in `increaseSupply()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 24 | `supplyController` in `increaseSupply()` | ✅ TP | 3 reads, no assignment between them |
| 25 | `balances` in `decreaseSupply()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 26 | `supplyController` in `decreaseSupply()` | ✅ TP | 4 reads, no assignment between them |
| 27 | `totalSupply_` in `decreaseSupply()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 28 | `frozen` in `_betaDelegatedTransfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 29 | `balances` in `_betaDelegatedTransfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 30 | `nextSeqs` in `_betaDelegatedTransfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 31 | `betaDelegateWhitelister` in `setBetaDelegateWhitelister()` | ❌ FP | assignment to `betaDelegateWhitelister` at body-line 4 between reads |
| 32 | `betaDelegateWhitelist` in `whitelistBetaDelegate()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 33 | `betaDelegateWhitelist` in `unwhitelistBetaDelegate()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |

### String vs Bytes32 — 3 temuan → TP=3 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `name` | ✅ TP | value="BUSD" (4 chars ≤ 32) |
| 2 | `symbol` | ✅ TP | value="BUSD" (4 chars ≤ 32) |
| 3 | `EIP191_HEADER` | ✅ TP | value="\x19\x01" (8 chars ≤ 32) |

### Public vs External — 25 temuan → TP=25 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `totalSupply()` | ✅ TP |  |
| 2 | `transfer()` | ✅ TP |  |
| 3 | `balanceOf()` | ✅ TP |  |
| 4 | `transferFrom()` | ✅ TP |  |
| 5 | `approve()` | ✅ TP |  |
| 6 | `allowance()` | ✅ TP |  |
| 7 | `proposeOwner()` | ✅ TP |  |
| 8 | `disregardProposeOwner()` | ✅ TP |  |
| 9 | `claimOwnership()` | ✅ TP |  |
| 10 | `unpause()` | ✅ TP |  |
| 11 | `setAssetProtectionRole()` | ✅ TP |  |
| 12 | `freeze()` | ✅ TP |  |
| 13 | `unfreeze()` | ✅ TP |  |
| 14 | `wipeFrozenAddress()` | ✅ TP |  |
| 15 | `isFrozen()` | ✅ TP |  |
| 16 | `setSupplyController()` | ✅ TP |  |
| 17 | `increaseSupply()` | ✅ TP |  |
| 18 | `decreaseSupply()` | ✅ TP |  |
| 19 | `nextSeqOf()` | ✅ TP |  |
| 20 | `betaDelegatedTransfer()` | ✅ TP |  |
| 21 | `betaDelegatedTransferBatch()` | ✅ TP |  |
| 22 | `isWhitelistedBetaDelegate()` | ✅ TP |  |
| 23 | `setBetaDelegateWhitelister()` | ✅ TP |  |
| 24 | `whitelistBetaDelegate()` | ✅ TP |  |
| 25 | `unwhitelistBetaDelegate()` | ✅ TP |  |

---

## [09] WrappedPunk (NFT)

LOC: 1376 | Est. Savings: 70,910 gas

### Redundant SLOAD — 14 temuan → TP=3 FP=2 ?=9 (precision≈60%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_owner` in `renounceOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 2 | `_owner` in `transferOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 3 | `_ownedTokensCount` in `_transferFrom()` | ✅ TP | 2 reads, no assignment between them |
| 4 | `_tokenApprovals` in `_clearApproval()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 5 | `_ownedTokens` in `_addTokenToOwnerEnumeration()` | ✅ TP | 2 reads, no assignment between them |
| 6 | `_allTokens` in `_addTokenToAllTokensEnumeration()` | ✅ TP | 2 reads, no assignment between them |
| 7 | `_ownedTokens` in `_removeTokenFromOwnerEnumeration()` | ❌ FP | assignment to `_ownedTokens` at body-line 22 between reads |
| 8 | `_ownedTokensIndex` in `_removeTokenFromOwnerEnumeration()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 9 | `_allTokens` in `_removeTokenFromAllTokensEnumeration()` | ❌ FP | assignment to `_allTokens` at body-line 24 between reads |
| 10 | `_allTokensIndex` in `_removeTokenFromAllTokensEnumeration()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 11 | `_baseURI` in `tokenURI()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 12 | `_tokenURIs` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 13 | `_owner` in `transfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 14 | `_proxies` in `registerProxy()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |

### String vs Bytes32 — 10 temuan → TP=8 FP=0 ?=2 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 2 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 3 | `_baseURI` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 4 | `name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 5 | `symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 6 | `_tokenURI` | ⚠️ ? | `_tokenURI` not found as top-level state variable — may be inherited or local |
| 7 | `baseURI` | ⚠️ ? | `baseURI` not found as top-level state variable — may be inherited or local |
| 8 | `name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 9 | `symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 10 | `baseUri` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |

### Public vs External — 22 temuan → TP=22 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `owner()` | ✅ TP |  |
| 2 | `renounceOwnership()` | ✅ TP |  |
| 3 | `transferOwnership()` | ✅ TP |  |
| 4 | `paused()` | ✅ TP |  |
| 5 | `supportsInterface()` | ✅ TP |  |
| 6 | `approve()` | ✅ TP |  |
| 7 | `setApprovalForAll()` | ✅ TP |  |
| 8 | `transferFrom()` | ✅ TP |  |
| 9 | `tokenOfOwnerByIndex()` | ✅ TP |  |
| 10 | `tokenByIndex()` | ✅ TP |  |
| 11 | `name()` | ✅ TP |  |
| 12 | `symbol()` | ✅ TP |  |
| 13 | `tokenURI()` | ✅ TP |  |
| 14 | `baseURI()` | ✅ TP |  |
| 15 | `punkContract()` | ✅ TP |  |
| 16 | `setBaseURI()` | ✅ TP |  |
| 17 | `pause()` | ✅ TP |  |
| 18 | `unpause()` | ✅ TP |  |
| 19 | `registerProxy()` | ✅ TP |  |
| 20 | `proxyInfo()` | ✅ TP |  |
| 21 | `mint()` | ✅ TP |  |
| 22 | `burn()` | ✅ TP |  |

### Dead Code — 8 temuan → TP=7 FP=1 ?=0 (precision≈88%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_msgData()` | ✅ TP | no callers found in file |
| 2 | `add()` | ❌ FP | called at lines [2065] |
| 3 | `mul()` | ✅ TP | no callers found in file |
| 4 | `div()` | ✅ TP | no callers found in file |
| 5 | `mod()` | ✅ TP | no callers found in file |
| 6 | `toPayable()` | ✅ TP | no callers found in file |
| 7 | `_tokensOfOwner()` | ✅ TP | no callers found in file |
| 8 | `_setTokenURI()` | ✅ TP | no callers found in file |

---

## [10] SuperRareV2 (NFT)

LOC: 999 | Est. Savings: 67,836 gas

### Redundant SLOAD — 16 temuan → TP=0 FP=2 ?=14 (precision≈0%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_tokenOwner` in `_addTokenTo()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 2 | `_ownedTokensCount` in `_addTokenTo()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 3 | `_ownedTokensCount` in `_removeTokenFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `_tokenApprovals` in `_clearApproval()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 5 | `_ownedTokens` in `_addTokenTo()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 6 | `_ownedTokensIndex` in `_removeTokenFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 7 | `_ownedTokens` in `_removeTokenFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 8 | `_allTokens` in `_mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 9 | `_allTokensIndex` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 10 | `_allTokens` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 11 | `_tokenURIs` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 12 | `_owner` | ❌ FP | assignment to `_owner` at body-line 1746 between reads |
| 13 | `_owner` in `renounceOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 14 | `_owner` in `_transferOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 15 | `oldSuperRare` | ❌ FP | assignment to `oldSuperRare` at body-line 2064 between reads |
| 16 | `idCounter` in `_createToken()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |

### String vs Bytes32 — 12 temuan → TP=12 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 2 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 3 | `name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 4 | `symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 5 | `uri` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 6 | `name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 7 | `symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 8 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 9 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 10 | `_uri` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 11 | `_uri` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 12 | `_uri` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |

### Public vs External — 20 temuan → TP=19 FP=1 ?=0 (precision≈95%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `creatorOfToken()` | ✅ TP |  |
| 2 | `onERC721Received()` | ❌ FP | called internally at lines [1219] |
| 3 | `approve()` | ✅ TP |  |
| 4 | `setApprovalForAll()` | ✅ TP |  |
| 5 | `tokenOfOwnerByIndex()` | ✅ TP |  |
| 6 | `tokenByIndex()` | ✅ TP |  |
| 7 | `approve()` | ✅ TP |  |
| 8 | `setApprovalForAll()` | ✅ TP |  |
| 9 | `tokenOfOwnerByIndex()` | ✅ TP |  |
| 10 | `tokenByIndex()` | ✅ TP |  |
| 11 | `owner()` | ✅ TP |  |
| 12 | `renounceOwnership()` | ✅ TP |  |
| 13 | `transferOwnership()` | ✅ TP |  |
| 14 | `enableWhitelist()` | ✅ TP |  |
| 15 | `addToWhitelist()` | ✅ TP |  |
| 16 | `removeFromWhitelist()` | ✅ TP |  |
| 17 | `initWhitelist()` | ✅ TP |  |
| 18 | `addNewToken()` | ✅ TP |  |
| 19 | `deleteToken()` | ✅ TP |  |
| 20 | `updateTokenMetadata()` | ✅ TP |  |

### Dead Code — 3 temuan → TP=3 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `mul()` | ✅ TP | no callers found in file |
| 2 | `div()` | ✅ TP | no callers found in file |
| 3 | `mod()` | ✅ TP | no callers found in file |

---

## [11] BalancerGovernanceToken (Token)

LOC: 1280 | Est. Savings: 59,326 gas

### Redundant SLOAD — 6 temuan → TP=1 FP=0 ?=5 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_balances` in `_transfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 2 | `_totalSupply` in `_mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 3 | `_balances` in `_mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `_balances` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 5 | `_totalSupply` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 6 | `_currentSnapshotId` in `_snapshot()` | ✅ TP | 2 reads, no assignment between them |

### String vs Bytes32 — 5 temuan → TP=3 FP=0 ?=2 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 2 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 3 | `version` | ✅ TP | value="1" (1 chars ≤ 32) |
| 4 | `name` | ⚠️ ? | `name` not found as top-level state variable — may be inherited or local |
| 5 | `symbol` | ⚠️ ? | `symbol` not found as top-level state variable — may be inherited or local |

### Public vs External — 20 temuan → TP=17 FP=0 ?=3 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `getRoleMemberCount()` | ✅ TP |  |
| 2 | `getRoleMember()` | ✅ TP |  |
| 3 | `getRoleAdmin()` | ✅ TP |  |
| 4 | `grantRole()` | ✅ TP |  |
| 5 | `revokeRole()` | ✅ TP |  |
| 6 | `renounceRole()` | ✅ TP |  |
| 7 | `name()` | ✅ TP |  |
| 8 | `symbol()` | ✅ TP |  |
| 9 | `decimals()` | ✅ TP |  |
| 10 | `transfer()` | ⚠️ ? | has override keyword (line 2029) — may need public for interface |
| 11 | `approve()` | ⚠️ ? | has override keyword (line 2067) — may need public for interface |
| 12 | `transferFrom()` | ⚠️ ? | has override keyword (line 2101) — may need public for interface |
| 13 | `increaseAllowance()` | ✅ TP |  |
| 14 | `decreaseAllowance()` | ✅ TP |  |
| 15 | `balanceOfAt()` | ✅ TP |  |
| 16 | `totalSupplyAt()` | ✅ TP |  |
| 17 | `mint()` | ✅ TP |  |
| 18 | `burn()` | ✅ TP |  |
| 19 | `burnFrom()` | ✅ TP |  |
| 20 | `snapshot()` | ✅ TP |  |

### Dead Code — 10 temuan → TP=7 FP=1 ?=2 (precision≈88%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `isContract()` | ✅ TP | no callers found in file |
| 2 | `sendValue()` | ✅ TP | no callers found in file |
| 3 | `_msgData()` | ⚠️ ? | virtual/override function — may be called from child contract |
| 4 | `_setRoleAdmin()` | ⚠️ ? | virtual/override function — may be called from child contract |
| 5 | `mul()` | ✅ TP | no callers found in file |
| 6 | `max()` | ✅ TP | no callers found in file |
| 7 | `min()` | ✅ TP | no callers found in file |
| 8 | `decrement()` | ✅ TP | no callers found in file |
| 9 | `_setupDecimals()` | ✅ TP | no callers found in file |
| 10 | `_valueAt()` | ❌ FP | called at lines [2597, 2615] |

---

## [12] WyvernProxyRegistry (Utility)

LOC: 383 | Est. Savings: 58,757 gas

### Redundant SLOAD — 9 temuan → TP=0 FP=0 ?=9 (precision≈n/a)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `owner` in `transferOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 2 | `owner` in `renounceOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 3 | `pending` in `startGrantAuthentication()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `contracts` in `endGrantAuthentication()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 5 | `pending` in `endGrantAuthentication()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 6 | `proxies` in `registerProxy()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 7 | `initialAddressSet` in `grantInitialAuthentication()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 8 | `initialized` in `initialize()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 9 | `_implementation` in `_upgradeTo()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |

### String vs Bytes32 — 1 temuan → TP=1 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `name` | ✅ TP | value="Project Wyvern Proxy Registry" (29 chars ≤ 32) |

### Public vs External — 21 temuan → TP=19 FP=2 ?=0 (precision≈90%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `transferOwnership()` | ✅ TP |  |
| 2 | `renounceOwnership()` | ✅ TP |  |
| 3 | `totalSupply()` | ✅ TP |  |
| 4 | `balanceOf()` | ✅ TP |  |
| 5 | `transfer()` | ✅ TP |  |
| 6 | `allowance()` | ✅ TP |  |
| 7 | `transferFrom()` | ❌ FP | called internally at lines [167] |
| 8 | `approve()` | ✅ TP |  |
| 9 | `receiveApproval()` | ✅ TP |  |
| 10 | `startGrantAuthentication()` | ✅ TP |  |
| 11 | `endGrantAuthentication()` | ✅ TP |  |
| 12 | `revokeAuthentication()` | ✅ TP |  |
| 13 | `registerProxy()` | ✅ TP |  |
| 14 | `grantInitialAuthentication()` | ✅ TP |  |
| 15 | `proxyType()` | ✅ TP |  |
| 16 | `initialize()` | ❌ FP | called internally at lines [339] |
| 17 | `setRevoke()` | ✅ TP |  |
| 18 | `proxyAssert()` | ✅ TP |  |
| 19 | `proxyType()` | ✅ TP |  |
| 20 | `transferProxyOwnership()` | ✅ TP |  |
| 21 | `upgradeToAndCall()` | ✅ TP |  |

---

## [13] DSToken (Governance)

LOC: 371 | Est. Savings: 58,737 gas

### Redundant SLOAD — 14 temuan → TP=0 FP=0 ?=14 (precision≈n/a)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `owner` in `setOwner()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 2 | `authority` in `setAuthority()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 3 | `authority` in `isAuthorized()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 4 | `WAD` in `wmul()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 5 | `RAY` in `rmul()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 6 | `_approvals` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 7 | `_balances` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 8 | `_approvals` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 9 | `_balances` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 10 | `_balances` in `mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 11 | `_supply` in `mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 12 | `_approvals` in `burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 13 | `_balances` in `burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 14 | `_supply` in `burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |

### Public vs External — 21 temuan → TP=16 FP=5 ?=0 (precision≈76%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `canCall()` | ❌ FP | called internally at lines [141] |
| 2 | `setOwner()` | ✅ TP |  |
| 3 | `setAuthority()` | ✅ TP |  |
| 4 | `stop()` | ✅ TP |  |
| 5 | `start()` | ✅ TP |  |
| 6 | `totalSupply()` | ✅ TP |  |
| 7 | `balanceOf()` | ✅ TP |  |
| 8 | `allowance()` | ✅ TP |  |
| 9 | `transfer()` | ✅ TP |  |
| 10 | `approve()` | ❌ FP | called via super.approve() at lines [825, 833] |
| 11 | `totalSupply()` | ✅ TP |  |
| 12 | `balanceOf()` | ✅ TP |  |
| 13 | `allowance()` | ✅ TP |  |
| 14 | `transfer()` | ✅ TP |  |
| 15 | `approve()` | ❌ FP | called via super.approve() at lines [825, 833] |
| 16 | `approve()` | ❌ FP | called via super.approve() at lines [825, 833] |
| 17 | `approve()` | ❌ FP | called via super.approve() at lines [825, 833] |
| 18 | `push()` | ✅ TP |  |
| 19 | `pull()` | ✅ TP |  |
| 20 | `move()` | ✅ TP |  |
| 21 | `setName()` | ✅ TP |  |

### Dead Code — 8 temuan → TP=8 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `min()` | ✅ TP | no callers found in file |
| 2 | `max()` | ✅ TP | no callers found in file |
| 3 | `imin()` | ✅ TP | no callers found in file |
| 4 | `imax()` | ✅ TP | no callers found in file |
| 5 | `wmul()` | ✅ TP | no callers found in file |
| 6 | `wdiv()` | ✅ TP | no callers found in file |
| 7 | `rdiv()` | ✅ TP | no callers found in file |
| 8 | `rpow()` | ✅ TP | no callers found in file |

---

## [14] AvastarTeleporter (NFT)

LOC: 2171 | Est. Savings: 54,335 gas

### Redundant SLOAD — 37 temuan → TP=9 FP=2 ?=26 (precision≈82%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `minters` in `addMinter()` | ✅ TP | 2 reads, no assignment between them |
| 2 | `owners` in `addOwner()` | ✅ TP | 2 reads, no assignment between them |
| 3 | `admins` in `addSysAdmin()` | ✅ TP | 2 reads, no assignment between them |
| 4 | `admins` in `stripRoles()` | ✅ TP | 2 reads, no assignment between them |
| 5 | `minters` in `stripRoles()` | ✅ TP | 2 reads, no assignment between them |
| 6 | `owners` in `stripRoles()` | ✅ TP | 2 reads, no assignment between them |
| 7 | `_ownedTokensCount` in `_transferFrom()` | ✅ TP | 2 reads, no assignment between them |
| 8 | `_tokenApprovals` in `_clearApproval()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 9 | `_ownedTokens` in `_addTokenToOwnerEnumeration()` | ✅ TP | 2 reads, no assignment between them |
| 10 | `_allTokens` in `_addTokenToAllTokensEnumeration()` | ✅ TP | 2 reads, no assignment between them |
| 11 | `_ownedTokens` in `_removeTokenFromOwnerEnumeration()` | ❌ FP | assignment to `_ownedTokens` at body-line 22 between reads |
| 12 | `_ownedTokensIndex` in `_removeTokenFromOwnerEnumeration()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 13 | `_allTokens` in `_removeTokenFromAllTokensEnumeration()` | ❌ FP | assignment to `_allTokens` at body-line 24 between reads |
| 14 | `_allTokensIndex` in `_removeTokenFromAllTokensEnumeration()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 15 | `_tokenURIs` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 16 | `traits` in `getTraitInfoById()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 17 | `traits` in `getTraitNameById()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 18 | `traits` in `getTraitArtById()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 19 | `_name` in `createTrait()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 20 | `traits` in `createTrait()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 21 | `traits` in `extendTraitArt()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 22 | `tokenIdByGenerationWaveAndSerial` in `mintAvastar()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 23 | `avastars` in `mintAvastar()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 24 | `avastars` in `getAvastarWaveByTokenId()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 25 | `avastars` in `renderAvastar()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 26 | `primesByGeneration` in `getPrimeByGenerationAndSerial()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 27 | `avastars` in `getPrimeByTokenId()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 28 | `avastars` in `getPrimeReplicationByTokenId()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 29 | `primeCountByGenAndSeries` in `mintPrime()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 30 | `primesByGeneration` in `mintPrime()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 31 | `replicantsByGeneration` in `getReplicantByGenerationAndSerial()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 32 | `avastars` in `getReplicantByTokenId()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 33 | `replicantCountByGeneration` in `mintReplicant()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 34 | `replicantsByGeneration` in `mintReplicant()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 35 | `traitHandlerByPrimeTokenId` in `approveTraitAccess()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 36 | `avastars` in `useTraits()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 37 | `traitHandlerByPrimeTokenId` in `useTraits()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |

### String vs Bytes32 — 19 temuan → TP=16 FP=0 ?=3 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 2 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 3 | `TOKEN_NAME` | ✅ TP | value="Avastar" (7 chars ≤ 32) |
| 4 | `TOKEN_SYMBOL` | ✅ TP | value="AVASTAR" (7 chars ≤ 32) |
| 5 | `_a` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 6 | `_b` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 7 | `errorMessage` | ⚠️ ? | `errorMessage` not found as top-level state variable — may be inherited or local |
| 8 | `errorMessage` | ⚠️ ? | `errorMessage` not found as top-level state variable — may be inherited or local |
| 9 | `errorMessage` | ⚠️ ? | `errorMessage` not found as top-level state variable — may be inherited or local |
| 10 | `name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 11 | `symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 12 | `uri` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 13 | `name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 14 | `symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 15 | `_artist` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 16 | `_infoURI` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 17 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 18 | `_svg` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 19 | `_svg` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |

### Public vs External — 11 temuan → TP=10 FP=1 ?=0 (precision≈91%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `transferFrom()` | ✅ TP |  |
| 2 | `approve()` | ✅ TP |  |
| 3 | `setApprovalForAll()` | ✅ TP |  |
| 4 | `onERC721Received()` | ❌ FP | called internally at lines [2365] |
| 5 | `approve()` | ✅ TP |  |
| 6 | `setApprovalForAll()` | ✅ TP |  |
| 7 | `transferFrom()` | ✅ TP |  |
| 8 | `tokenOfOwnerByIndex()` | ✅ TP |  |
| 9 | `tokenByIndex()` | ✅ TP |  |
| 10 | `tokenOfOwnerByIndex()` | ✅ TP |  |
| 11 | `tokenByIndex()` | ✅ TP |  |

### Dead Code — 7 temuan → TP=7 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `uintToStr()` | ✅ TP | no callers found in file |
| 2 | `mul()` | ✅ TP | no callers found in file |
| 3 | `_msgData()` | ✅ TP | no callers found in file |
| 4 | `toPayable()` | ✅ TP | no callers found in file |
| 5 | `sendValue()` | ✅ TP | no callers found in file |
| 6 | `_tokensOfOwner()` | ✅ TP | no callers found in file |
| 7 | `_setTokenURI()` | ✅ TP | no callers found in file |

---

## [15] MANAToken (Token)

LOC: 222 | Est. Savings: 54,175 gas

### Redundant SLOAD — 8 temuan → TP=0 FP=0 ?=8 (precision≈n/a)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `balances` in `transfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 2 | `allowed` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 3 | `balances` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `allowed` in `approve()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 5 | `totalSupply` in `mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 6 | `balances` in `mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 7 | `balances` in `burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 8 | `totalSupply` in `burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |

### String vs Bytes32 — 2 temuan → TP=2 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `symbol` | ✅ TP | value="MANA" (4 chars ≤ 32) |
| 2 | `name` | ✅ TP | value="Decentraland MANA" (17 chars ≤ 32) |

### Public vs External — 19 temuan → TP=11 FP=8 ?=0 (precision≈58%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `balanceOf()` | ✅ TP |  |
| 2 | `transfer()` | ❌ FP | called via super.transfer() at lines [479] |
| 3 | `transferOwnership()` | ✅ TP |  |
| 4 | `pause()` | ✅ TP |  |
| 5 | `unpause()` | ✅ TP |  |
| 6 | `allowance()` | ✅ TP |  |
| 7 | `transferFrom()` | ❌ FP | called via super.transferFrom() at lines [487] |
| 8 | `approve()` | ✅ TP |  |
| 9 | `transfer()` | ❌ FP | called via super.transfer() at lines [479] |
| 10 | `balanceOf()` | ✅ TP |  |
| 11 | `transferFrom()` | ❌ FP | called via super.transferFrom() at lines [487] |
| 12 | `approve()` | ✅ TP |  |
| 13 | `allowance()` | ✅ TP |  |
| 14 | `mint()` | ✅ TP |  |
| 15 | `finishMinting()` | ✅ TP |  |
| 16 | `transfer()` | ❌ FP | called via super.transfer() at lines [479] |
| 17 | `transferFrom()` | ❌ FP | called via super.transferFrom() at lines [487] |
| 18 | `burn()` | ❌ FP | called via super.burn() at lines [551] |
| 19 | `burn()` | ❌ FP | called via super.burn() at lines [551] |

### Dead Code — 2 temuan → TP=2 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `mul()` | ✅ TP | no callers found in file |
| 2 | `div()` | ✅ TP | no callers found in file |

---

## [16] LinkToken (Token)

LOC: 250 | Est. Savings: 53,617 gas

### Redundant SLOAD — 5 temuan → TP=0 FP=0 ?=5 (precision≈n/a)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `balances` in `transfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 2 | `allowed` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 3 | `balances` in `transferFrom()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `allowed` in `increaseApproval()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 5 | `allowed` in `decreaseApproval()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |

### String vs Bytes32 — 2 temuan → TP=2 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `name` | ✅ TP | constant/immutable string, could be bytes32 |
| 2 | `symbol` | ✅ TP | constant/immutable string, could be bytes32 |

### Public vs External — 19 temuan → TP=6 FP=13 ?=0 (precision≈32%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `balanceOf()` | ✅ TP |  |
| 2 | `transfer()` | ❌ FP | called via super.transfer() at lines [381, 513] |
| 3 | `allowance()` | ✅ TP |  |
| 4 | `transferFrom()` | ❌ FP | called via super.transferFrom() at lines [567] |
| 5 | `approve()` | ❌ FP | called via super.approve() at lines [539] |
| 6 | `transferAndCall()` | ❌ FP | called via super.transferAndCall() at lines [487] |
| 7 | `onTokenTransfer()` | ❌ FP | called internally at lines [411] |
| 8 | `transfer()` | ❌ FP | called via super.transfer() at lines [381, 513] |
| 9 | `balanceOf()` | ✅ TP |  |
| 10 | `transferFrom()` | ❌ FP | called via super.transferFrom() at lines [567] |
| 11 | `approve()` | ❌ FP | called via super.approve() at lines [539] |
| 12 | `allowance()` | ✅ TP |  |
| 13 | `increaseApproval()` | ✅ TP |  |
| 14 | `decreaseApproval()` | ✅ TP |  |
| 15 | `transferAndCall()` | ❌ FP | called via super.transferAndCall() at lines [487] |
| 16 | `transferAndCall()` | ❌ FP | called via super.transferAndCall() at lines [487] |
| 17 | `transfer()` | ❌ FP | called via super.transfer() at lines [381, 513] |
| 18 | `approve()` | ❌ FP | called via super.approve() at lines [539] |
| 19 | `transferFrom()` | ❌ FP | called via super.transferFrom() at lines [567] |

### Dead Code — 2 temuan → TP=2 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `mul()` | ✅ TP | no callers found in file |
| 2 | `div()` | ✅ TP | no callers found in file |

---

## [17] Token (Governance)

LOC: 528 | Est. Savings: 53,579 gas

### Redundant SLOAD — 8 temuan → TP=0 FP=1 ?=7 (precision≈0%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_balances` in `_transfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 2 | `_totalSupply` in `_mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 3 | `_balances` in `_mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `_totalSupply` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 5 | `_balances` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 6 | `_owner` | ❌ FP | assignment to `_owner` at body-line 1050 between reads |
| 7 | `_owner` in `renounceOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |
| 8 | `_owner` in `_transferOwnership()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |

### String vs Bytes32 — 7 temuan → TP=4 FP=0 ?=3 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 2 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 3 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 4 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 5 | `name` | ⚠️ ? | `name` not found as top-level state variable — may be inherited or local |
| 6 | `symbol` | ⚠️ ? | `symbol` not found as top-level state variable — may be inherited or local |
| 7 | `name` | ⚠️ ? | `name` not found as top-level state variable — may be inherited or local |

### Public vs External — 17 temuan → TP=17 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `totalSupply()` | ✅ TP |  |
| 2 | `balanceOf()` | ✅ TP |  |
| 3 | `transfer()` | ✅ TP |  |
| 4 | `allowance()` | ✅ TP |  |
| 5 | `approve()` | ✅ TP |  |
| 6 | `transferFrom()` | ✅ TP |  |
| 7 | `increaseAllowance()` | ✅ TP |  |
| 8 | `decreaseAllowance()` | ✅ TP |  |
| 9 | `name()` | ✅ TP |  |
| 10 | `symbol()` | ✅ TP |  |
| 11 | `burn()` | ✅ TP |  |
| 12 | `burnFrom()` | ✅ TP |  |
| 13 | `owner()` | ✅ TP |  |
| 14 | `renounceOwnership()` | ✅ TP |  |
| 15 | `transferOwnership()` | ✅ TP |  |
| 16 | `changeName()` | ✅ TP |  |
| 17 | `name()` | ✅ TP |  |

### Dead Code — 3 temuan → TP=3 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `mul()` | ✅ TP | no callers found in file |
| 2 | `div()` | ✅ TP | no callers found in file |
| 3 | `mod()` | ✅ TP | no callers found in file |

---

## [18] YFI (Governance)

LOC: 191 | Est. Savings: 46,911 gas

### Redundant SLOAD — 6 temuan → TP=0 FP=0 ?=6 (precision≈n/a)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_balances` in `_transfer()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 2 | `_totalSupply` in `_mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 3 | `_balances` in `_mint()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `_balances` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 5 | `_totalSupply` in `_burn()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 6 | `governance` in `setGovernance()` | ⚠️ ? | only 1 reads found in function body — may be cross-function or parse issue |

### String vs Bytes32 — 6 temuan → TP=2 FP=0 ?=4 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_name` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 2 | `_symbol` | ✅ TP | no literal initializer; string state var likely short (name/symbol/version pa... |
| 3 | `name` | ⚠️ ? | `name` not found as top-level state variable — may be inherited or local |
| 4 | `symbol` | ⚠️ ? | `symbol` not found as top-level state variable — may be inherited or local |
| 5 | `errorMessage` | ⚠️ ? | `errorMessage` not found as top-level state variable — may be inherited or local |
| 6 | `errorMessage` | ⚠️ ? | `errorMessage` not found as top-level state variable — may be inherited or local |

### Public vs External — 15 temuan → TP=14 FP=1 ?=0 (precision≈93%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `totalSupply()` | ✅ TP |  |
| 2 | `balanceOf()` | ✅ TP |  |
| 3 | `transfer()` | ✅ TP |  |
| 4 | `allowance()` | ❌ FP | called internally at lines [347] |
| 5 | `approve()` | ✅ TP |  |
| 6 | `transferFrom()` | ✅ TP |  |
| 7 | `increaseAllowance()` | ✅ TP |  |
| 8 | `decreaseAllowance()` | ✅ TP |  |
| 9 | `name()` | ✅ TP |  |
| 10 | `symbol()` | ✅ TP |  |
| 11 | `decimals()` | ✅ TP |  |
| 12 | `mint()` | ✅ TP |  |
| 13 | `setGovernance()` | ✅ TP |  |
| 14 | `addMinter()` | ✅ TP |  |
| 15 | `removeMinter()` | ✅ TP |  |

### Dead Code — 5 temuan → TP=5 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `_burn()` | ✅ TP | no callers found in file |
| 2 | `mul()` | ✅ TP | no callers found in file |
| 3 | `safeTransfer()` | ✅ TP | no callers found in file |
| 4 | `safeTransferFrom()` | ✅ TP | no callers found in file |
| 5 | `safeApprove()` | ✅ TP | no callers found in file |

---

## [19] MultiSigWallet (Utility)

LOC: 334 | Est. Savings: 33,931 gas

### Redundant SLOAD — 11 temuan → TP=0 FP=0 ?=11 (precision≈n/a)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `isOwner` in `MultiSigWallet()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 2 | `owners` in `removeOwner()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 3 | `owners` in `replaceOwner()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 4 | `isOwner` in `replaceOwner()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 5 | `owners` in `isConfirmed()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 6 | `transactionCount` in `addTransaction()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 7 | `owners` in `getConfirmationCount()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 8 | `transactions` in `getTransactionCount()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 9 | `owners` in `getConfirmations()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 10 | `transactionCount` in `getTransactionIds()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |
| 11 | `transactions` in `getTransactionIds()` | ⚠️ ? | only 0 reads found in function body — may be cross-function or parse issue |

### Unoptimized Loop — 5 temuan → TP=5 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `owners.length` | ✅ TP | state array `.length` in for-loop at line 279 |
| 2 | `owners.length` | ✅ TP | state array `.length` in for-loop at line 279 |
| 3 | `owners.length` | ✅ TP | state array `.length` in for-loop at line 279 |
| 4 | `owners.length` | ✅ TP | state array `.length` in for-loop at line 279 |
| 5 | `owners.length` | ✅ TP | state array `.length` in for-loop at line 279 |

### Public vs External — 10 temuan → TP=10 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `addOwner()` | ✅ TP |  |
| 2 | `removeOwner()` | ✅ TP |  |
| 3 | `replaceOwner()` | ✅ TP |  |
| 4 | `submitTransaction()` | ✅ TP |  |
| 5 | `revokeConfirmation()` | ✅ TP |  |
| 6 | `getConfirmationCount()` | ✅ TP |  |
| 7 | `getTransactionCount()` | ✅ TP |  |
| 8 | `getOwners()` | ✅ TP |  |
| 9 | `getConfirmations()` | ✅ TP |  |
| 10 | `getTransactionIds()` | ✅ TP |  |

---

## [20] AppProxyUpgradeable (DeFi)

LOC: 279 | Est. Savings: 21,384 gas

### Public vs External — 8 temuan → TP=7 FP=1 ?=0 (precision≈88%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `hasPermission()` | ✅ TP |  |
| 2 | `acl()` | ✅ TP |  |
| 3 | `hasPermission()` | ✅ TP |  |
| 4 | `setApp()` | ✅ TP |  |
| 5 | `getApp()` | ❌ FP | called internally at lines [709] |
| 6 | `proxyType()` | ✅ TP |  |
| 7 | `isDepositable()` | ✅ TP |  |
| 8 | `proxyType()` | ✅ TP |  |

### Dead Code — 3 temuan → TP=3 FP=0 ?=0 (precision≈100%)

| # | Subject | Verdict | Alasan |
|---|---|---|---|
| 1 | `getStorageUint256()` | ✅ TP | no callers found in file |
| 2 | `setStorageUint256()` | ✅ TP | no callers found in file |
| 3 | `setDepositable()` | ✅ TP | no callers found in file |

---
