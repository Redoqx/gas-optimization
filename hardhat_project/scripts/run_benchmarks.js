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
