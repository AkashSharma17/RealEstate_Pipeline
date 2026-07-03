"""
Feature engineering module for the RealEstate Pipeline.

Creates derived features from existing columns to enhance analytical
capabilities and support downstream business analysis.
"""

import logging

import pandas as pd


class FeatureEngineering:
    """
    Builds new derived features on top of the cleaned real estate dataset.
    """

    @staticmethod
    def add_price_per_sqft(df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a ``Price_Per_Sqft`` feature representing property value density.

        This helps identify overpriced or underpriced properties relative
        to market norms.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing 'Price' and 'Area_Sqft' columns.

        Returns
        -------
        pd.DataFrame
            Dataset with the new 'Price_Per_Sqft' column added.

        Raises
        ------
        KeyError
            If required columns (Price, Area_Sqft) are missing.

        Examples
        --------
        >>> df = FeatureEngineering.add_price_per_sqft(df)
        """
        try:
            # Step 1: Validate required columns exist
            required_columns = ["Price", "Area_Sqft"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise KeyError(f"Required columns missing: {missing_columns}")

            # Step 2: Ensure both columns are numeric
            if not pd.api.types.is_numeric_dtype(df["Price"]):
                df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
            if not pd.api.types.is_numeric_dtype(df["Area_Sqft"]):
                df["Area_Sqft"] = pd.to_numeric(df["Area_Sqft"], errors="coerce")

            # Step 3: Warn on zero/negative area (results in NaN, not a crash)
            invalid_area_count = (df["Area_Sqft"] <= 0).sum()
            if invalid_area_count > 0:
                logging.warning(
                    f"Found {invalid_area_count} records with Area_Sqft <= 0. "
                    "These will result in NaN for Price_Per_Sqft."
                )

            # Step 4: Create the feature
            logging.info("Creating Price_Per_Sqft feature")
            df["Price_Per_Sqft"] = df["Price"] / df["Area_Sqft"]

            # Step 5: Log feature statistics
            logging.info(
                "Price_Per_Sqft feature created successfully - "
                f"Mean: {df['Price_Per_Sqft'].mean():.2f}, "
                f"Median: {df['Price_Per_Sqft'].median():.2f}, "
                f"Std: {df['Price_Per_Sqft'].std():.2f}"
            )

            return df

        except KeyError as e:
            logging.error(f"Required columns missing: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in add_price_per_sqft: {e}")
            raise
