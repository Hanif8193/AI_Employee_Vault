
import os
import sys
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd

# =============================================================================
# WINDOWS-SAFE LOGGING SETUP (NO EMOJI ERRORS)
# =============================================================================
logger = logging.getLogger("bronze_ingestion")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

# Clear existing handlers (important on Windows)
if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(console_handler)

# =============================================================================
# BRONZE INGESTION CLASS
# =============================================================================
class BronzeIngestion:

    def __init__(self):
        self.raw_data_path = Path(__file__).resolve().parent.parent / "data" / "raw"
        self.ingested_files = 0
        self.failed_files = 0

    def ingest_csv(self, file_path: Path) -> pd.DataFrame:
        """Read and validate CSV file"""
        logger.info(f"Ingesting file: {file_path.name}")

        df = pd.read_csv(file_path)

        logger.info(f"File size: {file_path.stat().st_size} bytes")
        logger.info(f"Rows: {len(df)}")
        logger.info(f"Columns: {len(df.columns)}")

        return df

    def log_schema_and_sample(self, df: pd.DataFrame, file_name: str):
        """Log schema and sample data"""
        print("\n" + "=" * 80)
        print(f"SCHEMA: {file_name}")
        print("=" * 80)
        print(df.dtypes)

        print("\n" + "=" * 80)
        print(f"SAMPLE DATA (First 5 rows): {file_name}")
        print("=" * 80)
        print(df.head())

    def run_ingestion(self):
        logger.info("=" * 80)
        logger.info("BRONZE LAYER INGESTION STARTED")
        logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)

        if not self.raw_data_path.exists():
            logger.error(f"Raw data path not found: {self.raw_data_path}")
            return

        csv_files = list(self.raw_data_path.glob("*.csv"))
        logger.info(f"Found {len(csv_files)} CSV file(s) in {self.raw_data_path}")

        for csv_file in csv_files:
            try:
                df = self.ingest_csv(csv_file)
                self.log_schema_and_sample(df, csv_file.name)
                self.ingested_files += 1
                logger.info(f"Successfully ingested: {csv_file.name}\n")

            except Exception as e:
                self.failed_files += 1
                logger.error(f"Failed to ingest {csv_file.name}: {e}")

        logger.info("=" * 80)
        logger.info("INGESTION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total files found: {len(csv_files)}")
        logger.info(f"Successfully ingested: {self.ingested_files}")
        logger.info(f"Failed: {self.failed_files}")
        logger.info("=" * 80)
        logger.info("BRONZE LAYER INGESTION COMPLETED")
        logger.info("=" * 80)


# =============================================================================
# MAIN
# =============================================================================
def main():
    ingestion = BronzeIngestion()
    ingestion.run_ingestion()


if __name__ == "__main__":
    main()
