const { ethers } = require("hardhat");

async function main() {
  const F = await ethers.getContractFactory("TestGas");
  const c = await F.deploy();
  await c.waitForDeployment();           // ethers v6

  const t1 = await c.setBoros(5); const r1 = await t1.wait();
  const t2 = await c.setHemat(5); const r2 = await t2.wait();

  const diff    = r1.gasUsed - r2.gasUsed;  // BigInt arithmetic
  const pctSave = (Number(diff) * 100 / Number(r1.gasUsed)).toFixed(2);

  console.log("=== HASIL PENGUKURAN GAS ===");
  console.log("setBoros  :", r1.gasUsed.toString());
  console.log("setHemat  :", r2.gasUsed.toString());
  console.log("Selisih   :", diff.toString(), "gas");
  console.log("Penghematan:", pctSave + "%");
}
main().catch(e => { console.error(e); process.exitCode = 1; });
