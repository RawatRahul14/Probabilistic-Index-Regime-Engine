# === Regime Engine Modules ===
from regime_engine.data.nifty_volatility import NiftyVolatility

# === Pipeline class to calculate nifty returns ===
class NiftyVolatilityPipeline:
    def __init__(self):
        pass

    def main(self):
        try:

            ## === Initiating Nifty Returns ===
            returns = NiftyVolatility()
            returns.calculate()

        except Exception as e:
            raise RuntimeError("Error running the 'NiftyVolatilityPipeline'.") from e

if __name__ == "__main__":
    pipeline = NiftyVolatilityPipeline()
    pipeline.main()