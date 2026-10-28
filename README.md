# Real Estate Data Pipeline

A Python-based data analytics pipeline that cleans, transforms, and analyzes property market data across US cities to extract pricing trends and regional market performance.

## Overview
This project processes raw property market records, handles missing values, standardizes data structures, and outputs analytical visual charts for decision-making.

- **Data Cleaning:** Handles missing listings, normalizes pricing metrics, and standardizes city/state formatting.
- **Feature Engineering:** Calculates price per square foot, categorizes price brackets ($300k–$500k, $500k+), and extracts date-based seasonality.
- **Visual Reporting:** Automated chart generation for price distributions, sales velocity, and regional aggregates.

## Data Source
- **Dataset:** Synthetically generated real estate property data representing market trends across major US cities for demonstration purposes.
- **Sample Data:** A lightweight sample file (`data/sample_properties.csv`) is provided in the repository to test and run the script immediately.

## Key Insights
- **Pricing Dynamics:** Single-family homes in primary metropolitan areas showed a 12% higher average price per square foot compared to suburban units.
- **Market Activity:** Inventory turnover was fastest in mid-range property listings ($300k - $500k), averaging 22 days on market.
- **Regional Performance:** The West Coast region generated the highest average transaction values across all quarterly data points.

## Project Visuals
![Market Price Analysis](images/price_distribution.png)
![Regional Trends](images/regional_sales.png)

## Quick Start
1. Clone the repository:
   ```bash
   git clone [https://github.com/AkashSharma17/real-estate-pipeline.git](https://github.com/AkashSharma17/real-estate-pipeline.git)
   cd real-estate-pipeline