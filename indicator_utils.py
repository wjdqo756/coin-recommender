import numpy as np
import pandas as pd

def get_rsi(prices, period=14):
    delta = np.diff(prices)
    gain = delta.clip(min=0)
    loss = -delta.clip(max=0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def get_macd_histogram(prices, short=12, long=26, signal=9):
    prices = pd.Series(prices)
    ema_short = prices.ewm(span=short).mean()
    ema_long = prices.ewm(span=long).mean()
    macd = ema_short - ema_long
    signal_line = macd.ewm(span=signal).mean()
    hist = macd - signal_line
    return hist.iloc[-1]

def get_vwap(candles):
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df[['close', 'volume']] = df[['close', 'volume']].astype(float)
    cumulative_vp = (df['close'] * df['volume']).cumsum()
    cumulative_vol = df['volume'].cumsum()
    vwap = cumulative_vp / cumulative_vol
    return vwap.iloc[-1]

def get_bollinger_bands(prices, period=20, num_std=2):
    prices = pd.Series(prices)
    ma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper = ma + (std * num_std)
    lower = ma - (std * num_std)
    return upper.iloc[-1], lower.iloc[-1]

def get_volume_spike_ratio(candles):
    volumes = [float(c[5]) for c in candles]
    avg_vol = np.mean(volumes[:-1])
    curr_vol = volumes[-1]
    return curr_vol / avg_vol if avg_vol > 0 else 0