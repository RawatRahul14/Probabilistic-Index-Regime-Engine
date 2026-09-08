# === Regime Engine Modules ===
from regime_engine.data.nifty_returns import NiftyReturns

# === Pipeline class to calculate nifty returns ===
class NiftyReturnsPipeline:
    def __init__(self):
        pass

    def main(self):
        try:

            ## === Initiating Nifty Returns ===
            returns = NiftyReturns()
            returns.calculate()

        except Exception as e:
            raise RuntimeError("Error running the 'NiftyReturnsPipeline'.") from e

if __name__ == "__main__":
    pipeline = NiftyReturnsPipeline()
    pipeline.main()