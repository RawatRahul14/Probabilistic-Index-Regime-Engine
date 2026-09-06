# === Regime Engine Modules ===
from regime_engine.models.nifty_model import NiftyCandle

# === Database Modules ===
import duckdb
import pandas as pd

# === Yfinance Modules ===
import yfinance

# === Path Modules ===
from pathlib import Path

# === Data Ingestion Class ===
class NiftyIngest:
    def __init__(
            self,
            interval: str = "1d",
            period: str = "5y",
            file_path: str = "data/raw/nifty"
    ):
        """
        Class to Ingest Historical Nifty Index data into Duckdb.
        """
        self.interval = interval
        self.period = period

        self._init_db(file_path = file_path)

    def _ingest_data(self) -> pd.DataFrame:
        """
        Ingesting data using yfinance
        """
        try:

            ## === Downloading Data ===
            data = yfinance.download(
                tickers = "^NSEI",
                multi_level_index = False,
                interval = self.interval,
                period = self.period,
                rounding = True
            )

            ## === Cleaning Data ===
            data = data.drop(
                columns = "Volume",
                errors = "ignore"
            ).reset_index()

            data.columns = data.columns.str.lower()

            return data

        except Exception as e:
            raise ValueError(f"Error Downloading Data: {e}")

    def _init_db(
            self,
            file_path: str
    ) -> None:
        """
        Initiates the database if not exists.
        """
        ## === Path ===
        self.db_path = Path((file_path) + ".db")

        ## === Creating Directory ===
        self.db_path.parent.mkdir(
            exist_ok = True,
            parents = True
        )

        ## === Schema ===
        TABLE_SCHEMA = """
            CREATE TABLE IF NOT EXISTS nifty (
                date TIMESTAMP PRIMARY KEY,
                close DOUBLE,
                high DOUBLE,
                low DOUBLE,
                open DOUBLE
            )
        """

        ## === Database connection ===
        with duckdb.connect(str(self.db_path)) as conn:
            conn.execute(
                TABLE_SCHEMA
            )

    def _insert_data(
            self,
            data: pd.DataFrame
    ) -> None:
        """
        Inserts the data into the Duckdb Database
        """
        try:

            ## === Database Connection ===
            with duckdb.connect(str(self.db_path)) as conn:

                ## === Inserting data ===
                conn.execute(
                    """
                        INSERT OR REPLACE INTO nifty (
                            date,
                            close,
                            high,
                            low,
                            open
                        )
                        SELECT
                            date,
                            close,
                            high,
                            low,
                            open
                        FROM data
                    """
                )

        except Exception as e:
            raise RuntimeError(
                f"Error inserting Nifty data: {e}"
            )