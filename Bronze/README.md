# Bronze Layer - AI Employee Vault

## Overview
The Bronze layer is the **raw data ingestion layer** in the medallion architecture. It stores data in its original format without any transformations or cleaning.

## Purpose
- Store raw employee-related data (CSV/Excel/JSON)
- Perform basic validation (file exists, schema readable)
- No cleaning, normalization, or transformations
- Serve as the source of truth for raw data

## Directory Structure
```
Bronze/
├── data/
│   └── raw/              # Raw CSV/Excel/JSON files
├── notebooks/            # Jupyter notebooks for exploration
├── scripts/              # Python ingestion scripts
│   └── ingest_raw_data.py
└── README.md
```

## Dataset: employees.csv

### Schema
| Column | Type | Description |
|--------|------|-------------|
| id | int | Unique employee identifier |
| name | str | Employee full name |
| age | int | Employee age |
| department | str | Department name (Engineering, Data Science, HR, Finance, Marketing) |
| role | str | Job title/role |
| salary | int | Annual salary in USD |
| experience_years | int | Years of professional experience |
| city | str | Office location |

### Sample Data
The dataset contains 30 employee records suitable for AI/HR analytics use cases:
- Diverse departments: Engineering, Data Science, HR, Finance, Marketing
- Various roles: Data Engineers, ML Engineers, Scientists, Managers
- Salary range: $58K - $145K
- Experience range: 2-18 years
- Multiple office locations

## Ingestion Script

### Usage
```bash
cd scripts
python ingest_raw_data.py
```

### What the Script Does

#### 1. **Path Validation**
```python
def validate_path(self) -> bool:
    """Validate that raw data path exists"""
```
- Checks if `data/raw/` directory exists
- Logs error if path is invalid

#### 2. **File Discovery**
```python
def get_csv_files(self) -> list:
    """Get all CSV files from raw data directory"""
```
- Scans `data/raw/` for all CSV files
- Returns list of file paths
- Logs count of files found

#### 3. **Data Ingestion**
```python
def ingest_csv(self, file_path: Path) -> pd.DataFrame:
    """Ingest a single CSV file"""
```
- Reads CSV file using pandas
- **No transformations applied** (Bronze layer principle)
- Logs file size, row count, column count
- Returns raw DataFrame

#### 4. **Schema Display**
```python
def display_schema(self, df: pd.DataFrame, filename: str):
    """Display schema information"""
```
- Prints column names and data types
- Uses `df.dtypes` to show pandas inferred types

#### 5. **Sample Data Display**
```python
def display_sample(self, df: pd.DataFrame, filename: str, n_rows: int = 5):
    """Display first N rows"""
```
- Prints first 5 rows by default
- Shows actual data values for validation

#### 6. **Logging**
- Logs to both console and `bronze_ingestion.log` file
- Timestamp format: `YYYY-MM-DD HH:MM:SS`
- Structured logging levels: INFO, WARNING, ERROR

### Output Example
```
2026-02-10 14:45:00 - INFO - 🚀 BRONZE LAYER INGESTION STARTED
2026-02-10 14:45:00 - INFO - Found 1 CSV file(s) in data/raw
2026-02-10 14:45:00 - INFO - 📥 Ingesting: employees.csv
2026-02-10 14:45:00 - INFO -    ✓ File size: 2145 bytes
2026-02-10 14:45:00 - INFO -    ✓ Rows: 30
2026-02-10 14:45:00 - INFO -    ✓ Columns: 8

================================================================================
SCHEMA: employees.csv
================================================================================
id                   int64
name                object
age                  int64
department          object
role                object
salary               int64
experience_years     int64
city                object

================================================================================
SAMPLE DATA (First 5 rows): employees.csv
================================================================================
id        name  age    department                    role  salary  experience_years           city
 1  John Smith   35   Engineering  Senior Data Engineer   95000                 8  San Francisco
 2 Maria Garcia   28   Engineering           ML Engineer   85000                 4       New York
...
```

## Best Practices Implemented

### 1. **Separation of Concerns**
- Class-based design (`BronzeIngestion`)
- Single responsibility methods
- Clear method signatures

### 2. **Logging & Observability**
- Dual logging (console + file)
- Structured log messages with emojis for readability
- Timestamp tracking for audit trail

### 3. **Error Handling**
- Try-except blocks for file operations
- Graceful failure (continues processing other files)
- Detailed error messages

### 4. **Path Management**
- Uses `pathlib.Path` for cross-platform compatibility
- Relative paths from script location

### 5. **Type Hints**
- Function signatures include type annotations
- Improves code readability and IDE support

### 6. **Documentation**
- Comprehensive docstrings
- Inline comments for complex logic
- Clear variable names

## Bronze Layer Principles

✅ **DO:**
- Store raw data as-is
- Validate file existence and readability
- Log ingestion metadata (timestamp, file size, row count)
- Display schema and sample data for verification

❌ **DON'T:**
- Clean or normalize data
- Handle missing values
- Remove duplicates
- Perform type casting beyond pandas inference
- Apply business logic or transformations

## Next Steps
After Bronze ingestion, data moves to:
1. **Silver Layer**: Cleaned, deduplicated, validated data
2. **Gold Layer**: Aggregated, business-ready datasets

## Requirements
- Python 3.10+
- pandas

Install dependencies:
```bash
pip install pandas
```

## Running the Ingestion
```bash
# From Bronze/scripts/ directory
python ingest_raw_data.py

# Or from Bronze/ directory
python scripts/ingest_raw_data.py
```

## Extending the Bronze Layer
To add more raw datasets:
1. Place CSV/Excel/JSON files in `data/raw/`
2. Run `ingest_raw_data.py` - it auto-discovers all CSV files
3. For other formats (Excel, JSON), extend the `BronzeIngestion` class

---

**Data Engineering Team**
AI Employee Vault Project
Updated: 2026-02-10
