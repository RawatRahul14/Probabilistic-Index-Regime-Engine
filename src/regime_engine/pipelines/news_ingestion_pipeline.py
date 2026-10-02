# === Python Modules ===
import asyncio

# === regime Engine Modules ===
from regime_engine.news.apis.async_tavily import fetch_news
from regime_engine.utils.news_utils import fetch_queries, flatten_news_data, filter_articles

from regime_engine.data.raw_news import RawNews

class NewsIngestionPipeline:
    def __init__(self):
        self.news_data = fetch_queries(file_path = "config/news_queries.yaml")
        self.market_condition = "open_market"
        self.raw_news = RawNews()

    async def main(self):
        try:

            ## === Fetching the news ===
            news_content: dict = await fetch_news(
                data = self.news_data,
                market_time = self.market_condition
            )

            ## === Flattening the news ===
            news_content = flatten_news_data( news_data = news_content)

            ## === filtering the articles ===
            news_content = filter_articles(news_data = news_content)

            ## === Saving the filtered news ===
            count = self.raw_news.insert_articles(news_data = news_content)

            return count

        except Exception as e:
            raise RuntimeError("Error Running the 'NewsIngestionPipeline'.") from e

if __name__ == "__main__":
    pipeline = NewsIngestionPipeline()
    asyncio.run(pipeline.main())