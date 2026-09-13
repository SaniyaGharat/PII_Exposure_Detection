const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("PIINecessityAudit Smart Contract", function () {
  let auditContract;
  let owner, recipient, unauthorizedAccount;

  // Test data hashes
  const sampleDocHash = ethers.keccak256(ethers.toUtf8Bytes("Sample Document 001 Raw Text Content"));
  const sampleReportHash = ethers.keccak256(ethers.toUtf8Bytes(JSON.stringify({ doc_id: "doc_001", flagged: 3, total: 10 })));
  const samplePurpose = "employment_screening";
  const sampleFlaggedCount = 3n;
  const sampleTotalCount = 10n;

  const sampleFieldTypeHash = ethers.keccak256(ethers.toUtf8Bytes("home_address"));
  const sampleJustificationHash = ethers.keccak256(ethers.toUtf8Bytes("Candidate approved relocation assistance review"));

  beforeEach(async function () {
    [owner, recipient, unauthorizedAccount] = await ethers.getSigners();
    const Factory = await ethers.getContractFactory("PIINecessityAudit");
    auditContract = await Factory.deploy();
    await auditContract.waitForDeployment();
  });

  describe("1. Document Share Registration", function () {
    it("should successfully register a document share and emit DocumentShared event", async function () {
      const tx = await auditContract.registerDocumentShare(
        sampleDocHash,
        recipient.address,
        samplePurpose,
        sampleReportHash,
        sampleFlaggedCount,
        sampleTotalCount
      );

      const receipt = await tx.wait();
      expect(receipt.status).to.equal(1);

      await expect(tx)
        .to.emit(auditContract, "DocumentShared")
        .withArgs(
          sampleDocHash,
          owner.address,
          recipient.address,
          samplePurpose,
          sampleReportHash,
          sampleFlaggedCount,
          sampleTotalCount,
          (ts) => ts > 0n
        );
    });

    it("should measure exact gas used for registerDocumentShare", async function () {
      const tx = await auditContract.registerDocumentShare(
        sampleDocHash,
        recipient.address,
        samplePurpose,
        sampleReportHash,
        sampleFlaggedCount,
        sampleTotalCount
      );
      const receipt = await tx.wait();
      console.log(`\n    [Gas Benchmark] registerDocumentShare gas used: ${receipt.gasUsed.toString()} units`);
      expect(receipt.gasUsed).to.be.gt(0n);
    });

    it("should reject duplicate registration of the same docHash with DocumentAlreadyRegistered", async function () {
      await auditContract.registerDocumentShare(
        sampleDocHash,
        recipient.address,
        samplePurpose,
        sampleReportHash,
        sampleFlaggedCount,
        sampleTotalCount
      );

      // Attempt second registration with same docHash
      await expect(
        auditContract.registerDocumentShare(
          sampleDocHash,
          recipient.address,
          "another_purpose",
          sampleReportHash,
          1n,
          5n
        )
      ).to.be.revertedWithCustomError(auditContract, "DocumentAlreadyRegistered");
    });

    it("should reject zero docHash or empty purpose", async function () {
      await expect(
        auditContract.registerDocumentShare(
          ethers.ZeroHash,
          recipient.address,
          samplePurpose,
          sampleReportHash,
          sampleFlaggedCount,
          sampleTotalCount
        )
      ).to.be.revertedWithCustomError(auditContract, "InvalidZeroHash");

      await expect(
        auditContract.registerDocumentShare(
          sampleDocHash,
          recipient.address,
          "",
          sampleReportHash,
          sampleFlaggedCount,
          sampleTotalCount
        )
      ).to.be.revertedWithCustomError(auditContract, "EmptyPurposeString");
    });
  });

  describe("2. On-Chain Verification (verifyShare)", function () {
    it("should return exact registered data matching off-chain report parameters", async function () {
      const tx = await auditContract.registerDocumentShare(
        sampleDocHash,
        recipient.address,
        samplePurpose,
        sampleReportHash,
        sampleFlaggedCount,
        sampleTotalCount
      );
      await tx.wait();

      const record = await auditContract.verifyShare(sampleDocHash);
      expect(record.sender).to.equal(owner.address);
      expect(record.recipient).to.equal(recipient.address);
      expect(record.purpose).to.equal(samplePurpose);
      expect(record.reportHash).to.equal(sampleReportHash);
      expect(record.flaggedCount).to.equal(sampleFlaggedCount);
      expect(record.totalFieldCount).to.equal(sampleTotalCount);
      expect(record.overridden).to.equal(false);
      expect(record.timestamp).to.be.gt(0n);
    });

    it("should revert with DocumentNotFound if docHash has not been registered", async function () {
      const unknownHash = ethers.keccak256(ethers.toUtf8Bytes("Unknown Document"));
      await expect(auditContract.verifyShare(unknownHash)).to.be.revertedWithCustomError(
        auditContract,
        "DocumentNotFound"
      );
    });
  });

  describe("3. Compliance & Human Overrides (logOverride)", function () {
    beforeEach(async function () {
      await auditContract.registerDocumentShare(
        sampleDocHash,
        recipient.address,
        samplePurpose,
        sampleReportHash,
        sampleFlaggedCount,
        sampleTotalCount
      );
    });

    it("should allow original sender to log an override and update overridden state", async function () {
      const tx = await auditContract.logOverride(
        sampleDocHash,
        sampleFieldTypeHash,
        sampleJustificationHash
      );
      const receipt = await tx.wait();

      console.log(`\n    [Gas Benchmark] logOverride gas used: ${receipt.gasUsed.toString()} units`);

      await expect(tx)
        .to.emit(auditContract, "OverrideLogged")
        .withArgs(
          sampleDocHash,
          owner.address,
          sampleFieldTypeHash,
          sampleJustificationHash,
          (ts) => ts > 0n
        );

      const record = await auditContract.verifyShare(sampleDocHash);
      expect(record.overridden).to.equal(true);

      const overrideCount = await auditContract.getOverrideCount(sampleDocHash);
      expect(overrideCount).to.equal(1n);

      const overrideDetail = await auditContract.getOverride(sampleDocHash, 0);
      expect(overrideDetail.fieldTypeHash).to.equal(sampleFieldTypeHash);
      expect(overrideDetail.justificationHash).to.equal(sampleJustificationHash);
      expect(overrideDetail.approver).to.equal(owner.address);
    });

    it("should reject override from unauthorized account with UnauthorizedCaller error", async function () {
      await expect(
        auditContract.connect(unauthorizedAccount).logOverride(
          sampleDocHash,
          sampleFieldTypeHash,
          sampleJustificationHash
        )
      ).to.be.revertedWithCustomError(auditContract, "UnauthorizedCaller");
    });

    it("should reject override on non-existent document with DocumentNotFound", async function () {
      const unknownHash = ethers.keccak256(ethers.toUtf8Bytes("NonExistentDoc"));
      await expect(
        auditContract.logOverride(
          unknownHash,
          sampleFieldTypeHash,
          sampleJustificationHash
        )
      ).to.be.revertedWithCustomError(auditContract, "DocumentNotFound");
    });
  });
});
