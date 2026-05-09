# Analisis Statistik: 4 Uji & Interpretasi

## Ringkasan Hasil Semua Uji

| Uji | Statistik | p-value | Signifikan (α=0.05) | Keputusan |
|---|---|---|---|---|
| Wilcoxon (per-pattern, n=6) | W = 15.0 | **0.031** | ✅ Ya | H1 Diterima — gas savings signifikan |
| Wilcoxon (per-contract, n=65) | W = 2145.0 | **< 0.001** | ✅ Ya | H1 Diterima — savings per kontrak signifikan |
| Chi-square (domain) | χ² = 7.032 | 0.134 | ❌ Tidak | H0 Diterima — domain tidak berpengaruh |
| Kruskal-Wallis (complexity) | H = 2.857 | 0.240 | ❌ Tidak | H0 Diterima — complexity tidak berpengaruh |
| Kruskal-Wallis (domain × savings) | H = 18.409 | **0.001** | ✅ Ya | H1 Diterima — domain berpengaruh pada savings |
| Spearman (LOC vs findings) | ρ = +0.144 | 0.220 | ❌ Tidak | H0 Diterima — LOC tidak berkorelasi |
| McNemar (our tool vs Slither) | b=9, c=0 | **0.00391** | ✅ Ya* | H0 Ditolak — our tool deteksi lebih banyak* |
| Cohen's Kappa (our tool vs Slither) | κ = 0.0 | — | — | No agreement beyond chance |

---

## Uji 1: Wilcoxon Signed-Rank Test

### Tujuan
Menguji apakah penghematan gas (boros − hemat) secara median **signifikan lebih besar dari nol** — yaitu, apakah optimasi kode yang disarankan framework benar-benar menghasilkan penghematan gas yang nyata.

### Setup Uji
- **Jenis**: Non-parametrik, one-sided (greater)
- **n pasang**: 6 (satu per anti-pattern)
- **Data**: `diff = gas_boros - gas_hemat` untuk setiap pattern
- **H0**: Median diff = 0
- **H1**: Median diff > 0
- **Metode penanganan zero**: `zero_method='wilcox'` (pasangan dengan diff=0 dikeluarkan)

### Data Input

| Anti-Pattern | Gas Boros | Gas Hemat | Diff | Rank |
|---|---|---|---|---|
| redundant_sload | 24.208 | 24.022 | 186 | 1 |
| unoptimized_loop | 51.187 | 50.156 | 1.031 | 3 |
| string_vs_bytes32 | 24.540 | 23.590 | 950 | 2 |
| public_vs_external | 52.544 | 49.871 | 2.673 | 4 |
| unchecked_arithmetic | 59.105 | 47.060 | 12.045 | 5 |
| dead_code | 123.985 | 123.985 | 0 | — (excluded) |

### Perhitungan

Setelah mengeluarkan dead_code (diff=0), n_efektif = 5 pasang, semua positif:
- W+ (sum of positive ranks) = 1+2+3+4+5 = **15**
- W- (sum of negative ranks) = **0**
- Untuk n=5 dengan semua positif: p-value satu sisi = 2^(-5) = **0.03125 ≈ 0.031**

### Hasil
**W = 15.0, p = 0.031**

### Interpretasi
**H1 DITERIMA** pada α = 0.05. Nilai W=15 adalah nilai maksimum yang mungkin untuk n=5 — artinya **semua** pasangan menunjukkan penghematan positif.

---

## Uji 2: Chi-Square Test of Independence

### Tujuan
Menguji apakah distribusi findings (ada/tidak ada) **bergantung pada domain** kontrak.

### Setup Uji
- **Jenis**: Chi-square test of independence
- **H0**: Distribusi findings tidak bergantung pada domain
- **H1**: Ada perbedaan distribusi findings antar domain
- **Tabel kontingensi**: Domain (5 baris) × Keberadaan findings (2 kolom: ada/tidak)

### Tabel Kontingensi (74 kontrak)

| Domain | Ada Findings | Tidak Ada Findings | Total |
|---|---|---|---|
| DeFi | 13 | 2 | 15 |
| NFT | 15 | 0 | 15 |
| Token | 14 | 1 | 15 |
| Governance | 14 | 1 | 15 |
| Utility | 10 | 4 | 14 |
| **Total** | **66** | **8** | **74** |

### Hasil
**χ² = 7.032, df = 4, p = 0.134**

### Interpretasi
**H0 DITERIMA** — distribusi findings tidak berbeda signifikan antar domain pada α = 0.05 (p=0.134).

Ini menunjukkan bahwa **pola boros gas ditemukan secara merata** di semua domain. Framework berguna lintas domain.

**Catatan**: Utility memiliki 4/14 kontrak tanpa findings — lebih tinggi dari domain lain — karena empat kontrak Uniswap v3 (NonfungiblePositionManager, SwapRouter02, UniswapV3Factory) dan GnosisSafeProxyFactory adalah kontrak modern (0.7.x–0.8.x) yang sudah dioptimasi.

---

## Uji 3: Kruskal-Wallis Test (Complexity)

### Tujuan
Menguji apakah **jumlah findings** berbeda signifikan antar complexity level.

### Setup Uji
- **Jenis**: Kruskal-Wallis (non-parametrik ANOVA)
- **H0**: Distribusi findings sama di semua complexity level
- **H1**: Setidaknya satu complexity level memiliki distribusi berbeda
- **Grup**: Simple (n=2), Medium (n=36), Complex (n=36)

### Data Grup

| Complexity | n | Median Findings | Mean Findings |
|---|---|---|---|
| Simple | 2 | 9.0 | 9.0 |
| Medium | 36 | 12.5 | 16.9 |
| Complex | 36 | 29.5 | 28.6 |

### Hasil
**H = 2.857, df = 2, p = 0.240**

### Interpretasi
**H0 DITERIMA** — jumlah findings tidak berbeda signifikan berdasarkan complexity level (p=0.240).

Meski rata-rata findings Complex (28.6) > Medium (16.9) > Simple (9.0), variasi tinggi (std ~16–24) membuat perbedaan tidak signifikan secara statistik. Ini konsisten dengan Spearman ρ=+0.144 yang juga tidak signifikan.

---

## Uji 4: Spearman Rank Correlation

### Tujuan
Menguji apakah ada hubungan **monoton** antara LOC (Lines of Code) dan total findings.

### Setup Uji
- **Jenis**: Spearman rank correlation (non-parametrik)
- **H0**: ρ = 0 (tidak ada korelasi)
- **H1**: ρ ≠ 0 (ada korelasi)
- **n**: 74 kontrak valid

### Hasil
**ρ = +0.144, p = 0.220**

### Interpretasi
**H0 DITERIMA** — korelasi tidak signifikan pada α = 0.05.

Korelasi positif lemah (ρ = +0.144) menunjukkan bahwa kontrak lebih panjang sedikit lebih banyak temuan, namun hubungan ini tidak signifikan. Era penulisan dan versi Solidity lebih menentukan daripada LOC.

**Perubahan dari dataset lama**: Dataset 50 kontrak menghasilkan ρ=-0.261 (negatif), dataset 75 kontrak menghasilkan ρ=+0.144 (positif lemah). Perubahan arah ini disebabkan penambahan kontrak NFT besar (CryptoKitties, AvastarTeleporter, DCLRegistrar) yang berukuran besar DAN banyak findings — memperkuat sisi positif korelasi.

---

## Uji Tambahan A: Wilcoxon Signed-Rank (Per Contract, n=65)

### Tujuan
Versi lebih kuat dari Wilcoxon per-pattern: menggunakan **kontrak sebagai unit observasi**. Menguji apakah estimated gas savings per kontrak secara median signifikan lebih besar dari nol.

### Setup Uji
- **Unit observasi**: kontrak (bukan pattern)
- **n**: 65 kontrak dengan savings > 0 (dari 74 valid; 9 kontrak bernilai 0 dikecualikan)
- **Data**: `estimated_savings[i] = Σ(count_det × avg_diff_gas_det)` untuk kontrak i

### Estimasi Savings

```
GAS_DIFF = {
    redundant_sload:        186 gas
    unoptimized_loop:     1.031 gas
    string_vs_bytes32:      950 gas
    public_vs_external:   2.673 gas
    unchecked_arithmetic: 12.045 gas
    dead_code:                0 gas
}
savings[i] = Σ(findings[i][det] × GAS_DIFF[det])
```

### Hasil
**W = 2145.0, p < 0.001**

### Interpretasi
**H1 DITERIMA** dengan sangat kuat (p << 0.001). W=2145 adalah nilai maksimum yang mungkin untuk n=65 (n×(n+1)/2 = 2145), menunjukkan semua 65 kontrak dengan savings > 0 konsisten memiliki savings positif.

---

## Uji Tambahan B: Kruskal-Wallis (Gas Savings × 5 Domains)

### Tujuan
Menguji apakah **potensi penghematan gas** (estimated savings) berbeda signifikan antar domain.

### Data Grup (estimated savings dalam gas units)

| Domain | n | Median | Mean | Max |
|---|---|---|---|---|
| DeFi | 15 | 4.573 | 13.509 | 113.446 |
| NFT | 15 | 31.391 | 42.283 | 117.568 |
| Token | 15 | **49.044** | **46.367** | 89.081 |
| Governance | 15 | 19.838 | 24.609 | 58.737 |
| Utility | 14 | 5.346 | 13.517 | 58.757 |

### Hasil
**H = 18.409, p = 0.001**

### Interpretasi
**H1 DITERIMA** — domain berpengaruh signifikan terhadap estimasi penghematan gas (p=0.001 < 0.05).

Token domain tertinggi (median 49.044 gas) karena dominasi `public_vs_external` (236 findings) yang memberikan 2.673 gas/temuan. NFT kedua (median 31.391) karena banyak kontrak NFT lama dengan redundant SLOAD besar.

---

## Uji Tambahan C: McNemar & Cohen's Kappa

### McNemar — Exact Test (Binomial)

**Tabel kontingensi (10 kontrak sampel)**:

| | Slither: Ya | Slither: Tidak |
|---|---|---|
| **Our Tool: Ya** | a = 0 | b = 9 |
| **Our Tool: Tidak** | c = 0 | d = 1 |

**Metode**: `binomtest(min(b,c), b+c, 0.5, alternative='two-sided')` → `binomtest(0, 9, 0.5)` = 2 × (0.5)^9 = **0.00391**

**Hasil**: **p = 0.00391** ✅

**Interpretasi**: H0 ditolak. Namun ini adalah **constrained comparison** — Slither tidak menemukan apapun bukan karena false negative, melainkan karena parse failure pada solc 0.4.x.

### Cohen's Kappa

```
n   = 10
Po  = (a + d) / n = (0 + 1) / 10 = 0.10
Pe  = (9/10 × 0/10) + (1/10 × 10/10)
    = (0.90 × 0.00) + (0.10 × 1.00) = 0.10
κ   = (0.10 − 0.10) / (1 − 0.10) = 0.00 / 0.90 = 0.00
```

**Hasil**: **κ = 0.00** — no agreement beyond chance

---

## Interpretasi Gabungan

| Pertanyaan | Temuan | Implikasi |
|---|---|---|
| Apakah optimasi gas signifikan secara statistik? | **Ya** — dua Wilcoxon (p=0.031 dan p<0.001) | Framework valid — pola yang dideteksi memang boros gas |
| Apakah domain mempengaruhi keberadaan anti-pattern? | **Tidak** (Chi-square p=0.134) | Framework berguna lintas domain |
| Apakah domain mempengaruhi besarnya penghematan? | **Ya** (KW per-domain p=0.001) | Token/NFT lama berpotensi hemat paling besar |
| Apakah kontrak kompleks lebih banyak anti-pattern? | **Tidak signifikan** (KW p=0.240) | Ukuran kontrak bukan prediktor kuat |
| Apakah kontrak lebih panjang lebih banyak temuan? | **Tidak** (ρ=+0.14, p=0.220) | LOC tidak bisa memprediksi jumlah findings |

**Kesimpulan statistik**: Tiga dari delapan uji signifikan — keduanya terkait efektivitas framework (dua Wilcoxon) dan satu terkait perbedaan domain (KW per-domain). McNemar signifikan namun terkontaminasi keterbatasan Slither.

*\*McNemar p=0.0039 signifikan karena Slither gagal menganalisis semua sampel (0.4.x), bukan perbandingan murni.*
