#!/usr/bin/env python3
"""
Silver Layer Transformation Script
Transforms raw Bronze data into cleaned, validated Silver data.

Purpose:
- Clean and standardize employee data from Bronze layer
- Apply data quality rules and validation
- Remove duplicates and handle missing values
- Prepare data for Gold layer business transformations

Author: Data Engineering Team
Date: 2026-02-10
"""

import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import Tuple, Dict


class SilverTransformation:
    """Handles Bronze to Silver data transformation and cleaning."""

    def __init__(self):
        """Initialize transformation with logging and paths."""
        self.setup_logging()
        self.setup_paths()
        self.stats = {
            'original_rows': 0,
            'duplicate_rows_removed': 0,
            'invalid_rows_removed': 0,
            'missing_values_handled': 0,
            'final_rows': 0
        }

    def setup_logging(self):
        """Configure logging to file and console."""
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"silver_transformation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Logging to: {log_file}")

    def setup_paths(self):
        """Setup input and output paths."""
        base_dir = Path(__file__).parent.parent.parent
        self.bronze_path = base_dir / "Bronze" / "data" / "raw"
        self.silver_path = base_dir / "Silver" / "data" / "clean"

        # Create output directory if it doesn't exist
        self.silver_path.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Bronze path: {self.bronze_path}")
        self.logger.info(f"Silver path: {self.silver_path}")

    def read_bronze_data(self, filename: str = "employees.csv") -> pd.DataFrame:
        """
        Read raw CSV data from Bronze layer.

        Args:
            filename: Name of the CSV file to read

        Returns:
            DataFrame with raw Bronze data
        """
        file_path = self.bronze_path / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Bronze file not found: {file_path}")

        self.logger.info(f"📥 Reading Bronze data from: {filename}")
        df = pd.read_csv(file_path)

        self.stats['original_rows'] = len(df)
        self.logger.info(f"   ✓ Loaded {len(df)} rows, {len(df.columns)} columns")
        self.logger.info(f"   ✓ Columns: {list(df.columns)}")

        return df

    def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names to snake_case.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with standardized column names
        """
        self.logger.info("🔤 Standardizing column names to snake_case...")

        original_columns = df.columns.tolist()

        # Convert to snake_case (already in snake_case in this dataset)
        # This handles cases like 'experienceYears' -> 'experience_years'
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        new_columns = df.columns.tolist()

        if original_columns != new_columns:
            self.logger.info(f"   ✓ Column names changed:")
            for old, new in zip(original_columns, new_columns):
                if old != new:
                    self.logger.info(f"      {old} -> {new}")
        else:
            self.logger.info(f"   ✓ Column names already in snake_case")

        return df

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the dataset.

        Strategy:
        - Numeric columns: Fill with median
        - Categorical columns: Fill with mode or 'Unknown'
        - Log all missing value operations

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with missing values handled
        """
        self.logger.info("🔍 Checking for missing values...")

        missing_counts = df.isnull().sum()
        total_missing = missing_counts.sum()

        if total_missing == 0:
            self.logger.info("   ✓ No missing values found")
            return df

        self.logger.info(f"   ⚠ Found {total_missing} missing values:")
        for col, count in missing_counts[missing_counts > 0].items():
            self.logger.info(f"      {col}: {count} missing")

        # Handle missing values by column type
        for col in df.columns:
            if df[col].isnull().any():
                if df[col].dtype in ['int64', 'float64']:
                    # Numeric: use median
                    median_val = df[col].median()
                    df[col].fillna(median_val, inplace=True)
                    self.logger.info(f"   ✓ Filled {col} with median: {median_val}")
                else:
                    # Categorical: use mode or 'Unknown'
                    if not df[col].mode().empty:
                        mode_val = df[col].mode()[0]
                        df[col].fillna(mode_val, inplace=True)
                        self.logger.info(f"   ✓ Filled {col} with mode: {mode_val}")
                    else:
                        df[col].fillna('Unknown', inplace=True)
                        self.logger.info(f"   ✓ Filled {col} with 'Unknown'")

        self.stats['missing_values_handled'] = total_missing

        return df

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate rows from the dataset.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with duplicates removed
        """
        self.logger.info("🔍 Checking for duplicate rows...")

        original_count = len(df)
        df_clean = df.drop_duplicates()
        duplicates_removed = original_count - len(df_clean)

        if duplicates_removed > 0:
            self.logger.info(f"   ✓ Removed {duplicates_removed} duplicate row(s)")
            self.stats['duplicate_rows_removed'] = duplicates_removed
        else:
            self.logger.info("   ✓ No duplicate rows found")

        return df_clean

    def fix_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fix and enforce correct data types.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with corrected data types
        """
        self.logger.info("🔧 Fixing data types...")

        type_mappings = {
            'id': 'int64',
            'name': 'string',
            'age': 'int64',
            'department': 'string',
            'role': 'string',
            'salary': 'int64',
            'experience_years': 'int64',
            'city': 'string'
        }

        for col, dtype in type_mappings.items():
            if col in df.columns:
                try:
                    original_dtype = df[col].dtype
                    df[col] = df[col].astype(dtype)
                    if str(original_dtype) != str(dtype):
                        self.logger.info(f"   ✓ {col}: {original_dtype} -> {dtype}")
                except Exception as e:
                    self.logger.warning(f"   ⚠ Could not convert {col} to {dtype}: {e}")

        return df

    def validate_business_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply business validation rules and remove invalid rows.

        Rules:
        - age >= 18 (legal working age)
        - salary > 0 (must have positive salary)
        - experience_years >= 0 (cannot have negative experience)

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with only valid rows
        """
        self.logger.info("✅ Applying validation rules...")

        original_count = len(df)

        # Rule 1: Age >= 18
        invalid_age = df['age'] < 18
        if invalid_age.any():
            count = invalid_age.sum()
            self.logger.warning(f"   ⚠ Found {count} row(s) with age < 18")
            self.logger.info(f"      Invalid ages: {df.loc[invalid_age, 'age'].tolist()}")
            df = df[~invalid_age]
        else:
            self.logger.info("   ✓ All ages >= 18")

        # Rule 2: Salary > 0
        invalid_salary = df['salary'] <= 0
        if invalid_salary.any():
            count = invalid_salary.sum()
            self.logger.warning(f"   ⚠ Found {count} row(s) with salary <= 0")
            self.logger.info(f"      Invalid salaries: {df.loc[invalid_salary, 'salary'].tolist()}")
            df = df[~invalid_salary]
        else:
            self.logger.info("   ✓ All salaries > 0")

        # Rule 3: Experience >= 0
        invalid_experience = df['experience_years'] < 0
        if invalid_experience.any():
            count = invalid_experience.sum()
            self.logger.warning(f"   ⚠ Found {count} row(s) with experience < 0")
            self.logger.info(f"      Invalid experience: {df.loc[invalid_experience, 'experience_years'].tolist()}")
            df = df[~invalid_experience]
        else:
            self.logger.info("   ✓ All experience_years >= 0")

        invalid_rows_removed = original_count - len(df)
        self.stats['invalid_rows_removed'] = invalid_rows_removed

        if invalid_rows_removed > 0:
            self.logger.info(f"   ✓ Total invalid rows removed: {invalid_rows_removed}")
        else:
            self.logger.info("   ✓ All rows passed validation")

        return df

    def save_to_silver(self, df: pd.DataFrame, filename: str = "employees_clean.csv"):
        """
        Save cleaned data to Silver layer.

        Args:
            df: Cleaned DataFrame
            filename: Output filename
        """
        output_path = self.silver_path / filename

        self.logger.info(f"💾 Saving cleaned data to: {filename}")
        df.to_csv(output_path, index=False)

        self.stats['final_rows'] = len(df)

        file_size = output_path.stat().st_size
        self.logger.info(f"   ✓ Saved {len(df)} rows, {len(df.columns)} columns")
        self.logger.info(f"   ✓ File size: {file_size:,} bytes")
        self.logger.info(f"   ✓ Location: {output_path}")

    def print_transformation_summary(self):
        """Print summary statistics of the transformation."""
        self.logger.info("\n" + "="*80)
        self.logger.info("TRANSFORMATION SUMMARY")
        self.logger.info("="*80)
        self.logger.info(f"Original rows:              {self.stats['original_rows']}")
        self.logger.info(f"Duplicate rows removed:     {self.stats['duplicate_rows_removed']}")
        self.logger.info(f"Invalid rows removed:       {self.stats['invalid_rows_removed']}")
        self.logger.info(f"Missing values handled:     {self.stats['missing_values_handled']}")
        self.logger.info(f"Final rows:                 {self.stats['final_rows']}")

        data_retention = (self.stats['final_rows'] / self.stats['original_rows'] * 100) if self.stats['original_rows'] > 0 else 0
        self.logger.info(f"Data retention rate:        {data_retention:.2f}%")
        self.logger.info("="*80)

    def transform(self, input_filename: str = "employees.csv",
                  output_filename: str = "employees_clean.csv"):
        """
        Execute complete Bronze to Silver transformation pipeline.

        Pipeline steps:
        1. Read Bronze data
        2. Standardize column names
        3. Handle missing values
        4. Remove duplicates
        5. Fix data types
        6. Validate business rules
        7. Save to Silver layer
        8. Print summary

        Args:
            input_filename: Bronze CSV filename
            output_filename: Silver CSV filename
        """
        try:
            self.logger.info("\n" + "="*80)
            self.logger.info("🚀 SILVER LAYER TRANSFORMATION STARTED")
            self.logger.info("="*80 + "\n")

            # Step 1: Read Bronze data
            df = self.read_bronze_data(input_filename)

            # Step 2: Standardize column names
            df = self.standardize_column_names(df)

            # Step 3: Handle missing values
            df = self.handle_missing_values(df)

            # Step 4: Remove duplicates
            df = self.remove_duplicates(df)

            # Step 5: Fix data types
            df = self.fix_data_types(df)

            # Step 6: Validate business rules
            df = self.validate_business_rules(df)

            # Step 7: Save to Silver
            self.save_to_silver(df, output_filename)

            # Step 8: Print summary
            self.print_transformation_summary()

            self.logger.info("\n✨ SILVER LAYER TRANSFORMATION COMPLETED SUCCESSFULLY\n")

        except Exception as e:
            self.logger.error(f"❌ Transformation failed: {e}", exc_info=True)
            raise


def main():
    """Main execution function."""
    transformer = SilverTransformation()
    transformer.transform()


if __name__ == "__main__":
    main()
