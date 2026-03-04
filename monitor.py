import os
import requests
from flask import Flask, request, abort

app = Flask(__name__)

# --- 設定（環境変数から読み込む） ---
SHOP_ID = 17764
SITECD = "e014001536"
DATE = "2026-03-14"
TARGET_HEADCOUNT = 2
TARGET_TIME = "11:00"

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") # 安全のためのパスワード

URL = f"https://ebicaapi-for-booking.ebica.jp/booking/v2_1/stocks?shop_id={SHOP_ID}&sitecd={SITECD}&reservation_date={DATE}"

def check_availability():
    res = requests.get(URL)
    data = res.json()
    for stock in data.get("stocks", []):
        if stock["headcount"] == TARGET_HEADCOUNT:
            for t in stock["times"]:
                if t["time"] == TARGET_TIME:
                    return t["sets"] > 0
    return False

@app.route("/check")
def monitor():
    # 安全性の担保：クエリパラメータの token が一致するかチェック
    token = request.args.get("token")
    if token != ACCESS_TOKEN:
        abort(403) # 不正なアクセスは拒否

    if check_availability():
        requests.post(WEBHOOK_URL, json={"content": f"🔥 {DATE} {TARGET_TIME} 空きが出ました！"})
        return "Found and Notified", 200
    
    return "No availability", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
