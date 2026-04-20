// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TestGas {
    uint256 public angka;

    // Anti-pattern: baca storage 3x
    function setBoros(uint256 x) public {
        angka = x;
        if (angka > 0) {        // SLOAD ke-2
            angka = angka + 1;  // SLOAD ke-3
        }
    }

    // Optimal: baca storage 1x
    function setHemat(uint256 x) public {
        uint256 _tmp = x;
        if (_tmp > 0) { _tmp = _tmp + 1; }
        angka = _tmp;
    }
}
