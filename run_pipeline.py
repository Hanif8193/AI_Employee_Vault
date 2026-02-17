#!/usr/bin/env python3
"""
AI Employee Vault - Medallion Architecture CLI
Run the complete data pipeline from Bronze → Silver → Gold layers
"""

import sys
import os
from pathlib import Path
import argparse
import subprocess
from datetime import datetime


class MedallionCLI:
    """Command-line interface for running the Medallion Architecture pipeline."""

    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.bronze_script = self.root_dir / "Bronze" / "scripts" / "ingest_raw_data.py"
        self.silver_script = self.root_dir / "Silver" / "scripts" / "transform_bronze_to_silver.py"
        self.gold_script = self.root_dir / "Gold" / "scripts" / "generate_gold_data.py"
        self.gmail_ingest_script = self.root_dir / "Bronze" / "scripts" / "gmail_ingest.py"
        self.gmail_notify_script = self.root_dir / "Gold" / "scripts" / "gmail_notify.py"

    def print_banner(self):
        """Print welcome banner."""
        print("\n" + "=" * 80)
        print("  AI EMPLOYEE VAULT - MEDALLION ARCHITECTURE PIPELINE")
        print("=" * 80)
        print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80 + "\n")

    def print_layer_header(self, layer_name: str, emoji: str):
        """Print layer execution header."""
        print("\n" + "-" * 80)
        print(f"{emoji}  {layer_name.upper()} LAYER")
        print("-" * 80)

    def run_script(self, script_path: Path, layer_name: str) -> bool:
        """
        Run a Python script and return success status.

        Args:
            script_path: Path to the script
            layer_name: Name of the layer (for logging)

        Returns:
            True if successful, False otherwise
        """
        if not script_path.exists():
            print(f"[ERROR] ERROR: Script not found: {script_path}")
            return False

        try:
            print(f"> Running {layer_name} layer...")
            print(f"  Script: {script_path}")
            print()

            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=script_path.parent,
                check=True,
                text=True,
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8:replace', 'PYTHONUTF8': '1'}
            )

            print(f"\n[OK] {layer_name} layer completed successfully!")
            return True

        except subprocess.CalledProcessError as e:
            print(f"\n[ERROR] {layer_name} layer failed with exit code {e.returncode}")
            return False
        except Exception as e:
            print(f"\n[ERROR] {layer_name} layer failed: {e}")
            return False

    def run_bronze(self) -> bool:
        """Run Bronze layer (raw data ingestion)."""
        self.print_layer_header("Bronze", "[BRONZE]")
        return self.run_script(self.bronze_script, "Bronze")

    def run_silver(self) -> bool:
        """Run Silver layer (data cleaning)."""
        self.print_layer_header("Silver", "[SILVER]")
        return self.run_script(self.silver_script, "Silver")

    def run_gold(self) -> bool:
        """Run Gold layer (business aggregations)."""
        self.print_layer_header("Gold", "[GOLD]")
        return self.run_script(self.gold_script, "Gold")

    def run_gmail_ingest(self) -> bool:
        """Run Gmail ingestion into Bronze layer."""
        self.print_layer_header("Gmail Ingest", "[GMAIL]")
        return self.run_script(self.gmail_ingest_script, "Gmail Ingest")

    def run_gmail_notify(self) -> bool:
        """Send Gold report via Gmail notification."""
        self.print_layer_header("Gmail Notify", "[GMAIL]")
        return self.run_script(self.gmail_notify_script, "Gmail Notify")

    def run_complete_pipeline(self) -> bool:
        """Run the complete Bronze -> Silver -> Gold pipeline."""
        self.print_banner()

        print(">> Starting COMPLETE pipeline execution...")
        print("   Pipeline: Bronze -> Silver -> Gold")
        print()

        start_time = datetime.now()

        # Run Bronze
        if not self.run_bronze():
            print("\n[ERROR] Pipeline FAILED at Bronze layer")
            return False

        # Run Silver
        if not self.run_silver():
            print("\n[ERROR] Pipeline FAILED at Silver layer")
            return False

        # Run Gold
        if not self.run_gold():
            print("\n[ERROR] Pipeline FAILED at Gold layer")
            return False

        # Success summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n" + "=" * 80)
        print("[SUCCESS] PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"  Total execution time: {duration:.2f} seconds")
        print(f"  Layers executed: Bronze -> Silver -> Gold")
        print()
        print("[FILES] Output locations:")
        print(f"  - Bronze: {self.root_dir / 'Bronze' / 'data' / 'raw'}")
        print(f"  - Silver: {self.root_dir / 'Silver' / 'data' / 'clean'}")
        print(f"  - Gold:   {self.root_dir / 'Gold' / 'data' / 'gold'}")
        print("=" * 80 + "\n")

        return True

    def show_status(self):
        """Show pipeline status and output files."""
        self.print_banner()

        print("[STATUS] PIPELINE STATUS\n")

        # Check Bronze
        bronze_data = self.root_dir / "Bronze" / "data" / "raw" / "employees.csv"
        bronze_status = "[OK] EXISTS" if bronze_data.exists() else "[ERROR] MISSING"
        print(f"[BRONZE] Bronze Layer: {bronze_status}")
        if bronze_data.exists():
            size = bronze_data.stat().st_size
            print(f"   - File: employees.csv ({size:,} bytes)")

        # Check Silver
        silver_data = self.root_dir / "Silver" / "data" / "clean" / "employees_clean.csv"
        silver_status = "[OK] EXISTS" if silver_data.exists() else "[ERROR] MISSING"
        print(f"\n[SILVER] Silver Layer: {silver_status}")
        if silver_data.exists():
            size = silver_data.stat().st_size
            print(f"   - File: employees_clean.csv ({size:,} bytes)")

        # Check Gold
        gold_dir = self.root_dir / "Gold" / "data" / "gold"
        gold_files = list(gold_dir.glob("*.csv")) if gold_dir.exists() else []
        gold_txt = list(gold_dir.glob("*.txt")) if gold_dir.exists() else []
        gold_status = "[OK] EXISTS" if gold_files or gold_txt else "[ERROR] MISSING"
        print(f"\n[GOLD] Gold Layer: {gold_status}")
        if gold_files or gold_txt:
            print(f"   - CSV files: {len(gold_files)}")
            print(f"   - Text reports: {len(gold_txt)}")
            print(f"   - Total datasets: {len(gold_files) + len(gold_txt)}")

        print("\n" + "=" * 80 + "\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Employee Vault - Medallion Architecture Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete pipeline
  python run_pipeline.py --all

  # Run individual layers
  python run_pipeline.py --bronze
  python run_pipeline.py --silver
  python run_pipeline.py --gold

  # Check pipeline status
  python run_pipeline.py --status

  # Run multiple layers in sequence
  python run_pipeline.py --silver --gold
        """
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Run complete pipeline (Bronze -> Silver -> Gold)"
    )
    parser.add_argument(
        "--bronze",
        action="store_true",
        help="Run Bronze layer only (raw data ingestion)"
    )
    parser.add_argument(
        "--silver",
        action="store_true",
        help="Run Silver layer only (data cleaning)"
    )
    parser.add_argument(
        "--gold",
        action="store_true",
        help="Run Gold layer only (business aggregations)"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show pipeline status and output files"
    )
    parser.add_argument(
        "--gmail-ingest",
        action="store_true",
        help="Fetch emails from Gmail into Bronze layer (requires .env setup)"
    )
    parser.add_argument(
        "--notify",
        action="store_true",
        help="Send Gold report email via Gmail (requires .env setup)"
    )

    args = parser.parse_args()

    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    cli = MedallionCLI()

    # Handle status check
    if args.status:
        cli.show_status()
        sys.exit(0)

    # Handle complete pipeline
    if args.all:
        success = cli.run_complete_pipeline()
        sys.exit(0 if success else 1)

    # Handle individual layers
    success = True

    if args.bronze:
        cli.print_banner()
        if not cli.run_bronze():
            success = False

    if args.silver:
        if not args.bronze:  # Print banner only if not already printed
            cli.print_banner()
        if not cli.run_silver():
            success = False

    if args.gold:
        if not args.bronze and not args.silver:  # Print banner only if not already printed
            cli.print_banner()
        if not cli.run_gold():
            success = False

    if args.gmail_ingest:
        if not any([args.bronze, args.silver, args.gold]):
            cli.print_banner()
        if not cli.run_gmail_ingest():
            success = False

    if args.notify:
        if not any([args.bronze, args.silver, args.gold, args.gmail_ingest]):
            cli.print_banner()
        if not cli.run_gmail_notify():
            success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
