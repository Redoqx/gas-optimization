# Diskusi Temuan & Keterbatasan

## Diskusi Temuan Utama

### 1. Public vs External Mendominasi (43.8% dari Temuan)

`public_vs_external` menghasilkan 283 dari 646 temuan — hampir separuh. Ini mencerminkan realitas historis Solidity: pada versi 0.4.x–0.5.x, praktik standar adalah mendeklarasikan semua fungsi sebagai `public`. Keyword `external` baru populer setelah komunitas Ethereum mulai memperhatikan gas optimization sekitar 2019–2020.

**Implikasi**: Kontrak-kontrak lama (deployed sebelum 2020) yang masih berjalan di mainnet membawa "technical debt" gas yang bisa diminimalkan dengan refactoring sederhana — cukup mengubah `public` → `external` dan `memory` → `calldata` untuk parameter array.

**Catatan penting untuk penulisan**: Tidak semua `public` yang di-flag adalah false positive, tapi mayoritas besar memang tidak pernah dipanggil secara internal (hanya dari luar kontrak). Ini adalah optimasi yang aman untuk diterapkan.

### 2. Unchecked Arithmetic: Penghematan Terbesar (20.38%)

Meski hanya 10 temuan di dataset (karena sebagian besar kontrak menggunakan solc <0.8.0), penghematan per penggunaan adalah yang terbesar. Untuk loop 100 iterasi, `unchecked { i++ }` menghemat 12.045 gas — hampir 1/5 dari total biaya loop.

**Konteks**: EIP-1884 dan Solidity 0.8.0 (2020) menambahkan overflow protection otomatis. Sebelumnya, programmer harus menggunakan SafeMath library yang justru lebih mahal. Sejak 0.8.0, unchecked block menjadi cara resmi untuk skip proteksi saat sudah terjamin tidak overflow.

**Implikasi**: Untuk kontrak baru yang ditulis dengan Solidity 0.8.x, optimasi ini sangat relevan — terutama loop counter yang jelas bounded.

### 3. Dead Code = 0% Penghematan (pada Pengukuran)

Hasil yang mungkin mengejutkan: meskipun 52 temuan dead code ditemukan di dataset, pengukuran gas menunjukkan 0% penghematan.

**Penjelasan teknis**: Compiler Solidity mengeksklusi fungsi internal yang tidak pernah dipanggil dari deployment bytecode **bahkan tanpa optimizer**. Ini karena fungsi internal di-inline atau diresolusi secara statik saat compile. Hasilnya: `WithDeadCode` dan `WithoutDeadCode` menghasilkan bytecode identik untuk bagian yang dieksekusi.

**Nuansa penting**: Ini BUKAN berarti dead code tidak bermasalah. Dead code:
- Menambah **complexity kognitif** (programmer membaca kode tidak perlu)
- Dapat menjadi **attack surface** jika secara tidak sengaja diaktifkan
- Pada kondisi tertentu (fungsi yang lebih kompleks, atau compiler versi tertentu), MUNGKIN tetap masuk bytecode

Untuk tujuan penulisan: sebutkan bahwa temuan dead code valid sebagai quality metric, namun dampak gas-nya minimal dalam pengukuran ini.

### 4. Unoptimized Loop Hanya 5 Temuan

Hanya MultiSigWallet (Utility domain) yang memiliki loop dengan state variable `.length`. Ini bukan berarti pattern tidak umum — melainkan karena:
1. Kontrak modern menggunakan mapping (O(1) lookup) daripada array iterasi
2. Kontrak yang menggunakan array biasanya mengcache length secara manual (sudah sadar)
3. Detektor kita hanya mendeteksi loop dengan state variable array; local variable array tidak dideteksi

### 5. Korelasi Spearman Negatif (ρ = -0.261)

Counter-intuitive: kontrak lebih panjang justru sedikit lebih sedikit pola boros. Penjelasan yang masuk akal:

- **Selection bias era**: Kontrak besar yang dianalisis (Seaport 11.395 LOC, UniswapV3 4.595 LOC) adalah produk 2021–2022, ditulis dengan tim berpengalaman dan sudah diaudit. Kontrak kecil-menengah (TetherToken 893 LOC, WETH9 1.511 LOC) adalah kontrak 2017–2018 dari era sebelum gas optimization menjadi perhatian utama.
- **Audit effect**: Kontrak besar dan populer lebih mungkin melalui audit profesional yang mengidentifikasi gas inefficiency

Untuk penulisan: jelaskan bahwa "ukuran kontrak bukan proxy yang baik untuk kualitas gas efficiency" — melainkan era penulisan dan pengalaman tim yang lebih menentukan.

### 6. Slither Tidak Dapat Menganalisis Kontrak Lama

Slither 0.11.5 gagal menganalisis 10 kontrak sampel karena semua menggunakan solc 0.4.x. Ini bukan kelemahan inherent Slither — melainkan trade-off antara modernitas tool (Slither dioptimasi untuk kontrak modern) vs keragaman dataset.

**Untuk penulisan**: Sebutkan bahwa perbandingan Slither vs framework kita tidak dapat dilakukan secara penuh karena keterbatasan ini. Framework kita memiliki keunggulan spesifik dalam mendukung multi-versi solc (0.4.x hingga 0.8.x) melalui py-solcx.

---

## Keterbatasan Penelitian

### Keterbatasan 1: Ukuran Sampel Uji Statistik

Uji Wilcoxon menggunakan n=6 (5 efektif) — sangat kecil untuk analisis statistik robust. Meski hasilnya signifikan (p=0.031), power statistik rendah berarti:
- Potensi Type II error (gagal mendeteksi efek kecil) tinggi
- Generalisasi terbatas

**Saran penelitian lanjutan**: Perbanyak variasi benchmark — berbeda ukuran array, berbeda jumlah iterasi, berbeda kondisi EVM state — untuk memperluas n.

### Keterbatasan 2: Benchmark Terkontrol vs Real-World

Gas diukur pada kontrak benchmark yang dikonstruksi khusus dengan kondisi terisolasi. Pada kontrak nyata:
- Gas bervariasi tergantung state EVM saat itu (warm/cold storage access)
- Kompiler versi berbeda dengan optimization setting berbeda menghasilkan bytecode berbeda
- Interaksi antar pattern (satu fungsi bisa punya multiple anti-pattern) tidak diukur

### Keterbatasan 3: Refactoring Otomatis Terbatas

Modul `refactorer.py` menggunakan pendekatan heuristik berbasis line number + regex:
- `public_vs_external`: patch otomatis tapi tidak sempurna (tidak track inheritance chain)
- `unoptimized_loop`: patch otomatis dengan word-boundary matching (masih bisa false positive untuk parameter bernama mirip state variable)
- `redundant_sload`: hanya tambah komentar TODO — full auto-patch butuh data-flow analysis

Contoh kegagalan yang terdokumentasi: MultiSigWallet memiliki parameter `_owners` dan state variable `owners`. Loop iterasi menggunakan parameter `_owners.length`, bukan state variable `owners.length` — sehingga detektor false positive, dan refactorer (sebelum fix) salah mempatch.

### Keterbatasan 4: False Positive dalam Deteksi

**redundant_sload**: Tidak membedakan read dari write. Jika state variable ditulis (diubah) di antara dua pembacaan, membaca ulang dari storage adalah **benar** (bukan redundant). Detektor saat ini tidak tracking assignment.

**public_vs_external**: Tidak dapat mendeteksi pemanggilan via `this.functionName()` (yang adalah external call meski dari dalam kontrak) atau via interface/inheritance lintas file.

**dead_code**: Tidak dapat tracking jika fungsi dipanggil secara dinamis (via `call()` atau contract upgrade pattern).

### Keterbatasan 5: Dataset Tidak Seimbang

- Complexity Simple: 0 kontrak (semua kontrak mainnet ≥ 100 LOC)
- Sebagian besar kontrak adalah solc 0.4.x–0.6.x era (memengaruhi distribusi unchecked_arithmetic)
- 4 dari 50 kontrak gagal compile — ada selection bias

---

## Validitas Internal vs Eksternal

**Validitas internal** (tinggi): Pengukuran gas dilakukan secara konsisten dengan kondisi tetap (solc 0.8.20, optimizer off, Hardhat local EVM). Hasil benchmark dapat direproduksi.

**Validitas eksternal** (sedang): Temuan berlaku untuk kontrak era lama yang serupa dengan dataset. Generalisasi ke kontrak era baru (solc 0.8.x) atau domain lain (L2, Cosmos-based EVM) perlu studi lebih lanjut.

---

## Perbandingan dengan Ekspektasi Teoritis

| Anti-Pattern | Ekspektasi Teoritis | Hasil Pengukuran | Sesuai? |
|---|---|---|---|
| redundant_sload | SLOAD 2100 gas × (n-1) penghematan | 186 gas (sangat kecil) | Sebagian — SLOAD mungkin warm access (100 gas) |
| unoptimized_loop | n × (SLOAD_cost - MLOAD_cost) | 1.031 gas untuk n=10 | ✅ Sesuai (~103 gas/iterasi |
| string_vs_bytes32 | Static vs dynamic storage | 950 gas | ✅ Sesuai |
| public_vs_external | Memory copy vs calldata | 2.673 gas | ✅ Sesuai |
| unchecked_arithmetic | Overflow check overhead × n | 12.045 gas | ✅ Sesuai (120 gas/iterasi) |
| dead_code | Deployment bytecode lebih kecil | 0 gas | ❌ Tidak — compiler elides anyway |

**Catatan redundant_sload**: Penghematan kecil (186 gas) menunjukkan bahwa akses storage yang diukur adalah **warm access** (slot sudah diakses sebelumnya dalam transaksi yang sama), yang hanya 100 gas. Cold access (2100 gas) tidak diukur dalam benchmark ini karena fungsi `setup()` dipanggil lebih dulu.
