# === Database Modules ===
import duckdb
import pandas as pd

# === Path Modules ===
from pathlib import Path

# === Class to Save Deduplicated News Data ===
class DedupNews:
    def __init__(
            self,
            file_path: str = "data/news/dedup_news.db"
    ):
        """
        Saves the deduplicated news data into DuckDB.
        """
        self.file_path = file_path

        ## === Initialising the Database ===
        self._init_db()

    def _init_db(
            self
    ) -> None:
        """
        Initiates the database for storing deduplicated news.
        """
        path: Path = Path(self.file_path)
        path.parent.mkdir(
            parents = True,
            exist_ok = True
        )

        ## === Query ===
        query = """
            CREATE TABLE IF NOT EXISTS dedup_news (
                id UUID DEFAULT uuid(),
                category VARCHAR,
                query VARCHAR,
                topic VARCHAR,
                title VARCHAR,
                url VARCHAR UNIQUE,
                content VARCHAR,
                score DOUBLE,
                published_date TIMESTAMP,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """

        ## === Database Connection ===
        with duckdb.connect(str(self.file_path)) as conn:
            conn.execute(query)

    def insert_articles(
            self,
            dedup_news: pd.DataFrame
    ) -> None:
        """
        Inserts deduplicated news articles into the DuckDB database.
        """
        try:

            ## === Empty Data Check ===
            if dedup_news.empty:
                return

            ## === Selecting Required Columns ===
            insert_data = dedup_news.copy()

            ## === Database Connection ===
            with duckdb.connect(str(self.file_path)) as conn:

                ## === Insert Query ===
                conn.execute("""
                    INSERT INTO dedup_news (
                        category,
                        query,
                        topic,
                        title,
                        url,
                        content,
                        score,
                        published_date
                    )
                    SELECT
                        category,
                        query,
                        topic,
                        title,
                        url,
                        content,
                        score,
                        published_date
                    FROM insert_data
                    ON CONFLICT (url) DO NOTHING
                """)

        except Exception as e:
            raise RuntimeError("Error inserting deduplicated news articles into database.") from e