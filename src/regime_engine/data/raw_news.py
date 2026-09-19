# === Python Modules ===
from email.utils import parsedate_to_datetime

# === Database Modules ===
import duckdb

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

    def insert_articles(
            self,
            news_data: dict[str, list[dict]]
    ):
        """
        Inserts filtered news articles into the DuckDB database.
        """
        try:

            ## === Database Connection ===
            with duckdb.connect(str(self.file_path)) as conn:

                ## === Looping through the News Categories ===
                for category, articles in news_data.items():

                    ## === Looping through artciles ===
                    for article in articles:

                        ## === Published Date ===
                        published_date = article.get("published_date")

                        if published_date:
                            published_date = parsedate_to_datetime(published_date)

                        ## === Insert Query ===
                        query = """
                            INSERT OR IGNORE INTO raw_news (
                                category,
                                query,
                                topic,
                                title,
                                url,
                                content,
                                score,
                                published_date
                            )

                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """

                        ## === Inserting the data ===
                        conn.execute(
                            query,
                            [
                                category,
                                article.get("query"),
                                article.get("topic"),
                                article.get("title"),
                                article.get("url"),
                                article.get("content"),
                                article.get("score"),
                                published_date
                            ]
                        )

        except Exception as e:
            raise RuntimeError(f"Error inserting news articles into database.") from e