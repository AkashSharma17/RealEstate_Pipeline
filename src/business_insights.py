"""
Business insights module for the RealEstate Pipeline.

Extracts actionable, ranked insights from the cleaned dataset: most/least
expensive markets and the top/bottom priced individual properties.
"""

import logging

import pandas as pd

from src.utils import format_money, format_number


class BusinessInsights:
    """
    Strategic insight extraction utilities for the real estate dataset.
    """

    @staticmethod
    def expensive_city(df: pd.DataFrame) -> None:
        """
        Log cities ranked by average price, highest first.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing 'City' and 'Price' columns.
        """
        try:
            logging.info("Analyzing most expensive cities")

            required_cols = ["City", "Price"]
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise KeyError(f"Required columns missing: {missing_cols}")

            city_price = (
                df.groupby("City")["Price"]
                .agg(["mean", "median", "count"])
                .sort_values("mean", ascending=False)
                .round(2)
            )

            if len(city_price) == 0:
                raise ValueError("No city data available for analysis")

            logging.info("=" * 70)
            logging.info("MOST EXPENSIVE CITIES (Ranked by Average Price)")
            logging.info("=" * 70)

            for rank, (city, row) in enumerate(city_price.iterrows(), 1):
                logging.info(
                    f"{rank}. {city:20s} | Avg: {format_money(row['mean']):>10s} | "
                    f"Median: {format_money(row['median']):>10s} | Count: {int(row['count']):>3d}"
                )

            logging.info("=" * 70)
            logging.info("Expensive city analysis completed")

        except KeyError as e:
            logging.error(f"Missing required columns: {e}")
            raise
        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error in expensive_city analysis: {e}")
            raise

    @staticmethod
    def affordable_city(df: pd.DataFrame) -> None:
        """
        Log cities ranked by average price, lowest first.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing 'City' and 'Price' columns.
        """
        try:
            logging.info("Analyzing most affordable cities")

            required_cols = ["City", "Price"]
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise KeyError(f"Required columns missing: {missing_cols}")

            city_price = (
                df.groupby("City")["Price"]
                .agg(["mean", "median", "count"])
                .sort_values("mean")
                .round(2)
            )

            if len(city_price) == 0:
                raise ValueError("No city data available for analysis")

            logging.info("=" * 70)
            logging.info("MOST AFFORDABLE CITIES (Ranked by Average Price)")
            logging.info("=" * 70)

            for rank, (city, row) in enumerate(city_price.iterrows(), 1):
                logging.info(
                    f"{rank}. {city:20s} | Avg: {format_money(row['mean']):>10s} | "
                    f"Median: {format_money(row['median']):>10s} | Count: {int(row['count']):>3d}"
                )

            logging.info("=" * 70)
            logging.info("Affordable city analysis completed")

        except KeyError as e:
            logging.error(f"Missing required columns: {e}")
            raise
        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error in affordable_city analysis: {e}")
            raise

    @staticmethod
    def _log_property_list(df: pd.DataFrame, title: str) -> None:
        """
        Shared helper to log a ranked list of property records.

        Parameters
        ----------
        df : pd.DataFrame
            Subset of properties to display (already sorted/limited).
        title : str
            Section title for the log output.
        """
        logging.info("=" * 90)
        logging.info(title)
        logging.info("=" * 90)

        for idx, (_, row) in enumerate(df.iterrows(), 1):
            city = row.get("City", "N/A")
            price = row.get("Price", 0)
            bedrooms = row.get("Bedrooms", "N/A")
            bathrooms = row.get("Bathrooms", "N/A")
            area = row.get("Area_Sqft", "N/A")
            price_per_sqft = row.get("Price_Per_Sqft", "N/A")

            logging.info(f"{idx}. PROPERTY DETAILS:")
            logging.info(f"   City: {city}")
            logging.info(f"   Price: {format_money(price) if isinstance(price, (int, float)) else price}")
            logging.info(f"   Bedrooms: {bedrooms} | Bathrooms: {bathrooms}")
            area_str = f"{format_number(area)} Sqft" if isinstance(area, (int, float)) else f"{area} Sqft"
            logging.info(f"   Area: {area_str}")
            if isinstance(price_per_sqft, (int, float)):
                logging.info(f"   Price Per Sqft: {format_money(price_per_sqft)}")

        logging.info("=" * 90)

    @staticmethod
    def top_expensive_properties(df: pd.DataFrame) -> None:
        """
        Log the top 5 most expensive properties in the dataset.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing 'Price' and related columns.
        """
        try:
            logging.info("Finding top expensive properties")

            if "Price" not in df.columns:
                raise KeyError("Price column not found")

            top_expensive = df.sort_values(by="Price", ascending=False).head(5).reset_index(drop=True)

            if len(top_expensive) == 0:
                raise ValueError("No property data available")

            BusinessInsights._log_property_list(top_expensive, "TOP 5 MOST EXPENSIVE PROPERTIES")
            logging.info("Top expensive properties analysis completed")

        except KeyError as e:
            logging.error(f"Missing required column: {e}")
            raise
        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error in top_expensive_properties analysis: {e}")
            raise

    @staticmethod
    def cheapest_properties(df: pd.DataFrame) -> None:
        """
        Log the top 5 cheapest properties in the dataset.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing 'Price' and related columns.
        """
        try:
            logging.info("Finding cheapest properties")

            if "Price" not in df.columns:
                raise KeyError("Price column not found")

            cheapest = df.sort_values(by="Price").head(5).reset_index(drop=True)

            if len(cheapest) == 0:
                raise ValueError("No property data available")

            BusinessInsights._log_property_list(cheapest, "TOP 5 CHEAPEST PROPERTIES")
            logging.info("Cheapest properties analysis completed")

        except KeyError as e:
            logging.error(f"Missing required column: {e}")
            raise
        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error in cheapest_properties analysis: {e}")
            raise