import requests
import os

SHOP_ID = 17764
SITECD = "e014001536"
DATE = "2026-03-14"
TARGET_HEADCOUNT = 2
TARGET_TIME = "11:00"

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

URL = f"https://ebicaapi-for-booking.ebica.jp/booking/v2_1/stocks?shop_id={SHOP_ID}&sitecd={SITECD}&reservation_date={DATE}"

def send_discord(message):
    requests.post(WEBHOOK_URL, json={"content": message})

def check_availability():
    res = requests.get(URL)
    data = res.json()

    for stock in data.get("stocks", []):
        if stock["headcount"] == TARGET_HEADCOUNT:
            for t in stock["times"]:
                if t["time"] == TARGET_TIME:
                    return t["sets"] > 0
    return False

send_discord("✅ テスト通知です（GitHub Actions動作確認）")
