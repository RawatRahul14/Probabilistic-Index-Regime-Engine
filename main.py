# === Python Modules ===
import asyncio

# === Database Modules ===
import duckdb

# === Regime Engine Pipelines ===
from regime_engine.pipelines import (
    NiftyIngestPipeline,
    NiftyReturnsPipeline,
    NiftyVolatilityPipeline
)

from regime_engine.pipelines import (
    NewsIngestionPipeline,
    NewsDedupPipeline
)

# === Main Function ===
def run_nifty_pipelines() -> None:

    ## === ingestion Pipeline ===
    ingest_pipeline = NiftyIngestPipeline()
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
    await news_pipeline.main()

    ## === Calling the Data ===
    with duckdb.connect("data/news/raw_news.db") as conn:
        data = conn.execute("SELECT * FROM raw_news").fetch_df()

    ## === Deuplication ===
    dedup_pipeline = NewsDedupPipeline()
    dedup_pipeline.main(data = data)

async def main_fun() -> None:

    await asyncio.gather(
        asyncio.to_thread(run_nifty_pipelines),
        run_news_pipelines()
    )

if __name__ == "__main__":
    asyncio.run(main_fun())