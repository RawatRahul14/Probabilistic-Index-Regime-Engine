# === Path Modules ===
from pathlib import Path

# === Yaml Modules ===
import yaml

# === Function to Imncrement the last downloaded Date ===
def increment_date(
        date: str,
        file_path: str = "config/nifty_date.yaml"
) -> None:
    """
    Changes the `last_update_date` to latest run's date
    """
    ## === Changing to Path ===
    path = Path(file_path)

    ## === Create the file ===
    with open(path, "w") as f:
        yaml.dump(
            {"last_update_date": date},
            f
        )

# === Function to get the last date ===
def get_date(
        file_path: str = "config/nifty_date.yaml"
) -> None | dict:
    """
    Retrieves the last date
    """
    ## === Changing to Path ===
    path = Path(file_path)

    ## === If File exists ===
    if path.exists():

        ## === Create the file ===
        with open(path, "r") as f:
            last_date = yaml.full_load(f)

        return last_date

    ## === If it doesnt ===
    else:
        return None

# === Function to change the date based on the time ===
def change_date(
        time
) -> bool:
    """
    Checksthe date to see if there's need to change the date or not
    """
    if time > "12:00:00":
        return True
    else:
        return False