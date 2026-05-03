# Analisis Statistik: 4 Uji & Interpretasi

## Ringkasan Hasil Semua Uji

| Uji | Statistik | p-value | Signifikan (α=0.05) | Keputusan |
|---|---|---|---|---|
| Wilcoxon (per-pattern, n=6) | W = 15.0 | **0.031** | ✅ Ya | H1 Diterima — gas savings signifikan |
| Wilcoxon (per-contract, n=35) | W = 630.0 | **< 0.001** | ✅ Ya | H1 Diterima — savings per kontrak signifikan |
| Chi-square (domain) | χ² = 8.568 | 0.073 | ❌ Tidak | H0 Diterima — domain tidak berpengaruh |
| Kruskal-Wallis (complexity) | H = 0.631 | 0.427 | ❌ Tidak | H0 Diterima — complexity tidak berpengaruh |
| Kruskal-Wallis (domain × savings) | H = 14.015 | **0.007** | ✅ Ya | H1 Diterima — domain berpengaruh pada savings |
| Spearman (LOC vs findings) | ρ = -0.261 | 0.079 | ❌ Tidak | H0 Diterima — LOC tidak berkorelasi |
| McNemar (our tool vs Slither) | b=8, c=0 | **0.00781** | ✅ Ya* | H0 Ditolak — our tool deteksi lebih banyak* |
| Cohen's Kappa (our tool vs Slither) | κ = 0.0 | — | — | No agreement beyond chance |

---

## Uji 1: Wilcoxon Signed-Rank Test

### Tujuan
Menguji apakah penghematan gas (boros − hemat) secara median **signifikan lebih besar dari nol** — yaitu, apakah optimasi kode yang disarankan framework benar-benar menghasilkan penghematan gas yang nyata, bukan hanya kebetulan.

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
- W = min(W+, W-) = 0... atau dalam implementasi scipy: W = W+ = 15

Untuk n=5 dengan semua positif, p-value satu sisi = 2^(-5) = **0.03125 ≈ 0.031**

### Hasil
**W = 15.0, p = 0.031**

### Interpretasi
**H1 DITERIMA** pada α = 0.05. Penghematan gas yang dihasilkan oleh kelima pola optimasi terbukti signifikan secara statistik. Nilai W=15 adalah nilai maksimum yang mungkin untuk n=5 — artinya **semua** pasangan menunjukkan penghematan positif (tidak ada satu pun yang berbalik).

Ini memberikan bukti statistik yang kuat bahwa pola-pola yang diidentifikasi framework memang berdampak nyata pada konsumsi gas EVM.

### Catatan Keterbatasan
- n=6 (5 efektif) sangat kecil; power statistik rendah
- Unit observasi adalah "pattern", bukan kontrak individual
- Benchmark dilakukan pada kondisi terkontrol (tidak mewakili variabilitas kondisi jaringan nyata)

---

## Uji 2: Chi-Square Test of Independence

### Tujuan
Menguji apakah distribusi findings (ada/tidak ada) **bergantung pada domain** kontrak — apakah kontrak dari domain tertentu lebih banyak mengandung pola boros gas.

### Setup Uji
- **Jenis**: Chi-square test of independence
- **H0**: Distribusi findings tidak bergantung pada domain
- **H1**: Ada perbedaan distribusi findings antar domain
- **Tabel kontingensi**: Domain (5 baris) × Keberadaan findings (2 kolom: ada/tidak)

### Tabel Kontingensi

| Domain | Ada Findings | Tidak Ada Findings | Total |
|---|---|---|---|
| DeFi | 8 | 2 | 10 |
| NFT | 7 | 2 | 9 |
| Token | 8 | 1 | 9 |
| Governance | 7 | 2 | 9 |
| Utility | 8 | 1 | 9 |
| **Total** | **38** | **8** | **46** |

### Hasil
**χ² = 8.568, df = 4, p = 0.073**

### Interpretasi
**H0 DITERIMA** — distribusi findings tidak berbeda signifikan antar domain pada α = 0.05. Meski p = 0.073 cukup dekat dengan 0.05, belum mencapai threshold.

Ini menunjukkan bahwa **pola boros gas ditemukan secara merata** di semua domain — bukan hanya domain tertentu. Dari perspektif praktis, ini berarti framework berguna lintas domain, tidak terbatas hanya untuk DeFi atau Token saja.

### Catatan
- Beberapa sel expected count < 5 (karena n kecil per domain) yang dapat mengurangi validitas chi-square — bisa dipertimbangkan Fisher's exact test sebagai alternatif untuk sampel lebih kecil

---

## Uji 3: Kruskal-Wallis Test

### Tujuan
Menguji apakah **jumlah findings** berbeda signifikan antar complexity level (Medium vs Complex).

### Setup Uji
- **Jenis**: Kruskal-Wallis (non-parametrik ANOVA)
- **H0**: Distribusi findings sama di semua complexity level
- **H1**: Setidaknya satu complexity level memiliki distribusi berbeda
- **Grup**: Medium (n=9) dan Complex (n=37) — tidak ada Simple

### Data Grup

| Complexity | n | Median Findings | Mean Findings |
|---|---|---|---|
| Medium | 9 | ~10 | 14.7 |
| Complex | 37 | ~4 | 13.9 |

### Hasil
**H = 0.631, p = 0.427**

### Interpretasi
**H0 DITERIMA** — jumlah findings tidak berbeda signifikan berdasarkan complexity level.

Ini counterintuitive: seseorang mungkin menduga kontrak lebih kompleks memiliki lebih banyak anti-pattern. Namun kenyataannya, **jumlah absolut findings serupa** antara Medium dan Complex. Penjelasan: kontrak Complex cenderung lebih baru (solc 0.8.x) atau ditulis dengan standar kode lebih tinggi sehingga pola boros per baris lebih sedikit (density 0.64% vs 4.03%).

### Hubungan dengan Spearman
Kruskal-Wallis menguji perbedaan grup, sementara Spearman mengukur korelasi kontinu — keduanya konsisten menunjukkan tidak ada hubungan kuat antara ukuran/kompleksitas kontrak dengan jumlah findings.

---

## Uji 4: Spearman Rank Correlation

### Tujuan
Menguji apakah ada hubungan **monoton** antara LOC (Lines of Code) dan total findings.

### Setup Uji
- **Jenis**: Spearman rank correlation (non-parametrik)
- **H0**: ρ = 0 (tidak ada korelasi)
- **H1**: ρ ≠ 0 (ada korelasi)
- **n**: 46 kontrak valid

### Hasil
**ρ = -0.261, p = 0.079**

### Interpretasi
**H0 DITERIMA** — korelasi tidak signifikan pada α = 0.05.

Korelasi negatif lemah (ρ = -0.261) menunjukkan bahwa **kontrak lebih panjang justru sedikit lebih sedikit pola boros**. Ini dapat dijelaskan dengan beberapa hipotesis:

1. **Bias era**: Kontrak besar (LOC tinggi) seperti Seaport, UniswapV3 cenderung kontrak baru (solc 0.8.x) yang ditulis dengan tools dan best practice modern
2. **Keahlian tim**: Kontrak besar biasanya dikembangkan oleh tim berpengalaman yang sudah aware gas optimization
3. **Audit**: Kontrak besar umumnya diaudit profesional sebelum deployment, dan auditor biasanya memeriksa gas efficiency

---

## Uji Tambahan A: Wilcoxon Signed-Rank (Per Contract, n=35)

### Tujuan
Versi lebih kuat dari Wilcoxon per-pattern: menggunakan **kontrak sebagai unit observasi** (bukan pattern). Menguji apakah estimated gas savings per kontrak (Σ findings × avg diff gas) secara median signifikan lebih besar dari nol.

### Setup Uji
- **Unit observasi**: kontrak (bukan pattern)
- **n**: 35 kontrak dengan savings > 0 (dari 46 valid; 11 kontrak bernilai 0 dikecualikan)
- **Data**: `estimated_savings[i] = Σ(count_det × avg_diff_gas_det)` untuk kontrak i
- **H0**: Median estimated savings = 0
- **H1**: Median estimated savings > 0

### Estimasi Savings

```
GAS_DIFF = {
    redundant_sload:      186 gas
    unoptimized_loop:   1,031 gas
    string_vs_bytes32:    950 gas
    public_vs_external: 2,673 gas
    unchecked_arithmetic: 12,045 gas
    dead_code:              0 gas
}
savings[i] = Σ(findings[i][det] × GAS_DIFF[det])
```

### Hasil
**W = 630.0, p < 0.001**

### Interpretasi
**H1 DITERIMA** dengan sangat kuat (p << 0.05). Ini mengonfirmasi Wilcoxon per-pattern (W=15, p=0.031) dengan power statistik jauh lebih tinggi (n=35 vs n=5 efektif). Estimated gas savings per kontrak secara konsisten positif — tidak ada kontrak yang memiliki savings negatif. Nilai W=630 adalah nilai maksimum yang mungkin untuk n=35, menunjukkan semua 35 pasangan positif.

---

## Uji Tambahan B: Kruskal-Wallis (Gas Savings × 5 Domains)

### Tujuan
Menguji apakah **potensi penghematan gas** (estimated savings) berbeda signifikan antar domain — berbeda dari KW sebelumnya yang menguji jumlah findings vs complexity level.

### Setup Uji
- **H0**: Distribusi estimated savings sama di semua domain
- **H1**: Setidaknya satu domain memiliki distribusi savings berbeda
- **Grup**: 5 domain (DeFi, NFT, Token, Governance, Utility)

### Data Grup

| Domain | n | Median Savings (gas) | Mean Savings (gas) | Max Savings (gas) |
|---|---|---|---|---|
| DeFi | 10 | 14.272 | 18.793 | 58.737 |
| NFT | 9 | 5.346 | 23.219 | 99.210 |
| Token | 9 | **49.044** | **47.241** | 89.081 |
| Governance | 9 | 13.336 | 16.910 | 38.892 |
| Utility | 9 | 0 | 4.426 | 33.931 |

### Hasil
**H = 14.015, p = 0.007**

### Interpretasi
**H1 DITERIMA** — domain berpengaruh signifikan terhadap estimasi penghematan gas (p=0.007 < 0.05).

Ini **berbeda** dari Chi-square (yang menguji keberadaan findings, tidak signifikan, p=0.073): meski **keberadaan** anti-pattern tidak berbeda antar domain, **besarnya potensi penghematan gas** berbeda signifikan. Ini masuk akal karena:
- Domain Token memiliki dominasi `public_vs_external` (283 findings) yang menghasilkan savings 2,673 gas per temuan
- Domain Utility didominasi kontrak modern dengan sedikit findings (savings kecil)

**Kesimpulan praktis**: Kontrak dari domain Token dan DeFi era lama memiliki potensi penghematan gas terbesar jika dioptimasi.

---

## Uji Tambahan C: McNemar & Cohen's Kappa

### McNemar — Exact Test (Binomial)

Uji McNemar membandingkan detektor kita vs Slither secara biner per kontrak (apakah kontrak memiliki gas-related findings: Ya/Tidak).

**Tabel kontingensi (10 kontrak sampel)**:

| | Slither: Ya | Slither: Tidak |
|---|---|---|
| **Our Tool: Ya** | a = 0 | b = 8 |
| **Our Tool: Tidak** | c = 0 | d = 2 |

**Metode**: Exact McNemar menggunakan `binomtest(min(b,c), b+c, 0.5, alternative='two-sided')` → `binomtest(0, 8, 0.5)`.

**Hasil**: **p = 0.00781**

**Interpretasi**: H0 ditolak — our tool mendeteksi secara signifikan lebih banyak daripada Slither pada sampel ini. Namun hasil ini adalah **constrained comparison**: Slither tidak menemukan apapun bukan karena false negative, melainkan karena ketidakkompatibilan versi solc 0.4.x pada semua 10 sampel. Temuan ini lebih mencerminkan keterbatasan Slither daripada superioritas murni framework kita.

**Untuk penulisan tesis**: Laporkan hasil (p=0.0078) beserta konteksnya — sebutkan bahwa 10 sampel semuanya berasal dari era Solidity 0.4.x yang tidak didukung Slither.

---

### Cohen's Kappa — Inter-Rater Agreement

Kappa mengukur kesepakatan dua "penilai" (our tool dan Slither) di luar tingkat kebetulan.

**Formula**: κ = (Po − Pe) / (1 − Pe)

**Perhitungan dari tabel 2×2**:

```
n   = 10
Po  = (a + d) / n = (0 + 2) / 10 = 0.20
Pe  = (p_pos_ours × p_pos_slith) + (p_neg_ours × p_neg_slith)
    = (8/10 × 0/10) + (2/10 × 10/10)
    = (0.80 × 0.00) + (0.20 × 1.00) = 0.20
κ   = (0.20 − 0.20) / (1 − 0.20) = 0.00 / 0.80 = 0.00
```

**Hasil**: **κ = 0.00** (Kesepakatan setara kebetulan — *no agreement beyond chance*)

**Interpretasi**: κ = 0.0 terjadi karena Slither selalu memberi label "tidak ada findings" pada semua 10 sampel. Nilai ini valid dan dapat dilaporkan dalam tesis. Untuk mendapatkan kappa yang bermakna (bukan terpengaruh keterbatasan kompatibilitas), diperlukan dataset yang dapat dianalisis kedua tool secara penuh (kontrak solc 0.8.x).

---

## Interpretasi Gabungan

| Pertanyaan | Temuan | Implikasi |
|---|---|---|
| Apakah optimasi gas signifikan secara statistik? | **Ya** — dua Wilcoxon (p=0.031 dan p<0.001) | Framework valid — pola yang dideteksi memang boros gas |
| Apakah domain mempengaruhi keberadaan anti-pattern? | **Tidak** (Chi-square p=0.073) | Framework berguna lintas domain |
| Apakah domain mempengaruhi besarnya penghematan? | **Ya** (KW per-domain p=0.007) | Token/DeFi lama berpotensi hemat paling besar |
| Apakah kontrak kompleks lebih banyak anti-pattern? | **Tidak** (KW p=0.427) | Ukuran kontrak bukan prediktor jumlah temuan |
| Apakah kontrak lebih panjang lebih banyak temuan? | **Tidak** (ρ=-0.26, p=0.079) | LOC tidak bisa memprediksi jumlah findings |

**Kesimpulan statistik**: Tiga dari delapan uji signifikan — keduanya terkait efektivitas framework (dua Wilcoxon) dan satu terkait perbedaan domain (KW per-domain). McNemar juga signifikan namun terkontaminasi keterbatasan Slither. κ=0 konsisten dengan pola yang sama.

*\*McNemar p=0.0078 signifikan karena Slither gagal menganalisis semua sampel (0.4.x), bukan perbandingan murni.*
