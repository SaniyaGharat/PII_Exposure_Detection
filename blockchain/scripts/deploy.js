const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("============================================================");
  console.log("  DEPLOYING PIINecessityAudit CONTRACT TO GANACHE");
  console.log("============================================================");

  const [deployer] = await hre.ethers.getSigners();
  const network = await hre.ethers.provider.getNetwork();
  const balance = await hre.ethers.provider.getBalance(deployer.address);

  console.log(`Deployer Account: ${deployer.address}`);
  console.log(`Deployer Balance: ${hre.ethers.formatEther(balance)} ETH`);
  console.log(`Target Network:   ${network.name} (Chain ID: ${network.chainId})`);

  const Factory = await hre.ethers.getContractFactory("PIINecessityAudit");
  const contract = await Factory.deploy();
  await contract.waitForDeployment();

  const contractAddress = await contract.getAddress();
  const deploymentTx = contract.deploymentTransaction();
  const receipt = await deploymentTx.wait();

  console.log(`\n[+] Contract Deployed Successfully!`);
  console.log(`    - Contract Address: ${contractAddress}`);
  console.log(`    - Tx Hash:          ${deploymentTx.hash}`);
  console.log(`    - Block Number:     ${receipt.blockNumber}`);
  console.log(`    - Gas Used:         ${receipt.gasUsed.toString()}`);

  // Load ABI from Hardhat artifact
  const artifactPath = path.join(
    __dirname,
    "../artifacts/contracts/PIINecessityAudit.sol/PIINecessityAudit.json"
  );
  const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf-8"));

  const deploymentData = {
    contract_name: "PIINecessityAudit",
    contract_address: contractAddress,
    deployer_address: deployer.address,
    network: {
      name: network.name,
      chainId: Number(network.chainId),
      rpc_url: hre.network.config.url || "http://127.0.0.1:8545",
    },
    deployment_tx_hash: deploymentTx.hash,
    deployment_block: receipt.blockNumber,
    deployment_gas_used: receipt.gasUsed.toString(),
    deployment_timestamp: Math.floor(Date.now() / 1000),
    abi: artifact.abi,
  };

  const outputPath = path.join(__dirname, "../deployment.json");
  fs.writeFileSync(outputPath, JSON.stringify(deploymentData, null, 2), "utf-8");
  console.log(`\n[+] Deployment metadata & ABI saved to: ${outputPath}`);
}

main().catch((error) => {
  console.error("Deployment failed:", error);
  process.exitCode = 1;
});
