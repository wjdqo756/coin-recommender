import requests
from config import config

def send_alert_if_needed(coin_data):
    if coin_data["추천 신호"] == "진입 신호":
        message = f"""📢 [코인 진입 알림]
코인: {coin_data['코인']}
현재가: {coin_data['현재가(USDT)']} USDT
RSI: {coin_data['RSI(14)']}
MACD 히스토그램: {coin_data['MACD 히스토그램']}
신호: {coin_data['추천 신호']}"""

        send_telegram_message(message)

def send_telegram_message(msg):
    bot_token = config["telegram_bot_token"]
    chat_id = config["telegram_user_id"]
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": msg
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")