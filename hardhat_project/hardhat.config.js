import "@nomicfoundation/hardhat-toolbox";

export default {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: { enabled: false },  // WAJIB false
    },
  },
  networks: { hardhat: {} },
};
