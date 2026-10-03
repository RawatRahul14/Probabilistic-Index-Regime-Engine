<div align="center">

# Probabilistic Index Regime Engine

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg)](#)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_Workflows-FF4081.svg)](#)
[![DuckDB](https://img.shields.io/badge/DuckDB-Analytics_Engine-FFF000?labelColor=black.svg)](#)
[![Probability](https://img.shields.io/badge/Modelling-Probabilistic-00C853.svg)](#)
[![C++](https://img.shields.io/badge/C%2B%2B-20-00599C.svg)](#)
[![Pydantic](https://img.shields.io/badge/Pydantic-Data_Validation-E92063.svg)](#)
[![yfinance](https://img.shields.io/badge/yfinance-Market_Data-6C63FF.svg)](#)
[![Tavily](https://img.shields.io/badge/Tavily-News_Intelligence-111827.svg)](#)
[![AsyncIO](https://img.shields.io/badge/AsyncIO-Concurrent_Pipelines-3776AB.svg)](#)

A quantitative research platform for modelling Indian index-market conditions as probabilistic states using price dynamics, volatility, and financial news intelligence.

</div>

---
<!-- 
## Features

### Core Capabilities

- **State Modelling:** Probabilistic regime detection using hidden state estimation across broad-market indices.
- **Multi-Modal Signals:** Combines continuous price dynamics, volatility surface indicators, and unstructured financial news sentiment.
- **Quantitative Engine:** Built for backtesting, regime transition tracking, and automated metric extraction. -->

## Table of Contents

* [Project Description](#project-description)

  * [The Problem](#the-problem)
  * [What This Project Tackles](#what-this-project-tackles)
  * [Core Research Question](#core-research-question)
* [Features](#features)
* [System Architecture](#system-architecture)
* [Market Data Pipeline](#market-data-pipeline)
* [News Intelligence Pipeline](#news-intelligence-pipeline)
* [Probabilistic News Representation](#probabilistic-news-representation)
* [Data Storage](#data-storage)
* [Incremental Processing](#incremental-processing)
* [Concurrency and Orchestration](#concurrency-and-orchestration)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Configuration](#configuration)
* [Running the Engine](#running-the-engine)
* [Current Implementation](#current-implementation)
* [Roadmap](#roadmap)
* [Limitations](#limitations)
* [Disclaimer](#disclaimer)
* [License](#license)

---

# Project Description

The **Probabilistic Index Regime Engine** is a quantitative research and data-engineering project focused on building a probabilistic representation of market conditions in Indian equity indices.

The project is being developed around a central idea:

> **Markets should be represented as probabilistic states rather than reduced to deterministic technical indicators or binary BUY/SELL signals.**

Instead of asking:

```text
"Should I buy or sell?"
```

the system is designed to work toward a more general research problem:

```text
P(Future Market Outcome | Current Market State)
```

where the **current market state** can incorporate multiple dimensions of market information, including:

* Price behaviour
* Returns
* Volatility
* Market conditions
* Financial news
* News sentiment
* News importance
* News novelty
* Affected sectors and market segments
* Event categories

The current implementation establishes the data and feature-engineering foundation required for this broader regime-modelling problem.

---

## The Problem

Financial markets are influenced by multiple interacting sources of information.

A traditional indicator-driven system may reduce this complexity into a small number of deterministic rules:

```text
RSI > X        → BUY
Moving Average → BUY
Volatility > X → SELL
```

Such representations can be useful for specific strategies, but they do not provide a rich representation of **what state the market is currently in**.

This project approaches the problem differently.

Rather than treating individual indicators as isolated trading signals, the objective is to construct a structured market state from multiple sources of information and eventually estimate the distribution of possible future outcomes conditioned on that state.

---

## What This Project Tackles

The current system focuses on building the underlying infrastructure for this approach.

It currently tackles:

1. **Reliable NIFTY market-data ingestion**
2. **OHLC data validation**
3. **Return feature generation**
4. **Multi-horizon volatility estimation**
5. **Financial-news ingestion**
6. **News quality filtering**
7. **Semantic news deduplication**
8. **Structured probabilistic news classification**
9. **Persistent feature/data storage using DuckDB**
10. **Incremental feature computation**
11. **Asynchronous news processing**
12. **Concurrent market-data and news pipelines**

The longer-term objective is to combine these components into a unified **probabilistic market-regime representation**.

---

## Core Research Question

The project is ultimately centred around:

```text
P(Future Market Outcome | Current Market State)
```

The current implementation does **not** claim to solve this complete prediction problem yet.

Instead, it is building the data, feature, storage, and information-processing infrastructure required to investigate it.

---

# Features

### Market Data

* NIFTY 50 index data ingestion
* Historical data bootstrapping
* Incremental data updates
* OHLC schema validation
* Persistent DuckDB storage
* Duplicate-safe database insertion

### Quantitative Features

* 1-period returns
* 5-period returns
* 10-period returns
* 20-period returns
* Log returns
* 3-period volatility
* 5-period volatility
* 7-period volatility
* 10-period volatility
* 21-period volatility
* Annualized volatility using `√252`

### News Intelligence

* Config-driven financial-news queries
* Pre-market and open-market query sets
* Asynchronous Tavily search
* Concurrent query execution
* Article quality filtering
* URL-based duplicate protection
* Semantic duplicate detection
* Embedding-based similarity analysis
* Relevance-score-based duplicate selection

### Probabilistic News Classification

Each processed article can be represented using:

```text
p_bull
p_neutral
p_bear
confidence
importance
novelty
affected_scope
event_type
```

The directional probabilities are constrained to form a valid probability distribution:

```text
p_bull + p_neutral + p_bear = 1
```

### Engineering

* Async I/O
* Controlled concurrency
* Incremental feature computation
* Modular pipeline architecture
* Pydantic validation
* DuckDB analytical storage
* YAML-based configuration
* Python package structure using `src/`
* Optional C++/Python integration through `pybind11`

---

# System Architecture

At a high level, the current system consists of two major processing branches.

```text
                         ┌─────────────────────┐
                         │     Main Runner     │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
          ┌────────────────────┐        ┌────────────────────┐
          │  Market Data Flow  │        │   News Data Flow   │
          └─────────┬──────────┘        └─────────┬──────────┘
                    │                             │
                    ▼                             ▼
          ┌────────────────────┐        ┌────────────────────┐
          │   NIFTY Ingestion  │        │  News Ingestion    │
          └─────────┬──────────┘        └─────────┬──────────┘
                    │                             │
                    ▼                             ▼
          ┌────────────────────┐        ┌────────────────────┐
          │   Data Validation  │        │  Quality Filtering │
          └─────────┬──────────┘        └─────────┬──────────┘
                    │                             │
                    ▼                             ▼
          ┌────────────────────┐        ┌────────────────────┐
          │   Return Engine    │        │ Semantic Dedup     │
          └─────────┬──────────┘        └─────────┬──────────┘
                    │                             │
                    ▼                             ▼
          ┌────────────────────┐        ┌────────────────────┐
          │ Volatility Engine  │        │ News Classification│
          └─────────┬──────────┘        └─────────┬──────────┘
                    │                             │
                    ▼                             ▼
          ┌────────────────────┐        ┌────────────────────┐
          │      DuckDB        │        │      DuckDB        │
          └────────────────────┘        └────────────────────┘
```

The two branches are executed concurrently by the main orchestration layer.

---

# Market Data Pipeline

The market-data pipeline currently processes NIFTY 50 index data through several stages.

```text
NIFTY 50
   │
   ▼
Data Ingestion
   │
   ▼
OHLC Validation
   │
   ▼
DuckDB Raw Storage
   │
   ├───────────────┐
   ▼               ▼
Returns         Volatility
   │               │
   ▼               ▼
DuckDB          DuckDB
```

## NIFTY Data Ingestion

The system uses `yfinance` to retrieve NIFTY 50 index data through the `^NSEI` ticker.

The ingestion layer supports:

* Initial historical download
* Incremental downloads
* Daily data
* OHLC persistence
* Duplicate-safe insertion

The initial configuration currently uses a historical bootstrap period of five years.

The stored schema is:

```text
date
open
high
low
close
```

Volume is intentionally removed during ingestion because the current project focuses on the NIFTY index rather than treating index-level volume as a conventional equity-volume series.

---

## Data Validation

Market candles are validated using Pydantic before being written to storage.

The validation layer checks conditions including:

```text
High >= Open
High >= Close

Low <= Open
Low <= Close

Low <= High
```

This provides a schema boundary between externally sourced market data and downstream feature calculations.

---

# Return Engineering

Returns are generated directly inside DuckDB using window functions.

The current implementation calculates:

```text
return_1
return_5
return_10
return_20
log_return_1
```

For example:

```text
return_n = Close_t / Close_(t-n) - 1
```

The log return is calculated as:

```text
log_return_1 = ln(Close_t / Close_(t-1))
```

The return pipeline supports incremental processing and only calculates new observations after the previously stored maximum date.

---

# Volatility Engineering

The volatility engine currently calculates rolling sample standard deviation of one-period log returns over:

```text
3 periods
5 periods
7 periods
10 periods
21 periods
```

The resulting volatility estimates are annualized using:

```text
σ_annualized = σ_window × √252
```

The volatility engine also supports incremental processing.

When new observations arrive, the pipeline retrieves the required previous observations to construct the rolling windows instead of recalculating the entire historical dataset.

---

# News Intelligence Pipeline

The news pipeline provides the second major information source for the market-state representation.

```text
YAML Queries
     │
     ▼
Async Tavily Search
     │
     ▼
Flatten Results
     │
     ▼
Quality Filtering
     │
     ▼
Raw News Database
     │
     ▼
Embedding Generation
     │
     ▼
Semantic Similarity
     │
     ▼
Deduplicated News
     │
     ▼
Structured LLM Classification
     │
     ▼
Sentiment / Event Metadata
     │
     ▼
Sentiment Database
```

---

## Query-Driven News Collection

News queries are stored externally in:

```text
config/news_queries.yaml
```

The configuration currently separates queries into:

```text
pre_market
open_market
```

and organizes them across categories such as:

* Macro
* RBI policy
* Global markets
* Crude and currency
* FII/DII
* Volatility
* Derivatives
* Banking
* IT
* Commodities
* Geopolitics
* Corporate events
* Sector rotation

This keeps the search universe configuration-driven rather than hard-coded inside the processing logic.

---

## Asynchronous News Retrieval

The Tavily integration uses asynchronous requests.

Multiple queries are processed concurrently with a semaphore controlling the maximum number of simultaneous requests.

The current implementation uses:

```text
Concurrency: 15
Maximum results per query: 3
Search depth: advanced
Time range: day
```

This allows the news pipeline to collect information across multiple market-relevant categories without processing every query sequentially.

---

## News Quality Filtering

Before articles enter the downstream processing pipeline, they are filtered using basic data-quality requirements.

An article must contain:

```text
title
content
url
```

and must satisfy a minimum Tavily relevance score.

The current default threshold is:

```text
score >= 0.40
```

---

# Semantic News Deduplication

Financial news providers frequently publish multiple articles covering the same event.

A URL-level duplicate check alone cannot identify semantically equivalent articles from different sources.

The project therefore uses:

```text
Sentence Transformers
        │
        ▼
all-MiniLM-L6-v2
        │
        ▼
Normalized Embeddings
        │
        ▼
Cosine Similarity
        │
        ▼
Semantic Duplicate Detection
```

The deduplicator combines:

```text
Article Title + First 500 characters of Content
```

and generates normalized embeddings.

Articles with cosine similarity above the current threshold of:

```text
0.85
```

are treated as semantic duplicates.

When duplicates are detected, the article with the higher Tavily relevance score is retained.

---

# Probabilistic News Representation

The news-classification layer is designed to avoid turning an article directly into a deterministic market prediction.

Instead, the structured model represents the article using a probability distribution:

```text
p_bull
p_neutral
p_bear
```

with:

```text
p_bull + p_neutral + p_bear = 1
```

For example, an article could conceptually be represented as:

```text
p_bull    = 0.20
p_neutral = 0.55
p_bear    = 0.25
```

This does **not** mean:

```text
"NIFTY will fall."
```

It represents the model's classification of the **potential directional effect contained in the information**.

Additional metadata includes:

| Field            | Purpose                                      |
| ---------------- | -------------------------------------------- |
| `confidence`     | Confidence in the classification             |
| `importance`     | Potential market significance                |
| `novelty`        | How new or unique the information is         |
| `affected_scope` | Market segments/sectors potentially affected |
| `event_type`     | Type of financial/economic event             |

Supported event categories include:

```text
monetary_policy
inflation
economic_data
corporate
earnings
merger_acquisition
regulatory
government_policy
geopolitical
global_market
currency
commodities
derivatives
market_structure
analyst_rating
management_commentary
other
```

The current classifier is explicitly instructed to **classify the information rather than predict whether NIFTY will actually rise or fall**.

---

# Data Storage

DuckDB is used as the primary analytical storage layer.

The current system separates different processing stages into independent databases.

```text
data/
├── raw/
│   └── nifty.db
│
├── returns/
│   └── nifty_returns.db
│
├── volatility/
│   └── nifty_volatility.db
│
└── news/
    ├── raw_news.db
    ├── dedup_news.db
    └── sentiment_news.db
```

This provides clear separation between:

```text
Raw Data
   ↓
Derived Features
   ↓
Processed Intelligence
```

and makes individual stages independently queryable.

---

# Incremental Processing

One of the main engineering goals of the project is avoiding unnecessary recomputation.

The market-data workflow tracks the latest processed date and uses it to determine what needs to be processed on subsequent runs.

The return engine only inserts observations after the latest calculated date while retrieving the required historical lookback for rolling calculations.

The volatility engine similarly combines the necessary previous observations with newly available returns before calculating new volatility values.

This gives the processing layer a basic incremental-data architecture rather than rebuilding the entire feature store on every execution.

---

# Concurrency and Orchestration

The main runner executes the market-data and news branches concurrently.

Conceptually:

```python
await asyncio.gather(
    asyncio.to_thread(run_nifty_pipelines),
    run_news_pipelines()
)
```

This allows:

```text
Market Data Pipeline
        │
        │
        ├──── concurrent execution ────┐
        │                              │
        ▼                              ▼
NIFTY ingestion                  News ingestion
Returns                          Deduplication
Volatility                       Classification
```

The news pipeline itself also uses asynchronous concurrency for external API requests and concurrent LLM processing.

The sentiment pipeline currently limits LLM processing through an asynchronous semaphore with a default concurrency of `10`.

---

# Technology Stack

| Category                  | Technology              |
| ------------------------- | ----------------------- |
| Language                  | Python 3.11+            |
| Data Processing           | Pandas, NumPy           |
| Analytical Database       | DuckDB                  |
| Market Data               | yfinance                |
| News Search               | Tavily                  |
| LLM Integration           | LangChain OpenAI        |
| Structured Validation     | Pydantic                |
| Embeddings                | Sentence Transformers   |
| Async Processing          | asyncio                 |
| Configuration             | YAML                    |
| Testing                   | pytest / pytest-asyncio |
| Linting                   | Ruff                    |
| Type Checking             | mypy                    |
| Optional Native Extension | pybind11 / C++          |

---

# Project Structure

```text
rawatrahul14-probabilistic-index-regime-engine/
│
├── main.py
├── pyproject.toml
│
├── config/
│   ├── news_queries.yaml
│   └── nifty_date.yaml
│
└── src/
    └── regime_engine/
        │
        ├── data/
        │   ├── dedup_news.py
        │   ├── news_sentiment.py
        │   ├── nifty_ingest.py
        │   ├── nifty_returns.py
        │   ├── nifty_validator.py
        │   ├── nifty_volatility.py
        │   └── raw_news.py
        │
        ├── models/
        │   └── nifty_model.py
        │
        ├── news/
        │   ├── agents/
        │   │   └── news_sentiment.py
        │   │
        │   ├── apis/
        │   │   └── async_tavily.py
        │   │
        │   ├── models/
        │   │   ├── deduplicator.py
        │   │   ├── embedding_model.py
        │   │   └── sentiment_model.py
        │   │
        │   └── schemas/
        │
        ├── pipelines/
        │   ├── news_dedup_pipeline.py
        │   ├── news_ingestion_pipeline.py
        │   ├── news_sentiment_pipeline.py
        │   ├── nifty_date_change_pipeline.py
        │   ├── nifty_pipeline.py
        │   ├── nifty_returns_pipeline.py
        │   └── nifty_volatility_pipeline.py
        │
        └── utils/
            ├── news_utils.py
            └── nifty_utils.py
```

### Architectural Responsibilities

**`data/`**

Handles persistence and quantitative data processing.

**`models/`**

Contains structured data models and validation logic.

**`news/`**

Contains external news APIs, embeddings, deduplication, and LLM-based classification.

**`pipelines/`**

Provides orchestration boundaries around individual processing stages.

**`utils/`**

Contains configuration, date management, data transformation, and supporting utilities.

---

# Installation

## Requirements

* Python `3.11+`
* Git
* Internet connection for external market/news APIs
* API key for Tavily
* API key for OpenAI

Clone the repository:

```bash
git clone https://github.com/RawatRahul14/Probabilistic-Index-Regime-Engine.git

cd Probabilistic-Index-Regime-Engine
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the project:

```bash
pip install -e .
```

For development dependencies:

```bash
pip install -e ".[dev]"
```

For optional C++/Python integration:

```bash
pip install -e ".[cpp]"
```

---

# Configuration

The system uses environment variables for external API credentials.

Set:

```text
OPENAI_API_KEY
TAVILY_API_KEY
```

### Windows PowerShell

```powershell
$env:OPENAI_API_KEY="your-openai-key"
$env:TAVILY_API_KEY="your-tavily-key"
```

### Linux / macOS

```bash
export OPENAI_API_KEY="your-openai-key"
export TAVILY_API_KEY="your-tavily-key"
```

News-search behaviour can be modified through:

```text
config/news_queries.yaml
```

The NIFTY incremental-update state is maintained through:

```text
config/nifty_date.yaml
```

---

# Running the Engine

The complete pipeline can be started through:

```bash
python main.py
```

The main runner starts:

```text
NIFTY Pipeline
    ├── Date handling
    ├── Data ingestion
    ├── Returns
    └── Volatility

News Pipeline
    ├── News ingestion
    ├── Deduplication
    └── Sentiment classification
```

Both branches are orchestrated concurrently.

---

# Current Implementation

The current release is **v0.4.0** and is classified as **Pre-Alpha**.

### Implemented

* NIFTY 50 historical data ingestion
* Incremental NIFTY data updates
* OHLC validation
* DuckDB-based market-data storage
* Multi-horizon return calculations
* Log-return calculation
* Rolling annualized volatility
* Incremental return computation
* Incremental volatility computation
* Configurable financial-news queries
* Asynchronous Tavily ingestion
* News quality filtering
* Raw news persistence
* Semantic news deduplication
* Embedding-based similarity
* Structured LLM news classification
* Probabilistic bullish/neutral/bearish news representation
* News metadata classification
* Concurrent news processing
* Concurrent market/news pipeline execution

### In Development

The current implementation is primarily the **data and intelligence foundation** of the larger regime-engine architecture.

The complete market-regime modelling layer is still under development.

---

# Roadmap

The project is intended to evolve from a feature and intelligence pipeline into a complete probabilistic regime-research platform.

## Phase 1 — Data Foundation

* [x] NIFTY data ingestion
* [x] Data validation
* [x] Incremental updates
* [x] Return calculations
* [x] Volatility calculations
* [x] DuckDB persistence

## Phase 2 — News Intelligence

* [x] Config-driven news queries
* [x] Async news retrieval
* [x] News filtering
* [x] Semantic deduplication
* [x] Structured sentiment classification
* [x] Event classification
* [x] Market-scope classification

## Phase 3 — Market State Construction

* [ ] Unified market-state schema
* [ ] Trend features
* [ ] Breadth features
* [ ] India VIX integration
* [ ] Derivatives features
* [ ] Cross-asset features
* [ ] News aggregation
* [ ] News-pressure features

## Phase 4 — Regime Modelling

* [ ] Market-state clustering
* [ ] Probabilistic regime classification
* [ ] Regime transition modelling
* [ ] State persistence analysis
* [ ] Distribution-shift analysis

## Phase 5 — Outcome Modelling

* [ ] Forward-return distributions
* [ ] Conditional outcome probabilities
* [ ] Multi-horizon forecasting
* [ ] Probability calibration
* [ ] Out-of-sample evaluation

## Phase 6 — Research & Evaluation

* [ ] Walk-forward evaluation
* [ ] Backtesting framework
* [ ] Regime-specific performance analysis
* [ ] Calibration metrics
* [ ] Robustness testing
* [ ] Transaction-cost modelling

## Phase 7 — Production Research Infrastructure

* [ ] Broker/data-provider integration
* [ ] Real-time market-state updates
* [ ] Monitoring
* [ ] Experiment tracking
* [ ] Feature versioning
* [ ] Research dashboards

---

# Limitations

This project is currently a **research and engineering prototype**, not a production trading system.

Important limitations include:

* The complete probabilistic regime-detection layer is not yet implemented.
* Current market features are primarily based on NIFTY price-derived data.
* News classification is dependent on an external LLM.
* News relevance depends on the quality of the external search provider.
* Semantic deduplication uses a fixed similarity threshold.
* No live broker execution is currently implemented.
* No claim is made that the current news probabilities represent calibrated market probabilities.
* The current implementation does not establish profitable trading performance.
* Backtesting and out-of-sample validation of the complete regime model are still future components.

These limitations are intentional boundaries around the current research stage.

---

# Disclaimer

This project is intended for **research, experimentation, and educational purposes**.

It is not financial advice and does not constitute a recommendation to buy, sell, or hold any financial instrument.

The probabilistic outputs generated by the news-classification component represent model classifications of information and should not be interpreted as guaranteed forecasts of market movements.

---

# License

This project is released under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

## Author

**Rahul Rawat**

Quantitative Finance · Machine Learning · Data Engineering

GitHub: [@RawatRahul14](https://github.com/RawatRahul14)

Repository: [Probabilistic Index Regime Engine](https://github.com/RawatRahul14/Probabilistic-Index-Regime-Engine)