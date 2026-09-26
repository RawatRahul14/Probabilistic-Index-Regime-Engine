# === Python Modules ===
from functools import lru_cache

# === Path Modules ===
from pathlib import Path

# === Transformers Modules ===
from sentence_transformers import SentenceTransformer

# === Project Root ===
PROJECT_ROOT = Path("models")

# === Model Path ===
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_PATH = PROJECT_ROOT / "all-MiniLM-L6-v2"

# === Code to download Model ===
@lru_cache(maxsize = 1)
def load_embedding_model() -> SentenceTransformer:
    """
    Loads the `all-MiniLM-L6-v2` into the memory
    """

    ## === If the Model is already downloaded ===
    if PROJECT_ROOT.exists():
        return SentenceTransformer(
            str(MODEL_PATH)
        )

    else:
        ## === Making the directory ===
        MODEL_PATH.mkdir(
            parents = True,
            exist_ok = True
        )

        ## === Downloading the Model ===
        model = SentenceTransformer(MODEL_NAME)

        model.save(path = MODEL_PATH)

        return model