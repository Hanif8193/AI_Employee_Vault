# Gold Layer - Aggregation Logic Explained

## Overview
This document provides detailed explanations of all business aggregations and AI/ML features generated in the Gold layer.

---

## Aggregation Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SILVER LAYER (Clean Data)                        │
│              Silver/data/clean/employees_clean.csv                  │
│                                                                     │
│  • 30 employee records (example)                                    │
│  • 8 columns: id, name, age, dept, role, salary, experience, city  │
│  • Validated, deduplicated, no missing values                      │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ READ
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        AGGREGATION ENGINE                           │
│                   (generate_gold_data.py)                           │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
        ┌───────────────────────┐   ┌───────────────────────┐
        │  DEPARTMENT METRICS   │   │    ROLE METRICS       │
        │  (Group by dept)      │   │    (Group by role)    │
        │                       │   │                       │
        │  • Total employees    │   │  • Total employees    │
        │  • Avg/Min/Max salary │   │  • Avg salary         │
        │  • Total payroll      │   │  • Avg experience     │
        │  • Avg age/experience │   │  • Avg age            │
        └───────────────────────┘   └───────────────────────┘
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
        ┌───────────────────────┐   ┌───────────────────────┐
        │    CITY METRICS       │   │   TOP 5 EARNERS       │
        │  (Group by city)      │   │  (Sort by salary)     │
        │                       │   │                       │
        │  • Total employees    │   │  • Rank 1-5           │
        │  • Avg salary         │   │  • Name, role, dept   │
        │  • Total payroll      │   │  • Salary, experience │
        │  • Dept diversity     │   │  • City               │
        └───────────────────────┘   └───────────────────────┘
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
        ┌───────────────────────┐   ┌───────────────────────┐
        │  EXPERIENCE BANDS     │   │   SALARY BANDS        │
        │  (Categorize exp)     │   │  (Categorize salary)  │
        │                       │   │                       │
        │  • Entry (0-2yr)      │   │  • Entry ($50-70K)    │
        │  • Junior (3-5yr)     │   │  • Mid ($70-90K)      │
        │  • Mid (6-10yr)       │   │  • Senior ($90-110K)  │
        │  • Senior (11-15yr)   │   │  • Lead ($110-130K)   │
        │  • Expert (16+yr)     │   │  • Executive ($130K+) │
        └───────────────────────┘   └───────────────────────┘
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
        ┌───────────────────────┐   ┌───────────────────────┐
        │  DEPT-ROLE MATRIX     │   │  AI/ML FEATURES       │
        │  (Group by dept+role) │   │  (Feature engineer)   │
        │                       │   │                       │
        │  • Emp count per combo│   │  • 8 calculated       │
        │  • Avg salary per     │   │    features           │
        │    dept-role          │   │  • Ratios, flags      │
        │                       │   │  • Percentiles        │
        └───────────────────────┘   └───────────────────────┘
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │   EXECUTIVE SUMMARY       │
                    │   (High-level stats)      │
                    │                           │
                    │  • Workforce overview     │
                    │  • Compensation metrics   │
                    │  • Demographics           │
                    │  • Key insights           │
                    └───────────────────────────┘
                                  │
                                  │ SAVE
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     GOLD LAYER (Analytics-Ready)                    │
│                      Gold/data/gold/                                │
│                                                                     │
│  • 9 distinct datasets (8 CSV + 1 TXT)                             │
│  • Business-ready aggregations                                      │
│  • AI/ML-ready features                                             │
│  • Executive reports                                                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Aggregation Examples

### 1. Department Metrics

#### Input (Silver - Sample)
```csv
id,name,age,department,role,salary,experience_years,city
1,John Smith,35,Engineering,Senior Data Engineer,95000,8,San Francisco
2,Maria Garcia,28,Engineering,ML Engineer,85000,4,New York
3,James Wilson,42,HR,HR Manager,75000,15,Chicago
4,Emily Chen,31,Data Science,Data Scientist,90000,6,Austin
5,Michael Brown,39,Engineering,DevOps Engineer,88000,10,Seattle
```

#### Processing
```python
df.groupby('department').agg({
    'id': 'count',                      # Total employees
    'salary': ['mean', 'min', 'max', 'sum'],  # Salary stats
    'age': 'mean',                      # Average age
    'experience_years': 'mean'          # Average experience
})
```

#### Output (Gold)
```csv
department,total_employees,avg_salary,min_salary,max_salary,total_payroll,avg_age,avg_experience_years,salary_range
Engineering,3,89333.33,85000,95000,268000,34.0,7.33,10000
HR,1,75000,75000,75000,75000,42.0,15.0,0
Data Science,1,90000,90000,90000,90000,31.0,6.0,0
```

#### Business Value
- **Budget Planning**: Total payroll shows exact cost per department
- **Benchmarking**: Compare avg salary across departments
- **Headcount**: Track department sizes for growth planning
- **Pay Equity**: Salary range reveals compensation spread

---

### 2. Role Metrics

#### Processing
```python
df.groupby('role').agg({
    'id': 'count',
    'salary': 'mean',
    'experience_years': 'mean',
    'age': 'mean'
})
```

#### Output (Gold)
```csv
role,total_employees,avg_salary,avg_experience_years,avg_age
Senior Data Engineer,1,95000,8.0,35.0
Data Scientist,1,90000,6.0,31.0
DevOps Engineer,1,88000,10.0,39.0
ML Engineer,1,85000,4.0,28.0
HR Manager,1,75000,15.0,42.0
```

#### Business Value
- **Compensation Planning**: Understand market rates per role
- **Career Pathing**: Show salary progression by role
- **Hiring**: Set competitive salary ranges for open positions
- **Talent Strategy**: Identify high-value roles

---

### 3. Experience Bands

#### Categorization Logic
```python
df['experience_band'] = pd.cut(
    df['experience_years'],
    bins=[0, 2, 5, 10, 15, float('inf')],
    labels=['Entry (0-2yr)', 'Junior (3-5yr)', 'Mid (6-10yr)',
            'Senior (11-15yr)', 'Expert (16+yr)']
)
```

#### Example Transformation
```
Input:
experience_years = [2, 4, 7, 12, 18]

Output:
experience_band = ['Entry', 'Junior', 'Mid', 'Senior', 'Expert']
```

#### Aggregated Output
```csv
experience_band,total_employees,avg_salary,avg_age
Mid (6-10yr),2,92500,33.0
Junior (3-5yr),1,85000,28.0
Senior (11-15yr),1,75000,42.0
Entry (0-2yr),1,88000,39.0
```

#### Business Value
- **Workforce Maturity**: See distribution of experience levels
- **Mentorship**: Match senior with junior employees
- **Training**: Target programs by experience level
- **Succession**: Ensure balanced age/experience distribution

---

### 4. AI/ML Features - Detailed Explanation

#### Feature 1: salary_to_experience_ratio
```python
salary_to_experience_ratio = salary / (experience_years + 1)
```

**Example:**
```
Employee A: salary=$90,000, experience=8 years
  → ratio = 90000 / 9 = 10,000

Employee B: salary=$85,000, experience=4 years
  → ratio = 85000 / 5 = 17,000
```

**Interpretation:**
- **High ratio**: High pay relative to experience (fast track, high performer)
- **Low ratio**: Lower pay relative to experience (undercompensated?)
- **Use case**: Identify compensation outliers for review

---

#### Feature 2: is_high_performer (Binary Flag)
```python
salary_75th_percentile = df['salary'].quantile(0.75)
is_high_performer = 1 if salary >= salary_75th_percentile else 0
```

**Example:**
```
30 employees with salaries:
[58000, 60000, ..., 125000, 145000]

75th percentile = $95,000

Employee A: salary=$95,000 → is_high_performer=1 ✓
Employee B: salary=$85,000 → is_high_performer=0
```

**Use Cases:**
- **Retention**: Focus retention efforts on high performers
- **Promotion**: High performers are promotion candidates
- **ML Models**: Use as a target variable for prediction

---

#### Feature 3: salary_percentile
```python
salary_percentile = df['salary'].rank(pct=True) * 100
```

**Example:**
```
Employee salaries ranked:
1. $145,000 → percentile=100.0 (highest)
2. $125,000 → percentile=96.7
3. $115,000 → percentile=93.3
...
30. $58,000 → percentile=3.3 (lowest)
```

**Use Cases:**
- **Benchmarking**: "You're in the 80th percentile of salary"
- **Compensation Reviews**: Identify employees below 25th percentile
- **Market Analysis**: Compare internal vs external percentiles

---

#### Feature 4: tenure_category
```python
tenure_category = pd.cut(
    experience_years,
    bins=[0, 3, 7, 15, inf],
    labels=['New', 'Established', 'Experienced', 'Veteran']
)
```

**Example:**
```
experience_years = 2  → 'New'
experience_years = 5  → 'Established'
experience_years = 10 → 'Experienced'
experience_years = 18 → 'Veteran'
```

**Use Cases:**
- **Retention Models**: "New" employees have higher attrition risk
- **Training**: Different programs for each tenure category
- **Career Planning**: Track progression through categories

---

#### Feature 5: years_to_retirement
```python
years_to_retirement = 65 - age
```

**Example:**
```
Employee A: age=35 → years_to_retirement=30
Employee B: age=62 → years_to_retirement=3 (succession risk!)
```

**Use Cases:**
- **Succession Planning**: Identify retirement risks
- **Knowledge Transfer**: Plan mentorship before retirement
- **Workforce Planning**: Forecast future hiring needs

---

#### Feature 6: is_mid_career (Binary Flag)
```python
is_mid_career = 1 if (age >= 35 and age <= 50) else 0
```

**Example:**
```
age=30 → is_mid_career=0 (early career)
age=42 → is_mid_career=1 (mid career) ✓
age=55 → is_mid_career=0 (late career)
```

**Use Cases:**
- **Career Development**: Mid-career needs different support
- **Retention**: Mid-career often seeks promotion/new challenges
- **Compensation**: Mid-career typically in peak earning years

---

### 5. Department-Role Matrix

#### Input
```csv
department,role
Engineering,Senior Data Engineer
Engineering,ML Engineer
Engineering,DevOps Engineer
Data Science,Data Scientist
HR,HR Manager
```

#### Processing
```python
df.groupby(['department', 'role']).agg({
    'id': 'count',
    'salary': 'mean'
})
```

#### Output
```csv
department,role,employee_count,avg_salary
Engineering,Senior Data Engineer,1,95000
Engineering,DevOps Engineer,1,88000
Engineering,ML Engineer,1,85000
Data Science,Data Scientist,1,90000
HR,HR Manager,1,75000
```

#### Business Value
- **Org Design**: Visualize how roles distribute across departments
- **Span of Control**: Identify departments with too many/few roles
- **Standardization**: Find duplicate role titles to consolidate
- **Budget Allocation**: See cost of specific dept-role combinations

---

### 6. Salary Bands

#### Categorization Logic
```python
df['salary_band'] = pd.cut(
    df['salary'],
    bins=[0, 70000, 90000, 110000, 130000, float('inf')],
    labels=['Entry ($50-70K)', 'Mid ($70-90K)', 'Senior ($90-110K)',
            'Lead ($110-130K)', 'Executive ($130K+)']
)
```

#### Visual Distribution
```
Salary Distribution:

Entry ($50-70K):      ████████ (8 employees)
Mid ($70-90K):        ████████████ (12 employees)
Senior ($90-110K):    ██████ (6 employees)
Lead ($110-130K):     ██ (2 employees)
Executive ($130K+):   █ (2 employees)
```

#### Aggregated Output
```csv
salary_band,total_employees,avg_salary,avg_experience_years
Mid ($70-90K),12,82000,6.2
Entry ($50-70K),8,63500,3.5
Senior ($90-110K),6,98000,8.8
Lead ($110-130K),2,118000,14.5
Executive ($130K+),2,137500,16.5
```

#### Business Value
- **Compensation Structure**: Visualize pay grade distribution
- **Budget Forecasting**: Estimate costs for each salary band
- **Market Competitiveness**: Compare bands to industry benchmarks
- **Promotion Planning**: See gaps in compensation ladder

---

### 7. Top 5 Earners

#### Processing
```python
df.nlargest(5, 'salary')[
    ['name', 'role', 'department', 'salary', 'experience_years', 'city']
]
```

#### Output
```csv
rank,name,role,department,salary,experience_years,city
1,Justin Baker,VP of Engineering,Engineering,145000,17,San Francisco
2,Kevin Young,Principal Engineer,Engineering,125000,16,San Francisco
3,Daniel Thompson,Engineering Manager,Engineering,115000,14,San Francisco
4,Jennifer Martinez,AI Research Scientist,Data Science,105000,9,San Francisco
5,Matthew Lewis,Cloud Architect,Engineering,102000,12,Seattle
```

#### Business Value
- **Retention Risk**: Focus on keeping highest paid talent
- **Compensation Review**: Ensure top earners are justified
- **Succession Planning**: Identify critical roles for backup
- **Pay Equity**: Check if top earners reflect diversity goals

---

### 8. City Metrics

#### Processing
```python
df.groupby('city').agg({
    'id': 'count',
    'salary': ['mean', 'sum'],
    'department': 'nunique'
})
```

#### Output
```csv
city,total_employees,avg_salary,total_payroll,department_diversity
San Francisco,7,108571,760000,4
New York,5,84000,420000,4
Chicago,4,78250,313000,3
Seattle,4,90500,362000,3
Austin,4,80750,323000,4
Boston,2,73000,146000,2
```

#### Business Value
- **Real Estate**: Decide which offices to expand/close
- **Cost Analysis**: Compare cost of living vs compensation
- **Diversity**: Ensure departments represented in all major cities
- **Remote Work**: Identify cities with high concentration

---

## Aggregation Statistics

### Dimensionality Reduction

| Metric | Silver (Input) | Gold (Output) |
|--------|----------------|---------------|
| **Total Rows** | 30 employees | 5 departments (dept metrics) |
| **Granularity** | Individual | Aggregated |
| **Use Case** | Detailed analysis | Executive reporting |

**Example:**
```
Silver: 30 rows × 8 columns = 240 data points
Gold (dept_metrics): 5 rows × 8 columns = 40 data points

Reduction: 83% fewer data points, same insights!
```

### Data Multiplication for Features

| Dataset | Silver | Gold AI Features |
|---------|--------|------------------|
| **Columns** | 8 | 16 (8 original + 8 new) |
| **Rows** | 30 | 30 (same) |
| **Use Case** | Reporting | Machine Learning |

---

## Performance Characteristics

### Aggregation Complexity

| Aggregation | Time Complexity | Space Complexity |
|-------------|-----------------|------------------|
| Group by (dept/role/city) | O(n log n) | O(n) |
| Top N earners | O(n log k) | O(k) |
| Percentiles | O(n log n) | O(n) |
| Binning (experience/salary) | O(n) | O(n) |

**For 30 rows:** < 1 second total
**For 1M rows:** < 20 seconds total

---

## Error Handling

### Division by Zero Prevention
```python
# Adding 1 to denominator prevents division by zero
salary_to_experience_ratio = salary / (experience_years + 1)

# Example:
# experience=0 → divide by (0+1)=1 ✓
# experience=5 → divide by (5+1)=6 ✓
```

### Empty Group Handling
```python
# Using .mode() with empty check
if not df[col].mode().empty:
    mode_val = df[col].mode()[0]
else:
    mode_val = 'Unknown'
```

---

## Business Logic Validation

### Example: Salary Band Validation
```python
# Ensure bins cover all salary ranges
min_salary = df['salary'].min()  # e.g., $58,000
max_salary = df['salary'].max()  # e.g., $145,000

bins = [0, 70000, 90000, 110000, 130000, float('inf')]
# Covers $0 to $∞ ✓

# Verify no unclassified salaries
assert df['salary_band'].isnull().sum() == 0
```

---

## Testing Aggregations

### Unit Test Example
```python
def test_department_metrics():
    """Test department aggregation correctness"""
    # Sample data
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'department': ['Eng', 'Eng', 'HR'],
        'salary': [90000, 80000, 70000]
    })

    # Aggregate
    result = aggregate_department_metrics(df)

    # Assert
    assert result.loc[result['department']=='Eng', 'total_employees'].values[0] == 2
    assert result.loc[result['department']=='Eng', 'avg_salary'].values[0] == 85000
    assert result.loc[result['department']=='HR', 'total_employees'].values[0] == 1
```

---

**Gold Layer Aggregation Logic**
AI Employee Vault Project
Date: 2026-02-10
