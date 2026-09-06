# === Nifty Ingestion ===
from regime_engine.data.nifty_ingest import NiftyIngest

# === Ingestion Pipeline ===
class NiftyIngestPipeline:
    def __init__(self):
        pass

    def main(self):
        try:

            ## === Initiating Nifty Ingest ===
            ingest = NiftyIngest()

            ## === Downloading data ===
            data = ingest._ingest_data()

            ## === Saving Data ===
            ingest._insert_data(data = data)

        except Exception as e:
            raise ValueError(f"Error running the 'NiftyIngestPipeline': {e}")