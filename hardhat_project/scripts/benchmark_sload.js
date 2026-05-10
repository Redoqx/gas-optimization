const { ethers } = require("hardhat");

async function main() {
  const F = await ethers.getContractFactory("BenchmarkSLOAD");
  const c = await F.deploy();
  await c.waitForDeployment();

  // Populate 10 items
  const tx0 = await c.populateItems(10); await tx0.wait();

  // Ukur computeBoros vs computeHemat
  const g1 = await c.computeBoros.estimateGas();
  const g2 = await c.computeHemat.estimateGas();
  const d1 = g1 - g2;
  const p1 = (Number(d1) * 100 / Number(g1)).toFixed(2);

  // Ukur sumBoros vs sumHemat
  const g3 = await c.sumBoros.estimateGas();
  const g4 = await c.sumHemat.estimateGas();
  const d2 = g3 - g4;
  const p2 = (Number(d2) * 100 / Number(g3)).toFixed(2);

  console.log("=== BENCHMARK ANTI-PATTERN GAS ===");
  console.log("[Redundant SLOAD — compute]");
  console.log("  computeBoros :", g1.toString(), "gas");
  console.log("  computeHemat :", g2.toString(), "gas");
  console.log("  Selisih      :", d1.toString(), "gas ("+p1+"%)");
  console.log("");
  console.log("[Unoptimized Loop — sum(10 items)]");
  console.log("  sumBoros     :", g3.toString(), "gas");
  console.log("  sumHemat     :", g4.toString(), "gas");
  console.log("  Selisih      :", d2.toString(), "gas ("+p2+"%)");
}
main().catch(e => { console.error(e); process.exitCode = 1; });
