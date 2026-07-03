# 🏘️ Real Estate Data Pipeline

A modular, production-style Python pipeline that ingests raw real estate listing data, cleans and enriches it, performs statistical analysis, generates visualizations, and extracts actionable business insights — all with structured logging at every step.

---

## 📌 Overview

This project automates the end-to-end workflow of analyzing a real estate dataset:

**Raw CSV → Clean → Engineer Features → Analyze → Visualize → Extract Insights**

Every stage logs its progress and results to both the console and a persistent log file, making the pipeline easy to debug and audit.

---

## 📁 Project Structure

```
RealEstate_Pipeline/
├── data/
│   ├── raw/
│   │   └── messy_properties.csv     # Source dataset (input)
│   ├── processed/                   # Reserved for processed data output
│   └── cleaned/                     # Reserved for cleaned data output
├── logs/
│   └── RealEstate.log               # Auto-generated run logs
├── output/
│   └── visualizations/              # Auto-generated charts (PNG)
│       ├── 01_price_distribution.png
│       ├── 02_city_wise_average_price.png
│       ├── 03_bedrooms_distribution.png
│       ├── 04_area_vs_price.png
│       └── 05_boxplot_price.png
├── src/
│   ├── loader.py                    # CSV loading & validation
│   ├── data_cleaner.py              # Cleaning & preprocessing
│   ├── feature_engineering.py       # Derived feature creation
│   ├── business_analysis.py         # Statistical analysis
│   ├── business_insights.py         # Business intelligence extraction
│   ├── data_visualization.py        # Chart generation
│   └── logger.py                    # Centralized logging setup
├── main.py                          # Pipeline orchestrator / entry point
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd RealEstate_Pipeline
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your dataset**

Place your raw CSV file at:
```
data/raw/messy_properties.csv
```

> Expected columns: `City`, `Price`, `Bedrooms`, `Bathrooms`, `Area_Sqft`

---

## ▶️ Usage

Run the entire pipeline from the project root:

```bash
python main.py
```

### Pipeline Execution Flow

| Step | Module | Description |
|:---:|---|---|
| 1 | `logger.py` | Initializes logging (file + console) |
| 2 | `loader.py` | Loads raw CSV data, skips malformed rows |
| 3 | `data_cleaner.py` | Removes duplicates, standardizes text, fixes types, imputes missing values, filters invalid records |
| 4 | `feature_engineering.py` | Adds `Price_Per_Sqft` feature |
| 5 | `business_analysis.py` | Runs basic, city-wise, bedroom, bathroom, and price-per-sqft statistics |
| 6 | `data_visualization.py` | Generates 5 charts (distribution, city comparison, bedrooms, scatter, boxplot) |
| 7 | `business_insights.py` | Extracts expensive/affordable cities, top & cheapest properties |

All results are logged to `logs/RealEstate.log` and charts are saved to `output/visualizations/`.

---

## 🧩 Module Reference

### `loader.py` — `DataLoader`
Loads the raw CSV using `pandas.read_csv()` with `on_bad_lines='skip'`. Auto-detects the project root by locating the `data/` folder, so it works regardless of where the script is invoked from. Returns `None` on failure instead of raising, allowing `main.py` to handle it gracefully.

### `data_cleaner.py` — `DataCleaner`
Cleaning steps applied in sequence:
1. Drop duplicate rows
2. Strip whitespace & title-case city names
3. Convert `Price` from currency string (`$`, `,`) to numeric
4. Convert `Bedrooms`, `Bathrooms`, `Area_Sqft` to numeric
5. Impute missing `Bedrooms`/`Bathrooms` with median
6. Drop rows with `Area_Sqft <= 0`, negative `Bedrooms`, or missing `Price`

### `feature_engineering.py` — `FeatureEngineering`
Adds a `Price_Per_Sqft` column (`Price / Area_Sqft`), with validation for non-numeric and zero/negative area values.

### `business_analysis.py` — `DataAnalysis`
Computes and logs:
- Overall price/area statistics (mean, median, std, min, max)
- City-wise property counts & pricing
- Bedroom/bathroom distributions
- Price-per-sqft breakdown by city

### `business_insights.py` — `BusinessInsights`
Extracts:
- Most expensive & most affordable cities (ranked)
- Top 5 most expensive properties
- Top 5 cheapest properties

### `data_visualization.py` — `Visualizer`
Generates and saves 5 charts to `output/visualizations/` using `matplotlib` + `seaborn`:
- Price distribution (histogram + KDE)
- Average price by city (bar chart)
- Bedroom distribution (count plot)
- Area vs. price (scatter plot)
- Price distribution (box plot)

### `logger.py` — `LoggerSetup`
Configures a root logger with both a `FileHandler` (`logs/RealEstate.log`) and a `StreamHandler` (console), using UTF-8 encoding and clearing existing handlers to avoid duplicate logs on re-runs (e.g., in Jupyter).

---

## 📦 Requirements

```
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

---

## 🛡️ Error Handling

Every module uses targeted exception handling (`KeyError`, `ValueError`, `FileNotFoundError`, generic `Exception`) with descriptive log messages, so failures at any stage clearly indicate which step and which column/data issue caused them.

---

## 📝 Notes

- `data/raw/`, `data/processed/`, `data/cleaned/`, `logs/`, and `output/visualizations/` are excluded from version control via `.gitignore` — only folder structure is preserved using `.gitkeep` files.
- The cleaning step currently returns an in-memory DataFrame; it does not persist cleaned data to `data/processed/` or `data/cleaned/` unless explicitly extended to do so.

---

## 📄 License

Add your preferred license here (MIT, Apache 2.0, etc.)
