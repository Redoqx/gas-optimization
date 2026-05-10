# Gambaran Umum Eksperimen 50 Kontrak

**Branch**: `experiment/50-contracts`  
**Dataset**: `contracts_selection_50.json` — 50 kontrak, 10 per domain  
**Tujuan**: Replikasi eksperimen utama dengan dataset yang lebih bersih (tanpa duplikat struktural)

---

## Ringkasan Hasil

| Metrik | Nilai |
|---|---|
| Total kontrak | 50 |
| Compile OK | 50 (100%) |
| Kontrak dengan ≥1 temuan | 45 (90.0%) |
| Total temuan | **1.383** |
| Rata-rata temuan/kontrak | 27.7 |
| Median temuan/kontrak | 26.5 |
| Maksimum temuan | 90 (DCLRegistrar, NFT) |

---

## Distribusi Temuan per Domain

| Domain | n | rs | ul | sb | pe | ua | dc | TOTAL | Avg |
|---|---|---|---|---|---|---|---|---|---|
| DeFi | 10 | 148 | 2 | 22 | 45 | 0 | 23 | **240** | 24.0 |
| NFT | 10 | 208 | 0 | 94 | 150 | 0 | 34 | **486** | 48.6 |
| Token | 10 | 110 | 0 | 27 | 179 | 0 | 27 | **343** | 34.3 |
| Governance | 10 | 67 | 0 | 52 | 80 | 0 | 16 | **215** | 21.5 |
| Utility | 10 | 28 | 5 | 2 | 64 | 0 | 0 | **99** | 9.9 |
| **TOTAL** | **50** | **561** | **7** | **197** | **518** | **0** | **100** | **1.383** | **27.7** |

**Keterangan**: rs=redundant_sload, ul=unoptimized_loop, sb=string_vs_bytes32, pe=public_vs_external, ua=unchecked_arithmetic, dc=dead_code

---

## Distribusi Temuan per Anti-Pattern

| Anti-Pattern | Jumlah | % dari Total |
|---|---|---|
| redundant_sload | 561 | 40.6% |
| public_vs_external | 518 | 37.5% |
| string_vs_bytes32 | 197 | 14.2% |
| dead_code | 100 | 7.2% |
| unoptimized_loop | 7 | 0.5% |
| unchecked_arithmetic | 0 | 0.0% |

---

## Hasil Statistik Utama

| Uji | Statistik | p-value | Signifikan? |
|---|---|---|---|
| Wilcoxon signed-rank (gas savings, n=5) | W = 15.0 | **0.031** | ✅ Ya |
| Chi-square (domain vs keberadaan findings) | χ² = 4.44 | 0.349 | ❌ Tidak |
| Kruskal-Wallis (complexity vs findings) | H = 5.606 | 0.061 | ❌ Tidak |
| Spearman (LOC vs findings) | ρ = +0.329 | **0.020** | ✅ Ya |

**Temuan kunci**: Spearman ρ = +0.329 (p=0.020) **signifikan** — berbeda dari dataset 75 kontrak (ρ=+0.144, p=0.220 tidak signifikan). Pada dataset yang lebih bersih, kontrak lebih besar memang cenderung memiliki lebih banyak gas anti-pattern.

---

## Perbandingan Cepat: 50 vs 75 Kontrak

| Metrik | 50 kontrak | 75 kontrak |
|---|---|---|
| Total findings | 1.383 | 1.655 |
| Avg findings/contract | 27.7 | 22.4 |
| % contracts with findings | 90.0% | 89.2% |
| Spearman ρ (LOC vs findings) | **+0.329** (sig.) | +0.144 (tidak sig.) |
| Chi-square domain (p) | 0.349 | 0.134 |
| KW complexity (p) | 0.061 | 0.240 |
| Wilcoxon gas savings (p) | 0.031 | 0.031 |
