import time
import requests
from indicator_utils import (
    get_rsi,
    get_macd_histogram,
    get_vwap,
    get_bollinger_bands,
    get_volume_spike_ratio
)
from google_sheet_util import update_sheet
from telegram_bot import send_alert_if_needed

def fetch_all_usdt_symbols():
    url = "https://api.binance.com/api/v3/ticker/price"
    all_tickers = requests.get(url).json()
    usdt_pairs = [t['symbol'] for t in all_tickers if t['symbol'].endswith('USDT')]
    return usdt_pairs

def fetch_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    return float(requests.get(url).json()['price'])

def fetch_klines(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
    return requests.get(url).json()

def analyze_coin(symbol):
    candles = fetch_klines(symbol)
    close_prices = [float(c[4]) for c in candles]

    rsi = get_rsi(close_prices)
    macd_hist = get_macd_histogram(close_prices)
    vwap = get_vwap(candles)
    bb_upper, bb_lower = get_bollinger_bands(close_prices)
    vol_spike = get_volume_spike_ratio(candles)
    price = fetch_price(symbol)

    signal = ""
    if rsi < 35 and macd_hist > 0 and price < bb_lower and vol_spike > 2:
        signal = "진입 신호"
    elif rsi > 70:
        signal = "과매수"
    else:
        signal = "관망"

    return {
        "코인": symbol,
        "현재가(USDT)": price,
        "RSI(14)": round(rsi, 2),
        "MACD 히스토그램": round(macd_hist, 4),
        "VWAP": round(vwap, 4),
        "BB_하단": round(bb_lower, 4),
        "볼스파이크": round(vol_spike, 2),
        "추천 신호": signal
    }

def main_loop():
    symbols = fetch_all_usdt_symbols()
    while True:
        results = []
        for sym in symbols:
            try:
                result = analyze_coin(sym)
                results.append(result)
                send_alert_if_needed(result)
            except Exception as e:
                print(f"분석 실패: {sym} / {e}")
        update_sheet(results)
        print("✅ 업데이트 완료. 10분 후 다시 실행됩니다.")
        time.sleep(600)

if __name__ == "__main__":
    main_loop()