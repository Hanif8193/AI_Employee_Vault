# Silver Layer - Data Cleaning Logic Explained

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         BRONZE LAYER (Raw)                          │
│                  Bronze/data/raw/employees.csv                      │
│                                                                     │
│  • 30 employee records                                              │
│  • 8 columns                                                        │
│  • Raw, unvalidated data                                            │
│  • May contain issues                                               │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ READ (read_bronze_data)
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 1: STANDARDIZE COLUMNS                      │
│                   (standardize_column_names)                        │
│                                                                     │
│  Transform: All column names → snake_case                           │
│  Example: "experienceYears" → "experience_years"                    │
│  Result: Consistent naming convention                               │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  STEP 2: HANDLE MISSING VALUES                      │
│                   (handle_missing_values)                           │
│                                                                     │
│  Numeric columns → Fill with MEDIAN                                 │
│    Example: age [25, 30, NULL, 40] → [25, 30, 32.5, 40]            │
│                                                                     │
│  Categorical columns → Fill with MODE or "Unknown"                  │
│    Example: city ["NYC", NULL, "NYC"] → ["NYC", "NYC", "NYC"]      │
│                                                                     │
│  Log: All fill operations recorded                                  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 3: REMOVE DUPLICATES                        │
│                      (remove_duplicates)                            │
│                                                                     │
│  Method: Identify exact duplicate rows                              │
│  Action: Keep FIRST occurrence, remove rest                         │
│  Log: Count of duplicates removed                                   │
│                                                                     │
│  Before: [Row1, Row2, Row1, Row3] → After: [Row1, Row2, Row3]      │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 4: FIX DATA TYPES                           │
│                       (fix_data_types)                              │
│                                                                     │
│  Enforce correct types:                                             │
│    • id: int64                                                      │
│    • name: string                                                   │
│    • age: int64                                                     │
│    • department: string                                             │
│    • role: string                                                   │
│    • salary: int64                                                  │
│    • experience_years: int64                                        │
│    • city: string                                                   │
│                                                                     │
│  Example: salary "95000" (str) → 95000 (int64)                     │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│               STEP 5: VALIDATE BUSINESS RULES                       │
│                  (validate_business_rules)                          │
│                                                                     │
│  Rule 1: age >= 18                                                  │
│    ❌ Remove: age = 15, 17, 10                                      │
│    ✅ Keep: age = 18, 25, 42                                        │
│                                                                     │
│  Rule 2: salary > 0                                                 │
│    ❌ Remove: salary = 0, -1000, -500                               │
│    ✅ Keep: salary = 50000, 95000, 120000                           │
│                                                                     │
│  Rule 3: experience_years >= 0                                      │
│    ❌ Remove: experience = -1, -5, -10                              │
│    ✅ Keep: experience = 0, 5, 15                                   │
│                                                                     │
│  Log: All invalid rows with values before removal                   │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ SAVE (save_to_silver)
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       SILVER LAYER (Clean)                          │
│              Silver/data/clean/employees_clean.csv                  │
│                                                                     │
│  ✅ No missing values                                               │
│  ✅ No duplicates                                                   │
│  ✅ Correct data types                                              │
│  ✅ All validation rules passed                                     │
│  ✅ Standardized column names                                       │
│  ✅ Ready for Gold layer                                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Cleaning Examples

### Example 1: Missing Value Handling

#### Scenario: Age column has missing values

**Input (Bronze):**
```csv
id,name,age,department,salary
1,John,35,Engineering,95000
2,Maria,,Engineering,85000      ← Missing age
3,James,42,HR,75000
4,Emily,31,Data Science,90000
5,Bob,,Finance,82000             ← Missing age
```

**Processing:**
1. Detect missing values in 'age' column (2 missing)
2. Calculate median of non-missing values: median([35, 42, 31]) = 35
3. Fill missing values with median

**Output (Silver):**
```csv
id,name,age,department,salary
1,John,35,Engineering,95000
2,Maria,35,Engineering,85000      ← Filled with median (35)
3,James,42,HR,75000
4,Emily,31,Data Science,90000
5,Bob,35,Finance,82000             ← Filled with median (35)
```

**Log Entry:**
```
⚠ Found 2 missing values:
   age: 2 missing
✓ Filled age with median: 35
```

---

### Example 2: Duplicate Removal

#### Scenario: Duplicate employee records exist

**Input (Bronze):**
```csv
id,name,age,department,salary,experience_years
1,John Smith,35,Engineering,95000,8
2,Maria Garcia,28,Engineering,85000,4
3,James Wilson,42,HR,75000,15
1,John Smith,35,Engineering,95000,8     ← DUPLICATE of row 1
4,Emily Chen,31,Data Science,90000,6
2,Maria Garcia,28,Engineering,85000,4    ← DUPLICATE of row 2
```

**Processing:**
1. Identify exact duplicate rows (rows 4 and 6)
2. Keep FIRST occurrence of each duplicate
3. Remove subsequent duplicates

**Output (Silver):**
```csv
id,name,age,department,salary,experience_years
1,John Smith,35,Engineering,95000,8
2,Maria Garcia,28,Engineering,85000,4
3,James Wilson,42,HR,75000,15
4,Emily Chen,31,Data Science,90000,6
```

**Log Entry:**
```
✓ Removed 2 duplicate row(s)
```

---

### Example 3: Validation Rule Enforcement

#### Scenario: Invalid data violates business rules

**Input (Bronze):**
```csv
id,name,age,department,salary,experience_years
1,John Smith,35,Engineering,95000,8
2,Sarah Connor,15,HR,60000,2          ← age < 18 (INVALID)
3,Tom Brady,42,Finance,0,15           ← salary = 0 (INVALID)
4,Anna Lee,28,Marketing,-5,3          ← experience < 0 (INVALID - typo)
5,Bob Jones,25,Engineering,75000,3
```

**Processing:**

**Rule 1: age >= 18**
- Row 2: age = 15 ❌ INVALID → Remove

**Rule 2: salary > 0**
- Row 3: salary = 0 ❌ INVALID → Remove

**Rule 3: experience_years >= 0**
- Row 4: experience = -5 ❌ INVALID → Remove

**Output (Silver):**
```csv
id,name,age,department,salary,experience_years
1,John Smith,35,Engineering,95000,8
5,Bob Jones,25,Engineering,75000,3
```

**Log Entry:**
```
⚠ Found 1 row(s) with age < 18
   Invalid ages: [15]
⚠ Found 1 row(s) with salary <= 0
   Invalid salaries: [0]
⚠ Found 1 row(s) with experience < 0
   Invalid experience: [-5]
✓ Total invalid rows removed: 3
```

---

### Example 4: Data Type Enforcement

#### Scenario: Data types are inconsistent

**Input (Bronze):**
```python
# Read CSV - pandas infers types
df = pd.read_csv('employees.csv')
print(df.dtypes)

# Output:
id                   int64    ✓ Correct
name                object    ✗ Should be string
age                  int64    ✓ Correct
department          object    ✗ Should be string
role                object    ✗ Should be string
salary               int64    ✓ Correct
experience_years     int64    ✓ Correct
city                object    ✗ Should be string
```

**Processing:**
```python
# Convert object → string for text columns
df['name'] = df['name'].astype('string')
df['department'] = df['department'].astype('string')
df['role'] = df['role'].astype('string')
df['city'] = df['city'].astype('string')
```

**Output (Silver):**
```python
print(df.dtypes)

# Output:
id                   int64    ✓ Correct
name                string    ✓ Fixed
age                  int64    ✓ Correct
department          string    ✓ Fixed
role                string    ✓ Fixed
salary               int64    ✓ Correct
experience_years     int64    ✓ Correct
city                string    ✓ Fixed
```

**Log Entry:**
```
✓ name: object -> string
✓ department: object -> string
✓ role: object -> string
✓ city: object -> string
```

---

## Transformation Statistics

### Metrics Tracked

For every transformation run, the following statistics are captured:

```python
stats = {
    'original_rows': 30,              # Input row count
    'duplicate_rows_removed': 0,      # Duplicates eliminated
    'invalid_rows_removed': 0,        # Failed validation rules
    'missing_values_handled': 0,      # NULL values filled
    'final_rows': 30                  # Output row count
}

# Calculate data retention
data_retention = (final_rows / original_rows) × 100
# Example: (30 / 30) × 100 = 100.00%
```

### Quality Thresholds

| Metric | Target | Status |
|--------|--------|--------|
| Data Retention Rate | ≥ 95% | ✅ 100% |
| Missing Value Rate | < 5% | ✅ 0% |
| Duplicate Rate | < 1% | ✅ 0% |
| Validation Pass Rate | ≥ 95% | ✅ 100% |

---

## Why Each Cleaning Step Matters

### 1. Standardize Column Names
**Problem:** Inconsistent naming makes code harder to maintain
- `experienceYears` vs `experience_years` vs `ExperienceYears`

**Solution:** snake_case convention
- Readable: `experience_years`
- Pythonic: Follows PEP 8
- SQL-friendly: Compatible with database column names

### 2. Handle Missing Values
**Problem:** NULL values break calculations and ML models
- `mean([50, 60, NULL, 80])` → Error
- ML models require complete data

**Solution:** Intelligent imputation
- Numeric: Median (robust to outliers)
- Categorical: Mode (most common value)
- Preserves data distribution

### 3. Remove Duplicates
**Problem:** Duplicates skew statistics and waste storage
- Counting employees: 30 unique, but 35 rows = incorrect metrics
- Storage: Redundant data costs money

**Solution:** Deduplication
- Keeps first occurrence
- Removes exact duplicates
- Maintains data integrity

### 4. Fix Data Types
**Problem:** Wrong types cause silent errors
- String "95000" + 5000 = "950005000" (concatenation, not addition!)
- object dtype uses more memory than string

**Solution:** Explicit type enforcement
- Numeric operations work correctly
- Memory efficiency improved
- Type safety for downstream processing

### 5. Validate Business Rules
**Problem:** Invalid data leads to wrong business decisions
- Hiring someone aged 12 = Legal violation
- Salary of $0 = Incomplete record
- Negative experience = Data entry error

**Solution:** Rule-based validation
- Enforce business constraints
- Catch data entry errors
- Ensure regulatory compliance

---

## Code Architecture

### Class Structure

```python
class SilverTransformation:
    """
    Encapsulates all Bronze → Silver transformation logic.

    Design Pattern: Pipeline Pattern
    - Each method is a transformation step
    - Steps executed in sequence
    - Each step returns transformed DataFrame
    - Immutable: Original Bronze data never modified
    """

    def __init__(self):
        """Initialize logging and paths"""

    def transform(self):
        """Main pipeline executor"""
        df = self.read_bronze_data()
        df = self.standardize_column_names(df)
        df = self.handle_missing_values(df)
        df = self.remove_duplicates(df)
        df = self.fix_data_types(df)
        df = self.validate_business_rules(df)
        self.save_to_silver(df)
        self.print_transformation_summary()
```

### Method Signatures

```python
def read_bronze_data(self, filename: str = "employees.csv") -> pd.DataFrame:
    """Read raw CSV from Bronze layer"""

def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to snake_case"""

def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
    """Fill NULL values with median/mode"""

def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows"""

def fix_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
    """Enforce correct dtypes"""

def validate_business_rules(self, df: pd.DataFrame) -> pd.DataFrame:
    """Apply age/salary/experience validations"""

def save_to_silver(self, df: pd.DataFrame, filename: str = "employees_clean.csv"):
    """Write cleaned data to Silver layer"""

def print_transformation_summary(self):
    """Display statistics"""
```

---

## Testing Strategy

### Manual Testing

```bash
# 1. Run transformation
python Silver/scripts/transform_bronze_to_silver.py

# 2. Check row count matches
wc -l Bronze/data/raw/employees.csv
wc -l Silver/data/clean/employees_clean.csv
# Both should be 31 lines (30 data + 1 header)

# 3. Verify no missing values
grep ",," Silver/data/clean/employees_clean.csv
# Should return nothing

# 4. Check data types visually
head Silver/data/clean/employees_clean.csv

# 5. Validate business rules
awk -F',' 'NR>1 {if ($3<18) print "Age violation: "$3}' Silver/data/clean/employees_clean.csv
awk -F',' 'NR>1 {if ($6<=0) print "Salary violation: "$6}' Silver/data/clean/employees_clean.csv
awk -F',' 'NR>1 {if ($7<0) print "Experience violation: "$7}' Silver/data/clean/employees_clean.csv
# All should return nothing
```

### Automated Testing (Future)

```python
# test_silver_transformation.py
import pytest
import pandas as pd
from transform_bronze_to_silver import SilverTransformation

def test_no_missing_values():
    """Ensure cleaned data has no NULL values"""
    df = pd.read_csv('Silver/data/clean/employees_clean.csv')
    assert df.isnull().sum().sum() == 0

def test_no_duplicates():
    """Ensure no duplicate rows"""
    df = pd.read_csv('Silver/data/clean/employees_clean.csv')
    assert len(df) == len(df.drop_duplicates())

def test_age_validation():
    """Ensure all ages >= 18"""
    df = pd.read_csv('Silver/data/clean/employees_clean.csv')
    assert (df['age'] >= 18).all()

def test_salary_validation():
    """Ensure all salaries > 0"""
    df = pd.read_csv('Silver/data/clean/employees_clean.csv')
    assert (df['salary'] > 0).all()

def test_experience_validation():
    """Ensure all experience >= 0"""
    df = pd.read_csv('Silver/data/clean/employees_clean.csv')
    assert (df['experience_years'] >= 0).all()
```

---

## Performance Characteristics

### Current Dataset (30 rows)
- Execution time: < 1 second
- Memory usage: < 50 MB
- CPU usage: Single core, < 10% utilization

### Scaling Considerations

| Dataset Size | Expected Time | Memory | Recommendation |
|--------------|---------------|--------|----------------|
| 100 rows | < 1 sec | 50 MB | Current script |
| 10K rows | < 2 sec | 100 MB | Current script |
| 1M rows | ~30 sec | 2 GB | Current script |
| 100M rows | ~1 hour | 200 GB | Use chunking or Spark |

### Optimization for Large Datasets

```python
# For datasets > 10M rows, use chunked processing
def read_bronze_data_chunked(self, filename: str, chunksize: int = 100000):
    """Read large CSV in chunks"""
    chunks = []
    for chunk in pd.read_csv(self.bronze_path / filename, chunksize=chunksize):
        # Apply transformations to chunk
        chunk = self.standardize_column_names(chunk)
        chunk = self.handle_missing_values(chunk)
        chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)
```

---

**Silver Layer Cleaning Logic Documentation**
AI Employee Vault Project
Date: 2026-02-10
