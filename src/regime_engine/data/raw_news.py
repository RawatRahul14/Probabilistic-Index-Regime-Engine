# === Python Modules ===
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

# === Database Modules ===
import duckdb
import pandas as pd

# === Path Modules ===
from pathlib import Path

# === Class to Save raw news data ===
class RawNews:
    def __init__(
            self,
            file_path: str = "data/news/raw_news.db"
    ):
        """
        Saves the raw news data into duckdb
        """
        self.file_path = file_path

        ## === Initialiasing the database ===
        self._init_db()

    def _init_db(
            self
    ) -> None:
        """
        Initiates the Database for storing the Raw News.
        """
        path: Path = Path(self.file_path)

        path.parent.mkdir(
            parents = True,
            exist_ok = True
        )

        ## === Query ===
        query = """
            CREATE TABLE IF NOT EXISTS raw_news (
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

    def _convert_to_df(
            self,
            news_data: dict[str, list[dict]]
    ) -> pd.DataFrame:
        """
        Converts fetched news data into a DataFrame matching the raw_news database schema.
        """
        ## === List to hold the data ===
        rows = []

        ## === Fetch Time ===
        fetch_time = datetime.now(timezone.utc)

        ## === Looping through the News Categories ===
        for category, articles in news_data.items():

            ## === Looping through articles ===
            for article in articles:

                ## === Published Date ===
                published_date = article.get("published_date")

                if published_date:
                    published_date = parsedate_to_datetime(published_date)

                ## === Appending the row ===
                rows.append({
                    "category": category,
                    "query": article.get("query"),
                    "topic": article.get("topic"),
                    "title": article.get("title"),
                    "url": article.get("url"),
                    "content": article.get("content"),
                    "score": article.get("score"),
                    "published_date": published_date,
                    "fetched_at": fetch_time
                })

        ## === Creating the DataFrame ===
        return pd.DataFrame(
            rows,
            columns = [
                "category",
                "query",
                "topic",
                "title",
                "url",
                "content",
                "score",
                "published_date",
                "fetched_at"
            ]
        )

    def insert_articles(
            self,
            news_data: dict[str, list[dict]]
    ):
        """
        Inserts filtered news articles into the DuckDB database.
        """
        ## === Convert to DataFrame ===
        news_df = self._convert_to_df(news_data)

        if news_df.empty:
            return None

        try:
            ## === Database Connection ===
            with duckdb.connect(str(self.file_path)) as conn:

                ### === Inserting the DataFrame into the Database ===
                conn.register("news_df", news_df)

                conn.execute(
                    """
                    INSERT OR IGNORE INTO raw_news (
                        category,
                        query,
                        topic,
                        title,
                        url,
                        content,
                        score,
                        published_date,
                        fetched_at
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
                        fetched_at
                    FROM news_df
                    """
                )

            ## === Returning the fetched_at ===
            return news_df["fetched_at"].iloc[0]
    
        except duckdb.Error as e:
            raise RuntimeError(f"Error inserting news articles into database: {e}") from e

        except Exception as e:
            raise RuntimeError(f"Error inserting news articles into database. {e}") from e