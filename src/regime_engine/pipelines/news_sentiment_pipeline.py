# === Python modules ===
import pandas as pd

# === Regime Engine Modules ===
from regime_engine.news.agents.news_sentiment import sentiment_analysis
from regime_engine.data.news_sentiment import SentimentNews

# === Sentiment Analysis Pipeline ===
class NewsSentimentPipeline:
    """
    Pipeline for performing sentiment analysis on news articles.
    """

    def __init__(
            self,
            concurrency: int = 10
    ):
        self.concurrency = concurrency

    async def run(
            self,
            articles: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Run the sentiment analysis pipeline on a DataFrame of articles.
        """
        try:
            results_df = await sentiment_analysis(
                articles = articles,
                concurrency = self.concurrency
            )

            ## === Save the results to DuckDB ===
            sentiment_news = SentimentNews()
            sentiment_news.insert_articles(results_df)

            return results_df
        except Exception as e:
            raise ValueError(f"Error in NewsSentimentPipeline.run.") from e