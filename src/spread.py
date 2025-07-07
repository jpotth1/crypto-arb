import pandas as pd

def compute_spread(bin_csv: str, kra_csv: str) -> pd.DataFrame:
    """
    Load two CSVs of OHLCV data, merge on timestamp, 
    compute the price spread, and flag positive spreads.

    Args:
        bin_csv: Path to Binance (or Binance.US/Coinbase) CSV
        kra_csv: Path to Kraken CSV

    Returns:
        DataFrame with columns:
          - ts: timestamp
          - open_bin, high_bin, low_bin, close_bin, vol_bin
          - open_kra, high_kra, low_kra, close_kra, vol_kra
          - spread: close_bin - close_kra
          - signal: True where spread > 0
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

    # Compute spread and simple signal
    df['spread'] = df['close_bin'] - df['close_kra']
    df['signal'] = df['spread'] > 0

    return df
