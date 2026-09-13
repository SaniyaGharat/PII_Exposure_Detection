"""
PII Exposure Detection - Blockchain Audit Client (Web3.py Integration)
Provides high-level Python interfaces for anchoring document-sharing events,
necessity reports, and policy overrides onto the Solidity PIINecessityAudit contract.

Strict Privacy & Compliance Guarantee:
No raw document text or PII values are ever transmitted to or stored on the blockchain.
All operations anchor cryptographic Keccak-256 hashes and non-sensitive summary counts.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from hexbytes import HexBytes
from web3 import Web3


def canonicalize_json(data: Union[Dict[str, Any], List[Any]]) -> bytes:
    """
    Produces deterministic canonical JSON byte representation (sorted keys, compact separators).
    Ensures identical JSON objects always produce identical cryptographic hashes cross-platform.
    """
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


class BlockchainAuditClient:
    """
    Python client interfacing with the on-chain PIINecessityAudit smart contract.
    """

    def __init__(
        self,
        deployment_file: Optional[Union[str, Path]] = None,
        rpc_url: Optional[str] = None,
        default_account: Optional[str] = None,
    ):
        """
        Initializes Web3 provider, loads contract ABI and deployed address.
        """
        if deployment_file is None:
            # Default to project blockchain/deployment.json
            project_root = Path(__file__).resolve().parent.parent.parent
            deployment_file = project_root / "blockchain" / "deployment.json"

        self.deployment_file = Path(deployment_file)
        if not self.deployment_file.exists():
            raise FileNotFoundError(
                f"Blockchain deployment file not found at: {self.deployment_file}. "
                "Please deploy the contract first via 'npx hardhat run scripts/deploy.js --network localhost'."
            )

        with open(self.deployment_file, "r", encoding="utf-8") as f:
            self.deployment_data = json.load(f)

        self.contract_address = Web3.to_checksum_address(self.deployment_data["contract_address"])
        self.abi = self.deployment_data["abi"]

        # Configure RPC provider
        target_rpc = rpc_url or self.deployment_data.get("network", {}).get("rpc_url", "http://127.0.0.1:8545")
        self.w3 = Web3(Web3.HTTPProvider(target_rpc))

        if not self.w3.is_connected():
            raise ConnectionError(
                f"Failed to connect to Ethereum / Ganache node at {target_rpc}. "
                "Ensure Ganache is running on the specified port."
            )

        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

        # Set default account (defaulting to first funded account in Ganache)
        available_accounts = self.w3.eth.accounts
        if default_account:
            self.default_account = Web3.to_checksum_address(default_account)
        elif available_accounts:
            self.default_account = Web3.to_checksum_address(available_accounts[0])
        else:
            self.default_account = None

    # -------------------------------------------------------------------------
    # Cryptographic Hashing Utilities (Keccak-256)
    # -------------------------------------------------------------------------

    @staticmethod
    def compute_document_hash(document_path: Union[str, Path, bytes]) -> bytes:
        """
        Computes the Keccak-256 cryptographic hash of a document file's raw bytes.
        Matches Solidity keccak256(bytes).
        """
        if isinstance(document_path, (str, Path)):
            file_bytes = Path(document_path).read_bytes()
        elif isinstance(document_path, bytes):
            file_bytes = document_path
        else:
            raise TypeError("document_path must be a str, Path, or bytes object")

        return Web3.keccak(file_bytes)

    @staticmethod
    def compute_report_hash(report_data: Union[str, Path, Dict[str, Any]]) -> bytes:
        """
        Computes the Keccak-256 hash of a canonicalized necessity JSON audit report.
        """
        if isinstance(report_data, (str, Path)):
            with open(report_data, "r", encoding="utf-8") as f:
                parsed = json.load(f)
            canonical_bytes = canonicalize_json(parsed)
        elif isinstance(report_data, dict):
            canonical_bytes = canonicalize_json(report_data)
        else:
            raise TypeError("report_data must be a filepath (str/Path) or dict")

        return Web3.keccak(canonical_bytes)

    @staticmethod
    def compute_string_hash(text: str) -> bytes:
        """
        Computes Keccak-256 hash of a UTF-8 string (used for field types and override justifications).
        """
        return Web3.keccak(text=text)

    # -------------------------------------------------------------------------
    # Core Blockchain Audit Actions
    # -------------------------------------------------------------------------

    def is_document_registered(self, document_path: Union[str, Path, bytes]) -> bool:
        """
        Checks whether a document is already registered on-chain.
        """
        if isinstance(document_path, bytes) and len(document_path) == 32:
            doc_hash = document_path
        else:
            doc_hash = self.compute_document_hash(document_path)

        try:
            record = self.contract.functions.shareRecords(doc_hash).call()
            # record struct: sender, recipient, purpose, reportHash, flaggedCount, totalFieldCount, overridden, timestamp
            return record[7] > 0
        except Exception:
            return False

    def register_share(
        self,
        document_path: Union[str, Path],
        recipient_address: str,
        purpose: str,
        necessity_report: Union[str, Path, Dict[str, Any]],
        sender_address: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Anchors a document sharing event and its necessity assessment onto the blockchain.

        Args:
            document_path: Path to the raw document file (to compute docHash).
            recipient_address: Ethereum address of receiving organization.
            purpose: Declared data collection purpose (e.g. 'employment_screening').
            necessity_report: Necessity report dict or path to report JSON.
            sender_address: Optional sender address (defaults to self.default_account).

        Returns:
            Dictionary containing transaction hash, block number, gas used, and hashes.
        """
        sender = Web3.to_checksum_address(sender_address or self.default_account)
        recipient = Web3.to_checksum_address(recipient_address)

        # 1. Compute Cryptographic Hashes (NO raw PII leaves the client)
        doc_hash = self.compute_document_hash(document_path)
        report_hash = self.compute_report_hash(necessity_report)

        # 2. Extract Non-Sensitive Summary Statistics
        if isinstance(necessity_report, (str, Path)):
            with open(necessity_report, "r", encoding="utf-8") as f:
                report_dict = json.load(f)
        else:
            report_dict = necessity_report

        flagged_count = int(
            report_dict.get(
                "total_unnecessary_flagged",
                report_dict.get("flagged_for_minimization", report_dict.get("flagged_unnecessary_count", 0)),
            )
        )
        total_field_count = int(
            report_dict.get(
                "total_fields",
                report_dict.get("total_fields_evaluated", 0),
            )
        )

        # 3. Submit Transaction to Smart Contract
        tx_hash = self.contract.functions.registerDocumentShare(
            doc_hash,
            recipient,
            purpose,
            report_hash,
            flagged_count,
            total_field_count,
        ).transact({"from": sender})
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        tx_hex = receipt.transactionHash.hex()
        if not tx_hex.startswith("0x"):
            tx_hex = "0x" + tx_hex

        return {
            "status": "SUCCESS" if receipt.status == 1 else "FAILED",
            "transaction_hash": tx_hex,
            "block_number": receipt.blockNumber,
            "gas_used": int(receipt.gasUsed),
            "sender": sender,
            "recipient": recipient,
            "purpose": purpose,
            "doc_hash": "0x" + doc_hash.hex(),
            "report_hash": "0x" + report_hash.hex(),
            "flagged_count": flagged_count,
            "total_field_count": total_field_count,
        }

    def log_override(
        self,
        document_path: Union[str, Path, bytes],
        field_type: str,
        justification_text: str,
        approver_address: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Logs an authorized compliance override for a flagged field onto the blockchain.

        Args:
            document_path: Path to the document file or its raw bytes32 hash.
            field_type: Name of overridden field (e.g. 'home_address').
            justification_text: Text justifying why the flagged field is shared.
            approver_address: Caller address (must match the document's original sender).

        Returns:
            Dictionary containing transaction hash, gas used, and override details.
        """
        approver = Web3.to_checksum_address(approver_address or self.default_account)

        if isinstance(document_path, bytes) and len(document_path) == 32:
            doc_hash = document_path
        else:
            doc_hash = self.compute_document_hash(document_path)

        field_type_hash = self.compute_string_hash(field_type)
        justification_hash = self.compute_string_hash(justification_text)

        tx_hash = self.contract.functions.logOverride(
            doc_hash,
            field_type_hash,
            justification_hash,
        ).transact({"from": approver})

        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        ov_tx_hex = receipt.transactionHash.hex()
        if not ov_tx_hex.startswith("0x"):
            ov_tx_hex = "0x" + ov_tx_hex

        return {
            "status": "SUCCESS" if receipt.status == 1 else "FAILED",
            "transaction_hash": ov_tx_hex,
            "block_number": receipt.blockNumber,
            "gas_used": int(receipt.gasUsed),
            "doc_hash": "0x" + doc_hash.hex(),
            "field_type": field_type,
            "field_type_hash": "0x" + field_type_hash.hex(),
            "justification_text": justification_text,
            "justification_hash": "0x" + justification_hash.hex(),
            "approver": approver,
        }

    def verify_share(
        self,
        document_path: Union[str, Path, bytes],
    ) -> Dict[str, Any]:
        """
        Queries the blockchain to verify whether a document has an immutable sharing record,
        returning the on-chain metadata and any logged overrides.

        Args:
            document_path: Path to document file or its raw bytes32 hash.

        Returns:
            Structured dictionary with on-chain audit record details.
        """
        if isinstance(document_path, bytes) and len(document_path) == 32:
            doc_hash = document_path
        else:
            doc_hash = self.compute_document_hash(document_path)

        (
            sender,
            recipient,
            purpose,
            report_hash_bytes,
            flagged_count,
            total_field_count,
            overridden,
            timestamp,
        ) = self.contract.functions.verifyShare(doc_hash).call()

        # Fetch any logged overrides
        override_count = self.contract.functions.getOverrideCount(doc_hash).call()
        overrides: List[Dict[str, Any]] = []
        for i in range(override_count):
            ft_hash, just_hash, app_addr, ov_time = self.contract.functions.getOverride(doc_hash, i).call()
            overrides.append({
                "index": i,
                "field_type_hash": "0x" + ft_hash.hex() if isinstance(ft_hash, bytes) else str(ft_hash),
                "justification_hash": "0x" + just_hash.hex() if isinstance(just_hash, bytes) else str(just_hash),
                "approver": app_addr,
                "timestamp": ov_time,
            })

        return {
            "is_verified": True,
            "doc_hash": "0x" + doc_hash.hex(),
            "sender": sender,
            "recipient": recipient,
            "purpose": purpose,
            "report_hash": "0x" + report_hash_bytes.hex() if isinstance(report_hash_bytes, bytes) else str(report_hash_bytes),
            "flagged_count": int(flagged_count),
            "total_field_count": int(total_field_count),
            "overridden": overridden,
            "timestamp": int(timestamp),
            "override_count": override_count,
            "overrides": overrides,
        }
