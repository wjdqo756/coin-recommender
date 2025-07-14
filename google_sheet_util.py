import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import config
from datetime import datetime

# 구글 인증 연결
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# 시트 열기
sheet = client.open_by_key(config["sheet_id"]).sheet1

def update_sheet(data):
    sheet.clear()
    header = ["날짜", "코인", "현재가(USDT)", "RSI(14)", "MACD 히스토그램", "추천 신호"]
    sheet.append_row(header)

    today = datetime.today().strftime("%Y-%m-%d %H:%M")
    for row in data:
        sheet.append_row([
            today,
            row["코인"],
            row["현재가(USDT)"],
            row["RSI(14)"],
            row["MACD 히스토그램"],
            row["추천 신호"]
        ])