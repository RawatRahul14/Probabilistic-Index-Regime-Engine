# === Regime Engine Pipelines ===
from regime_engine.pipelines import (
    NiftyIngestPipeline,
    NiftyReturnsPipeline
)

# === Main Function ===
def main_func():

    ## === ingestion Pipeline ===
    ingest_pipeline = NiftyIngestPipeline()
    ingest_pipeline.main()

    ## === Returns Pipeline ===
    returns_pipeline = NiftyReturnsPipeline()
    returns_pipeline.main()

if __name__ == "__main__":
    main_func()