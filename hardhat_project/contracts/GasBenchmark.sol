// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @dev Benchmark 5 anti-pattern (gas per-call) + 2 kontrak untuk dead_code (deployment)
contract GasBenchmark {

    // -- 1. Redundant SLOAD --------------------------------------------------
    uint256 public counter;

    function sload_boros() external view returns (uint256) {
        // state var dibaca 3x dari storage
        return counter * counter + counter;
    }

    function sload_hemat() external view returns (uint256) {
        uint256 c = counter;            // 1x SLOAD, lalu pakai cache lokal
        return c * c + c;
    }

    // -- 2. Unoptimized Loop -------------------------------------------------
    uint256[] public items;

    function loop_boros() external view returns (uint256 s) {
        for (uint256 i = 0; i < items.length; i++) {  // SLOAD tiap iterasi
            s += items[i];
        }
    }

    function loop_hemat() external view returns (uint256 s) {
        uint256 n = items.length;   // 1x SLOAD sebelum loop
        for (uint256 i = 0; i < n; i++) {
            s += items[i];
        }
    }

    // -- 3. String vs Bytes32 ------------------------------------------------
    string  public nameStr = "Token";
    bytes32 public nameB32 = "Token";

    function str_boros() external view returns (string memory) { return nameStr; }
    function str_hemat() external view returns (bytes32)       { return nameB32; }

    // -- 4. Public vs External -----------------------------------------------
    uint256 public stored;

    function pub_boros(uint256[] memory d) public returns (uint256 s) {
        for (uint256 i = 0; i < d.length; i++) s += d[i];
        stored = s;
    }

    function ext_hemat(uint256[] calldata d) external returns (uint256 s) {
        for (uint256 i = 0; i < d.length; i++) s += d[i];
        stored = s;
    }

    // -- 5. Unchecked Arithmetic ---------------------------------------------
    function arith_boros(uint256 n) external pure returns (uint256 s) {
        for (uint256 i = 0; i < n; i++) { s += i; }
    }

    function arith_hemat(uint256 n) external pure returns (uint256 s) {
        for (uint256 i = 0; i < n;) {
            s += i;
            unchecked { i++; }
        }
    }

    // -- Setup helper --------------------------------------------------------
    function setup(uint256 n) external {
        counter = 7;
        delete items;
        for (uint256 i = 0; i < n; i++) items.push(i + 1);
    }
}

// -- 6. Dead Code -- deployment cost comparison -----------------------------
contract WithDeadCode {
    uint256 public x = 1;
    function get() external view returns (uint256) { return x; }
    function _unused1() internal pure returns (uint256) { return 42; }
    function _unused2() internal pure returns (uint256) { return 99; }
    function _unused3() internal pure returns (bytes32)  { return "hello"; }
}

contract WithoutDeadCode {
    uint256 public x = 1;
    function get() external view returns (uint256) { return x; }
}
