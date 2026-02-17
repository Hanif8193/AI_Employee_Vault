---
id: "001"
title: "Connect Gmail Integration"
stage: general
date: "2026-02-17"
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: PMLS
command: connect Gmail to AI Employee Vault
labels: ["gmail", "oauth2", "integration", "bronze", "gold"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .env.example
  - .env (created from example)
  - .gitignore (updated: token.json added)
  - Bronze/requirements.txt (created)
  - Bronze/scripts/gmail_connector.py (created)
  - Bronze/scripts/gmail_ingest.py (created)
  - Gold/requirements.txt (updated: python-dotenv added)
  - Gold/scripts/gmail_notify.py (created)
  - run_pipeline.py (updated: --gmail-ingest, --notify flags)
tests: []
---

## Prompt

i wmant to connect AI Employee Vault with gmai my gmail ddress is hanifdostmuhammad8193@gmail.com my client id is: 782831772763-3kl11frsajkq1og13efkpun60s0ov0l1.apps.googleusercontent.com kindly connect it

## Response

Built full Gmail OAuth2 integration for the AI Employee Vault:

1. `gmail_connector.py` — OAuth2 auth handler (reads credentials from .env, saves token.json)
2. `gmail_ingest.py` — Fetches inbox emails → saves as `Bronze/data/raw/gmail_emails.csv`
3. `gmail_notify.py` — Sends Gold layer report email via Gmail API
4. `.env.example` — Template with GMAIL_CLIENT_ID pre-filled; user must add GMAIL_CLIENT_SECRET
5. Updated `run_pipeline.py` with `--gmail-ingest` and `--notify` CLI flags
6. Installed packages: google-api-python-client, google-auth-oauthlib, python-dotenv

User must fill in `GMAIL_CLIENT_SECRET` in `.env` before first run.
