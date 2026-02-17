"""
Gmail OAuth2 Connector
Handles authentication and returns an authenticated Gmail API service.

First run: opens a browser window for you to grant access.
Subsequent runs: uses the saved token.json automatically.
"""

import os
import json
import logging
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load .env from project root
_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_ROOT / ".env")

logger = logging.getLogger(__name__)

# Scopes: read emails + send emails
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

# Token stored at project root (git-ignored)
TOKEN_PATH = _ROOT / "token.json"


def _build_client_config() -> dict:
    """Build OAuth2 client config from environment variables."""
    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise EnvironmentError(
            "Missing GMAIL_CLIENT_ID or GMAIL_CLIENT_SECRET in .env file.\n"
            "Copy .env.example to .env and fill in your credentials."
        )

    return {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
        }
    }


def get_gmail_service():
    """
    Authenticate with Gmail API and return a service object.

    First run: launches browser for OAuth2 consent.
    Subsequent runs: refreshes token automatically from token.json.

    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail service.
    """
    creds = None

    # Load existing token
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        logger.info("Loaded existing token from token.json")

    # Refresh or re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired token...")
            creds.refresh(Request())
        else:
            logger.info("Starting OAuth2 browser flow (one-time setup)...")
            client_config = _build_client_config()
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
            logger.info("OAuth2 authorization complete.")

        # Save token for next run
        TOKEN_PATH.write_text(creds.to_json())
        logger.info(f"Token saved to {TOKEN_PATH}")

    service = build("gmail", "v1", credentials=creds)
    logger.info("Gmail service ready.")
    return service
