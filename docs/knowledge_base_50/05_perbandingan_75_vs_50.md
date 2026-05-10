# Perbandingan Dataset 75 vs 50 Kontrak

Dokumen ini menganalisis perbedaan hasil eksperimen antara dataset 75 kontrak (branch `main`) dan dataset 50 kontrak yang lebih bersih (branch `experiment/50-contracts`).

---

## 1. Perbandingan Ukuran dan Coverage

| Metrik | Dataset 75 | Dataset 50 | Selisih |
|---|---|---|---|
| Total kontrak | 75 | 50 | -25 (33%) |
| Compile OK | 74 | 50 | -24 |
| % compile OK | 98.7% | 100% | +1.3% |
| Kontrak dgn findings | 66 (89.2%) | 45 (90.0%) | +0.8% |
| Total findings | 1.655 | 1.383 | -272 (16.4%) |
| Avg findings/contract | 22.4 | 27.7 | +5.3 |
| Max findings | 90 (DCLRegistrar) | 90 (DCLRegistrar) | Sama |

**Interpretasi**: Pengurangan 25 kontrak menghasilkan pengurangan 272 findings (-16.4%). Artinya kontrak yang dihapus rata-rata memiliki `272/25 = 10.9 findings/contract` — jauh di bawah rata-rata 50-contract dataset (27.7). Kontrak yang dihapus adalah kontrak dengan findings rendah (duplikat, modern, atau proxy generik).

---

## 2. Perbandingan per Domain

| Domain | 75 kontrak | 50 kontrak | Selisih findings | Avg 75 | Avg 50 |
|---|---|---|---|---|---|
| DeFi | 262 (15 kontrak) | 240 (10 kontrak) | -22 | 17.5 | 24.0 |
| NFT | 539 (15 kontrak) | 486 (10 kontrak) | -53 | 35.9 | 48.6 |
| Token | 478 (15 kontrak) | 343 (10 kontrak) | -135 | 31.9 | 34.3 |
| Governance | 272 (15 kontrak) | 215 (10 kontrak) | -57 | 18.1 | 21.5 |
| Utility | 104 (14 kontrak) | 99 (10 kontrak) | -5 | 7.4 | 9.9 |

**Temuan menarik**:
- **Token domain pengurangan terbesar** (-135 findings) padahal hanya berkurang 5 kontrak. Kontrak yang dihapus termasuk AdminUpgradeabilityProxy PAXG (68 findings) + OwnedUpgradeabilityProxy TUSD (41 findings) + SimpleToken/ApeCoin (2 findings) + ProxyERC20 (23 findings) + LQTYToken (1 finding) = 135 findings. Konsisten.
- **NFT pengurangan moderat** (-53) untuk 5 kontrak. Kontrak yang dihapus: Azuki (2), CloneX (2), Doodles (2), MutantApeYachtClub (2), AdminUpgradeabilityProxy (45) = 53 findings. Konsisten.
- **Utility hampir sama** (-5 findings) meski -4 kontrak. Jug(3)+ReverseRegistrar(2)+NonfungiblePositionManager(0)+SwapRouter02(0) = 5. Konsisten.
- **Avg 50 selalu lebih tinggi dari avg 75** — mengkonfirmasi bahwa kontrak yang dihapus memang yang ber-findings rendah.

---

## 3. Perbandingan per Anti-Pattern

| Anti-Pattern | Dataset 75 | % 75 | Dataset 50 | % 50 | Selisih |
|---|---|---|---|---|---|
| redundant_sload | 634 | 38.3% | 561 | 40.6% | -73 |
| public_vs_external | 649 | 39.2% | 518 | 37.5% | -131 |
| string_vs_bytes32 | 243 | 14.7% | 197 | 14.2% | -46 |
| dead_code | 122 | 7.4% | 100 | 7.2% | -22 |
| unoptimized_loop | 7 | 0.4% | 7 | 0.5% | 0 |
| unchecked_arithmetic | 0 | 0.0% | 0 | 0.0% | 0 |

**Temuan penting**:
- **Urutan dominasi berubah**: Dataset 75 → public_vs_external #1 (39.2%), dataset 50 → redundant_sload #1 (40.6%). Ini karena kontrak yang dihapus banyak yang memiliki `public_vs_external` (3 GovernorBravo, 2 AdminUpgradeabilityProxy Token, dll) — `public_vs_external` berkurang lebih banyak (-131) dibanding `redundant_sload` (-73).
- **Proporsi dead_code dan string_vs_bytes32 stabil** — perubahan distribusi minor.
- **unoptimized_loop identik** (7 findings) — kedua dataset mempertahankan MultiSigWallet dan KyberNetworkProxy.

---

## 4. Perbandingan Statistik

| Uji | Dataset 75 | Dataset 50 | Interpretasi |
|---|---|---|---|
| Wilcoxon gas savings | W=15, p=0.031 ✅ | W=15, p=0.031 ✅ | Identik — benchmark sintetis tidak berubah |
| Chi-square domain | χ²=7.03, p=0.134 ❌ | χ²=4.44, p=0.349 ❌ | Sama arah; dataset 50 lebih merata |
| KW complexity | H=2.86, p=0.240 ❌ | H=5.61, p=0.061 ❌ | Dataset 50 lebih dekat signifikan |
| Spearman LOC | ρ=+0.144, p=0.220 ❌ | ρ=+0.329, p=0.020 ✅ | **Berubah arah signifikansi!** |
| KW domain × savings | H=18.41, p=0.001 ✅ | *tidak di-rerun* | — |
| McNemar Slither | p=0.00391 ✅ | ~sama (reused) | Tidak berubah |

---

## 5. Implikasi untuk Penulisan Tesis

### Kapan menggunakan dataset 75?
- Sebagai **dataset utama** (lebih besar, lebih representatif dari populasi kontrak mainnet yang ada)
- Untuk menunjukkan cakupan domain yang luas
- Untuk referensi angka statistik yang lebih konservatif (Spearman tidak signifikan → lebih defensible)

### Kapan menggunakan dataset 50?
- Sebagai **sensitivity analysis** atau **robustness check**
- Untuk argumen bahwa temuan tidak bergantung pada kontrak duplikat
- Untuk menunjukkan bahwa korelasi LOC–findings muncul ketika dataset "bersih"
- Untuk mendukung klaim bahwa anti-pattern boros gas adalah masalah universal (% kontrak dengan findings sama: 90% vs 89.2%)

### Pernyataan yang dapat digunakan dalam tesis
> "Sebagai uji ketahanan (robustness check), eksperimen direplikasi pada subset 50 kontrak yang lebih bersih (10 per domain) setelah menghilangkan duplikat struktural dan kontrak proxy generik. Tiga dari empat uji statistik menghasilkan kesimpulan yang konsisten. Perbedaan utama adalah korelasi Spearman LOC–findings yang menjadi signifikan (ρ=+0.329, p=0.020) pada dataset yang lebih homogen, mengkonfirmasi bahwa hubungan positif antara ukuran kontrak dan jumlah gas anti-pattern memang ada tetapi dikaburkan oleh outlier pada dataset utama."

---

## 6. Ringkasan: Apa yang Berubah, Apa yang Stabil

### Stabil (konsisten antara kedua dataset)
- ✅ Penghematan gas signifikan secara statistik (Wilcoxon W=15, p=0.031)
- ✅ Domain tidak mempengaruhi keberadaan anti-pattern (Chi-square tidak signifikan)
- ✅ unchecked_arithmetic = 0 findings di kedua dataset
- ✅ dead_code = 0% gas savings (compiler behavior identik)
- ✅ DCLRegistrar tetap kontrak dengan findings terbanyak (90) di kedua dataset
- ✅ NFT domain tertinggi (35.1% vs 32.6%)
- ✅ Utility domain terendah (7.2% vs 6.3%)
- ✅ 89–90% kontrak memiliki ≥1 finding

### Berubah (berbeda signifikan antara kedua dataset)
- ⚠️ Urutan dominasi pattern: public_vs_external #1 (75) vs redundant_sload #1 (50)
- ⚠️ Spearman ρ: tidak signifikan (75) → **signifikan** (50)
- ⚠️ KW complexity: H=2.86 (75) → H=5.61 (50) — lebih dekat threshold
- ⚠️ Avg findings/contract: 22.4 (75) → 27.7 (50) — meningkat signifikan
