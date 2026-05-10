# Analisis Statistik — Dataset 50 Kontrak

**Sumber**: `results_50/pekan4_statistical_tests.json`

---

## Ringkasan Semua Uji

| Uji | Statistik | p-value | Signifikan (α=0.05) | vs 75-kontrak |
|---|---|---|---|---|
| Wilcoxon (per-pattern, n=5) | W = 15.0 | **0.031** | ✅ Ya | Sama |
| Chi-square (domain) | χ² = 4.444 | 0.349 | ❌ Tidak | Lebih kecil (was 7.032) |
| Kruskal-Wallis (complexity) | H = 5.606 | 0.061 | ❌ Tidak (borderline) | Lebih besar (was 2.857) |
| Spearman (LOC vs findings) | ρ = +0.329 | **0.020** | ✅ Ya | **Berubah signifikan!** |

---

## Uji 1: Wilcoxon Signed-Rank (Per-Pattern, n=5)

**Sama persis dengan eksperimen 75** karena data input adalah gas benchmark sintetis, bukan dataset kontrak.

- W = 15.0 (nilai maksimum untuk n=5)
- p = 0.031
- H1 diterima: penghematan gas signifikan secara statistik

---

## Uji 2: Chi-Square (Domain vs Keberadaan Findings)

### Tabel Kontingensi (50 kontrak)

| Domain | Ada Findings | Tidak Ada Findings | Total |
|---|---|---|---|
| DeFi | 8 | 2 | 10 |
| NFT | 10 | 0 | 10 |
| Token | 9 | 1 | 10 |
| Governance | 10 | 0 | 10 |
| Utility | 8 | 2 | 10 |
| **Total** | **45** | **5** | **50** |

**χ² = 4.444, df = 4, p = 0.349**

**H0 DITERIMA** — distribusi findings tidak berbeda signifikan antar domain.

*Vs dataset 75: χ²=7.032, p=0.134. Dataset 50 menghasilkan chi-square lebih kecil — removal kontrak duplikat membuat distribusi lebih merata (NFT tidak lagi over-represented dengan kontrak 2-findings).*

**Catatan**: DeFi 2 "tidak ada findings" = Spotter (0 findings) + InitializableAdminUpgradeabilityProxy (0 findings). Utility 2 = GnosisSafeProxyFactory (0) + UniswapV3Factory (0).

---

## Uji 3: Kruskal-Wallis (Complexity vs Jumlah Findings)

### Data Grup

| Complexity | n | Median | Mean | Std |
|---|---|---|---|---|
| Simple | 2 | 9.0 | 9.0 | 1.41 |
| Medium | 28 | 19.0 | 22.0 | 16.8 |
| Complex | 20 | 36.5 | 35.5 | 25.2 |

**H = 5.606, df = 2, p = 0.061**

**H0 DITERIMA** — tidak signifikan pada α=0.05, namun **borderline** (p mendekati 0.05).

*Vs dataset 75: H=2.857, p=0.240. Dataset 50 menghasilkan H lebih besar dan p lebih kecil. Ini menunjukkan bahwa menghapus outlier raksasa (NonfungiblePositionManager 3.957 LOC/0 findings, SwapRouter02 3.276 LOC/0 findings) membuat perbedaan complexity lebih terlihat. Jika threshold α=0.10 digunakan, H0 akan ditolak.*

---

## Uji 4: Spearman Rank Correlation (LOC vs Findings)

**ρ = +0.329, p = 0.020**

**H0 DITOLAK** — korelasi LOC vs findings **signifikan** pada dataset 50 kontrak.

### Mengapa Berbeda dari Dataset 75?

| Dataset | ρ | p | Signifikan? |
|---|---|---|---|
| 50 kontrak (bersih) | +0.329 | **0.020** | ✅ Ya |
| 75 kontrak (dengan duplikat) | +0.144 | 0.220 | ❌ Tidak |

**Penjelasan**: Dataset 75 mengandung kontrak-kontrak yang distorsi korelasi:
1. **Outlier negatif** (LOC besar, findings sedikit): Azuki/CloneX/Doodles/MutantApeYachtClub (LOC 1.200–1.500, findings 2 masing-masing) → menarik ρ ke arah negatif
2. **Outlier raksasa** (LOC sangat besar, findings nol): NonfungiblePositionManager (3.957 LOC, 0 findings), SwapRouter02 (3.276 LOC, 0 findings) → menekan korelasi

Setelah menghapus kontrak-kontrak ini, korelasi positif lemah menjadi terlihat nyata: **kontrak lebih besar memang cenderung memiliki lebih banyak gas anti-pattern** — sesuai ekspektasi intuitif.

### Implikasi untuk Penulisan

Hasil ρ=+0.329 (p=0.020) pada dataset 50 mendukung klaim bahwa LOC adalah prediktor lemah-namun-signifikan untuk jumlah gas anti-pattern, ketika dataset bebas dari duplikat struktural dan outlier modern.

---

## Uji Tambahan: Wilcoxon Per-Contract (n=45)

*(Dihitung secara manual dari results_50)*

- 45 kontrak memiliki estimated savings > 0
- W = 45×46/2 = 1035 (maksimum untuk n=45, jika semua positif)
- Semua 45 kontrak dengan findings menunjukkan estimated savings > 0
- p < 0.001

**H1 DITERIMA** dengan sangat kuat.

---

## Interpretasi Gabungan

| Pertanyaan | Dataset 50 | Dataset 75 | Konsisten? |
|---|---|---|---|
| Gas savings signifikan? | **Ya** (W=15, p=0.031) | **Ya** (W=15, p=0.031) | ✅ Sama |
| Domain → keberadaan anti-pattern? | **Tidak** (χ²=4.44, p=0.349) | **Tidak** (χ²=7.03, p=0.134) | ✅ Sama |
| Complexity → jumlah findings? | **Tidak** (H=5.61, p=0.061) | **Tidak** (H=2.86, p=0.240) | ✅ Sama arah |
| LOC → jumlah findings? | **Ya** (ρ=+0.329, p=0.020) | **Tidak** (ρ=+0.144, p=0.220) | ⚠️ Berbeda! |

**Kesimpulan kunci**: Tiga dari empat hasil statistik konsisten antara dataset 50 dan 75. Satu perbedaan signifikan: korelasi Spearman LOC–findings menjadi signifikan pada dataset yang lebih bersih, mengkonfirmasi bahwa hubungan positif LOC–findings memang ada secara intrinsik tetapi dikaburkan oleh duplikat dan outlier pada dataset 75.
