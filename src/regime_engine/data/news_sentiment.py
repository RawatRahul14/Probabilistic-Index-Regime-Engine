# === Database Modules ===
import duckdb
import pandas as pd

# === Path Modules ===
from pathlib import Path

# === Class to Save Deduplicated News Data ===
class SentimentNews:
    def __init__(
            self,
            file_path: str = "data/news/sentiment_news.db"
    ):
        """
        Saves the sentiment news data into DuckDB.
        """
        self.file_path = file_path

        ## === Initialising the Database ===
        self._init_db()

    def _init_db(
            self
    ) -> None:
        """
        Initiates the database for storing sentiment news.
        """
        path: Path = Path(self.file_path)
        path.parent.mkdir(
            parents = True,
            exist_ok = True
        )

        ## === Query ===
        query = """
            CREATE TABLE IF NOT EXISTS sentiment_news (
                id UUID DEFAULT uuid(),
                category VARCHAR,
                query VARCHAR,
                topic VARCHAR,
                title VARCHAR,
                url VARCHAR UNIQUE,
                content VARCHAR,
                score DOUBLE,
                published_date TIMESTAMP,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                p_bull DOUBLE,
                p_neutral DOUBLE,
                p_bear DOUBLE,
                confidence DOUBLE,
                importance DOUBLE,
                novelty DOUBLE,
                affected_scope VARCHAR[],
                event_type VARCHAR
            )
        """

        ## === Database Connection ===
        with duckdb.connect(str(self.file_path)) as conn:
            conn.execute(query)

    def insert_articles(
            self,
            sentiment_news: pd.DataFrame
    ) -> None:
        """
        Inserts sentiment news articles into the DuckDB database.
        """
        try:

            ## === Empty Data Check ===
            if sentiment_news.empty:
                return

            ## === Selecting Required Columns ===
            insert_data = sentiment_news.copy()

            ## === Database Connection ===
            with duckdb.connect(str(self.file_path)) as conn:

                ## === Insert Query ===
                conn.execute("""
                    INSERT INTO sentiment_news (
                        category,
                        query,
                        topic,
                        title,
                        url,
                        content,
                        score,
                        published_date,
                        p_bull,
                        p_neutral,
                        p_bear,
                        confidence,
                        importance,
                        novelty,
                        affected_scope,
                        event_type
                    )
                    SELECT
                        category,
                        query,
                        topic,
                        title,
                        url,
                        content,
                        score,
                        published_date,
                        p_bull,
                        p_neutral,
                        p_bear,
                        confidence,
                        importance,
                        novelty,
                        affected_scope,
                        event_type
                    FROM insert_data
                    ON CONFLICT (url) DO NOTHING
                """)

        except Exception as e:
            raise RuntimeError("Error inserting sentiment news articles into database.") from e