# === Python Modules ===
import asyncio

# === Database Modules ===
import duckdb

# === Regime Engine Pipelines ===
from regime_engine.pipelines import (
    NiftyDateChangePipeline,
    NiftyIngestPipeline,
    NiftyReturnsPipeline,
    NiftyVolatilityPipeline
)

from regime_engine.pipelines import (
    NewsIngestionPipeline,
    NewsDedupPipeline,
    NewsSentimentPipeline
)

# === Utils ===
from regime_engine.utils.news_utils import get_data_as_dataframe

# === Main Function ===
def run_nifty_pipelines() -> None:

    ## === Getting the date ===
    date_pipeline = NiftyDateChangePipeline()
    date = date_pipeline.main()

    if date is not None:
        date = date.get("last_update_date").split("T")[0]

    ## === ingestion Pipeline ===
    ingest_pipeline = NiftyIngestPipeline(ingest_date = date)
    ingest_pipeline.main()

    ## === Returns Pipeline ===
    returns_pipeline = NiftyReturnsPipeline()
    returns_pipeline.main()

    ## === Volatility Pipeline ===
    volatility_pipeline = NiftyVolatilityPipeline()
    volatility_pipeline.main()

async def run_news_pipelines() -> None:

    ## === News ingestion ===
    news_pipeline = NewsIngestionPipeline()
    fetched_at_time = await news_pipeline.main()

    ## === Dataframe Conversion ===
    data = get_data_as_dataframe(time = fetched_at_time)

    ## === Deuplication ===
    dedup_pipeline = NewsDedupPipeline()
    dedup_data = dedup_pipeline.main(data = data)

    ## === Sentiment Analysis ===
    sentiment_pipeline = NewsSentimentPipeline()
    _ = await sentiment_pipeline.run(articles = dedup_data)

async def main_fun() -> None:

    await asyncio.gather(
        asyncio.to_thread(run_nifty_pipelines),
        run_news_pipelines()
    )

if __name__ == "__main__":
    asyncio.run(main_fun())