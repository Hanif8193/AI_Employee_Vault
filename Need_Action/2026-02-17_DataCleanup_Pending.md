# Task: Data Cleanup — Bronze Layer

**Priority:** [HIGH]
**Status:** Pending
**Created:** 2026-02-17
**Assigned To:** AI Agent
**Due Date:** 2026-02-18

---

## Description

Raw CSV files have been received in the `inbox/` folder. They need to be validated, cleaned, and pushed through the Bronze → Silver → Gold pipeline.

---

## Steps

- [ ] 1. Move raw files from `inbox/` to Bronze layer input
- [ ] 2. Run validation — check for nulls, duplicates, schema mismatches
- [ ] 3. Log any data quality issues found
- [ ] 4. Execute `run_pipeline.py` to process through Silver and Gold layers
- [ ] 5. Verify Gold layer output is complete and accurate
- [ ] 6. Move this task file to `Done/` and update `Dashboard.md`

---

## Acceptance Criteria

- No null values in required fields
- No duplicate records in output
- Gold layer file count matches expected record count
- Log entry created in `Logs/`

---

## Output

> _(To be filled when task is completed)_

---

## Notes

- If pipeline fails at any step, log the error and do not proceed to next step
- If data anomalies exceed 5%, escalate to Vault Owner before continuing
