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

line_bot_api = LineBotApi('q+ZNACXPzKHrgyHGoDQOP+ZhshM31lQAXA78xl0u+sUIjs8uxqSG7qgypEer/ZxjzOo/EYAcLL+EdKg0QD3bQ0tCg5aTXHH0ZEcqz3orh0eaQ2SyKA8yD2J/ASklAlfHD4BHWPMfrZxTEbRjkn+wFQdB04t89/1O/w1cDnyilFU=')
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()