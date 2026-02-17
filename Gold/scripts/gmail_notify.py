"""
Gmail Notification Sender - Gold Layer
Sends a summary email of the latest Gold layer reports via Gmail.

Usage:
    python gmail_notify.py
    python gmail_notify.py --to recipient@example.com
"""

import os
import sys
import base64
import logging
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

# Load .env from project root
_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_ROOT / ".env")

# Import connector from Bronze scripts
sys.path.insert(0, str(_ROOT / "Bronze" / "scripts"))
from gmail_connector import get_gmail_service

# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"gmail_notify_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("gmail_notify")

GOLD_PATH = Path(__file__).parent.parent / "data" / "gold"


# ─────────────────────────────────────────────────────────────────────────────
# Report builder
# ─────────────────────────────────────────────────────────────────────────────

def _collect_gold_summary() -> str:
    """Scan Gold data folder and build a plain-text summary."""
    lines = [
        f"AI Employee Vault — Gold Layer Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
    ]

    if not GOLD_PATH.exists():
        lines.append("Gold data folder not found — run the pipeline first.")
        return "\n".join(lines)

    csv_files = sorted(GOLD_PATH.glob("*.csv"))
    txt_files = sorted(GOLD_PATH.glob("*.txt"))
    all_files = csv_files + txt_files

    if not all_files:
        lines.append("No Gold data files found — run: python run_pipeline.py --gold")
        return "\n".join(lines)

    lines.append(f"\nDatasets available: {len(all_files)}")
    lines.append("")

    for f in csv_files:
        size_kb = f.stat().st_size / 1024
        lines.append(f"  [CSV] {f.name}  ({size_kb:.1f} KB)")

    for f in txt_files:
        size_kb = f.stat().st_size / 1024
        lines.append(f"  [TXT] {f.name}  ({size_kb:.1f} KB)")
        # Embed first 30 lines of text reports
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            preview = "\n".join(content.splitlines()[:30])
            lines.append(f"\n--- {f.name} (preview) ---")
            lines.append(preview)
            lines.append("--- end preview ---\n")
        except Exception:
            pass

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Email sender
# ─────────────────────────────────────────────────────────────────────────────

def send_report(to_address: str = None):
    """
    Compose and send a Gold report email.

    Args:
        to_address: Recipient email. Falls back to GMAIL_NOTIFY_TO in .env.
    """
    sender = os.getenv("GMAIL_ADDRESS")
    recipient = to_address or os.getenv("GMAIL_NOTIFY_TO") or sender

    if not sender:
        raise EnvironmentError("GMAIL_ADDRESS not set in .env")

    logger.info("=" * 80)
    logger.info("GMAIL NOTIFICATION - GOLD LAYER")
    logger.info(f"From : {sender}")
    logger.info(f"To   : {recipient}")
    logger.info("=" * 80)

    body_text = _collect_gold_summary()

    # Build MIME message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"AI Employee Vault Report — {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = sender
    msg["To"] = recipient

    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    # Encode to base64 URL-safe for Gmail API
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")

    service = get_gmail_service()
    result = service.users().messages().send(
        userId="me",
        body={"raw": raw},
    ).execute()

    logger.info(f"Email sent successfully! Message ID: {result.get('id')}")
    logger.info("=" * 80)
    logger.info("GMAIL NOTIFICATION COMPLETE")
    logger.info("=" * 80)
    return result


def main():
    parser = argparse.ArgumentParser(description="Send Gold report via Gmail")
    parser.add_argument("--to", type=str, default=None, help="Recipient email address")
    args = parser.parse_args()
    send_report(to_address=args.to)


if __name__ == "__main__":
    main()
