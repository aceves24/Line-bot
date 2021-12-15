from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('vfx8FZlhOJ733mUyNjP6Dkw1WXZuX5G9eTpwvbaxh2WqwospdqwP58SpKHSfYK9HzOo/EYAcLL+EdKg0QD3bQ0tCg5aTXHH0ZEcqz3orh0eaqMJJyAYqmkPjPuZmsfW/wIbs4X3AscGtLAxa1PzNzwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d20b4bb39e04f361d2d5e07e0d255065')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    s = '你吃飯了嗎'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s))


if __name__ == "__main__":
    app.run()