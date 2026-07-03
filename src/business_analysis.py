"""
Statistical analysis module for the RealEstate Pipeline.

Provides dataset-wide and segmented statistics: overall metrics, city-wise
breakdowns, and distributions by bedrooms, bathrooms, and price per sqft.
"""

import logging

import pandas as pd

from src.utils import format_money, format_number


class DataAnalysis:
    """
    Statistical analysis utilities for the cleaned real estate dataset.
    """

    @staticmethod
    def basic_statistics(df: pd.DataFrame) -> None:
        """
        Log fundamental dataset statistics: price and area distributions.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset for analysis.
        """
        try:
            logging.info("Starting basic statistics analysis")

            required_cols = ["Price", "Area_Sqft"]
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise KeyError(f"Required columns missing: {missing_cols}")

            avg_price = df["Price"].mean()
            max_price = df["Price"].max()
            min_price = df["Price"].min()
            median_price = df["Price"].median()
            std_price = df["Price"].std()

            avg_area = df["Area_Sqft"].mean()
            max_area = df["Area_Sqft"].max()
            min_area = df["Area_Sqft"].min()

            logging.info("=" * 60)
            logging.info("BASIC STATISTICS ANALYSIS")
            logging.info("=" * 60)
            logging.info(f"Total Properties: {len(df)}")
            logging.info(
                f"Price - Mean: {format_money(avg_price)} | Median: {format_money(median_price)} | "
                f"Std: {format_money(std_price)}"
            )
            logging.info(f"Price - Max: {format_money(max_price)} | Min: {format_money(min_price)}")
            logging.info(
                f"Area (Sqft) - Mean: {format_number(avg_area)} | Max: {format_number(max_area)} | "
                f"Min: {format_number(min_area)}"
            )
            logging.info("=" * 60)
            logging.info("Basic statistics analysis completed")

        except KeyError as e:
            logging.error(f"Missing required columns: {e}")
            raise
        except Exception as e:
            logging.error(f"Error in basic_statistics: {e}")
            raise

    @staticmethod
    def city_analysis(df: pd.DataFrame) -> None:
        """
        Log city-wise property counts and price statistics.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset for analysis.
        """
        try:
            logging.info("Starting city analysis")

            required_cols = ["City", "Price"]
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise KeyError(f"Required columns missing: {missing_cols}")

            city_counts = df["City"].value_counts()
            avg_price_by_city = (
                df.groupby("City")["Price"].agg(["mean", "min", "max", "count"]).round(2)
            )

            logging.info("=" * 60)
            logging.info("CITY-WISE ANALYSIS")
            logging.info("=" * 60)

            logging.info("Property Count Per City:")
            for city, count in city_counts.items():
                logging.info(f"  {city}: {count} properties")

            logging.info("Price Statistics Per City:")
            for city, row in avg_price_by_city.iterrows():
                logging.info(
                    f"  {city}: Avg {format_money(row['mean'])} | "
                    f"Min {format_money(row['min'])} | Max {format_money(row['max'])} | Count: {int(row['count'])}"
                )

            logging.info("=" * 60)
            logging.info("City analysis completed")

        except KeyError as e:
            logging.error(f"Missing required columns: {e}")
            raise
        except Exception as e:
            logging.error(f"Error in city_analysis: {e}")
            raise

    @staticmethod
    def bedroom_analysis(df: pd.DataFrame) -> None:
        """
        Log property distribution by bedroom count.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset for analysis.
        """
        try:
            logging.info("Starting bedroom analysis")

            if "Bedrooms" not in df.columns:
                raise KeyError("Bedrooms column not found")

            bedroom_counts = df["Bedrooms"].value_counts().sort_index()
            bedroom_percentages = (bedroom_counts / len(df) * 100).round(2)

            logging.info("=" * 60)
            logging.info("BEDROOM DISTRIBUTION ANALYSIS")
            logging.info("=" * 60)

            for bedrooms, count in bedroom_counts.items():
                logging.info(f"  {int(bedrooms)} Bedrooms: {count} properties ({bedroom_percentages[bedrooms]}%)")

            logging.info("=" * 60)
            logging.info("Bedroom analysis completed")

        except KeyError as e:
            logging.error(f"Missing required column: {e}")
            raise
        except Exception as e:
            logging.error(f"Error in bedroom_analysis: {e}")
            raise

    @staticmethod
    def bathroom_analysis(df: pd.DataFrame) -> None:
        """
        Log bathroom statistics and distribution.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset for analysis.
        """
        try:
            logging.info("Starting bathroom analysis")

            if "Bathrooms" not in df.columns:
                raise KeyError("Bathrooms column not found")

            avg_bathrooms = df["Bathrooms"].mean()
            min_bathrooms = df["Bathrooms"].min()
            max_bathrooms = df["Bathrooms"].max()
            median_bathrooms = df["Bathrooms"].median()
            bathroom_counts = df["Bathrooms"].value_counts().sort_index()

            logging.info("=" * 60)
            logging.info("BATHROOM ANALYSIS")
            logging.info("=" * 60)
            logging.info(f"Average Bathrooms: {avg_bathrooms:.2f}")
            logging.info(f"Median Bathrooms: {median_bathrooms:.2f}")
            logging.info(f"Range: {min_bathrooms:g} to {max_bathrooms:g}")

            logging.info("Bathroom Distribution:")
            for bathrooms, count in bathroom_counts.items():
                # Use up to 1 decimal so half-baths (e.g. 2.5) aren't hidden by rounding
                label = f"{bathrooms:g}"
                logging.info(f"  {label} Bathrooms: {count} properties")

            logging.info("=" * 60)
            logging.info("Bathroom analysis completed")

        except KeyError as e:
            logging.error(f"Missing required column: {e}")
            raise
        except Exception as e:
            logging.error(f"Error in bathroom_analysis: {e}")
            raise

    @staticmethod
    def price_per_sqft_analysis(df: pd.DataFrame) -> None:
        """
        Log price-per-sqft statistics overall and by city.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset with a 'Price_Per_Sqft' feature.
        """
        try:
            logging.info("Starting Price_Per_Sqft analysis")

            required_cols = ["City", "Price_Per_Sqft"]
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise KeyError(f"Required columns missing: {missing_cols}")

            price_per_sqft_by_city = (
                df.groupby("City")["Price_Per_Sqft"].agg(["mean", "min", "max"]).round(2)
            )
            overall_mean = df["Price_Per_Sqft"].mean()
            overall_median = df["Price_Per_Sqft"].median()

            logging.info("=" * 60)
            logging.info("PRICE PER SQFT ANALYSIS")
            logging.info("=" * 60)
            logging.info(f"Overall Average Price Per Sqft: {format_money(overall_mean)}")
            logging.info(f"Overall Median Price Per Sqft: {format_money(overall_median)}")

            logging.info("Price Per Sqft By City:")
            for city, row in price_per_sqft_by_city.iterrows():
                logging.info(
                    f"  {city}: Avg {format_money(row['mean'])} | "
                    f"Min {format_money(row['min'])} | Max {format_money(row['max'])}"
                )

            logging.info("=" * 60)
            logging.info("Price_Per_Sqft analysis completed")

        except KeyError as e:
            logging.error(f"Missing required columns: {e}")
            raise
        except Exception as e:
            logging.error(f"Error in price_per_sqft_analysis: {e}")
            raise