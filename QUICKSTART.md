# 🚀 Quick Start Guide - AI Employee Vault CLI

## Overview
Run your Medallion Architecture pipeline easily from the command line!

---

## Installation

### 1. Install Python Dependencies

```bash
# Install Silver layer dependencies
cd Silver
pip install -r requirements.txt
cd ..

# Install Gold layer dependencies
cd Gold
pip install -r requirements.txt
cd ..
```

---

## Usage

### Run Complete Pipeline (Recommended for First Time)

```bash
python run_pipeline.py --all
```

This will execute:
1. 🥉 **Bronze Layer** - Ingest raw employee data
2. 🥈 **Silver Layer** - Clean and validate data
3. 🥇 **Gold Layer** - Generate analytics and ML features

**Expected output:**
- Bronze: `Bronze/data/raw/employees.csv`
- Silver: `Silver/data/clean/employees_clean.csv`
- Gold: 9 datasets in `Gold/data/gold/`

---

## Individual Layer Commands

### Run Bronze Layer Only
```bash
python run_pipeline.py --bronze
```
Validates and displays raw data schema.

### Run Silver Layer Only
```bash
python run_pipeline.py --silver
```
Cleans Bronze data and saves to Silver layer.

### Run Gold Layer Only
```bash
python run_pipeline.py --gold
```
Aggregates Silver data into analytics datasets.

### Run Multiple Layers in Sequence
```bash
# Run Silver then Gold
python run_pipeline.py --silver --gold

# Run all three layers
python run_pipeline.py --bronze --silver --gold
# (same as --all)
```

---

## Check Pipeline Status

```bash
python run_pipeline.py --status
```

Shows:
- Which layers have been executed
- Output file locations
- File sizes and counts

---

## Examples

### Example 1: Fresh Start (First Time)
```bash
# Run complete pipeline
python run_pipeline.py --all

# Check status
python run_pipeline.py --status
```

### Example 2: Reprocess Silver and Gold Only
```bash
# Bronze data is already good, just reprocess Silver and Gold
python run_pipeline.py --silver --gold
```

### Example 3: Regenerate Gold Analytics Only
```bash
# Silver data is clean, just regenerate Gold aggregations
python run_pipeline.py --gold
```

---

## Output Structure

After running `--all`, you'll have:

```
AI_Employee_Vault/
├── Bronze/data/raw/
│   └── employees.csv                    # 30 employees
├── Silver/data/clean/
│   └── employees_clean.csv              # 30 employees (cleaned)
└── Gold/data/gold/
    ├── department_metrics.csv           # 5 departments
    ├── role_metrics.csv                 # 22 roles
    ├── city_metrics.csv                 # 6 cities
    ├── top_5_earners.csv                # Top 5 employees
    ├── experience_bands.csv             # 5 experience bands
    ├── salary_bands.csv                 # 5 salary bands
    ├── department_role_matrix.csv       # 25 combinations
    ├── ai_ml_features.csv               # 30 employees + ML features
    └── executive_summary.txt            # Executive report
```

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'pandas'"
**Solution:**
```bash
cd Silver
pip install -r requirements.txt
cd ../Gold
pip install -r requirements.txt
```

### Problem: "FileNotFoundError: Bronze file not found"
**Solution:** Run Bronze layer first:
```bash
python run_pipeline.py --bronze
```

### Problem: "Silver file not found"
**Solution:** Run Silver layer before Gold:
```bash
python run_pipeline.py --silver --gold
```

---

## Help Command

```bash
python run_pipeline.py --help
```

Shows all available options and examples.

---

## Expected Execution Time

- **Bronze Layer:** < 1 second
- **Silver Layer:** < 1 second
- **Gold Layer:** < 2 seconds
- **Complete Pipeline:** < 5 seconds

---

## Next Steps

1. ✅ Run the pipeline: `python run_pipeline.py --all`
2. ✅ Verify outputs: `python run_pipeline.py --status`
3. ✅ Explore Gold data: `cd Gold/data/gold && dir` (Windows) or `ls -lh` (Mac/Linux)
4. ✅ Read executive summary: `type Gold\data\gold\executive_summary.txt` (Windows)

---

## Advanced Usage

### Run with Python directly (alternative method)

```bash
# Bronze
cd Bronze/scripts
python ingest_raw_data.py

# Silver
cd ../../Silver/scripts
python transform_bronze_to_silver.py

# Gold
cd ../../Gold/scripts
python generate_gold_data.py
```

---

## Questions?

See the main documentation:
- `MEDALLION_ARCHITECTURE_COMPLETE.md` - Complete architecture guide
- `Bronze/README.md` - Bronze layer details
- `Silver/README.md` - Silver layer details
- `Gold/README.md` - Gold layer details

---

**Happy Data Engineering! 🎉**
