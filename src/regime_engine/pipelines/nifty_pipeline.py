# === Nifty Ingestion ===
from regime_engine.data.nifty_ingest import NiftyIngest

# === Ingestion Pipeline ===
class NiftyIngestPipeline:
    def __init__(self):
        pass

    def main(self):
        try:

            ## === Initiating Nifty Ingest ===
            ingest = NiftyIngest().run()

        except Exception as e:
            raise ValueError(f"Error running the 'NiftyIngestPipeline': {e}")

if __name__ == "__main__":
    nifty_pipeline = NiftyIngestPipeline()
    nifty_pipeline.main()