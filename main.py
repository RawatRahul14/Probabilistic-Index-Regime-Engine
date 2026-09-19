# === Python Modules ===
import asyncio

# === Regime Engine Pipelines ===
from regime_engine.pipelines import (
    NiftyIngestPipeline,
    NiftyReturnsPipeline,
    NiftyVolatilityPipeline
)

from regime_engine.pipelines import (
    NewsIngestionPipeline
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

async def main_fun() -> None:
    news_pipeline = NewsIngestionPipeline()

    await asyncio.gather(
        asyncio.to_thread(run_nifty_pipelines),
        news_pipeline.main()
    )

if __name__ == "__main__":
    asyncio.run(main_fun())