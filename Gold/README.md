# Gold Layer - AI Employee Vault

## Overview
The Gold layer is the **business logic and analytics layer** in the medallion architecture. It transforms cleaned Silver data into aggregated, analytics-ready datasets for business intelligence, reporting, and AI/ML applications.

## Purpose
- Read cleaned data from Silver layer
- Apply business logic and aggregations
- Generate department, role, and city-level metrics
- Create AI/ML-ready features
- Produce executive dashboards and reports
- Serve as the final consumption layer for analytics

## Directory Structure
```
Gold/
├── data/
│   └── gold/                                # Analytics-ready datasets
│       ├── department_metrics.csv           # Department-level aggregations
│       ├── role_metrics.csv                 # Role-level aggregations
│       ├── city_metrics.csv                 # City-level aggregations
│       ├── top_5_earners.csv                # Highest paid employees
│       ├── experience_bands.csv             # Experience category analysis
│       ├── salary_bands.csv                 # Salary category analysis
│       ├── department_role_matrix.csv       # Department-role distribution
│       ├── ai_ml_features.csv               # AI/ML-ready features
│       └── executive_summary.txt            # Executive summary report
├── scripts/
│   └── generate_gold_data.py                # Main aggregation script
├── logs/                                    # Aggregation logs
│   └── gold_aggregation_YYYYMMDD_HHMMSS.log
├── visualizations/                          # Future: Plots and charts
└── README.md
```

## Business Logic & Aggregations

The Gold layer applies the following business transformations:

### 1. **Department Metrics** (`department_metrics.csv`)
Provides comprehensive department-level KPIs for HR and finance teams.

**Aggregations:**
- `total_employees`: Count of employees per department
- `avg_salary`: Average salary per department
- `min_salary`: Lowest salary in department
- `max_salary`: Highest salary in department
- `total_payroll`: Sum of all salaries per department
- `avg_age`: Average age of employees in department
- `avg_experience_years`: Average years of experience in department
- `salary_range`: Difference between max and min salary

**Business Use Cases:**
- Budget planning and forecasting
- Departmental cost analysis
- Headcount planning
- Compensation benchmarking

**Sample Output:**
```csv
department,total_employees,avg_salary,min_salary,max_salary,total_payroll,avg_age,avg_experience_years,salary_range
Engineering,10,92000,78000,125000,920000,34.5,9.2,47000
Data Science,8,89500,68000,105000,716000,32.1,6.8,37000
```

---

### 2. **Role Metrics** (`role_metrics.csv`)
Analyzes compensation and demographics by job role.

**Aggregations:**
- `total_employees`: Count per role
- `avg_salary`: Average salary per role
- `avg_experience_years`: Average experience per role
- `avg_age`: Average age per role

**Business Use Cases:**
- Role-based compensation planning
- Career path analysis
- Talent acquisition targeting
- Succession planning

**Sample Output:**
```csv
role,total_employees,avg_salary,avg_experience_years,avg_age
VP of Engineering,1,145000,17.0,40.0
Principal Engineer,1,125000,16.0,43.0
Engineering Manager,1,115000,14.0,41.0
```

---

### 3. **City Metrics** (`city_metrics.csv`)
Provides office location-based analytics.

**Aggregations:**
- `total_employees`: Count per city
- `avg_salary`: Average salary per city
- `total_payroll`: Total payroll per city
- `department_diversity`: Number of unique departments in city

**Business Use Cases:**
- Real estate and office planning
- Regional cost analysis
- Geographic expansion decisions
- Remote vs on-site workforce analysis

**Sample Output:**
```csv
city,total_employees,avg_salary,total_payroll,department_diversity
San Francisco,7,108571,760000,4
New York,5,84000,420000,4
```

---

### 4. **Top 5 Earners** (`top_5_earners.csv`)
Identifies highest paid employees for executive reporting.

**Fields:**
- `rank`: 1-5 ranking
- `name`: Employee name
- `role`: Job title
- `department`: Department
- `salary`: Annual salary
- `experience_years`: Years of experience
- `city`: Office location

**Business Use Cases:**
- Executive compensation analysis
- Retention risk assessment
- Succession planning
- Pay equity analysis

**Sample Output:**
```csv
rank,name,role,department,salary,experience_years,city
1,Justin Baker,VP of Engineering,Engineering,145000,17,San Francisco
2,Kevin Young,Principal Engineer,Engineering,125000,16,San Francisco
3,Daniel Thompson,Engineering Manager,Engineering,115000,14,San Francisco
```

---

### 5. **Experience Bands** (`experience_bands.csv`)
Categorizes employees by experience level for workforce planning.

**Experience Categories:**
- **Entry (0-2 years)**: New hires, interns, junior roles
- **Junior (3-5 years)**: Early career professionals
- **Mid (6-10 years)**: Mid-career professionals
- **Senior (11-15 years)**: Senior professionals
- **Expert (16+ years)**: Industry veterans

**Aggregations:**
- `total_employees`: Count per band
- `avg_salary`: Average salary per band
- `avg_age`: Average age per band

**Business Use Cases:**
- Workforce maturity analysis
- Mentorship program planning
- Training and development targeting
- Career progression modeling

**Sample Output:**
```csv
experience_band,total_employees,avg_salary,avg_age
Mid (6-10yr),12,91500,34.5
Junior (3-5yr),8,75000,28.2
Senior (11-15yr),6,95000,40.1
```

---

### 6. **Salary Bands** (`salary_bands.csv`)
Categorizes employees by compensation level.

**Salary Categories:**
- **Entry ($50K-$70K)**: Entry-level compensation
- **Mid ($70K-$90K)**: Mid-level compensation
- **Senior ($90K-$110K)**: Senior-level compensation
- **Lead ($110K-$130K)**: Lead/Principal compensation
- **Executive ($130K+)**: Executive compensation

**Aggregations:**
- `total_employees`: Count per band
- `avg_salary`: Average salary in band
- `avg_experience_years`: Average experience in band

**Business Use Cases:**
- Compensation structure analysis
- Pay grade distribution
- Budget forecasting
- Market competitiveness assessment

**Sample Output:**
```csv
salary_band,total_employees,avg_salary,avg_experience_years
Senior ($90-110K),10,98500,8.5
Mid ($70-90K),12,82000,6.2
Lead ($110-130K),5,118000,14.5
```

---

### 7. **Department-Role Matrix** (`department_role_matrix.csv`)
Shows distribution of roles across departments.

**Fields:**
- `department`: Department name
- `role`: Role/job title
- `employee_count`: Number of employees
- `avg_salary`: Average salary for this dept-role combo

**Business Use Cases:**
- Organizational structure analysis
- Span of control assessment
- Role standardization initiatives
- Departmental role planning

**Sample Output:**
```csv
department,role,employee_count,avg_salary
Engineering,Senior Data Engineer,3,95000
Engineering,DevOps Engineer,2,88000
Data Science,Data Scientist,4,90000
```

---

### 8. **AI/ML Features** (`ai_ml_features.csv`)
Generates machine learning-ready features for predictive HR analytics.

**Generated Features:**

1. **salary_to_experience_ratio**
   - Formula: `salary / (experience_years + 1)`
   - Use: Identify over/under-compensated employees

2. **age_to_experience_ratio**
   - Formula: `age / (experience_years + 1)`
   - Use: Career progression speed indicator

3. **is_high_performer** (binary flag)
   - Formula: `1 if salary >= 75th percentile, else 0`
   - Use: High performer identification

4. **tenure_category**
   - Categories: New, Established, Experienced, Veteran
   - Use: Retention risk modeling

5. **salary_percentile**
   - Formula: Percentile rank of salary (0-100)
   - Use: Compensation benchmarking

6. **experience_percentile**
   - Formula: Percentile rank of experience (0-100)
   - Use: Experience distribution analysis

7. **years_to_retirement**
   - Formula: `65 - age`
   - Use: Succession planning, knowledge transfer

8. **is_mid_career** (binary flag)
   - Formula: `1 if age between 35-50, else 0`
   - Use: Career stage analysis

**AI/ML Use Cases:**
- Attrition prediction models
- Promotion readiness scoring
- Compensation optimization
- Talent segmentation
- Career path recommendation engines

**Sample Output:**
```csv
id,name,salary_to_experience_ratio,is_high_performer,salary_percentile,experience_percentile,...
1,John Smith,11875.00,1,68.5,55.2,...
```

---

### 9. **Executive Summary** (`executive_summary.txt`)
High-level text report for C-suite executives.

**Contents:**
- Workforce Overview (total employees, departments, roles, locations)
- Compensation Metrics (avg/median/min/max salary, total payroll)
- Demographics (avg age, avg experience, age range)
- Key Insights (largest dept, highest paid dept)

**Business Use Cases:**
- Board presentations
- Quarterly business reviews
- Investor relations
- Strategic planning

**Sample Output:**
```
================================================================================
EXECUTIVE SUMMARY - AI EMPLOYEE VAULT
================================================================================

WORKFORCE OVERVIEW
--------------------------------------------------------------------------------
Total Employees:           30
Total Departments:         5
Total Roles:               22
Total Office Locations:    6

COMPENSATION METRICS
--------------------------------------------------------------------------------
Average Salary:            $86,500.00
Median Salary:             $85,000.00
Min Salary:                $58,000
Max Salary:                $145,000
Total Annual Payroll:      $2,595,000

DEMOGRAPHICS
--------------------------------------------------------------------------------
Average Age:               33.5 years
Average Experience:        8.2 years
Youngest Employee:         25 years
Oldest Employee:           45 years

KEY INSIGHTS
--------------------------------------------------------------------------------
Largest Department:        Engineering
Highest Paid Department:   Engineering
```

---

## Aggregation Script

### Script: `generate_gold_data.py`

**Location:** `Gold/scripts/generate_gold_data.py`

**Features:**
- ✅ Class-based architecture (`GoldAggregation`)
- ✅ Comprehensive logging (file + console)
- ✅ 9 distinct aggregation datasets generated
- ✅ Statistical tracking and summary reporting
- ✅ Error handling with detailed messages
- ✅ Type hints for code clarity
- ✅ Configurable input/output paths

### How to Run

#### Option 1: From Gold/scripts/ directory
```bash
cd Gold/scripts
python generate_gold_data.py
```

#### Option 2: From project root
```bash
python Gold/scripts/generate_gold_data.py
```

#### Option 3: As executable (Unix/Linux/Mac)
```bash
cd Gold/scripts
./generate_gold_data.py
```

### What the Script Does

#### **Pipeline Overview**

```
Silver/data/clean/employees_clean.csv
    ↓
    ├─→ Department Metrics        → department_metrics.csv
    ├─→ Role Metrics              → role_metrics.csv
    ├─→ City Metrics              → city_metrics.csv
    ├─→ Top 5 Earners             → top_5_earners.csv
    ├─→ Experience Bands          → experience_bands.csv
    ├─→ Salary Bands              → salary_bands.csv
    ├─→ Department-Role Matrix    → department_role_matrix.csv
    ├─→ AI/ML Features            → ai_ml_features.csv
    └─→ Executive Summary         → executive_summary.txt
```

#### **Step-by-Step Execution**

**Step 1: Read Silver Data**
```python
def read_silver_data(self, filename: str = "employees_clean.csv") -> pd.DataFrame
```
- Reads cleaned data from Silver layer
- Validates file existence
- Logs total employees, departments, roles

**Step 2: Aggregate Department Metrics**
```python
def aggregate_department_metrics(self, df: pd.DataFrame) -> pd.DataFrame
```
- Groups by department
- Calculates count, avg/min/max salary, payroll, avg age/experience
- Sorts by total payroll (descending)

**Step 3: Aggregate Role Metrics**
```python
def aggregate_role_metrics(self, df: pd.DataFrame) -> pd.DataFrame
```
- Groups by role
- Calculates count, avg salary, avg experience, avg age
- Sorts by avg salary (descending)

**Step 4: Aggregate City Metrics**
```python
def aggregate_city_metrics(self, df: pd.DataFrame) -> pd.DataFrame
```
- Groups by city
- Calculates count, avg salary, total payroll, department diversity
- Sorts by employee count (descending)

**Step 5: Generate Top Earners**
```python
def generate_top_earners(self, df: pd.DataFrame, n: int = 5) -> pd.DataFrame
```
- Identifies top 5 highest paid employees
- Adds rank column
- Includes name, role, department, salary, experience, city

**Step 6: Generate Experience Bands**
```python
def generate_experience_bands(self, df: pd.DataFrame) -> pd.DataFrame
```
- Categorizes employees into 5 experience bands
- Aggregates count, avg salary, avg age per band

**Step 7: Generate Salary Bands**
```python
def generate_salary_bands(self, df: pd.DataFrame) -> pd.DataFrame
```
- Categorizes employees into 5 salary bands
- Aggregates count, avg salary, avg experience per band

**Step 8: Generate Department-Role Matrix**
```python
def generate_department_role_matrix(self, df: pd.DataFrame) -> pd.DataFrame
```
- Creates dept-role combinations with counts and avg salary
- Useful for org structure analysis

**Step 9: Generate AI/ML Features**
```python
def generate_ai_features(self, df: pd.DataFrame) -> pd.DataFrame
```
- Adds 8 calculated features for machine learning
- Includes ratios, flags, percentiles, categories

**Step 10: Generate Executive Summary**
```python
def generate_executive_summary(self, df: pd.DataFrame) -> Dict
```
- Creates high-level text report
- Includes workforce, compensation, demographics, insights

**Step 11: Save All Datasets**
- Saves each dataset to Gold/data/gold/
- Logs file size and row/column counts

**Step 12: Print Summary**
- Displays aggregation statistics
- Shows datasets generated count

---

## Example Output

### Console Output
```
================================================================================
🚀 GOLD LAYER AGGREGATION STARTED
================================================================================

2026-02-10 16:00:00 - INFO - 📥 Reading Silver data from: employees_clean.csv
2026-02-10 16:00:00 - INFO -    ✓ Loaded 30 employees
2026-02-10 16:00:00 - INFO -    ✓ Departments: 5
2026-02-10 16:00:00 - INFO -    ✓ Roles: 22

2026-02-10 16:00:00 - INFO - 📊 Aggregating department metrics...
2026-02-10 16:00:00 - INFO -    ✓ Generated metrics for 5 departments

2026-02-10 16:00:00 - INFO - 📊 Aggregating role metrics...
2026-02-10 16:00:00 - INFO -    ✓ Generated metrics for 22 roles

2026-02-10 16:00:00 - INFO - 📊 Aggregating city metrics...
2026-02-10 16:00:00 - INFO -    ✓ Generated metrics for 6 cities

2026-02-10 16:00:00 - INFO - 📊 Generating top 5 highest paid employees...
2026-02-10 16:00:00 - INFO -    ✓ Top earner: Justin Baker ($145,000)

2026-02-10 16:00:00 - INFO - 📊 Generating experience band analysis...
2026-02-10 16:00:00 - INFO -    ✓ Generated 5 experience bands

2026-02-10 16:00:00 - INFO - 📊 Generating salary band analysis...
2026-02-10 16:00:00 - INFO -    ✓ Generated 5 salary bands

2026-02-10 16:00:00 - INFO - 📊 Generating department-role matrix...
2026-02-10 16:00:00 - INFO -    ✓ Generated matrix with 25 department-role combinations

2026-02-10 16:00:00 - INFO - 🤖 Generating AI/ML-ready features...
2026-02-10 16:00:00 - INFO -    ✓ Generated 8 AI/ML features
2026-02-10 16:00:00 - INFO -    ✓ High performers: 8 employees

2026-02-10 16:00:00 - INFO - 📋 Generating executive summary...
2026-02-10 16:00:00 - INFO -    ✓ Total Employees: 30
2026-02-10 16:00:00 - INFO -    ✓ Average Salary: $86,500.00
2026-02-10 16:00:00 - INFO -    ✓ Total Payroll: $2,595,000

2026-02-10 16:00:00 - INFO - 💾 Saving dataset: department_metrics.csv
2026-02-10 16:00:00 - INFO -    ✓ Saved 5 rows, 8 columns
... (8 more datasets saved)

================================================================================
GOLD LAYER AGGREGATION SUMMARY
================================================================================
Source: Silver layer (cleaned data)
Total Employees Processed:  30
Total Departments:          5
Total Roles:                22
Datasets Generated:         9
================================================================================

✨ GOLD LAYER AGGREGATION COMPLETED SUCCESSFULLY
```

---

## Logging

### Log Files
Location: `Gold/logs/gold_aggregation_YYYYMMDD_HHMMSS.log`

Each aggregation run creates a timestamped log file containing:
- Detailed step-by-step execution trace
- Aggregation statistics
- File save operations
- Dataset dimensions (rows × columns)
- Error messages and stack traces

### Viewing Logs
```bash
# View latest log
cd Gold/logs
ls -lt | head -2
cat gold_aggregation_YYYYMMDD_HHMMSS.log

# Search for specific aggregations
grep "Generated" gold_aggregation_*.log
```

---

## Best Practices Implemented

### 1. **Business-Focused Aggregations**
- All aggregations serve specific business use cases
- Metrics aligned with HR, finance, and executive needs
- Clear documentation of business value

### 2. **AI/ML-Ready Features**
- Engineered features for predictive modeling
- Normalized and scaled values
- Binary flags for classification tasks
- Percentiles for ranking and comparison

### 3. **Comprehensive Logging**
- Dual output (console + file)
- Timestamped execution traces
- Statistical summaries
- Audit trail for governance

### 4. **Type Safety**
- Type hints on all functions
- Explicit data type handling
- Pandas dtype management

### 5. **Modular Design**
- Each aggregation is a separate method
- Easy to add new aggregations
- Independent and testable functions

### 6. **Error Handling**
- Try-except blocks around file operations
- Graceful failure with informative messages
- Stack traces logged for debugging

### 7. **No Upstream Modifications**
- Silver layer data is read-only
- Bronze layer untouched
- Gold is purely additive

---

## Gold Layer Principles

✅ **DO:**
- Apply business logic and aggregations
- Create multiple views of the data
- Generate AI/ML-ready features
- Produce executive reports
- Optimize for analytics queries
- Document business value of each dataset

❌ **DON'T:**
- Modify Silver or Bronze data
- Perform additional cleaning (that's Silver's job)
- Store raw individual records (use Silver for that)
- Create overly complex aggregations without business justification

---

## Use Cases by Stakeholder

### **HR Department**
- Department metrics for headcount planning
- Role metrics for job leveling
- Experience bands for career development
- Top earners for retention focus

### **Finance Department**
- Department metrics for budget allocation
- Salary bands for compensation planning
- Total payroll tracking
- City metrics for cost center analysis

### **Executive Leadership**
- Executive summary for board presentations
- Department metrics for strategic planning
- City metrics for expansion decisions
- Top earners for succession planning

### **Data Science/AI Team**
- AI/ML features for predictive models
- Attrition prediction
- Promotion readiness scoring
- Compensation optimization algorithms

### **Operations**
- Department-role matrix for org design
- City metrics for facility planning
- Experience bands for training programs

---

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

---

## Extending the Gold Layer

### Adding New Aggregations

1. **Add a new aggregation method** to `GoldAggregation` class:
```python
def aggregate_custom_metric(self, df: pd.DataFrame) -> pd.DataFrame:
    """Your custom aggregation logic"""
    result = df.groupby('custom_field').agg({'metric': 'sum'})
    return result
```

2. **Call it in the pipeline**:
```python
def aggregate(self, input_filename: str = "employees_clean.csv"):
    # ... existing code ...
    custom_data = self.aggregate_custom_metric(df)
    self.save_dataset(custom_data, "custom_metrics.csv")
```

3. **Document the business value** in README

---

## Testing

### Verify Output
```bash
# Run aggregation
python Gold/scripts/generate_gold_data.py

# Check all outputs exist
ls -lh Gold/data/gold/

# View department metrics
cat Gold/data/gold/department_metrics.csv

# View executive summary
cat Gold/data/gold/executive_summary.txt

# Check logs
tail -100 Gold/logs/gold_aggregation_*.log
```

### Data Quality Checks
```bash
# Ensure no duplicate departments
cat Gold/data/gold/department_metrics.csv | cut -d',' -f1 | sort | uniq -d

# Verify row counts make sense
wc -l Gold/data/gold/*.csv
```

---

## Performance

### Benchmarks on 30-row dataset
- Execution time: < 2 seconds
- Memory usage: < 100 MB
- 9 datasets generated

### Scaling Considerations

| Source Dataset | Expected Time | Memory | Recommendation |
|----------------|---------------|--------|----------------|
| 100 rows | < 2 sec | 100 MB | Current script |
| 10K rows | < 5 sec | 200 MB | Current script |
| 1M rows | ~20 sec | 3 GB | Current script |
| 100M rows | ~10 min | 50 GB | Use Spark/Dask |

---

## Data Lineage

```
Bronze/data/raw/employees.csv (Raw)
    ↓ (Cleaning, Validation)
Silver/data/clean/employees_clean.csv (Clean)
    ↓ (Aggregation, Business Logic)
Gold/data/gold/ (Analytics-Ready)
    ├─ department_metrics.csv
    ├─ role_metrics.csv
    ├─ city_metrics.csv
    ├─ top_5_earners.csv
    ├─ experience_bands.csv
    ├─ salary_bands.csv
    ├─ department_role_matrix.csv
    ├─ ai_ml_features.csv
    └─ executive_summary.txt
```

---

## Next Steps

1. **Run the Aggregation**
   ```bash
   cd Gold
   pip install -r requirements.txt
   python scripts/generate_gold_data.py
   ```

2. **Consume the Data**
   - Import Gold datasets into BI tools (Tableau, Power BI)
   - Use AI/ML features for predictive models
   - Share executive summary with leadership
   - Build dashboards on department/role metrics

3. **Future Enhancements**
   - Add time-series analysis (if historical data available)
   - Create visualization scripts (matplotlib, seaborn)
   - Build REST APIs to serve Gold data
   - Implement incremental updates (not full refresh)

---

**Data Engineering Team**
AI Employee Vault Project
Gold Layer Complete
Date: 2026-02-10
