# === Regime Engine Modules ===
from regime_engine.news.models import (
    NewsDeduplicator
)
from regime_engine.data.dedup_news import DedupNews

# === Class to deduplicate the news ===
class NewsDedupPipeline:
    def __init__(self):
        pass

    def main(self, data):
        try:

            ## === Deduplicating the news articles ===
            news_dedup = NewsDeduplicator()
            dedup_data = news_dedup.deduplicate(articles = data)

            ## === Saving the Dedup Data ===
            dedup_news_save = DedupNews()
            dedup_news_save.insert_articles(dedup_news = dedup_data)

            ## === Returning the dedup data for sentiment analysis ===
            return dedup_data

        except Exception as e:
            raise ValueError("Error deduping the news.") from e