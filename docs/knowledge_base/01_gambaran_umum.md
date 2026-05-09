# Gambaran Umum Project: Gas Optimization Framework

## Identitas Penelitian

| Atribut | Nilai |
|---|---|
| Judul | Gas Optimization Framework untuk Smart Contract Solidity |
| Jenis | Mini Project 3B — Tesis S2 |
| Program Studi | Komputasi Berbasis Jaringan (KBJ) |
| Institusi | Institut Teknologi Sumatera (ITERA) |
| Email Peneliti | ridho.119140038@student.itera.ac.id |

---

## Latar Belakang

Smart contract Solidity yang dieksekusi di Ethereum Virtual Machine (EVM) mengenakan biaya **gas** untuk setiap operasi. Gas adalah satuan pengukuran komputasi di Ethereum — setiap instruksi bytecode (SLOAD, SSTORE, ADD, dll.) memiliki biaya gas tetap sesuai spesifikasi EIP-150/EIP-2929.

Masalah utamanya: **programmer sering tanpa sadar menulis pola kode yang boros gas**. Pola-pola ini secara fungsional benar, tetapi menghabiskan gas lebih dari yang diperlukan. Pada kontrak yang sering dipanggil (misalnya DEX, token ERC-20), inefisiensi kecil ini berdampak besar secara kumulatif.

Contoh konkret: membaca state variable dari storage (operasi SLOAD) di dalam loop sebanyak 10 iterasi menghabiskan ~10× lebih banyak gas dibanding membaca sekali ke variabel lokal dan menggunakannya dalam loop.

---

## Rumusan Masalah

1. Pola anti-pattern gas apa saja yang umum ditemukan di smart contract Solidity nyata (deployed ke mainnet)?
2. Seberapa besar penghematan gas yang dihasilkan jika pola-pola tersebut diperbaiki?
3. Apakah framework deteksi statik berbasis AST dapat mengidentifikasi pola-pola tersebut secara otomatis?
4. Apakah perbedaan penghematan gas tersebut signifikan secara statistik?

---

## Tujuan Penelitian

1. Membangun tool analisis statik Python yang mendeteksi 6 anti-pattern boros gas pada kode Solidity
2. Mengukur penghematan gas empiris untuk tiap anti-pattern via Hardhat (local EVM)
3. Menguji framework pada 75 kontrak real-world dari Etherscan mainnet (15 per domain, 5 domain)
4. Memvalidasi hasil dengan uji statistik (Wilcoxon, Chi-square, Kruskal-Wallis, Spearman)
5. Membandingkan hasil dengan tool analisis komersial Slither

---

## Kontribusi Ilmiah

1. **Framework deteksi otomatis**: Tool Python open-source yang menganalisis file `.sol` via AST dan menghasilkan temuan terstruktur
2. **Benchmark gas empiris**: Pengukuran penghematan gas nyata untuk 6 pola via eksekusi di EVM (bukan estimasi teoritis)
3. **Dataset analisis**: Hasil deteksi pada 74 kontrak mainnet Ethereum mencakup 5 domain berbeda (75 kontrak, 1 gagal compile)
4. **Validasi statistik**: Bukti statistik bahwa pola-pola yang dideteksi memang berdampak signifikan terhadap konsumsi gas
5. **Modul auto-refactoring**: Implementasi awal patch otomatis source-level untuk 2 dari 6 anti-pattern (public_vs_external, unoptimized_loop)

---

## Batasan Penelitian

- Dataset terbatas pada 75 kontrak dari Etherscan (mainnet Ethereum, bukan L2/sidechain)
- Pengukuran gas menggunakan Hardhat local EVM, bukan transaksi mainnet aktual
- Optimizer Solidity dinonaktifkan untuk konsistensi pengukuran (kondisi tidak mewakili deployment produksi yang mengaktifkan optimizer)
- Refactoring otomatis hanya untuk 2 dari 6 anti-pattern dengan hasil bermakna (4 lainnya butuh analisis alur data penuh)
- Perbandingan Slither terbatas karena ketidakkompatibilan versi solc lama (0.4.x) dengan Slither v0.11.5
- `unchecked_arithmetic`: 0 findings pada 74 kontrak dataset — seluruh kontrak didominasi era solc 0.4.x–0.6.x yang tidak menggunakan fitur `unchecked {}` Solidity 0.8.0

---

## 6 Anti-Pattern yang Diteliti

| No | Nama | Penjelasan Singkat | Penghematan Empiris |
|---|---|---|---|
| 1 | Redundant SLOAD | State variable dibaca dari storage >1x tanpa cache lokal | 0.77% |
| 2 | Unoptimized Loop | `.length` array dibaca dari storage di setiap iterasi loop | 2.01% |
| 3 | String vs Bytes32 | Pakai `string` untuk teks pendek yang bisa pakai `bytes32` | 3.87% |
| 4 | Public vs External | Fungsi `public` yang tidak pernah dipanggil secara internal | 5.09% |
| 5 | Unchecked Arithmetic | Operasi `+`/`-` di loop yang sudah pasti tidak overflow | 20.38% |
| 6 | Dead Code | Fungsi yang tidak pernah dipanggil oleh siapapun | 0.00% (runtime) |

---

## Hasil Kunci (Ringkasan)

- **1.655 temuan** terdeteksi pada 74 kontrak valid dari total 75 kontrak dataset
- **66 dari 74 kontrak** (89.2%) memiliki setidaknya satu temuan
- **Penghematan gas tertinggi**: Unchecked Arithmetic (20.38%) — diukur via benchmark synthetic
- **Uji Wilcoxon per-pattern**: W=15.0, p=0.031 → penghematan gas **signifikan secara statistik** (α=0.05)
- **Uji Wilcoxon per-contract** (n=65): W=2145.0, p<0.001 → konfirmasi kuat
- **Anti-pattern paling umum**: Public vs External (649 temuan, 39.2% dari total), disusul Redundant SLOAD (634, 38.3%)
- **Domain tertinggi temuan**: NFT (539 temuan), Token (478 temuan)
- **Domain tertinggi potensi hemat gas**: Token (median savings 49.044 gas/contract)
