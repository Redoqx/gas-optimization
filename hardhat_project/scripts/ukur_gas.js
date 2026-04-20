import { ethers } from "hardhat";

async function main() {
  const F = await ethers.getContractFactory("TestGas");
  const c = await F.deploy();
  await c.waitForDeployment();

  const t1 = await c.setBoros(5); const r1 = await t1.wait();
  const t2 = await c.setHemat(5); const r2 = await t2.wait();

  const diff    = r1.gasUsed - r2.gasUsed;
  const pctSave = ((Number(diff) / Number(r1.gasUsed)) * 100).toFixed(2);

  console.log("=== HASIL PENGUKURAN GAS ===");
  console.log("setBoros  :", r1.gasUsed.toString());
  console.log("setHemat  :", r2.gasUsed.toString());
  console.log("Selisih   :", diff.toString(), "gas");
  console.log("Penghematan:", pctSave + "%");
}
main().catch(e => { console.error(e); process.exitCode = 1; });
