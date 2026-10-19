# PII Necessity Audit

## Goal
Build a projector-friendly, four-step PII audit demo on the home page. Mock mode starts enabled and keeps all demo state in memory.

## Experience
1. Choose a sample document or upload a `.txt`, select a domain, set a prefilled purpose, and review the document text.
2. Analyze through either realistic in-memory mock responses or the configurable HTTP API. Show full-result counts, optionally hide low-signal organization/URL rows, inspect score explanations, highlight selected values in the text, and justify flagged-field overrides.
3. Anchor the report and display copyable blockchain metadata, with hashes shortened for readability and a clear privacy statement.
4. Verify the record and compare off-chain report values with returned on-chain values, showing row-level matches and an overall result.

## Supporting states
Add a settings drawer for the API base URL and mock-mode switch; provide loading, retryable errors, and backend/CORS guidance. Add the persistent research-prototype footer.

## Technical details
- Implement the single-page experience in the existing TanStack Start home route; retain in-memory state and no authentication/database.
- Keep request/response shapes in a focused client/mock module, and add focused tests for mock-mode network isolation, low-signal filtering/counts, and returned status handling.
- Use the current Tailwind v4 design tokens for the requested light navy/teal palette; use existing shadcn controls where available.
- Give the home route app-specific title, description, Open Graph and Twitter metadata. Record the initial app structure in `AGENTS.md`.
