# Privacy Necessity Audit

Build a single-page web app called "PII Necessity Audit" for demoing a research

project. The project takes a shared document (job application, medical intake,

loan application, rental agreement), detects personal information (PII) in it,

scores whether each field is actually necessary for the document's purpose,

and then records the decision on a blockchain (hashes only, never raw PII).

The frontend is a guided demo of that 4-step flow.

TECH: React + TypeScript + Tailwind + shadcn/ui. No auth, no database. All

state in memory.

DESIGN: Clean, professional, light theme. Navy (#1F3864) primary, teal (#0F766E)

accent, light gray (#F5F7FA) background, white cards. Status colors: red =

flagged/unnecessary, amber = review/contextual, green = cleared/necessary.

Use a stepper at the top showing the 4 steps and the current one.

STEP 1 - SELECT DOCUMENT

- Dropdown of sample documents (from GET /api/samples) OR upload a .txt file.

- Domain select: job_application, medical_intake, loan_application,

  rental_agreement.

- Purpose text input, prefilled as "<domain>_review_and_processing".

- "Analyze document" button.

- Show the document text in a scrollable monospace panel.

STEP 2 - DETECTION AND NECESSITY RESULTS (after POST /api/analyze)

- Four summary cards: Total fields detected, Flagged (red), Needs review

  (amber), Cleared (green).

- Table with columns: Field type, Detected value, Necessity score N (show as a

  0-1 bar plus number), Status badge, and an expandable row showing R (rule

  score), M (model score) and the justification text.

- Status thresholds are returned by the API as "flagged" (N < 0.35),

  "review" (0.35 to 0.65), "cleared" (N > 0.65). Do not recompute them.

- Toggle "Hide low-signal organization/url detections" ON by default. When on,

  hide rows whose field_type is "organization" or "url" and show a note like

  "11 low-signal detections hidden (documented detector limitation); still

  included in the saved report". The summary cards must always show FULL counts,

  not filtered counts.

- Clicking a value in the table highlights that value in the document panel.

- On each flagged row, an "Override" button opens a modal asking for a

  justification, then calls POST /api/override. Show the returned transaction

  hash in a toast.

STEP 3 - ANCHOR ON-CHAIN

- Button "Anchor on blockchain" calls POST /api/anchor.

- Show a result card: transaction hash, block number, gas used, document hash,

  report hash, contract address, each with a copy button and the long hashes

  truncated in the middle.

- Callout: "Only hashes, the purpose, and counts are stored on-chain. The

  document and its PII never touch the chain."

STEP 4 - VERIFY

- Button "Verify on-chain record" calls GET /api/verify/{document_id}.

- Two-column comparison: Off-chain report (purpose, flagged count, total

  fields) vs On-chain record (sender, recipient, purpose, flagged count, total

  field count, overridden yes/no, timestamp). A green check beside each row

  that matches, a red cross if not. Overall banner: "Record verified" or

  "Mismatch detected".

API CONTRACT (base URL configurable in a settings drawer, default

http://localhost:8000):

- GET  /api/samples -> [{id, label, domain}]

- POST /api/analyze  body {document_text, domain, purpose}

    -> {document_id, domain, purpose, total_fields, flagged_count,

        fields:[{field_type, value, N, R, M, status, justification}]}

- POST /api/anchor   body {document_id}

    -> {transaction_hash, block_number, gas_used, doc_hash, report_hash,

        contract_address}

- POST /api/override body {document_id, field_type, justification}

    -> {transaction_hash, gas_used}

- GET  /api/verify/{document_id}

    -> {sender, recipient, purpose, flagged_count, total_field_count,

        overridden, timestamp}

Handle loading states, errors (friendly message + retry), and CORS failures

(message telling the user to check that the backend is running).

MOCK MODE: A "Use mock data" switch in the settings drawer, ON by default.

When on, never call the network; return realistic fake responses for a job

application with about 18 fields (full_name N=1.00 cleared; date_of_birth

N=0.00 flagged; religion N=0.02 flagged; marital_status N=0.10 flagged;

national_id N=0.03 flagged; gender N=0.48 review; email, phone, skills

cleared; plus 2 organization and 1 url row), a fake transaction hash, gas used

231147, and a verify response that matches.

FOOTER: Small persistent note: "Research prototype. Runs on a local test

blockchain (Ganache); not production-ready. OCR on scanned documents is a known

weak spot for medical and biometric fields."

Keep the UI uncluttered and presentation-friendly: large readable type, since

this will be shown live on a projector.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/e449cce3-4bc0-5c45-b681-5b4a6e403ad9).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
