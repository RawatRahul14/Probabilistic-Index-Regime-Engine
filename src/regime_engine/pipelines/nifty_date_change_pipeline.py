# === Regime Engine Modules ===
from regime_engine.utils.nifty_utils import (
    get_date,
    increment_date,
    change_date
)

# === Date Modules ===
from datetime import datetime

# === Pipeline to automate the whole date change logic ===
class NiftyDateChangePipeline:
    def __init__(self):
        self.date_time = datetime.now().isoformat()

    def main(self):
        try:

            ## === Retrieving the Last Date ===
            last_date_time: None | dict = get_date()

            ## === Checking the Time Flag ===
            if change_date(time = self.date_time.split("T")[1]):
                increment_date(date = self.date_time)

            ## === Returning the last date recieved ===
            return last_date_time

        except Exception as e:
            raise ValueError("Error running the `NiftyDateChangePipeline`.") from e