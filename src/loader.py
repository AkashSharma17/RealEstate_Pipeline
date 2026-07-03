"""
Data loading module for the RealEstate Pipeline.

Handles locating and reading the raw CSV dataset into a pandas DataFrame,
with defensive error handling for missing or malformed files.
"""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd


class DataLoader:
    """
    Loads raw real estate data from CSV into a pandas DataFrame.
    """

    DEFAULT_DATA_FILE = "data/raw/messy_properties.csv"

    @staticmethod
    def _resolve_default_path() -> Path:
        """
        Locate the project root (directory containing ``data/``) and build
        the default path to the raw data file.

        Returns
        -------
        Path
            Resolved path to the default raw data file.
        """
        current_dir = Path(__file__).resolve().parent
        for parent in current_dir.parents:
            if (parent / "data").exists():
                return parent / DataLoader.DEFAULT_DATA_FILE
        return Path(DataLoader.DEFAULT_DATA_FILE)

    @staticmethod
    def load_data(file_path: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        Load a CSV file and return it as a pandas DataFrame.

        Parameters
        ----------
        file_path : str, optional
            Path to the CSV file. If None, uses ``DEFAULT_DATA_FILE``
            resolved relative to the project root.

        Returns
        -------
        pd.DataFrame or None
            The loaded dataset, or None if loading failed.
        """
        try:
            path = Path(file_path) if file_path else DataLoader._resolve_default_path()

            if not path.exists():
                raise FileNotFoundError(f"Data file not found at: {path}")

            logging.info(f"Attempting to load data from: {path}")
            df = pd.read_csv(path, on_bad_lines="skip", encoding="utf-8")

            logging.info("Data loaded successfully")
            logging.info(f"Dataset shape: {df.shape[0]} rows x {df.shape[1]} columns")
            logging.info(f"Columns: {', '.join(df.columns.tolist())}")

            return df

        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            return None
        except pd.errors.EmptyDataError:
            logging.error("CSV file is empty")
            return None
        except pd.errors.ParserError as e:
            logging.error(f"Error parsing CSV file: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error loading data: {e}")
            return None
