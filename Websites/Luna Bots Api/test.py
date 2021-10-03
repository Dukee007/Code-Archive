import requests

r=requests.get("http://localhost:5000/botupdate/", headers={"authorization":"*Y*&£G**BBIBUIYG(*&^TG*(Y675y0(UH$&*GBt976r6", "bot": "nsfw", "api_request": "premium_users"})

data = json.loads(r.text)
print(str(data))
