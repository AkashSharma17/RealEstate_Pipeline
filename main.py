"""
Main execution entry point for the RealEstate Data Analysis Pipeline.

Pipeline flow:
    1. Initialize logger
    2. Load raw data
    3. Clean and preprocess data
    4. Engineer new features
    5. Perform statistical analysis
    6. Generate visualizations
    7. Extract business insights
"""

import logging
import sys
from pathlib import Path

# Add project root to Python path (for imports)
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.logger import LoggerSetup
from src.loader import DataLoader
from src.data_cleaner import DataCleaner
from src.feature_engineering import FeatureEngineering
from src.business_analysis import DataAnalysis
from src.data_visualization import Visualizer
from src.business_insights import BusinessInsights


def main() -> None:
    """
    Run the full RealEstate data analysis pipeline end-to-end.
    """
    try:
        # ========== STEP 1: Initialize Logger ==========
        LoggerSetup.setup_logger()
        logging.info("=" * 70)
        logging.info("REALESTATE PIPELINE - PROJECT STARTED")
        logging.info("=" * 70)

        # ========== STEP 2: Load Data ==========
        logging.info("[STEP 1/7] Loading data...")
        df = DataLoader.load_data()
        if df is None or df.empty:
            logging.error("Data loading failed. Exiting pipeline.")
            return

        # ========== STEP 3: Clean Data ==========
        logging.info("[STEP 2/7] Cleaning data...")
        df = DataCleaner.clean_data(df)
        if df is None or df.empty:
            logging.error("Data cleaning failed. Exiting pipeline.")
            return

        # Save cleaned/processed data so it persists for reuse or auditing
        processed_dir = project_root / "data" / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)
        processed_path = processed_dir / "cleaned_properties.csv"
        df.to_csv(processed_path, index=False)
        logging.info(f"Cleaned data saved to: {processed_path}")

        # ========== STEP 4: Feature Engineering ==========
        logging.info("[STEP 3/7] Engineering features...")
        df = FeatureEngineering.add_price_per_sqft(df)

        # ========== STEP 5: Business Analysis ==========
        logging.info("[STEP 4/7] Performing statistical analysis...")
        DataAnalysis.basic_statistics(df)
        DataAnalysis.city_analysis(df)
        DataAnalysis.bedroom_analysis(df)
        DataAnalysis.bathroom_analysis(df)
        DataAnalysis.price_per_sqft_analysis(df)

        # ========== STEP 6: Create Visualizations ==========
        logging.info("[STEP 5/7] Generating visualizations...")
        Visualizer.price_distribution(df)
        Visualizer.city_wise_average_price(df)
        Visualizer.bedrooms_distribution(df)
        Visualizer.area_vs_price(df)
        Visualizer.boxplot_price(df)

        # ========== STEP 7: Extract Business Insights ==========
        logging.info("[STEP 6/7] Extracting business insights...")
        BusinessInsights.expensive_city(df)
        BusinessInsights.affordable_city(df)
        BusinessInsights.top_expensive_properties(df)
        BusinessInsights.cheapest_properties(df)

        # ========== Final Summary ==========
        logging.info("[STEP 7/7] Pipeline execution completed")
        logging.info("=" * 70)
        logging.info("PROJECT COMPLETED SUCCESSFULLY")
        logging.info("=" * 70)
        logging.info("Check 'logs/' folder for detailed logs")
        logging.info("Check 'output/visualizations/' folder for plots")
        logging.info("=" * 70)

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        logging.error("Please check data file path in src/loader.py")
        raise
    except KeyError as e:
        logging.error(f"Required column missing: {e}")
        logging.error("Check if data file has all expected columns")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in pipeline: {e}")
        logging.error("Pipeline execution failed")
        raise


if __name__ == "__main__":
    main()