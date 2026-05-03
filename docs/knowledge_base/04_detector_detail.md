# Detail Implementasi Tiap Detektor (6 Anti-Pattern)

Semua detektor menggunakan interface yang seragam:
```python
def detect(ast) -> list[dict]:
    # Setiap finding adalah dict:
    # { 'detector': str, 'description': str, 'line': int|None, 'severity': str }
```

---

## Detektor 1: Redundant SLOAD

**File**: `src/detectors/redundant_sload.py`

### Masalah
Operasi SLOAD (read dari storage) di EVM menghabiskan **2.100 gas** (warm access, EIP-2929) atau **100 gas** (setelah warm). Membaca state variable yang sama >1x dalam satu fungsi tanpa cache lokal berarti SLOAD berulang.

```solidity
// Boros: 3x SLOAD untuk `counter`
function boros() view returns (uint256) {
    return counter * counter + counter;
}

// Hemat: 1x SLOAD, 2x akses lokal (MLOAD ~3 gas)
function hemat() view returns (uint256) {
    uint256 c = counter;
    return c * c + c;
}
```

### Logika Deteksi

1. Kumpulkan semua `StateVariableDeclaration` dari kontrak → daftar state variable names
2. Untuk setiap `FunctionDefinition`, traversal semua `Identifier` node di body
3. Hitung berapa kali setiap identifier yang merupakan state variable muncul
4. Jika count > 1 → flag sebagai redundant SLOAD

**AST node yang digunakan**: `ContractDefinition`, `StateVariableDeclaration`, `FunctionDefinition`, `Identifier`

### Keterbatasan

- Tidak membedakan read vs write (assignment juga dihitung sebagai akses)
- Tidak tracking apakah ada assignment di tengah (yang bisa mengubah nilai state var)
- False positive mungkin jika state variable dibaca >1x tapi dengan nilai yang berbeda (diubah di antara pembacaan)

### Hasil di Dataset
- **204 temuan** total dari 46 kontrak valid
- Domain tertinggi: DeFi (76 temuan)
- Kontrak tertinggi: CryptoPunksMarket (20), TetherToken (16)

---

## Detektor 2: Unoptimized Loop

**File**: `src/detectors/unoptimized_loop.py`

### Masalah
Mengakses `array.length` di kondisi for-loop menyebabkan SLOAD **setiap iterasi** jika `array` adalah state variable.

```solidity
// Boros: SLOAD tiap iterasi
for (uint i = 0; i < items.length; i++) { ... }

// Hemat: 1x SLOAD sebelum loop
uint256 n = items.length;
for (uint i = 0; i < n; i++) { ... }
```

### Logika Deteksi

1. Cari semua `ForStatement` di AST
2. Untuk setiap for-loop, cek `conditionExpression`
3. Jika condition mengandung `MemberAccess` dengan `memberName == "length"` dan expression-nya adalah `Identifier` yang merupakan state variable → flag

**AST node yang digunakan**: `ForStatement`, `MemberAccess`, `Identifier`, `StateVariableDeclaration`

### Keterbatasan

- Hanya mendeteksi `for` loop (bukan `while`)
- Tidak mendeteksi jika `.length` ada di body loop (bukan condition)
- False positive jika array yang diakses adalah local variable (bukan state variable) — bergantung pada kualitas state var detection

### Hasil di Dataset
- **5 temuan** — paling sedikit dari semua detektor
- Hanya pada domain Utility (MultiSigWallet: 5 temuan)
- Kontrak lain yang diperiksa tidak memiliki pattern ini

---

## Detektor 3: String vs Bytes32

**File**: `src/detectors/string_vs_bytes32.py`

### Masalah
Tipe `string` di Solidity adalah tipe dinamis (disimpan di storage dengan pointer + length + data). Untuk teks pendek (≤32 byte), `bytes32` jauh lebih efisien: disimpan sebagai satu slot storage (32 byte tepat).

```solidity
string  public name = "Token";    // boros: dynamic storage
bytes32 public name = "Token";    // hemat: 1 slot storage fixed
```

**Gas difference** untuk read: ~950 gas (24.540 → 23.590, hemat 3.87%)

### Logika Deteksi

1. Cari semua `StateVariableDeclaration` dengan type `string`
2. Cek apakah ada inisialisasi string literal
3. Jika panjang string literal ≤ 32 karakter → flag

**AST node yang digunakan**: `StateVariableDeclaration`, `ElementaryTypeName`, `StringLiteral`

### Keterbatasan

- Hanya mendeteksi state variables (bukan parameter fungsi)
- Tidak mendeteksi string yang tidak diinisialisasi (meski masih boros jika di-set nanti)
- String yang digunakan untuk output user-facing (deskripsi error, dll.) mungkin sengaja menggunakan `string` untuk flexibility

### Hasil di Dataset
- **72 temuan** dari 46 kontrak
- Domain tertinggi: DeFi (31) dan Token (25)
- Kontrak tertinggi: Uni (11 temuan), MiniMeToken (9)

---

## Detektor 4: Public vs External

**File**: `src/detectors/public_vs_external.py`

### Masalah
Fungsi `public` dapat dipanggil baik dari luar (external call) maupun dari dalam kontrak (internal call). Untuk external call, argumen array/struct dari `public` **dicopy ke memory** terlebih dahulu, sedangkan `external` dapat langsung membaca dari **calldata** (tidak ada copy). Calldata read jauh lebih murah.

```solidity
// Boros: array dicopy ke memory
function boros(uint256[] memory data) public returns (uint256 s) { ... }

// Hemat: array dibaca langsung dari calldata
function hemat(uint256[] calldata data) external returns (uint256 s) { ... }
```

**Gas difference** dengan array 10 elemen: ~2.673 gas (hemat 5.09%)

### Logika Deteksi

1. Kumpulkan semua `FunctionDefinition` dari kontrak
2. Kumpulkan semua pemanggilan fungsi internal (`FunctionCall` dengan expression berupa `Identifier`)
3. Untuk setiap fungsi `public` yang **tidak pernah dipanggil secara internal** → flag sebagai kandidat `external`
4. Pengecualian: constructor, fungsi yang di-override (interface)

**AST node yang digunakan**: `FunctionDefinition`, `FunctionCall`, `Identifier`, `MemberAccess`

### Keterbatasan

- False positive jika fungsi dipanggil via `this.functionName()` (dianggap external meski di dalam kontrak)
- Tidak bisa track pemanggilan melalui interface atau inheritance lintas file
- Kontrak yang memiliki banyak fungsi publik cenderung menghasilkan banyak temuan meski beberapa memang diperlukan `public`

### Hasil di Dataset
- **283 temuan** — paling banyak dari semua detektor (43.8% dari total)
- Domain tertinggi: Token (146 temuan)
- Kontrak tertinggi: WBTC (31), TetherToken (27), DSToken (21)

---

## Detektor 5: Unchecked Arithmetic

**File**: `src/detectors/unchecked_arithmetic.py`

### Masalah
Sejak Solidity 0.8.0, semua operasi aritmatika otomatis dilindungi overflow/underflow check. Proteksi ini menambah **overhead gas**. Di dalam loop counter yang dijamin tidak overflow (mis. `i < n` dimana n ≤ type(uint256).max), check ini tidak diperlukan.

```solidity
// Boros: setiap i++ memeriksa overflow
for (uint i = 0; i < n; i++) { ... }

// Hemat: skip overflow check untuk i++
for (uint i = 0; i < n;) {
    unchecked { i++; }
}
```

**Gas difference** untuk loop 100 iterasi: ~12.045 gas (hemat 20.38% — tertinggi!)

### Logika Deteksi

1. Cek pragma: hanya berlaku untuk Solidity ≥ 0.8.0 (pada versi lama tidak ada auto-check, jadi tidak relevan)
2. Cari semua `ForStatement` yang **belum** menggunakan `UncheckedStatement` di body atau loopExpression
3. Cek apakah `loopExpression` mengandung operasi aritmatika (`++`, `--`, `+=`, `-=`)
4. Jika ya → flag sebagai kandidat `unchecked`

**AST node yang digunakan**: `PragmaDirective` (cek versi), `ForStatement`, `UncheckedStatement`, `UnaryOperation`, `Assignment`, `BinaryOperation`

### Catatan Implementasi Penting

`PragmaDirective` di format AST modern menyimpan versi sebagai array `literals` (bukan field `value`):
```json
{"nodeType": "PragmaDirective", "literals": ["solidity", "^", "0.8", ".20"]}
```
Kode cek versi harus join literals dan parse angka dari string gabungan.

Loop increment bisa berupa:
- `UnaryOperation` operator `++` atau `--`
- `Assignment` operator `+=` atau `-=`
- `BinaryOperation` operator `+` atau `-` (jarang)

### Hasil di Dataset
- **10 temuan** dari 46 kontrak
- Hanya kontrak era ≥ 0.8 yang relevan; mayoritas dataset menggunakan 0.4.x–0.6.x (tidak relevan)
- Kontrak yang punya temuan: Land (8), Moonbirds (2)

---

## Detektor 6: Dead Code

**File**: `src/detectors/dead_code.py`

### Masalah
Fungsi yang tidak pernah dipanggil tetap dikompilasi dan sebagian masuk ke deployment bytecode. Ini meningkatkan biaya deployment (gas untuk deploy kontrak). Pada kontrak besar, dead functions dapat menambah deployment cost secara signifikan.

**Catatan penting**: Fungsi internal yang tidak dipanggil TERKADANG dieliminasi oleh compiler bahkan tanpa optimizer (karena unreachable). Itulah mengapa benchmark menunjukkan 0% penghematan untuk pola ini pada runtime cost — efeknya pada deployment cost lebih nyata tapi sulit diukur dengan `estimateGas`.

### Logika Deteksi

1. Kumpulkan semua `FunctionDefinition` di kontrak
2. Kumpulkan semua pemanggilan fungsi (dari `FunctionCall` dan `MemberAccess`) di seluruh source
3. Fungsi yang **tidak pernah muncul** dalam pemanggilan manapun → dead code

**AST node yang digunakan**: `FunctionDefinition`, `FunctionCall`, `Identifier`

### Keterbatasan

- False positive untuk fungsi yang dipanggil via interface / inheritance
- Tidak bisa track event handler atau callback (dipanggil oleh external sistem)
- Constructor tidak di-flag meski tidak pernah dipanggil internal

### Hasil di Dataset
- **52 temuan** dari 46 kontrak
- Domain tertinggi: Token (27 temuan)
- Kontrak tertinggi: BalancerGovernanceToken (10), DSToken (8)

---

## Rangkuman Perbandingan Detektor

| Detektor | Total Findings | % dari Total | Avg per Kontrak |
|---|---|---|---|
| redundant_sload | 204 | 31.6% | 4.43 |
| unoptimized_loop | 5 | 0.8% | 0.11 |
| string_vs_bytes32 | 72 | 11.1% | 1.57 |
| public_vs_external | 283 | 43.8% | 6.15 |
| unchecked_arithmetic | 10 | 1.5% | 0.22 |
| dead_code | 52 | 8.1% | 1.13 |
| **TOTAL** | **646** | 100% | **14.04** |

**Insight**: `public_vs_external` mendominasi karena hampir semua kontrak era 0.4.x–0.6.x menggunakan `public` secara default tanpa mempertimbangkan apakah fungsi dipanggil secara internal.
