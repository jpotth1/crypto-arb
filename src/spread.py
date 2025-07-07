import pandas as pd

def compute_spread(bin_csv: str, kra_csv: str, trade_size: float = 1.0, taker_fee_rate: float = 0.001, slippage: float = 0.001) -> pd.DataFrame:
    """
    Load two CSVs of OHLCV data, merge on timestamp, 
    compute the price spread, and flag positive spreads.

    Args:
        bin_csv: Path to Binance (or Binance.US/Coinbase) CSV
        kra_csv: Path to Kraken CSV
        trade_size: Units of asset per trade (default 1.0)
        taker_fee_rate: Fee rate per trade side (default 0.001)
        slippage: Slippage percentage (default 0.0005)

    Returns:
        DataFrame with columns:
          - ts: timestamp
          - open_bin, high_bin, low_bin, close_bin, vol_bin
          - open_kra, high_kra, low_kra, close_kra, vol_kra
          - spread: close_bin - close_kra
          - total_fee: total taker fee for a round-trip trade
          - min_spread: minimum spread to break even
          - signal_long: True where spread > min_spread (buy binance, sell kraken)
          - signal_short: True where spread < -min_spread (buy kraken, sell binance)
    """
    # Read data
    df_bin = pd.read_csv(bin_csv)
    df_kra = pd.read_csv(kra_csv)

    # Convert 'ts' from milliseconds to datetime
    df_bin['ts'] = pd.to_datetime(df_bin['ts'], unit='ms')
    df_kra['ts'] = pd.to_datetime(df_kra['ts'], unit='ms')

    # Merge on timestamp
    df = pd.merge(
        df_bin, df_kra,
        on='ts',
        suffixes=('_bin', '_kra')
    )

    # Compute spread
    df['spread'] = df['close_bin'] - df['close_kra']
    # Add slippage to the fee calculation
    effective_fee_rate = taker_fee_rate + slippage
    df['total_fee'] = trade_size * effective_fee_rate * (df['close_bin'] + df['close_kra'])
    df['min_spread'] = df['total_fee'] / trade_size  # minimum spread to break even

    # Signal for both directions
    df['signal_long'] = df['spread'] > df['min_spread']   # Buy on binance, sell on kraken
    df['signal_short'] = df['spread'] < -df['min_spread'] # Buy on kraken, sell on binance

    return df
