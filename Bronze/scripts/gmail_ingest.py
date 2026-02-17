"""
Gmail Email Ingestion - Bronze Layer
Fetches emails from Gmail and stores them as raw CSV in Bronze/data/raw/.

Usage:
    python gmail_ingest.py
    python gmail_ingest.py --max 100 --label INBOX
"""

import os
import sys
import base64
import logging
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

# Load .env from project root
_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_ROOT / ".env")

# Add scripts dir to path for gmail_connector import
sys.path.insert(0, str(Path(__file__).parent))
from gmail_connector import get_gmail_service

# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"gmail_ingest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("gmail_ingest")

# Output path
RAW_PATH = Path(__file__).parent.parent / "data" / "raw"
RAW_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = RAW_PATH / "gmail_emails.csv"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _decode_body(payload: dict) -> str:
    """Recursively extract plain-text body from a message payload."""
    mime_type = payload.get("mimeType", "")

    if mime_type == "text/plain":
        data = payload.get("body", {}).get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    if mime_type.startswith("multipart/"):
        for part in payload.get("parts", []):
            text = _decode_body(part)
            if text:
                return text

    return ""


def _get_header(headers: list, name: str) -> str:
    """Return a header value by name (case-insensitive)."""
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def fetch_emails(service, label: str = "INBOX", max_emails: int = 50) -> list[dict]:
    """
    Fetch emails from Gmail.

    Args:
        service: Authenticated Gmail service.
        label: Gmail label to read (INBOX, SENT, STARRED, etc.).
        max_emails: Maximum number of messages to fetch.

    Returns:
        List of email dicts.
    """
    logger.info(f"Fetching up to {max_emails} emails from [{label}]...")

    results = service.users().messages().list(
        userId="me",
        labelIds=[label],
        maxResults=max_emails,
    ).execute()

    messages = results.get("messages", [])
    logger.info(f"Found {len(messages)} message(s).")

    emails = []
    for i, msg_ref in enumerate(messages, 1):
        try:
            msg = service.users().messages().get(
                userId="me",
                id=msg_ref["id"],
                format="full",
            ).execute()

            headers = msg.get("payload", {}).get("headers", [])
            body = _decode_body(msg.get("payload", {}))

            emails.append({
                "message_id": msg["id"],
                "thread_id": msg.get("threadId", ""),
                "subject": _get_header(headers, "Subject"),
                "sender": _get_header(headers, "From"),
                "recipient": _get_header(headers, "To"),
                "date": _get_header(headers, "Date"),
                "snippet": msg.get("snippet", ""),
                "body_text": body[:2000],          # cap at 2000 chars for CSV
                "labels": ",".join(msg.get("labelIds", [])),
                "ingested_at": datetime.now().isoformat(),
            })

            if i % 10 == 0:
                logger.info(f"  Processed {i}/{len(messages)} emails...")

        except Exception as e:
            logger.warning(f"Could not fetch message {msg_ref['id']}: {e}")

    logger.info(f"Successfully fetched {len(emails)} emails.")
    return emails


# ─────────────────────────────────────────────────────────────────────────────
# Main ingestion
# ─────────────────────────────────────────────────────────────────────────────

def run_gmail_ingestion(max_emails: int = None, label: str = None):
    """Run the full Gmail ingestion pipeline."""
    max_emails = max_emails or int(os.getenv("GMAIL_MAX_EMAILS", 50))
    label = label or os.getenv("GMAIL_LABEL", "INBOX")

    logger.info("=" * 80)
    logger.info("GMAIL INGESTION - BRONZE LAYER")
    logger.info(f"Account : {os.getenv('GMAIL_ADDRESS', 'unknown')}")
    logger.info(f"Label   : {label}")
    logger.info(f"Max     : {max_emails} emails")
    logger.info(f"Output  : {OUTPUT_FILE}")
    logger.info("=" * 80)

    service = get_gmail_service()
    emails = fetch_emails(service, label=label, max_emails=max_emails)

    if not emails:
        logger.warning("No emails fetched — nothing to save.")
        return

    df = pd.DataFrame(emails)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    logger.info("=" * 80)
    logger.info("INGESTION SUMMARY")
    logger.info(f"Emails saved : {len(df)}")
    logger.info(f"Output file  : {OUTPUT_FILE}")
    logger.info(f"Columns      : {list(df.columns)}")
    logger.info("=" * 80)
    logger.info("GMAIL INGESTION COMPLETE")
    logger.info("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Gmail Email Ingestion - Bronze Layer")
    parser.add_argument("--max", type=int, default=None, help="Max emails to fetch")
    parser.add_argument("--label", type=str, default=None, help="Gmail label (INBOX, SENT, etc.)")
    args = parser.parse_args()
    run_gmail_ingestion(max_emails=args.max, label=args.label)


if __name__ == "__main__":
    main()
