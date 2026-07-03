"""
Data cleaning and preprocessing module for the RealEstate Pipeline.

Handles duplicate removal, text normalization, currency parsing, type
coercion, missing-value imputation, and removal of logically invalid rows.
"""

import logging

import pandas as pd


class DataCleaner:
    """
    Cleans and validates raw real estate data for downstream analysis.
    """

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Execute the full data cleaning pipeline.

        Steps
        -----
        1. Remove duplicate rows.
        2. Strip whitespace from text columns.
        3. Standardize city names to title case.
        4. Convert price from currency format to numeric.
        5. Convert numeric columns to proper dtypes.
        6. Fill missing values using median imputation.
        7. Remove logically invalid records.

        Parameters
        ----------
        df : pd.DataFrame
            Raw input dataset requiring cleaning.

        Returns
        -------
        pd.DataFrame
            Cleaned dataset ready for analysis.

        Examples
        --------
        >>> df_raw = pd.read_csv("data.csv")
        >>> df_clean = DataCleaner.clean_data(df_raw)
        """
        logging.info("Data cleaning pipeline started")
        df_cleaned = df.copy()

        # Step 1: Remove duplicate records
        initial_rows = len(df_cleaned)
        df_cleaned = df_cleaned.drop_duplicates()
        logging.info(f"Duplicate records removed: {initial_rows - len(df_cleaned)}")

        # Step 2 & 3: Clean and standardize City column
        if "City" in df_cleaned.columns:
            df_cleaned["City"] = df_cleaned["City"].astype(str).str.strip().str.title()
            logging.info("City column cleaned and standardized to title case")

        # Step 4: Convert Price currency format to numeric
        if "Price" in df_cleaned.columns:
            df_cleaned["Price"] = (
                df_cleaned["Price"]
                .astype(str)
                .str.replace("$", "", regex=False)
                .str.replace(",", "", regex=False)
            )
            df_cleaned["Price"] = pd.to_numeric(df_cleaned["Price"], errors="coerce")
            logging.info("Price column converted to numeric format")

        # Step 5: Convert numeric columns to proper dtypes
        numeric_columns = ["Bedrooms", "Bathrooms", "Area_Sqft"]
        for col in numeric_columns:
            if col in df_cleaned.columns:
                df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors="coerce")
        logging.info("Numeric columns converted to appropriate data types")

        # Step 6: Impute missing values using median
        for col in ("Bedrooms", "Bathrooms"):
            if col in df_cleaned.columns:
                median_value = df_cleaned[col].median()
                df_cleaned[col] = df_cleaned[col].fillna(median_value)
                logging.info(f"Missing {col} values filled with median: {median_value}")

        # Step 7: Remove logically invalid records
        if "Area_Sqft" in df_cleaned.columns:
            before = len(df_cleaned)
            df_cleaned = df_cleaned[df_cleaned["Area_Sqft"] > 0]
            logging.info(f"Records with invalid Area_Sqft removed: {before - len(df_cleaned)}")

        if "Bedrooms" in df_cleaned.columns:
            before = len(df_cleaned)
            df_cleaned = df_cleaned[df_cleaned["Bedrooms"] >= 0]
            logging.info(f"Records with invalid Bedrooms removed: {before - len(df_cleaned)}")

        if "Price" in df_cleaned.columns:
            before = len(df_cleaned)
            df_cleaned = df_cleaned.dropna(subset=["Price"])
            logging.info(f"Records with missing Price removed: {before - len(df_cleaned)}")

        logging.info("Data cleaning completed successfully")
        logging.info(f"Final dataset shape: {df_cleaned.shape[0]} rows x {df_cleaned.shape[1]} columns")

        return df_cleaned
