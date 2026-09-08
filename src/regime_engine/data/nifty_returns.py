# === Database Mofules ===
import duckdb

# === Path Modules ===
from pathlib import Path

# === Class to Calculate Returns using DuckDB ===
class NiftyReturns:
    def __init__(
            self,
            file_path: str = "data/returns/nifty_returns.db",
            raw_file_path: str = "data/raw/nifty.db"
    ):
        """
        Calculates the nifty's returns
        """
        self.file_path = file_path
        self.raw_file_path = raw_file_path

        ## === Initiating the table ===
        self._init_db()

        ## === File exists Flag ===
        self.flag_exists = self._has_data()

    def _has_data(
            self
    ) -> bool:
        """
        Chcks if the data exists inside the nifty_returns or not
        """

        ## === Database Connection ===
        with duckdb.connect(self.file_path) as conn:

            count = conn.execute("""
                        SELECT COUNT(*)
                        FROM nifty_returns
                    """).fetchone()[0]

        return count > 0

    def _init_db(
            self
    ) -> None:
        """
        Initiates the Database for storing the Nifty returns.
        """
        db_path: Path = Path(self.file_path)

        ## === Making sure the Folders exists ===
        db_path.parent.mkdir(
            exist_ok = True,
            parents = True
        )

        try:

            ## === Query ===
            query = """
                CREATE TABLE IF NOT EXISTS nifty_returns (
                    date TIMESTAMP PRIMARY KEY,
                    return_1 DOUBLE,
                    return_5 DOUBLE,
                    return_10 DOUBLE,
                    return_20 DOUBLE,
                    log_return_1 DOUBLE
                )
            """

            ## === Making the Database conncection ===
            with duckdb.connect(self.file_path) as conn:
                conn.execute(query)

        except Exception as e:
            raise RuntimeError("Error Creating the 'nifty_returns' table.") from e

    def _first_time_run(
            self
    ) -> None:
        """
        Calculates the nifty returns for the first time.
        """
        ## === Query ===
        query = """
            INSERT OR REPLACE INTO nifty_returns (
                date,
                return_1,
                return_5,
                return_10,
                return_20,
                log_return_1
            )

            SELECT
                date,
                close / LAG(close, 1) OVER (ORDER BY date) - 1 AS return_1,
                close / LAG(close, 5) OVER (ORDER BY date) - 1 AS return_5,
                close / LAG(close, 10) OVER (ORDER BY date) - 1 AS return_10,
                close / LAG(close, 20) OVER (ORDER BY date) - 1 AS return_20,
                LN(close / LAG(close, 1) OVER (ORDER BY date)) AS log_return_1

            FROM raw_data.nifty
            ORDER BY date;
        """

        try:

            ## === Database connection ===
            with duckdb.connect(self.file_path) as conn:

                ## === Adding a attachment ===
                conn.execute(
                    f"""ATTACH '{self.raw_file_path}' AS raw_data"""
                )

                conn.execute(query)

        except Exception as e:
            raise RuntimeError("Error calculating the returns.") from e

    def _incremental_run(
            self
    ) -> None:
        """
        Calculates the incremental returns
        """
        query = """
            WITH last_calculated AS (
                SELECT MAX(date) AS max_date
                FROM nifty_returns
            ),

        needed_data AS (
                SELECT *
                FROM raw_data.nifty
                WHERE date >= (
                    SELECT date
                    FROM raw_data.nifty
                    WHERE date <= (
                        SELECT max_date
                        FROM last_calculated
                    )
                    ORDER BY date DESC
                    OFFSET 20
                    LIMIT 1
                )
            ),

        calc AS (
            SELECT
                date,
                close / LAG(close, 1) OVER (ORDER BY date) - 1 AS return_1,
                close / LAG(close, 5) OVER (ORDER BY date) - 1 AS return_5,
                close / LAG(close, 10) OVER (ORDER BY date) - 1 AS return_10,
                close / LAG(close, 20) OVER (ORDER BY date) - 1 AS return_20,
                LN(close / LAG(close, 1) OVER (ORDER BY date) ) AS log_return_1
            FROM needed_data
        )

        INSERT INTO nifty_returns (
            date,
            return_1,
            return_5,
            return_10,
            return_20,
            log_return_1
        )

        SELECT
            date,
            return_1,
            return_5,
            return_10,
            return_20,
            log_return_1

        FROM calc

        WHERE date > (
            SELECT max_date
            FROM last_calculated
        )

        ORDER BY date;
        """

        try:

            ## === Database Connection ===
            with duckdb.connect(self.file_path) as conn:

                ## === Adding an attachment ===
                conn.execute(
                    f"ATTACH '{self.raw_file_path}' AS raw_data"
                )

                conn.execute(query)

        except Exception as e:
            raise RuntimeError("Error doing incremental calculations.") from e

    def calculate(
            self
    ) -> None:
        """
        Runs the class
        """
        if self.flag_exists:
            self._incremental_run()
        else:
            self._first_time_run()