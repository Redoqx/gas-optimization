// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BenchmarkSLOAD {
    uint256 public counter;
    uint256 public multiplier;

    constructor() { counter = 10; multiplier = 3; }

    // Anti-pattern: 3x SLOAD (counter dibaca 3x dari storage)
    function computeBoros() external view returns (uint256) {
        return counter * counter + counter;  // 3 SLOAD
    }

    // Optimal: 1x SLOAD + cache lokal
    function computeHemat() external view returns (uint256) {
        uint256 c = counter;  // 1 SLOAD
        return c * c + c;
    }

    // Anti-pattern: loop membaca .length dari storage setiap iterasi
    uint256[] public items;
    function sumBoros() external view returns (uint256 total) {
        for (uint256 i = 0; i < items.length; i++) {  // items.length = SLOAD tiap iterasi
            total += items[i];
        }
    }

    // Optimal: cache length sebelum loop
    function sumHemat() external view returns (uint256 total) {
        uint256 len = items.length;  // 1 SLOAD
        for (uint256 i = 0; i < len; i++) {
            total += items[i];
        }
    }

    function populateItems(uint256 n) external {
        for (uint256 i = 0; i < n; i++) items.push(i + 1);
    }
}
