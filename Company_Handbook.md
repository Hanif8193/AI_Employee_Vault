# AI Employee Vault — Company Handbook

> Version: 1.0
> Effective Date: 2026-02-17
> Authority: Vault Owner

---

## Purpose

This handbook defines the operating rules, standards, and expectations for all AI employees and agents working within this vault. Every agent must read, understand, and comply with these rules at all times.

---

## Core Rules

### Rule 1 — Always Log Important Actions

- Every significant action (file creation, deletion, task update, pipeline run) **must be logged** in the `Logs/` folder.
- Log entries must include: **date, action taken, outcome, and agent/user responsible**.
- Silence is not acceptable. If something happened, it must be recorded.

**Example log entry format:**
```
[2026-02-17] ACTION: Created Dashboard.md | OUTCOME: Success | BY: AI Agent
```

---

### Rule 2 — Never Take Destructive Actions Without Confirmation

- **Destructive actions** include: deleting files, overwriting data, clearing folders, dropping databases, or any irreversible operation.
- Always pause and ask for explicit confirmation before proceeding.
- If operating autonomously and confirmation is not possible, **abort the action** and log the reason.

**Confirmation template:**
```
⚠️ DESTRUCTIVE ACTION DETECTED
Action: [describe the action]
Target: [file/folder/data affected]
Awaiting confirmation before proceeding. Type YES to confirm.
```

---

### Rule 3 — Move Completed Tasks to Done

- When a task is fully finished and verified, move the relevant file or record to the `Done/` folder.
- Update `Dashboard.md` — remove from **Pending Tasks**, add to **Completed Tasks**.
- Never leave completed work sitting in `Need_Action/` or `inbox/`.

**Completion checklist:**
- [ ] Task output verified
- [ ] File moved to `Done/`
- [ ] Dashboard updated
- [ ] Log entry created

---

### Rule 4 — Keep Task Files Structured

- All task files must follow a consistent format with clear sections: **Title, Description, Steps, Status, Output**.
- Files in `Need_Action/` must have a priority label: `[HIGH]`, `[MEDIUM]`, or `[LOW]`.
- No loose, unnamed, or undated files. Every file gets a meaningful name.

**Naming convention:**
```
YYYY-MM-DD_TaskName_Status.md
Example: 2026-02-17_DataCleanup_Pending.md
```

---

### Rule 5 — If Unsure, Ask for Clarification

- When a task is ambiguous, instructions are incomplete, or the correct path forward is unclear — **stop and ask**.
- Do not guess or make assumptions that could lead to errors or wasted work.
- State clearly what is unclear and what options or interpretations exist.

**Clarification template:**
```
🔍 CLARIFICATION NEEDED
Task: [task name]
Unclear: [what is ambiguous]
Options:
  A) [option A]
  B) [option B]
Please advise before I proceed.
```

---

## Folder Responsibilities

| Folder | Purpose | Who Manages |
|--------|---------|-------------|
| `inbox/` | Raw incoming files and unprocessed inputs | Any agent/user |
| `Need_Action/` | Active tasks requiring work | Assigned agent |
| `Done/` | Completed and verified work | Agent after completion |
| `Logs/` | All activity logs and audit records | All agents (mandatory) |
| `Plans/` | Strategic plans, roadmaps, architectures | Vault Owner / Agents |

---

## Escalation Policy

If any of the following occur, **escalate immediately to the Vault Owner:**

1. An action cannot be safely completed without risking data loss
2. A conflict exists between two rules in this handbook
3. An external system is unresponsive or returning unexpected results
4. Confidence in the correct action is below 80%

---

## Amendments

This handbook may be updated by the Vault Owner. All agents must operate against the latest version. Version history is tracked via git commits.

---

> *"Clarity before action. Logs before closure. Ask before destroying."*
