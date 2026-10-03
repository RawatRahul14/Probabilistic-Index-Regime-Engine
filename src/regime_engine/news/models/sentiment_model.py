# === Python Modules ===
from typing import List, Literal

# === Pydantic Modules ===
from pydantic import BaseModel, Field, model_validator

# === Sentiment Model Output ===
class SentimentModel(BaseModel):

    ## === Directional Probabilities ===
    p_bull: float = Field(
        ge = 0.0,
        le = 1.0,
        description = "Probability that the news has a bullish effect on the NIFTY index."
    )
    p_neutral: float = Field(
        ge = 0.0,
        le = 1.0,
        description = "Probability that the news has a neutral or negligible effect on the NIFTY index."
    )
    p_bear:float = Field(
        ge = 0.0,
        le = 1.0,
        description = "Probability that the news has a bearish effect on the NIFTY index."
    )

    ## === Model Confidence ===
    confidence: float = Field(
        ge = 0.0,
        le = 1.0,
        description = "Confidence in the reliability of the directional classification for this news article."
    )

    ## === market Importance ===
    importance: float = Field(
        ge = 0.0,
        le = 1.0,
        description = "Importance of the news article in terms of its potential impact on the market."
    )

    ## === Novelty ===
    novelty: float = Field(
        ge = 0.0,
        le = 1.0,
        description = "Novelty of the news article, indicating how new or unique the information is."
    )

    ## === Affected Market Scope ===
    affected_scope : List[
        Literal[
            "nifty",
            "bank_nifty",
            "financials",
            "it",
            "energy",
            "pharma",
            "auto",
            "fmcg",
            "metal",
            "realty",
            "global_markets",
            "currency",
            "commodities",
            "bond_market",
            "derivatives",
            "volatility"
        ]
    ] = Field(
        description = "Market segments, sectors, or instruments that may be materially affected by the news."
        )

    ## === Event Type ===
    event_type: Literal[
        "monetary_policy",
        "inflation",
        "economic_data",
        "corporate",
        "earnings",
        "merger_acquisition",
        "regulatory",
        "government_policy",
        "geopolitical",
        "global_market",
        "currency",
        "commodities",
        "derivatives",
        "market_structure",
        "analyst_rating",
        "management_commentary",
        "other"
    ] = Field(
        description = "Primary type of event described by the news."
        )

    ## === Probability Validation ===
    @model_validator(mode = "after")
    def validate_probabilities(self):

        ## === Sum of Probabilities ===
        total_probability = self.p_bull + self.p_neutral + self.p_bear

        ## === Error Handling ===
        if total_probability <= 0.0:
            raise ValueError("The sum of p_bull, p_neutral, and p_bear must be greater than 0.0.")

        self.p_bull /= total_probability
        self.p_neutral /= total_probability
        self.p_bear /= total_probability

        return self