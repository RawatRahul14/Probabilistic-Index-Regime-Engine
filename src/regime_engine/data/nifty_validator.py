# === Database Modules ===
import pandas as pd

# === Regime Engine Modules ===
from regime_engine.models.nifty_model import NiftyCandle

# === Validator Class ===
class NiftyDataValidator:

    @staticmethod
    def validate_schema(
        data: pd.DataFrame
    ) -> None:

        ## === Looping through the current downloaded data ===
        for record in data.to_dict(orient = "records"):
            NiftyCandle.model_validate(record)