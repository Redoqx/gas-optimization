"""
GasEstimator: ukur penghematan gas empiris tiap anti-pattern via Hardhat.

Menulis GasBenchmark.sol + run_benchmarks.js ke hardhat_project/, lalu
menjalankan via `npx hardhat run` dan parsing hasil JSON dari stdout.
"""
import json
import subprocess
from pathlib import Path

HARDHAT_DIR = Path(__file__).parent.parent / 'hardhat_project'

# -- Benchmark contract (semua 6 pattern dalam satu file) ---------------------
_BENCHMARK_SOL = """\
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
"""

# -- Benchmark JS script -------------------------------------------------------
_BENCHMARK_JS = """\
const { ethers } = require("hardhat");

async function gas(fn, ...args) { return await fn.estimateGas(...args); }

async function main() {
  const F  = await ethers.getContractFactory("GasBenchmark");
  const bc = await F.deploy(); await bc.waitForDeployment();
  await (await bc.setup(10)).wait();

  const data10 = Array.from({length: 10}, (_, i) => BigInt(i + 1));

  const g = {
    sload_b : await gas(bc.sload_boros),
    sload_h : await gas(bc.sload_hemat),
    loop_b  : await gas(bc.loop_boros),
    loop_h  : await gas(bc.loop_hemat),
    str_b   : await gas(bc.str_boros),
    str_h   : await gas(bc.str_hemat),
    pub_b   : await gas(bc.pub_boros, data10),
    ext_h   : await gas(bc.ext_hemat, data10),
    arith_b : await gas(bc.arith_boros, 100n),
    arith_h : await gas(bc.arith_hemat, 100n),
  };

  // Dead code: deployment gas
  const Fw = await ethers.getContractFactory("WithDeadCode");
  const Fn = await ethers.getContractFactory("WithoutDeadCode");
  const [signer] = await ethers.getSigners();
  const dead_b = await signer.provider.estimateGas(await Fw.getDeployTransaction());
  const dead_h = await signer.provider.estimateGas(await Fn.getDeployTransaction());

  const rows = [
    { pattern: "redundant_sload",      boros: g.sload_b, hemat: g.sload_h },
    { pattern: "unoptimized_loop",     boros: g.loop_b,  hemat: g.loop_h  },
    { pattern: "string_vs_bytes32",    boros: g.str_b,   hemat: g.str_h   },
    { pattern: "public_vs_external",   boros: g.pub_b,   hemat: g.ext_h   },
    { pattern: "unchecked_arithmetic", boros: g.arith_b, hemat: g.arith_h },
    { pattern: "dead_code",            boros: dead_b,    hemat: dead_h    },
  ];

  console.log("GAS_RESULTS_BEGIN");
  for (const r of rows) {
    const diff = r.boros - r.hemat;
    const pct  = (Number(diff) * 100 / Number(r.boros)).toFixed(2);
    console.log(JSON.stringify({
      pattern : r.pattern,
      boros   : r.boros.toString(),
      hemat   : r.hemat.toString(),
      diff    : diff.toString(),
      pct_save: pct,
    }));
  }
  console.log("GAS_RESULTS_END");
}
main().catch(e => { console.error(e); process.exitCode = 1; });
"""

PATTERN_LABELS = {
    'redundant_sload':      'Redundant SLOAD (3x read vs 1x cache)',
    'unoptimized_loop':     'Unoptimized Loop (.length per iter vs cached, n=10)',
    'string_vs_bytes32':    'String vs Bytes32 (read)',
    'public_vs_external':   'Public vs External (calldata array n=10)',
    'unchecked_arithmetic': 'Unchecked Arithmetic (loop n=100)',
    'dead_code':            'Dead Code (deployment cost, 3 dead funcs)',
}


def write_benchmarks():
    """Tulis GasBenchmark.sol dan run_benchmarks.js ke hardhat_project/."""
    (HARDHAT_DIR / 'contracts' / 'GasBenchmark.sol').write_text(_BENCHMARK_SOL, encoding='utf-8')
    (HARDHAT_DIR / 'scripts'   / 'run_benchmarks.js').write_text(_BENCHMARK_JS, encoding='utf-8')
    r = subprocess.run(
        'npx hardhat compile', shell=True,
        capture_output=True, text=True, cwd=HARDHAT_DIR
    )
    if r.returncode != 0:
        raise RuntimeError(f'Hardhat compile failed:\n{r.stderr}')


def measure_all():
    """
    Jalankan semua 6 benchmark dan kembalikan list of dict:
      { pattern, label, boros_gas, hemat_gas, diff_gas, pct_save }
    """
    write_benchmarks()
    r = subprocess.run(
        'npx hardhat run scripts/run_benchmarks.js --network hardhat',
        shell=True, capture_output=True, text=True, cwd=HARDHAT_DIR
    )
    if r.returncode != 0:
        raise RuntimeError(f'Benchmark failed:\n{r.stderr}')

    results = []
    in_block = False
    for line in r.stdout.splitlines():
        stripped = line.strip()
        if stripped == 'GAS_RESULTS_BEGIN':
            in_block = True
            continue
        if stripped == 'GAS_RESULTS_END':
            break
        if in_block and stripped.startswith('{'):
            d = json.loads(stripped)
            results.append({
                'pattern'  : d['pattern'],
                'label'    : PATTERN_LABELS.get(d['pattern'], d['pattern']),
                'boros_gas': int(d['boros']),
                'hemat_gas': int(d['hemat']),
                'diff_gas' : int(d['diff']),
                'pct_save' : float(d['pct_save']),
            })
    return results


def print_results(results):
    """Pretty-print tabel hasil benchmark."""
    print(f'{"Pattern":<28} {"Boros":>9} {"Hemat":>9} {"Selisih":>9} {"Hemat%":>7}')
    print('-' * 67)
    for r in results:
        print(
            f'{r["pattern"]:<28} '
            f'{r["boros_gas"]:>9,} '
            f'{r["hemat_gas"]:>9,} '
            f'{r["diff_gas"]:>9,} '
            f'{r["pct_save"]:>6.1f}%'
        )
