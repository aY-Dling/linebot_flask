# linebot_flask.py
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage, TextSendMessage

import os
import requests

app = Flask(__name__)

# 替換為你的 LINE 資訊
LINE_CHANNEL_ACCESS_TOKEN = '你的 Channel Access Token'
LINE_CHANNEL_SECRET = '你的 Channel Secret'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 LINE 傳來的資料
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 圖片訊息處理
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_id = event.message.id
    image_content = line_bot_api.get_message_content(message_id)
    
    # 儲存圖片
    path = f"received_images/{message_id}.jpg"
    os.makedirs("received_images", exist_ok=True)
    with open(path, "wb") as f:
        for chunk in image_content.iter_content():
            f.write(chunk)

    # 回覆使用者
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="圖片已接收並儲存！")
    )

# 測試用 - 可加上
@app.route("/")
def index():
    return "LINE Bot is running!"

if __name__ == "__main__":
    app.run(port=5000)
