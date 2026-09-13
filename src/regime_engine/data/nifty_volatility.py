# === Database Mofules ===
import duckdb

# === Path Modules ===
from pathlib import Path

# === Class to Calculate Volatility Returns using DuckDB ===
class NiftyVolatility:
    def __init__(
            self,
            file_path: str = "data/volatilty/nifty_volatility.db",
            returns_file_path: str = "data/returns/nifty_returns.db"
    ):
        """
        Calculates the nifty's volatiltiy.
        """
        self.file_path = file_path
        self.returns_file_path = returns_file_path

        ## === initiating the database ===
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
                        FROM nifty_volatility
                    """).fetchone()[0]

        return count > 0

    def _init_db(
            self
    ) -> None:
        """
        Initiates the Database for storing the Nifty Volatility.
        """
        path: Path = Path(self.file_path)

        path.parent.mkdir(
            parents = True,
            exist_ok = True
        )

        ## === Query ===
        query = """
            CREATE TABLE IF NOT EXISTS nifty_volatility (
                date TIMESTAMP PRIMARY KEY,
                vol_3 DOUBLE,
                vol_5 DOUBLE,
                vol_7 DOUBLE,
                vol_10 DOUBLE,
                vol_21 DOUBLE
            )
        """

        ## === Database Connection ===
        with duckdb.connect(str(self.file_path)) as conn:
            conn.execute(query)

    def _first_time_run(
            self
    ) -> None:
        """
        Calculates the volatility of nifty returns for the first time.
        """
        # === Query ===
        query = """
            INSERT INTO nifty_volatility
            SELECT
                date,

                CASE
                    WHEN COUNT(log_return_1) OVER (
                        ORDER BY date
                        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                    ) = 3
                    THEN STDDEV_SAMP(log_return_1) OVER (
                        ORDER BY date
                        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                    ) * SQRT(252)
                END AS vol_3,

                CASE
                    WHEN COUNT(log_return_1) OVER (
                        ORDER BY date
                        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
                    ) = 5
                    THEN STDDEV_SAMP(log_return_1) OVER (
                        ORDER BY date
                        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
                    ) * SQRT(252)
                END AS vol_5,

                CASE
                    WHEN COUNT(log_return_1) OVER (
                        ORDER BY date
                        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                    ) = 7
                    THEN STDDEV_SAMP(log_return_1) OVER (
                        ORDER BY date
                        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                    ) * SQRT(252)
                END AS vol_7,

                CASE
                    WHEN COUNT(log_return_1) OVER (
                        ORDER BY date
                        ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
                    ) = 10
                    THEN STDDEV_SAMP(log_return_1) OVER (
                        ORDER BY date
                        ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
                    ) * SQRT(252)
                END AS vol_10,

                CASE
                    WHEN COUNT(log_return_1) OVER (
                        ORDER BY date
                        ROWS BETWEEN 20 PRECEDING AND CURRENT ROW
                    ) = 21
                    THEN STDDEV_SAMP(log_return_1) OVER (
                        ORDER BY date
                        ROWS BETWEEN 20 PRECEDING AND CURRENT ROW
                    ) * SQRT(252)
                END AS vol_21

            FROM return_db.nifty_returns
            ORDER BY date;

        """
        # === Database Connection ===
        with duckdb.connect(str(self.file_path)) as conn:

            # === Adding an attachment ===
            conn.execute(
                f"ATTACH '{self.returns_file_path}' AS return_db"
            )

            # === Running the Query ===
            conn.execute(query)

    def _incremental_run(
            self
    ) -> None:
        """
        Calculates volatility only for newly added return data.
        """
        query = f"""
            ATTACH '{self.returns_file_path}' AS returns_db;
            INSERT INTO nifty_volatility
            WITH previous_rows AS (
                SELECT
                    date,
                    log_return_1
                FROM returns_db.nifty_returns
                WHERE date <= (
                    SELECT MAX(date)
                    FROM nifty_volatility
                )
                ORDER BY date DESC
                LIMIT 20
            ),
            new_rows AS (
                SELECT
                    date,
                    log_return_1
                FROM returns_db.nifty_returns
                WHERE date > (
                    SELECT MAX(date)
                    FROM nifty_volatility
                )
            ),
            combined_data AS (
                SELECT *
                FROM previous_rows
                UNION ALL
                SELECT *
                FROM new_rows
            ),
            calculated_volatility AS (
                SELECT
                    date,
                    CASE
                        WHEN COUNT(log_return_1) OVER (
                            ORDER BY date
                            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                        ) = 3
                        THEN
                            STDDEV_SAMP(log_return_1) OVER (
                                ORDER BY date
                                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                            ) * SQRT(252)
                    END AS vol_3,
                    CASE
                        WHEN COUNT(log_return_1) OVER (
                            ORDER BY date
                            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
                        ) = 5
                        THEN
                            STDDEV_SAMP(log_return_1) OVER (
                                ORDER BY date
                                ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
                            ) * SQRT(252)
                    END AS vol_5,
                    CASE
                        WHEN COUNT(log_return_1) OVER (
                            ORDER BY date
                            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                        ) = 7
                        THEN
                            STDDEV_SAMP(log_return_1) OVER (
                                ORDER BY date
                                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                            ) * SQRT(252)
                    END AS vol_7,
                    CASE
                        WHEN COUNT(log_return_1) OVER (
                            ORDER BY date
                            ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
                        ) = 10
                        THEN
                            STDDEV_SAMP(log_return_1) OVER (
                                ORDER BY date
                                ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
                            ) * SQRT(252)
                    END AS vol_10,
                    CASE
                        WHEN COUNT(log_return_1) OVER (
                            ORDER BY date
                            ROWS BETWEEN 20 PRECEDING AND CURRENT ROW
                        ) = 21
                        THEN
                            STDDEV_SAMP(log_return_1) OVER (
                                ORDER BY date
                                ROWS BETWEEN 20 PRECEDING AND CURRENT ROW
                            ) * SQRT(252)
                    END AS vol_21
                FROM combined_data
            )
            SELECT
                date,
                vol_3,
                vol_5,
                vol_7,
                vol_10,
                vol_21
            FROM calculated_volatility
            WHERE date > (
                SELECT MAX(date)
                FROM nifty_volatility
            )
            ORDER BY date;
        """

        with duckdb.connect(str(self.file_path)) as conn:
            conn.execute(query)

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