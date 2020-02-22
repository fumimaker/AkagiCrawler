import requests
import json

# webhookURLを指定
webhook_url = "https://hooks.slack.com/services/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"

# 送信するテキストを定義
text = "PythonでSlackにメッセージを送るよ"

# Slackに送信する
requests.post(webhook_url, data=json.dumps({"text": text
}))
