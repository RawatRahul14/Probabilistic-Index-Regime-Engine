# === Python Modules ===
from datetime import datetime

# === Pydantic Modules ===
from pydantic import BaseModel, ConfigDict, model_validator

# === Nifty's Output Model ===
class NiftyCandle(BaseModel):

    model_config = ConfigDict(
        extra = "forbid"
    )

    date: datetime
    close: float
    high: float
    low: float
    open: float

    @model_validator(mode = "after")
    def validate_ohlc(self):

        ## ===  ===
        if self.high < max(self.open, self.close):
            raise ValueError(
                "High must be >= Open and Close"
            )

        ## ===  ===
        if self.low > min(self.open, self.close):
            raise ValueError(
                "Low must be <= Open and Close"
            )

        if self.low > self.high:
            raise ValueError(
                "Low cannot be greater than High"
            )

        return self