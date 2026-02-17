"""
Tests for Gold/scripts/gmail_notify.py

Covers:
  - _collect_gold_summary() output format and content
  - send_report() MIME message construction and Gmail API call
"""

import sys
import os
import importlib
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open
import pytest

# ── path setup so we can import gmail_notify without installing ────────────────
GOLD_SCRIPTS = Path(__file__).resolve().parent.parent / "Gold" / "scripts"
BRONZE_SCRIPTS = Path(__file__).resolve().parent.parent / "Bronze" / "scripts"

sys.path.insert(0, str(GOLD_SCRIPTS))
sys.path.insert(0, str(BRONZE_SCRIPTS))


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_module():
    """Import gmail_notify with Gmail service patched (avoids live auth at import)."""
    with patch("gmail_connector.get_gmail_service", return_value=MagicMock()):
        import gmail_notify
        importlib.reload(gmail_notify)
    return gmail_notify


# ── _collect_gold_summary tests ───────────────────────────────────────────────

class TestCollectGoldSummary:

    def test_header_always_present(self, tmp_path, monkeypatch):
        """Summary should always start with the report title."""
        mod = _load_module()
        monkeypatch.setattr(mod, "GOLD_PATH", tmp_path)
        # put one CSV in tmp_path so it isn't "no data" path
        (tmp_path / "department_metrics.csv").write_text("a,b\n1,2\n")

        summary = mod._collect_gold_summary()

        assert "AI Employee Vault" in summary
        assert "Gold Layer Report" in summary

    def test_missing_gold_folder(self, tmp_path, monkeypatch):
        """If Gold data folder doesn't exist, summary should say so."""
        mod = _load_module()
        monkeypatch.setattr(mod, "GOLD_PATH", tmp_path / "nonexistent")

        summary = mod._collect_gold_summary()

        assert "Gold data folder not found" in summary

    def test_no_files_message(self, tmp_path, monkeypatch):
        """If folder exists but is empty, summary should prompt user to run pipeline."""
        mod = _load_module()
        monkeypatch.setattr(mod, "GOLD_PATH", tmp_path)

        summary = mod._collect_gold_summary()

        assert "No Gold data files found" in summary

    def test_csv_files_listed(self, tmp_path, monkeypatch):
        """All CSV files in Gold folder should be listed in the summary."""
        mod = _load_module()
        monkeypatch.setattr(mod, "GOLD_PATH", tmp_path)
        (tmp_path / "department_metrics.csv").write_text("dept,count\nEng,10\n")
        (tmp_path / "role_metrics.csv").write_text("role,avg\nSWE,100000\n")

        summary = mod._collect_gold_summary()

        assert "department_metrics.csv" in summary
        assert "role_metrics.csv" in summary

    def test_txt_file_preview_embedded(self, tmp_path, monkeypatch):
        """Text report files should have their first 30 lines embedded."""
        mod = _load_module()
        monkeypatch.setattr(mod, "GOLD_PATH", tmp_path)
        content = "\n".join(f"Line {i}" for i in range(40))
        (tmp_path / "executive_summary.txt").write_text(content, encoding="utf-8")

        summary = mod._collect_gold_summary()

        assert "executive_summary.txt" in summary
        assert "Line 0" in summary
        assert "Line 29" in summary
        assert "Line 30" not in summary  # only first 30 lines

    def test_dataset_count_reported(self, tmp_path, monkeypatch):
        """Summary should report the total number of datasets found."""
        mod = _load_module()
        monkeypatch.setattr(mod, "GOLD_PATH", tmp_path)
        for name in ["a.csv", "b.csv", "c.txt"]:
            (tmp_path / name).write_text("data")

        summary = mod._collect_gold_summary()

        assert "Datasets available: 3" in summary


# ── send_report tests ─────────────────────────────────────────────────────────

class TestSendReport:

    def _make_env(self, monkeypatch, sender="sender@example.com", notify_to=None):
        monkeypatch.setenv("GMAIL_ADDRESS", sender)
        if notify_to:
            monkeypatch.setenv("GMAIL_NOTIFY_TO", notify_to)
        else:
            monkeypatch.delenv("GMAIL_NOTIFY_TO", raising=False)

    def test_raises_if_no_sender_env(self, monkeypatch):
        """send_report must raise EnvironmentError when GMAIL_ADDRESS is missing."""
        mod = _load_module()
        monkeypatch.delenv("GMAIL_ADDRESS", raising=False)

        with pytest.raises(EnvironmentError, match="GMAIL_ADDRESS not set"):
            with patch("gmail_connector.get_gmail_service", return_value=MagicMock()):
                mod.send_report()

    def test_uses_notify_to_env_as_recipient(self, tmp_path, monkeypatch):
        """Recipient should come from GMAIL_NOTIFY_TO when --to is not passed."""
        mod = _load_module()
        monkeypatch.setattr(mod, "GOLD_PATH", tmp_path)
        self._make_env(monkeypatch, sender="me@x.com", notify_to="boss@x.com")

        mock_service = MagicMock()
        execute_mock = mock_service.users.return_value.messages.return_value.send.return_value.execute
        execute_mock.return_value = {"id": "abc123"}

        with patch("gmail_notify.get_gmail_service", return_value=mock_service):
            result = mod.send_report()

        assert result["id"] == "abc123"

    def test_explicit_to_overrides_env(self, tmp_path, monkeypatch):
        """Explicit to_address argument should override GMAIL_NOTIFY_TO env var."""
        mod = _load_module()
        monkeypatch.setattr(mod, "GOLD_PATH", tmp_path)
        self._make_env(monkeypatch, sender="me@x.com", notify_to="env-recipient@x.com")

        mock_service = MagicMock()
        mock_service.users.return_value.messages.return_value.send.return_value.execute.return_value = {"id": "xyz"}

        with patch("gmail_notify.get_gmail_service", return_value=mock_service):
            mod.send_report(to_address="override@x.com")

        assert mock_service.users.return_value.messages.return_value.send.called

    def test_gmail_api_called_once(self, tmp_path, monkeypatch):
        """Gmail API send endpoint should be called exactly once per send_report call."""
        mod = _load_module()
        monkeypatch.setattr(mod, "GOLD_PATH", tmp_path)
        self._make_env(monkeypatch, sender="me@x.com")

        mock_service = MagicMock()
        mock_service.users.return_value.messages.return_value.send.return_value.execute.return_value = {"id": "once"}

        with patch("gmail_notify.get_gmail_service", return_value=mock_service):
            mod.send_report()

        assert mock_service.users.return_value.messages.return_value.send.call_count == 1

    def test_message_id_returned(self, tmp_path, monkeypatch):
        """send_report should return the Gmail API response dict."""
        mod = _load_module()
        monkeypatch.setattr(mod, "GOLD_PATH", tmp_path)
        self._make_env(monkeypatch, sender="me@x.com")

        mock_service = MagicMock()
        mock_service.users.return_value.messages.return_value.send.return_value.execute.return_value = {"id": "msg-999"}

        with patch("gmail_notify.get_gmail_service", return_value=mock_service):
            result = mod.send_report()

        assert result == {"id": "msg-999"}
