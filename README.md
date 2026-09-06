# Probabilistic Index Regime Engine: A Quantitative NIFTY and Options Research Platform

## Project Overview

The **Probabilistic Index Regime Engine** is a quantitative research and options analytics designed around a simple idea:

> Financial Markets are uncertain, so a trading system should estimate probabilities and payoff distributions rather than produce deterministic BUY/SELL signals from a collection of indicators.

The system primarily focues on NIFTY50 and NIFTY options ecosystem.

The central research problem is:

$$
[P(\text{Future Market Outcome} \mid \text{Current Market State})]

$$

Where the market state can eventually include:

$$
[X_t = [\text{Returns}, \text{Volatility}, \text{Trend}, \text{Breadth}, \text{VIX}, \text{News}, \text{Derivatives}]]

$$

## Main Research Question

The project should eventually answer 4 major questions.

### 1. What state the market currently in?

$[P(R_t = r_i \mid X_t)]$

Probabilty Regimes:

- Bull / Low Volatility
- Bull / High Volatility
- Bear / Low Volatility
- Bear / High Volatility
- Sideways / Low Volatility
- Sideways / High Volatility

### 2. What could happen next?

$[P(R_{t+1} > 0) \mid X_t]$
$[P(R_{t+1} > 1) \mid X_t]$
$[P(R_{t+1} < -1) \mid X_t]$
$[P(R_{t+1} > b) \mid X_t]$

### 3. What does this impy for options?

$[P(S_t > K)]$
$[P(\pi_t > 0)]$
$[P(\pi_t > 0.5 C_0)]$
$[P(\pi_t)]$

### 4. Is the reward worth the risk?

Evaluate:

- Expected PnL
- Median PnL
- Probability of Profit
- Probability of Large Loss
- Value at Risk
- Expected Shortfall
- Maximum Drawdown
- Transaction costs

---
### Phase - 1: Market Data Infrastructure

v0.1.0 - NIFTY Historical Data Ingestion using `yfinance`.
```text
timestamp
open
high
low
close
```