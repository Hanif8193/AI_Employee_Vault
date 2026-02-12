# Silver Layer - AI Employee Vault

## Overview
The Silver layer is the **data cleaning and validation layer** in the medallion architecture. It transforms raw Bronze data into clean, standardized, and validated datasets ready for business transformations.

## Purpose
- Read raw data from Bronze layer
- Clean and standardize data (missing values, duplicates, data types)
- Apply data quality validation rules
- Ensure data consistency and integrity
- Serve as the foundation for Gold layer business logic

## Directory Structure
```
Silver/
├── data/
│   └── clean/              # Cleaned and validated CSV files
│       └── employees_clean.csv
├── scripts/                # Python transformation scripts
│   └── transform_bronze_to_silver.py
├── logs/                   # Transformation logs
│   └── silver_transformation_YYYYMMDD_HHMMSS.log
└── README.md
```

## Data Cleaning Process

The Silver layer applies the following transformations to Bronze data:

### 1. **Column Name Standardization**
- Converts all column names to `snake_case`
- Removes leading/trailing whitespace
- Ensures consistent naming convention
- Example: `experienceYears` → `experience_years`

### 2. **Missing Value Handling**
Strategy varies by data type:
- **Numeric columns** (age, salary, experience_years): Fill with **median**
- **Categorical columns** (name, department, role, city): Fill with **mode** or "Unknown"
- Logs all missing value operations for audit trail

### 3. **Duplicate Removal**
- Identifies and removes exact duplicate rows
- Preserves first occurrence of duplicated records
- Logs count of duplicates removed

### 4. **Data Type Enforcement**
Ensures correct data types for each column:
```python
{
    'id': int64,
    'name': string,
    'age': int64,
    'department': string,
    'role': string,
    'salary': int64,
    'experience_years': int64,
    'city': string
}
```

### 5. **Business Validation Rules**
Removes rows that violate business constraints:

| Rule | Validation | Reason |
|------|------------|--------|
| **Age** | `age >= 18` | Legal working age requirement |
| **Salary** | `salary > 0` | Must have positive salary |
| **Experience** | `experience_years >= 0` | Cannot have negative experience |

Invalid rows are logged and excluded from the output.

## Transformation Script

### Script: `transform_bronze_to_silver.py`

**Location:** `Silver/scripts/transform_bronze_to_silver.py`

**Features:**
- ✅ Class-based design for maintainability
- ✅ Comprehensive logging (file + console)
- ✅ Statistical tracking (rows processed, removed, retained)
- ✅ Error handling with detailed messages
- ✅ Type hints for code clarity
- ✅ Configurable input/output paths

### How to Run

#### Option 1: From Silver/scripts/ directory
```bash
cd Silver/scripts
python transform_bronze_to_silver.py
```

#### Option 2: From project root
```bash
python Silver/scripts/transform_bronze_to_silver.py
```

#### Option 3: As executable (Unix/Linux/Mac)
```bash
cd Silver/scripts
./transform_bronze_to_silver.py
```

### What the Script Does

#### **Step 1: Read Bronze Data**
```python
def read_bronze_data(self, filename: str = "employees.csv") -> pd.DataFrame
```
- Reads raw CSV from `Bronze/data/raw/employees.csv`
- Validates file existence
- Logs original row count and column names

#### **Step 2: Standardize Column Names**
```python
def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame
```
- Converts column names to snake_case
- Removes whitespace and special characters
- Logs any name changes

#### **Step 3: Handle Missing Values**
```python
def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame
```
- Detects missing values in all columns
- Applies appropriate fill strategy (median/mode)
- Logs all missing value operations

#### **Step 4: Remove Duplicates**
```python
def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame
```
- Identifies duplicate rows
- Keeps first occurrence
- Logs count of duplicates removed

#### **Step 5: Fix Data Types**
```python
def fix_data_types(self, df: pd.DataFrame) -> pd.DataFrame
```
- Enforces correct data types for each column
- Handles type conversion errors gracefully
- Logs all type conversions

#### **Step 6: Validate Business Rules**
```python
def validate_business_rules(self, df: pd.DataFrame) -> pd.DataFrame
```
- Applies age, salary, and experience validations
- Removes invalid rows
- Logs invalid values found and removed

#### **Step 7: Save to Silver Layer**
```python
def save_to_silver(self, df: pd.DataFrame, filename: str = "employees_clean.csv")
```
- Saves cleaned data to `Silver/data/clean/employees_clean.csv`
- Logs final row count and file size

#### **Step 8: Print Transformation Summary**
```python
def print_transformation_summary(self)
```
- Displays comprehensive statistics
- Shows data retention rate
- Provides audit trail for quality assurance

### Example Output

```
================================================================================
🚀 SILVER LAYER TRANSFORMATION STARTED
================================================================================

2026-02-10 15:00:00 - INFO - Logging to: Silver/logs/silver_transformation_20260210_150000.log
2026-02-10 15:00:00 - INFO - Bronze path: Bronze/data/raw
2026-02-10 15:00:00 - INFO - Silver path: Silver/data/clean

2026-02-10 15:00:00 - INFO - 📥 Reading Bronze data from: employees.csv
2026-02-10 15:00:00 - INFO -    ✓ Loaded 30 rows, 8 columns
2026-02-10 15:00:00 - INFO -    ✓ Columns: ['id', 'name', 'age', 'department', 'role', 'salary', 'experience_years', 'city']

2026-02-10 15:00:00 - INFO - 🔤 Standardizing column names to snake_case...
2026-02-10 15:00:00 - INFO -    ✓ Column names already in snake_case

2026-02-10 15:00:00 - INFO - 🔍 Checking for missing values...
2026-02-10 15:00:00 - INFO -    ✓ No missing values found

2026-02-10 15:00:00 - INFO - 🔍 Checking for duplicate rows...
2026-02-10 15:00:00 - INFO -    ✓ No duplicate rows found

2026-02-10 15:00:00 - INFO - 🔧 Fixing data types...
2026-02-10 15:00:00 - INFO -    ✓ name: object -> string
2026-02-10 15:00:00 - INFO -    ✓ department: object -> string
2026-02-10 15:00:00 - INFO -    ✓ role: object -> string
2026-02-10 15:00:00 - INFO -    ✓ city: object -> string

2026-02-10 15:00:00 - INFO - ✅ Applying validation rules...
2026-02-10 15:00:00 - INFO -    ✓ All ages >= 18
2026-02-10 15:00:00 - INFO -    ✓ All salaries > 0
2026-02-10 15:00:00 - INFO -    ✓ All experience_years >= 0
2026-02-10 15:00:00 - INFO -    ✓ All rows passed validation

2026-02-10 15:00:00 - INFO - 💾 Saving cleaned data to: employees_clean.csv
2026-02-10 15:00:00 - INFO -    ✓ Saved 30 rows, 8 columns
2026-02-10 15:00:00 - INFO -    ✓ File size: 2,145 bytes
2026-02-10 15:00:00 - INFO -    ✓ Location: Silver/data/clean/employees_clean.csv

================================================================================
TRANSFORMATION SUMMARY
================================================================================
Original rows:              30
Duplicate rows removed:     0
Invalid rows removed:       0
Missing values handled:     0
Final rows:                 30
Data retention rate:        100.00%
================================================================================

✨ SILVER LAYER TRANSFORMATION COMPLETED SUCCESSFULLY
```

## Output Dataset: employees_clean.csv

### Schema
| Column | Type | Description | Validation |
|--------|------|-------------|------------|
| id | int64 | Unique employee identifier | - |
| name | string | Employee full name | Not null |
| age | int64 | Employee age | >= 18 |
| department | string | Department name | Not null |
| role | string | Job title/role | Not null |
| salary | int64 | Annual salary in USD | > 0 |
| experience_years | int64 | Years of professional experience | >= 0 |
| city | string | Office location | Not null |

### Data Quality Guarantees
- ✅ No missing values
- ✅ No duplicate rows
- ✅ All data types correctly enforced
- ✅ All business rules validated
- ✅ Column names standardized (snake_case)
- ✅ Ready for Gold layer transformations

## Logging

### Log Files
Location: `Silver/logs/silver_transformation_YYYYMMDD_HHMMSS.log`

Each transformation creates a timestamped log file containing:
- Detailed step-by-step execution trace
- Data quality issues found
- Validation rule violations
- Rows removed and reasons
- File operations (read/write)
- Error messages and stack traces

### Log Format
```
YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE
```

**Log Levels:**
- `INFO`: Normal operation messages
- `WARNING`: Data quality issues (missing values, duplicates, invalid data)
- `ERROR`: Execution failures

### Viewing Logs
```bash
# View latest log
cd Silver/logs
ls -lt | head -2
cat silver_transformation_YYYYMMDD_HHMMSS.log

# Search for warnings
grep "WARNING" silver_transformation_*.log

# Search for data quality issues
grep "removed" silver_transformation_*.log
```

## Best Practices Implemented

### 1. **Class-Based Design**
- `SilverTransformation` class encapsulates all logic
- Single responsibility methods
- Easy to extend and test

### 2. **Comprehensive Logging**
- Dual output (console + file)
- Timestamped log files
- Detailed audit trail for compliance

### 3. **Error Handling**
- Try-except blocks around file operations
- Graceful failure with informative messages
- Stack traces logged for debugging

### 4. **Type Safety**
- Type hints on all function signatures
- Explicit data type enforcement
- Prevents silent type coercion bugs

### 5. **Statistical Tracking**
- Tracks rows at each transformation step
- Calculates data retention rate
- Provides transparency into data loss

### 6. **Idempotency**
- Running the script multiple times produces the same output
- No side effects on Bronze layer
- Safe to re-run after failures

### 7. **Documentation**
- Comprehensive docstrings
- Inline comments for complex logic
- Clear variable and function names

## Silver Layer Principles

✅ **DO:**
- Clean and standardize data
- Handle missing values appropriately
- Remove duplicates
- Enforce data types
- Apply data quality validation rules
- Log all transformations
- Preserve raw Bronze data (read-only)

❌ **DON'T:**
- Apply business logic or aggregations (that's for Gold layer)
- Perform feature engineering or AI transformations
- Modify Bronze layer data
- Create new derived columns (unless for standardization)
- Join data from multiple sources

## Quality Metrics

The Silver layer tracks these data quality metrics:

| Metric | Description |
|--------|-------------|
| **Data Retention Rate** | (Final rows / Original rows) × 100 |
| **Duplicate Rate** | (Duplicates removed / Original rows) × 100 |
| **Invalid Data Rate** | (Invalid rows / Original rows) × 100 |
| **Missing Value Rate** | (Missing values / Total cells) × 100 |

Target: **>95% data retention rate** (less than 5% data loss due to quality issues)

## Troubleshooting

### Issue: Script cannot find Bronze data
```
FileNotFoundError: Bronze file not found: Bronze/data/raw/employees.csv
```
**Solution:**
- Ensure Bronze layer exists and contains `employees.csv`
- Run from project root or adjust paths in script

### Issue: Permission denied when saving to Silver
```
PermissionError: [Errno 13] Permission denied: 'Silver/data/clean/employees_clean.csv'
```
**Solution:**
- Check write permissions on Silver directory
- Close any open Excel/CSV viewers on the output file
- Run with appropriate user permissions

### Issue: Memory error with large datasets
```
MemoryError: Unable to allocate array
```
**Solution:**
- Use chunked reading with `pd.read_csv(chunksize=10000)`
- Process data in batches
- Increase available RAM or use distributed computing (Spark)

## Requirements

### Python Version
- Python 3.10 or higher

### Dependencies
```bash
pip install pandas
```

### Full Requirements File
Create `requirements.txt`:
```
pandas>=2.0.0
```

Install:
```bash
pip install -r requirements.txt
```

## Extending the Silver Layer

### Adding New Data Sources
1. Place new Bronze CSV in `Bronze/data/raw/`
2. Update `transform_bronze_to_silver.py` to accept filename parameter
3. Add source-specific validation rules if needed

### Custom Validation Rules
Add new validation methods to `SilverTransformation` class:
```python
def validate_email_format(self, df: pd.DataFrame) -> pd.DataFrame:
    """Validate email addresses using regex."""
    invalid_emails = ~df['email'].str.match(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    df = df[~invalid_emails]
    return df
```

### Advanced Cleaning
For complex scenarios:
- Text normalization (lowercase, remove special chars)
- Date parsing and standardization
- Currency conversion
- Outlier detection and handling

## Next Steps

After Silver cleaning, data flows to:
1. **Gold Layer**: Business aggregations, analytics, KPIs
2. **Platinum Layer** (optional): AI/ML feature engineering

## Testing

Run transformation and verify output:
```bash
# Run transformation
python Silver/scripts/transform_bronze_to_silver.py

# Verify output exists
ls -lh Silver/data/clean/employees_clean.csv

# Quick data check
head Silver/data/clean/employees_clean.csv

# Check logs
tail -50 Silver/logs/silver_transformation_*.log
```

## Performance

Benchmarks on employee dataset (30 rows):
- Execution time: < 1 second
- Memory usage: < 50 MB
- Output file size: ~2 KB

For production datasets (millions of rows), consider:
- Chunked processing
- Parallel execution (Dask, PySpark)
- Incremental updates instead of full reprocessing

## Data Lineage

```
Bronze/data/raw/employees.csv
    ↓ (read_bronze_data)
    ↓ (standardize_column_names)
    ↓ (handle_missing_values)
    ↓ (remove_duplicates)
    ↓ (fix_data_types)
    ↓ (validate_business_rules)
    ↓ (save_to_silver)
Silver/data/clean/employees_clean.csv
```

## Compliance & Auditing

The Silver layer provides:
- **Full audit trail** via timestamped logs
- **Data lineage tracking** (source → transformations → output)
- **Quality metrics** for compliance reporting
- **Reproducibility** (same input → same output)

Perfect for:
- SOC 2 compliance
- GDPR data processing records
- Financial audits
- Quality assurance

---

**Data Engineering Team**
AI Employee Vault Project
Updated: 2026-02-10
