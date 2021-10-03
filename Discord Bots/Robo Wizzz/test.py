import requests

r = requests.get(f'https://www.googleapis.com/youtube/v3/videos?id=JempwycIUS0&key=AIzaSyADpCI6QgLOiG8PH2vRnuRCNq_VGkvAVaA&part=snippet', timeout=1)
print(r.text)
