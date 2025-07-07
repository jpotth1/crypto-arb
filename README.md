# Crypto Arbitrage Bot

**Goal:** Paper-trade BTC/USD arbitrage between two exchanges.

## Project Structure
- `data/` — raw CSV price data
- `notebooks/` — Jupyter notebooks for EDA and backtests
- `src/` — reusable Python modules (e.g. spread calculator)
- `requirements.txt` — Python dependencies

## Getting Started
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jupyter lab
