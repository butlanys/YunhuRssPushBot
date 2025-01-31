import json,requests,base64,os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")  # bot token可在官网后台获取

def push(recvId, recvType, contentType, content):
    url = f"https://chat-go.jwzhd.com/open-apis/v1/bot/send?token={TOKEN}"
    payload = json.dumps({
        "recvId": recvId,
        "recvType": recvType,
        "contentType": contentType,
        "content": content
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(json.loads(response.text))
    #return json.loads(response.text)
