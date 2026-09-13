const { ethers } = require("ethers");

async function checkRpc(url, name) {
  try {
    const provider = new ethers.JsonRpcProvider(url);
    const network = await provider.getNetwork();
    const blockNumber = await provider.getBlockNumber();
    const accounts = await provider.listAccounts();

    console.log(`[+] SUCCESS: Connected to ${name} at ${url}`);
    console.log(`    - Chain ID:     ${network.chainId}`);
    console.log(`    - Block Number: ${blockNumber}`);
    console.log(`    - Accounts:     ${accounts.length} found`);

    if (accounts.length > 0) {
      const balance = await provider.getBalance(accounts[0].address);
      console.log(`    - Primary Test Account: ${accounts[0].address}`);
      console.log(`    - Balance:             ${ethers.formatEther(balance)} ETH`);
    }
    return { ok: true, url, chainId: Number(network.chainId) };
  } catch (err) {
    console.log(`[-] Could not connect to ${name} at ${url} (${err.message})`);
    return { ok: false, url, error: err.message };
  }
}

async function main() {
  console.log("============================================================");
  console.log("  BLOCKCHAIN CONNECTIVITY & RPC ENDPOINT DETECTOR");
  console.log("============================================================");

  const endpoints = [
    { url: "http://127.0.0.1:8545", name: "Ganache CLI / Local RPC (8545)" },
    { url: "http://127.0.0.1:7545", name: "Ganache GUI (7545)" },
  ];

  let anyConnected = false;
  for (const ep of endpoints) {
    const res = await checkRpc(ep.url, ep.name);
    if (res.ok) {
      anyConnected = true;
    }
  }

  if (!anyConnected) {
    console.log("\n[!] Notice: No external Ganache instance currently running on :8545 or :7545.");
    console.log("    Hardhat in-memory node and Ganache CLI npm scripts are available.");
  }
}

if (require.main === module) {
  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}

module.exports = { checkRpc };
