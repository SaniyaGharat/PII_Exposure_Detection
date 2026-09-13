// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title PIINecessityAudit
 * @author PII Exposure Detection & Necessity Minimization Research Framework
 * @notice Tamper-proof, privacy-preserving blockchain audit trail for PII minimization assessments.
 *
 * ==============================================================================================
 * CRITICAL PRIVACY & GDPR COMPLIANCE CONSTRAINT (SECTION 3.5 & 6.1):
 * ----------------------------------------------------------------------------------------------
 * UNDER NO CIRCUMSTANCES SHALL RAW PII (NAMES, SSNs, ADDRESSES, DATES OF BIRTH, PHONE NUMBERS,
 * MEDICAL RECORDS, OR FULL DOCUMENT TEXTS) EVER BE ACCEPTED, EMITTED IN EVENTS, OR STORED IN
 * ON-CHAIN STORAGE VARIABLES WITHIN THIS CONTRACT.
 *
 * IN COMPLIANCE WITH ARTICLE 17 (GDPR RIGHT TO ERASURE) AND PUBLIC/PERMISSIONED LEDGER IMMUTABILITY:
 * 1. Document files are anchored solely as cryptographic Keccak-256 hashes (`docHash`).
 * 2. Necessity evaluation reports are anchored solely as canonicalized JSON Keccak-256 hashes (`reportHash`).
 * 3. Overrides are anchored solely as field type and justification hashes (`fieldTypeHash`, `justificationHash`).
 * 4. All metadata is strictly non-sensitive (recipient addresses, purpose strings, aggregate field counts).
 * ==============================================================================================
 */
contract PIINecessityAudit {

    /// @notice Audit record capturing an anchored document-sharing event.
    struct ShareRecord {
        address sender;
        address recipient;
        string purpose;
        bytes32 reportHash;
        uint256 flaggedCount;
        uint256 totalFieldCount;
        bool overridden;
        uint256 timestamp;
    }

    /// @notice Audit record capturing a contextual human or compliance override.
    struct OverrideRecord {
        bytes32 fieldTypeHash;
        bytes32 justificationHash;
        address approver;
        uint256 timestamp;
    }

    /// @notice Primary mapping from document Keccak-256 hash to its immutable sharing record.
    mapping(bytes32 => ShareRecord) public shareRecords;

    /// @notice Mapping from document Keccak-256 hash to an array of recorded overrides.
    mapping(bytes32 => OverrideRecord[]) private overrideLogs;

    // --- Events ---

    event DocumentShared(
        bytes32 indexed docHash,
        address indexed sender,
        address indexed recipient,
        string purpose,
        bytes32 reportHash,
        uint256 flaggedCount,
        uint256 totalFieldCount,
        uint256 timestamp
    );

    event OverrideLogged(
        bytes32 indexed docHash,
        address indexed sender,
        bytes32 fieldTypeHash,
        bytes32 justificationHash,
        uint256 timestamp
    );

    // --- Custom Errors ---
    error DocumentAlreadyRegistered(bytes32 docHash, uint256 registeredTimestamp);
    error DocumentNotFound(bytes32 docHash);
    error UnauthorizedCaller(address caller, address expectedSender);
    error InvalidZeroHash(string parameter);
    error InvalidZeroAddress(string parameter);
    error EmptyPurposeString();

    /**
     * @notice Registers a new document-sharing audit event with necessity assessment summary.
     * @dev Enforces strict duplicate prevention: attempting to register the same `docHash` twice
     * reverts. Document audit records are immutable cryptographic anchors; if document content
     * is modified, its Keccak-256 hash changes accordingly. If identical bytes are shared again,
     * the initial provenance timestamp and audit report remain authoritative.
     *
     * @param docHash Keccak-256 hash of the complete document file bytes.
     * @param recipient Ethereum address of the intended receiving party/organization.
     * @param purpose Plaintext identifier for the data collection/sharing purpose.
     * @param reportHash Keccak-256 hash of the canonicalized necessity audit JSON report.
     * @param flaggedCount Number of fields flagged as unnecessary / minimized.
     * @param totalFieldCount Total number of PII fields detected in the document.
     */
    function registerDocumentShare(
        bytes32 docHash,
        address recipient,
        string calldata purpose,
        bytes32 reportHash,
        uint256 flaggedCount,
        uint256 totalFieldCount
    ) external {
        if (docHash == bytes32(0)) revert InvalidZeroHash("docHash");
        if (recipient == address(0)) revert InvalidZeroAddress("recipient");
        if (bytes(purpose).length == 0) revert EmptyPurposeString();
        if (reportHash == bytes32(0)) revert InvalidZeroHash("reportHash");

        // Immutable Anchor Check: Revert on duplicate registration
        if (shareRecords[docHash].timestamp != 0) {
            revert DocumentAlreadyRegistered(docHash, shareRecords[docHash].timestamp);
        }

        shareRecords[docHash] = ShareRecord({
            sender: msg.sender,
            recipient: recipient,
            purpose: purpose,
            reportHash: reportHash,
            flaggedCount: flaggedCount,
            totalFieldCount: totalFieldCount,
            overridden: false,
            timestamp: block.timestamp
        });

        emit DocumentShared(
            docHash,
            msg.sender,
            recipient,
            purpose,
            reportHash,
            flaggedCount,
            totalFieldCount,
            block.timestamp
        );
    }

    /**
     * @notice Logs an authorized human/compliance policy override for a previously flagged field.
     * @dev Restricts caller to the original sender address that anchored the document share.
     *
     * @param docHash Keccak-256 hash of the registered document.
     * @param fieldTypeHash Keccak-256 hash of the field type identifier (e.g., keccak256("marital_status")).
     * @param justificationHash Keccak-256 hash of the human justification text.
     */
    function logOverride(
        bytes32 docHash,
        bytes32 fieldTypeHash,
        bytes32 justificationHash
    ) external {
        ShareRecord storage record = shareRecords[docHash];
        if (record.timestamp == 0) revert DocumentNotFound(docHash);
        if (msg.sender != record.sender) revert UnauthorizedCaller(msg.sender, record.sender);
        if (fieldTypeHash == bytes32(0)) revert InvalidZeroHash("fieldTypeHash");
        if (justificationHash == bytes32(0)) revert InvalidZeroHash("justificationHash");

        record.overridden = true;

        overrideLogs[docHash].push(OverrideRecord({
            fieldTypeHash: fieldTypeHash,
            justificationHash: justificationHash,
            approver: msg.sender,
            timestamp: block.timestamp
        }));

        emit OverrideLogged(
            docHash,
            msg.sender,
            fieldTypeHash,
            justificationHash,
            block.timestamp
        );
    }

    /**
     * @notice Verifies an existing document share record by its cryptographic hash.
     * @param docHash Keccak-256 hash of the document.
     * @return sender Address of the sharing party.
     * @return recipient Address of the receiving party.
     * @return purpose Declared sharing purpose string.
     * @return reportHash Anchored hash of the off-chain necessity report.
     * @return flaggedCount Number of minimized/flagged fields.
     * @return totalFieldCount Total PII fields assessed.
     * @return overridden Boolean indicating whether any fields were overridden.
     * @return timestamp Block timestamp when the document share was anchored.
     */
    function verifyShare(bytes32 docHash)
        external
        view
        returns (
            address sender,
            address recipient,
            string memory purpose,
            bytes32 reportHash,
            uint256 flaggedCount,
            uint256 totalFieldCount,
            bool overridden,
            uint256 timestamp
        )
    {
        ShareRecord storage record = shareRecords[docHash];
        if (record.timestamp == 0) revert DocumentNotFound(docHash);

        return (
            record.sender,
            record.recipient,
            record.purpose,
            record.reportHash,
            record.flaggedCount,
            record.totalFieldCount,
            record.overridden,
            record.timestamp
        );
    }

    /**
     * @notice Retrieves the number of overrides logged for a specific document hash.
     * @param docHash Keccak-256 hash of the document.
     * @return count Total count of logged overrides.
     */
    function getOverrideCount(bytes32 docHash) external view returns (uint256 count) {
        if (shareRecords[docHash].timestamp == 0) revert DocumentNotFound(docHash);
        return overrideLogs[docHash].length;
    }

    /**
     * @notice Retrieves a specific override entry by document hash and index.
     * @param docHash Keccak-256 hash of the document.
     * @param index Zero-based index in the document's override log array.
     * @return fieldTypeHash Keccak-256 hash of the overridden field type.
     * @return justificationHash Keccak-256 hash of the justification text.
     * @return approver Address that authorized the override.
     * @return timestamp Block timestamp of the override event.
     */
    function getOverride(bytes32 docHash, uint256 index)
        external
        view
        returns (
            bytes32 fieldTypeHash,
            bytes32 justificationHash,
            address approver,
            uint256 timestamp
        )
    {
        if (shareRecords[docHash].timestamp == 0) revert DocumentNotFound(docHash);
        require(index < overrideLogs[docHash].length, "Override index out of bounds");
        OverrideRecord storage ov = overrideLogs[docHash][index];
        return (ov.fieldTypeHash, ov.justificationHash, ov.approver, ov.timestamp);
    }
}
