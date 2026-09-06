# === Python Modules ===
from datetime import datetime

# === Pydantic Modules ===
from pydantic import BaseModel

# === Nifty's Output Model ===
class NiftyCandle(BaseModel):
    date: datetime
    close: float
    high: float
    low: float
    open: float