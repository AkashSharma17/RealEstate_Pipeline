"""
Data visualization module for the RealEstate Pipeline.

Generates and saves analytical plots (distributions, comparisons,
correlations) to the output directory for business reporting.
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import pandas as pd

from src.utils import format_money


def _price_axis_formatter(x: float, _pos: int) -> str:
    """Format axis tick values as currency with K/M suffixes."""
    return format_money(x, decimals=0)


class Visualizer:
    """
    Generates and persists exploratory/analytical charts for the dataset.
    """

    OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output" / "visualizations"

    @classmethod
    def _setup_output_directory(cls) -> None:
        """Create the visualization output directory if it doesn't exist."""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        logging.info(f"Visualization output directory: {cls.OUTPUT_DIR}")

    @staticmethod
    def price_distribution(df: pd.DataFrame) -> None:
        """
        Save a histogram (with KDE) of property price distribution.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing 'Price' column.
        """
        try:
            logging.info("Creating Price Distribution plot")

            if "Price" not in df.columns:
                raise KeyError("Price column not found")

            price_data = df["Price"].dropna()
            if len(price_data) == 0:
                raise ValueError("No valid price data to visualize")

            plt.figure(figsize=(10, 6))
            ax = sns.histplot(price_data, bins=20, kde=True, color="steelblue")
            ax.xaxis.set_major_formatter(FuncFormatter(_price_axis_formatter))
            plt.title("Price Distribution", fontsize=14, fontweight="bold")
            plt.xlabel("Price", fontsize=12)
            plt.ylabel("Frequency", fontsize=12)
            plt.tight_layout()

            Visualizer._setup_output_directory()
            output_path = Visualizer.OUTPUT_DIR / "01_price_distribution.png"
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            logging.info(f"Price distribution plot saved: {output_path}")
            plt.close()

        except KeyError as e:
            logging.error(f"Missing required column: {e}")
            raise
        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error creating price distribution plot: {e}")
            raise

    @staticmethod
    def city_wise_average_price(df: pd.DataFrame) -> None:
        """
        Save a bar plot of average property price by city (descending).

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing 'City' and 'Price' columns.
        """
        try:
            logging.info("Creating City-wise Average Price plot")

            required_cols = ["City", "Price"]
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise KeyError(f"Missing columns: {missing_cols}")

            avg_price = (
                df.groupby("City")["Price"].mean().sort_values(ascending=False).reset_index()
            )
            if len(avg_price) == 0:
                raise ValueError("No city data to visualize")

            plt.figure(figsize=(12, 6))
            ax = sns.barplot(
                data=avg_price, x="City", y="Price",
                hue="City", palette="viridis", legend=False,
            )
            ax.yaxis.set_major_formatter(FuncFormatter(_price_axis_formatter))
            for bar, price in zip(ax.patches, avg_price["Price"]):
                ax.text(
                    bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    format_money(price, decimals=0), ha="center", va="bottom", fontsize=9,
                )
            plt.title("Average Price by City", fontsize=14, fontweight="bold")
            plt.xlabel("City", fontsize=12)
            plt.ylabel("Average Price", fontsize=12)
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()

            Visualizer._setup_output_directory()
            output_path = Visualizer.OUTPUT_DIR / "02_city_wise_average_price.png"
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            logging.info(f"City-wise average price plot saved: {output_path}")
            plt.close()

        except KeyError as e:
            logging.error(f"Missing required columns: {e}")
            raise
        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error creating city-wise price plot: {e}")
            raise

    @staticmethod
    def bedrooms_distribution(df: pd.DataFrame) -> None:
        """
        Save a count plot of properties by bedroom count.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing 'Bedrooms' column.
        """
        try:
            logging.info("Creating Bedrooms Distribution plot")

            if "Bedrooms" not in df.columns:
                raise KeyError("Bedrooms column not found")

            bedroom_data = df.dropna(subset=["Bedrooms"])
            if len(bedroom_data) == 0:
                raise ValueError("No valid bedroom data to visualize")

            # Use true numeric x-positions (not seaborn's categorical axis) so
            # matplotlib never has to guess/convert string-like float labels —
            # this avoids the "categorical units...parsable as floats" warning.
            counts = bedroom_data["Bedrooms"].astype(int).value_counts().sort_index()
            x_pos = counts.index.to_numpy()
            colors = sns.color_palette("Set2", len(counts))

            plt.figure(figsize=(10, 6))
            bars = plt.bar(x_pos, counts.values, color=colors, edgecolor="white", linewidth=1.2)
            for bar, count in zip(bars, counts.values):
                plt.text(
                    bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
                    str(int(count)), ha="center", va="bottom", fontsize=10, fontweight="bold",
                )
            plt.title("Bedroom Distribution", fontsize=14, fontweight="bold")
            plt.xlabel("Number of Bedrooms", fontsize=12)
            plt.ylabel("Count", fontsize=12)
            plt.xticks(x_pos)
            plt.tight_layout()

            Visualizer._setup_output_directory()
            output_path = Visualizer.OUTPUT_DIR / "03_bedrooms_distribution.png"
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            logging.info(f"Bedrooms distribution plot saved: {output_path}")
            plt.close()

        except KeyError as e:
            logging.error(f"Missing required column: {e}")
            raise
        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error creating bedrooms distribution plot: {e}")
            raise

    @staticmethod
    def area_vs_price(df: pd.DataFrame) -> None:
        """
        Save a scatter plot of property area versus price.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing 'Area_Sqft' and 'Price' columns.
        """
        try:
            logging.info("Creating Area vs Price scatter plot")

            required_cols = ["Area_Sqft", "Price"]
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise KeyError(f"Missing columns: {missing_cols}")

            plot_data = df.dropna(subset=required_cols)
            if len(plot_data) == 0:
                raise ValueError("No valid area-price data to visualize")

            has_city = "City" in plot_data.columns
            has_bedrooms = "Bedrooms" in plot_data.columns

            fig, ax = plt.subplots(figsize=(11, 7))

            scatter_kwargs = dict(alpha=0.75, edgecolor="white", linewidth=0.6, ax=ax)
            if has_city:
                scatter_kwargs["hue"] = "City"
                scatter_kwargs["palette"] = "husl"
            if has_bedrooms:
                scatter_kwargs["size"] = "Bedrooms"
                scatter_kwargs["sizes"] = (40, 240)

            sns.scatterplot(data=plot_data, x="Area_Sqft", y="Price", **scatter_kwargs)

            # Trend line showing the overall Area-Price relationship
            sns.regplot(
                data=plot_data, x="Area_Sqft", y="Price", scatter=False,
                color="black", line_kws={"linestyle": "--", "linewidth": 1.5, "alpha": 0.6}, ax=ax,
            )

            # Correlation annotation
            correlation = plot_data["Area_Sqft"].corr(plot_data["Price"])
            ax.text(
                0.02, 0.96, f"Correlation: {correlation:.2f}",
                transform=ax.transAxes, fontsize=11, fontweight="bold", va="top",
                bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray", alpha=0.85),
            )

            plt.title("Area vs Price Relationship", fontsize=14, fontweight="bold")
            plt.xlabel("Area (Sqft)", fontsize=12)
            plt.ylabel("Price", fontsize=12)
            ax.yaxis.set_major_formatter(FuncFormatter(_price_axis_formatter))
            if has_city or has_bedrooms:
                ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9, title_fontsize=10)
            plt.tight_layout()

            Visualizer._setup_output_directory()
            output_path = Visualizer.OUTPUT_DIR / "04_area_vs_price.png"
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            logging.info(f"Area vs price scatter plot saved: {output_path}")
            plt.close()

        except KeyError as e:
            logging.error(f"Missing required columns: {e}")
            raise
        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error creating area vs price plot: {e}")
            raise

    @staticmethod
    def boxplot_price(df: pd.DataFrame) -> None:
        """
        Save a box plot showing price distribution and outliers.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing 'Price' column.
        """
        try:
            logging.info("Creating Price Box plot")

            if "Price" not in df.columns:
                raise KeyError("Price column not found")

            price_data = df[["Price"]].dropna()
            if len(price_data) == 0:
                raise ValueError("No valid price data to visualize")

            fig, ax = plt.subplots(figsize=(9, 7))

            sns.boxplot(
                data=price_data, y="Price", color="#a8c8f0", width=0.35,
                showmeans=True,
                meanprops={
                    "marker": "D", "markerfacecolor": "darkorange",
                    "markeredgecolor": "black", "markersize": 9,
                },
                flierprops={"marker": "o", "markerfacecolor": "crimson", "markersize": 6, "alpha": 0.6},
                ax=ax,
            )
            sns.stripplot(
                data=price_data, y="Price", color="steelblue",
                alpha=0.45, size=5, jitter=0.15, ax=ax,
            )

            q1 = price_data["Price"].quantile(0.25)
            median = price_data["Price"].median()
            q3 = price_data["Price"].quantile(0.75)
            mean_price = price_data["Price"].mean()

            stats_text = (
                f"Q1: {format_money(q1)}\n"
                f"Median: {format_money(median)}\n"
                f"Q3: {format_money(q3)}\n"
                f"Mean: {format_money(mean_price)}"
            )
            ax.text(
                0.68, 0.97, stats_text, transform=ax.transAxes, fontsize=10, va="top",
                bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray", alpha=0.9),
            )

            ax.yaxis.set_major_formatter(FuncFormatter(_price_axis_formatter))
            plt.title("Price Distribution (Box Plot + Data Points)", fontsize=14, fontweight="bold")
            plt.ylabel("Price", fontsize=12)
            plt.tight_layout()

            Visualizer._setup_output_directory()
            output_path = Visualizer.OUTPUT_DIR / "05_boxplot_price.png"
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            logging.info(f"Price box plot saved: {output_path}")
            plt.close()

        except KeyError as e:
            logging.error(f"Missing required column: {e}")
            raise
        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error creating price box plot: {e}")
            raise