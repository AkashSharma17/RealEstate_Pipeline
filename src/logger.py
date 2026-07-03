"""
Logger configuration module for the RealEstate Pipeline project.

Sets up a root logger that writes simultaneously to a log file and the
console, ensuring consistent, timestamped logging across all pipeline stages.
"""

import logging
import sys
from pathlib import Path


class LoggerSetup:
    """
    Logger initialization and configuration for the RealEstate Pipeline project.

    Responsibilities:
        - Initializes the root logger at INFO level.
        - Configures a file handler for persistent logging (logs/RealEstate.log).
        - Configures a console handler for real-time feedback.
        - Ensures UTF-8 encoding for international characters.
        - Prevents duplicate handlers on repeated calls (e.g. in notebooks).
    """

    LOG_FILENAME = "RealEstate.log"

    @staticmethod
    def _find_project_root(start_path: Path) -> Path:
        """
        Walk up from ``start_path`` until a directory containing a ``data``
        folder is found, and treat it as the project root.

        Parameters
        ----------
        start_path : Path
            File path to begin the search from.

        Returns
        -------
        Path
            The resolved project root directory.

        Raises
        ------
        FileNotFoundError
            If no parent directory contains a ``data`` folder.
        """
        for parent in start_path.parents:
            if (parent / "data").exists():
                return parent

        raise FileNotFoundError(
            "Project 'data' folder not found. "
            "Ensure folder structure: RealEstate_Pipeline/src/ and RealEstate_Pipeline/data/"
        )

    @classmethod
    def setup_logger(cls) -> None:
        """
        Initialize and configure the logging system.

        Process
        -------
        1. Locate the project root by finding the ``data`` folder.
        2. Create the ``logs`` directory if it doesn't exist.
        3. Configure a file handler writing to ``logs/RealEstate.log``.
        4. Configure a console handler for terminal output.
        5. Attach both handlers to the root logger.

        Raises
        ------
        FileNotFoundError
            If the project root cannot be located.
        Exception
            For any unexpected configuration error.
        """
        try:
            # Step 1: Locate project root
            current_file = Path(__file__).resolve()
            project_root = cls._find_project_root(current_file)

            # Step 2: Create logs directory
            logs_dir = project_root / "logs"
            logs_dir.mkdir(exist_ok=True)
            log_file_path = logs_dir / cls.LOG_FILENAME

            # Step 3: Configure root logger (clear old handlers to avoid duplicates)
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.INFO)
            if root_logger.hasHandlers():
                root_logger.handlers.clear()

            # Step 4: File handler
            file_formatter = logging.Formatter(
                fmt="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)

            # Step 5: Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            if hasattr(console_handler.stream, "reconfigure"):
                console_handler.stream.reconfigure(encoding="utf-8")
            console_handler.setFormatter(logging.Formatter(fmt="%(levelname)s - %(message)s"))
            root_logger.addHandler(console_handler)

            logging.info("Logger initialized successfully")
            logging.info(f"Log file location: {log_file_path}")

        except FileNotFoundError as e:
            print(f"ERROR: {e}")
            raise
        except Exception as e:
            print(f"ERROR: Logger setup failed - {e}")
            raise
