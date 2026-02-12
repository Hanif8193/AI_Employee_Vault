#!/usr/bin/env python3
"""
Gold Layer Aggregation Script
Applies business logic and creates analytics-ready datasets from Silver data.

Purpose:
- Generate department-level metrics
- Create role-based analytics
- Produce executive dashboards
- Prepare AI/ML-ready features for HR analytics

Author: Data Engineering Team
Date: 2026-02-10
"""

import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class GoldAggregation:
    """Handles Silver to Gold data aggregation and business logic."""

    def __init__(self):
        """Initialize aggregation with logging and paths."""
        self.setup_logging()
        self.setup_paths()
        self.datasets = {}
        self.stats = {
            'total_employees': 0,
            'total_departments': 0,
            'total_roles': 0,
            'datasets_generated': 0
        }

    def setup_logging(self):
        """Configure logging to file and console."""
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"gold_aggregation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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
        self.silver_path = base_dir / "Silver" / "data" / "clean"
        self.gold_path = base_dir / "Gold" / "data" / "gold"

        # Create output directory if it doesn't exist
        self.gold_path.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Silver path: {self.silver_path}")
        self.logger.info(f"Gold path: {self.gold_path}")

    def read_silver_data(self, filename: str = "employees_clean.csv") -> pd.DataFrame:
        """
        Read cleaned CSV data from Silver layer.

        Args:
            filename: Name of the CSV file to read

        Returns:
            DataFrame with cleaned Silver data
        """
        file_path = self.silver_path / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Silver file not found: {file_path}")

        self.logger.info(f"📥 Reading Silver data from: {filename}")
        df = pd.read_csv(file_path)

        self.stats['total_employees'] = len(df)
        self.stats['total_departments'] = df['department'].nunique()
        self.stats['total_roles'] = df['role'].nunique()

        self.logger.info(f"   ✓ Loaded {len(df)} employees")
        self.logger.info(f"   ✓ Departments: {self.stats['total_departments']}")
        self.logger.info(f"   ✓ Roles: {self.stats['total_roles']}")
        self.logger.info(f"   ✓ Columns: {list(df.columns)}")

        return df

    def aggregate_department_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate metrics by department.

        Metrics:
        - Total employees per department
        - Average salary per department
        - Average age per department
        - Average experience per department
        - Min/Max salary per department
        - Total payroll per department

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with department-level aggregations
        """
        self.logger.info("📊 Aggregating department metrics...")

        dept_metrics = df.groupby('department').agg({
            'id': 'count',                    # Total employees
            'salary': ['mean', 'min', 'max', 'sum'],  # Salary stats
            'age': 'mean',                     # Average age
            'experience_years': 'mean'         # Average experience
        }).round(2)

        # Flatten multi-level columns
        dept_metrics.columns = [
            'total_employees',
            'avg_salary',
            'min_salary',
            'max_salary',
            'total_payroll',
            'avg_age',
            'avg_experience_years'
        ]

        dept_metrics = dept_metrics.reset_index()

        # Add calculated fields
        dept_metrics['salary_range'] = dept_metrics['max_salary'] - dept_metrics['min_salary']

        # Sort by total payroll (highest first)
        dept_metrics = dept_metrics.sort_values('total_payroll', ascending=False)

        self.logger.info(f"   ✓ Generated metrics for {len(dept_metrics)} departments")
        self.logger.info(f"   ✓ Columns: {list(dept_metrics.columns)}")

        return dept_metrics

    def aggregate_role_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate metrics by role.

        Metrics:
        - Total employees per role
        - Average salary per role
        - Average experience per role
        - Average age per role

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with role-level aggregations
        """
        self.logger.info("📊 Aggregating role metrics...")

        role_metrics = df.groupby('role').agg({
            'id': 'count',
            'salary': 'mean',
            'experience_years': 'mean',
            'age': 'mean'
        }).round(2)

        role_metrics.columns = [
            'total_employees',
            'avg_salary',
            'avg_experience_years',
            'avg_age'
        ]

        role_metrics = role_metrics.reset_index()

        # Sort by average salary (highest first)
        role_metrics = role_metrics.sort_values('avg_salary', ascending=False)

        self.logger.info(f"   ✓ Generated metrics for {len(role_metrics)} roles")

        return role_metrics

    def aggregate_city_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate metrics by city (office location).

        Metrics:
        - Total employees per city
        - Average salary per city
        - Total payroll per city
        - Department diversity per city

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with city-level aggregations
        """
        self.logger.info("📊 Aggregating city metrics...")

        city_metrics = df.groupby('city').agg({
            'id': 'count',
            'salary': ['mean', 'sum'],
            'department': 'nunique'
        }).round(2)

        city_metrics.columns = [
            'total_employees',
            'avg_salary',
            'total_payroll',
            'department_diversity'
        ]

        city_metrics = city_metrics.reset_index()

        # Sort by total employees (largest first)
        city_metrics = city_metrics.sort_values('total_employees', ascending=False)

        self.logger.info(f"   ✓ Generated metrics for {len(city_metrics)} cities")

        return city_metrics

    def generate_top_earners(self, df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
        """
        Generate top N highest paid employees.

        Args:
            df: Input DataFrame
            n: Number of top earners to return

        Returns:
            DataFrame with top N earners
        """
        self.logger.info(f"📊 Generating top {n} highest paid employees...")

        top_earners = df.nlargest(n, 'salary')[
            ['name', 'role', 'department', 'salary', 'experience_years', 'city']
        ].copy()

        top_earners['rank'] = range(1, len(top_earners) + 1)

        # Reorder columns
        top_earners = top_earners[['rank', 'name', 'role', 'department', 'salary', 'experience_years', 'city']]

        self.logger.info(f"   ✓ Top earner: {top_earners.iloc[0]['name']} (${top_earners.iloc[0]['salary']:,})")

        return top_earners

    def generate_experience_bands(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categorize employees into experience bands for AI/ML analysis.

        Bands:
        - Entry (0-2 years)
        - Junior (3-5 years)
        - Mid (6-10 years)
        - Senior (11-15 years)
        - Expert (16+ years)

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with experience band aggregations
        """
        self.logger.info("📊 Generating experience band analysis...")

        # Create experience bands
        df_copy = df.copy()
        df_copy['experience_band'] = pd.cut(
            df_copy['experience_years'],
            bins=[0, 2, 5, 10, 15, float('inf')],
            labels=['Entry (0-2yr)', 'Junior (3-5yr)', 'Mid (6-10yr)', 'Senior (11-15yr)', 'Expert (16+yr)'],
            include_lowest=True
        )

        # Aggregate by experience band
        exp_bands = df_copy.groupby('experience_band', observed=True).agg({
            'id': 'count',
            'salary': 'mean',
            'age': 'mean'
        }).round(2)

        exp_bands.columns = ['total_employees', 'avg_salary', 'avg_age']
        exp_bands = exp_bands.reset_index()

        self.logger.info(f"   ✓ Generated {len(exp_bands)} experience bands")

        return exp_bands

    def generate_salary_bands(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categorize employees into salary bands for compensation analysis.

        Bands:
        - Entry ($50K-$70K)
        - Mid ($70K-$90K)
        - Senior ($90K-$110K)
        - Lead ($110K-$130K)
        - Executive ($130K+)

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with salary band aggregations
        """
        self.logger.info("📊 Generating salary band analysis...")

        df_copy = df.copy()
        df_copy['salary_band'] = pd.cut(
            df_copy['salary'],
            bins=[0, 70000, 90000, 110000, 130000, float('inf')],
            labels=['Entry ($50-70K)', 'Mid ($70-90K)', 'Senior ($90-110K)', 'Lead ($110-130K)', 'Executive ($130K+)'],
            include_lowest=True
        )

        salary_bands = df_copy.groupby('salary_band', observed=True).agg({
            'id': 'count',
            'salary': 'mean',
            'experience_years': 'mean'
        }).round(2)

        salary_bands.columns = ['total_employees', 'avg_salary', 'avg_experience_years']
        salary_bands = salary_bands.reset_index()

        self.logger.info(f"   ✓ Generated {len(salary_bands)} salary bands")

        return salary_bands

    def generate_department_role_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a matrix showing employee distribution across departments and roles.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with department-role counts
        """
        self.logger.info("📊 Generating department-role matrix...")

        dept_role_matrix = df.groupby(['department', 'role']).agg({
            'id': 'count',
            'salary': 'mean'
        }).round(2)

        dept_role_matrix.columns = ['employee_count', 'avg_salary']
        dept_role_matrix = dept_role_matrix.reset_index()

        # Sort by department and employee count
        dept_role_matrix = dept_role_matrix.sort_values(['department', 'employee_count'], ascending=[True, False])

        self.logger.info(f"   ✓ Generated matrix with {len(dept_role_matrix)} department-role combinations")

        return dept_role_matrix

    def generate_ai_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate AI/ML-ready features for HR analytics and predictive modeling.

        Features:
        - salary_to_experience_ratio
        - age_to_experience_ratio
        - is_high_performer (top 25% salary)
        - tenure_category
        - salary_percentile
        - experience_percentile

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with AI-ready features
        """
        self.logger.info("🤖 Generating AI/ML-ready features...")

        ai_features = df.copy()

        # Feature 1: Salary to Experience Ratio
        ai_features['salary_to_experience_ratio'] = (
            ai_features['salary'] / (ai_features['experience_years'] + 1)
        ).round(2)

        # Feature 2: Age to Experience Ratio
        ai_features['age_to_experience_ratio'] = (
            ai_features['age'] / (ai_features['experience_years'] + 1)
        ).round(2)

        # Feature 3: High Performer Flag (top 25% salary)
        salary_75th = ai_features['salary'].quantile(0.75)
        ai_features['is_high_performer'] = (ai_features['salary'] >= salary_75th).astype(int)

        # Feature 4: Tenure Category
        ai_features['tenure_category'] = pd.cut(
            ai_features['experience_years'],
            bins=[0, 3, 7, 15, float('inf')],
            labels=['New', 'Established', 'Experienced', 'Veteran'],
            include_lowest=True
        )

        # Feature 5: Salary Percentile
        ai_features['salary_percentile'] = ai_features['salary'].rank(pct=True).mul(100).round(2)

        # Feature 6: Experience Percentile
        ai_features['experience_percentile'] = ai_features['experience_years'].rank(pct=True).mul(100).round(2)

        # Feature 7: Years Until Retirement (assuming 65)
        ai_features['years_to_retirement'] = 65 - ai_features['age']

        # Feature 8: Expected Career Midpoint (age 45)
        ai_features['is_mid_career'] = ((ai_features['age'] >= 35) & (ai_features['age'] <= 50)).astype(int)

        self.logger.info(f"   ✓ Generated 8 AI/ML features")
        self.logger.info(f"   ✓ High performers: {ai_features['is_high_performer'].sum()} employees")

        return ai_features

    def generate_executive_summary(self, df: pd.DataFrame) -> Dict:
        """
        Generate executive summary statistics.

        Args:
            df: Input DataFrame

        Returns:
            Dictionary with executive summary metrics
        """
        self.logger.info("📋 Generating executive summary...")

        summary = {
            'total_employees': int(len(df)),
            'total_departments': int(df['department'].nunique()),
            'total_roles': int(df['role'].nunique()),
            'total_cities': int(df['city'].nunique()),
            'avg_salary': float(df['salary'].mean().round(2)),
            'median_salary': float(df['salary'].median()),
            'min_salary': int(df['salary'].min()),
            'max_salary': int(df['salary'].max()),
            'total_payroll': int(df['salary'].sum()),
            'avg_age': float(df['age'].mean().round(2)),
            'avg_experience': float(df['experience_years'].mean().round(2)),
            'youngest_employee': int(df['age'].min()),
            'oldest_employee': int(df['age'].max()),
            'most_common_department': str(df['department'].mode()[0]),
            'highest_paid_department': str(df.groupby('department')['salary'].mean().idxmax())
        }

        self.logger.info(f"   ✓ Total Employees: {summary['total_employees']}")
        self.logger.info(f"   ✓ Average Salary: ${summary['avg_salary']:,.2f}")
        self.logger.info(f"   ✓ Total Payroll: ${summary['total_payroll']:,}")

        return summary

    def save_dataset(self, df: pd.DataFrame, filename: str):
        """
        Save aggregated dataset to Gold layer.

        Args:
            df: DataFrame to save
            filename: Output filename
        """
        output_path = self.gold_path / filename

        self.logger.info(f"💾 Saving dataset: {filename}")
        df.to_csv(output_path, index=False)

        self.stats['datasets_generated'] += 1

        file_size = output_path.stat().st_size
        self.logger.info(f"   ✓ Saved {len(df)} rows, {len(df.columns)} columns")
        self.logger.info(f"   ✓ File size: {file_size:,} bytes")

    def save_summary(self, summary: Dict, filename: str = "executive_summary.txt"):
        """
        Save executive summary to text file.

        Args:
            summary: Dictionary with summary metrics
            filename: Output filename
        """
        output_path = self.gold_path / filename

        self.logger.info(f"💾 Saving executive summary: {filename}")

        with open(output_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("EXECUTIVE SUMMARY - AI EMPLOYEE VAULT\n")
            f.write("=" * 80 + "\n\n")

            f.write("WORKFORCE OVERVIEW\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Employees:           {summary['total_employees']}\n")
            f.write(f"Total Departments:         {summary['total_departments']}\n")
            f.write(f"Total Roles:               {summary['total_roles']}\n")
            f.write(f"Total Office Locations:    {summary['total_cities']}\n\n")

            f.write("COMPENSATION METRICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Average Salary:            ${summary['avg_salary']:,.2f}\n")
            f.write(f"Median Salary:             ${summary['median_salary']:,.2f}\n")
            f.write(f"Min Salary:                ${summary['min_salary']:,}\n")
            f.write(f"Max Salary:                ${summary['max_salary']:,}\n")
            f.write(f"Total Annual Payroll:      ${summary['total_payroll']:,}\n\n")

            f.write("DEMOGRAPHICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Average Age:               {summary['avg_age']} years\n")
            f.write(f"Average Experience:        {summary['avg_experience']} years\n")
            f.write(f"Youngest Employee:         {summary['youngest_employee']} years\n")
            f.write(f"Oldest Employee:           {summary['oldest_employee']} years\n\n")

            f.write("KEY INSIGHTS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Largest Department:        {summary['most_common_department']}\n")
            f.write(f"Highest Paid Department:   {summary['highest_paid_department']}\n\n")

            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")

        self.logger.info(f"   ✓ Executive summary saved")

    def print_aggregation_summary(self):
        """Print summary statistics of the aggregation."""
        self.logger.info("\n" + "="*80)
        self.logger.info("GOLD LAYER AGGREGATION SUMMARY")
        self.logger.info("="*80)
        self.logger.info(f"Source: Silver layer (cleaned data)")
        self.logger.info(f"Total Employees Processed:  {self.stats['total_employees']}")
        self.logger.info(f"Total Departments:          {self.stats['total_departments']}")
        self.logger.info(f"Total Roles:                {self.stats['total_roles']}")
        self.logger.info(f"Datasets Generated:         {self.stats['datasets_generated']}")
        self.logger.info("="*80)

    def aggregate(self, input_filename: str = "employees_clean.csv"):
        """
        Execute complete Silver to Gold aggregation pipeline.

        Pipeline steps:
        1. Read Silver data
        2. Generate department metrics
        3. Generate role metrics
        4. Generate city metrics
        5. Generate top earners
        6. Generate experience bands
        7. Generate salary bands
        8. Generate department-role matrix
        9. Generate AI/ML features
        10. Generate executive summary
        11. Save all datasets
        12. Print summary

        Args:
            input_filename: Silver CSV filename
        """
        try:
            self.logger.info("\n" + "="*80)
            self.logger.info("🚀 GOLD LAYER AGGREGATION STARTED")
            self.logger.info("="*80 + "\n")

            # Step 1: Read Silver data
            df = self.read_silver_data(input_filename)

            # Step 2: Generate department metrics
            dept_metrics = self.aggregate_department_metrics(df)
            self.save_dataset(dept_metrics, "department_metrics.csv")

            # Step 3: Generate role metrics
            role_metrics = self.aggregate_role_metrics(df)
            self.save_dataset(role_metrics, "role_metrics.csv")

            # Step 4: Generate city metrics
            city_metrics = self.aggregate_city_metrics(df)
            self.save_dataset(city_metrics, "city_metrics.csv")

            # Step 5: Generate top earners
            top_earners = self.generate_top_earners(df, n=5)
            self.save_dataset(top_earners, "top_5_earners.csv")

            # Step 6: Generate experience bands
            exp_bands = self.generate_experience_bands(df)
            self.save_dataset(exp_bands, "experience_bands.csv")

            # Step 7: Generate salary bands
            salary_bands = self.generate_salary_bands(df)
            self.save_dataset(salary_bands, "salary_bands.csv")

            # Step 8: Generate department-role matrix
            dept_role_matrix = self.generate_department_role_matrix(df)
            self.save_dataset(dept_role_matrix, "department_role_matrix.csv")

            # Step 9: Generate AI/ML features
            ai_features = self.generate_ai_features(df)
            self.save_dataset(ai_features, "ai_ml_features.csv")

            # Step 10: Generate executive summary
            summary = self.generate_executive_summary(df)
            self.save_summary(summary, "executive_summary.txt")

            # Step 11: Print summary
            self.print_aggregation_summary()

            self.logger.info("\n✨ GOLD LAYER AGGREGATION COMPLETED SUCCESSFULLY\n")

        except Exception as e:
            self.logger.error(f"❌ Aggregation failed: {e}", exc_info=True)
            raise


def main():
    """Main execution function."""
    aggregator = GoldAggregation()
    aggregator.aggregate()


if __name__ == "__main__":
    main()
