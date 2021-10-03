from bs4 import BeautifulSoup
import requests, os, json

os.chdir("..")

post_base_url = r"https://api.anonfiles.com/upload?token=06eaf77f939e5624"
file_url = r"data/temp/508372340904558603_627193385033_tempGraph.png"

f = open(file_url, 'rb')
files = {"file": (file_url, f)}
re = requests.post(post_base_url, files = files)
r = requests.get(json.loads(re.text)["data"]["file"]["url"]["full"])
soup = BeautifulSoup(r.text, features="lxml")
images = soup.find_all('img')
for img in images:
    if img.has_attr('src'):
        if json.loads(re.text)["data"]["file"]["metadata"]["id"] in img["src"]:
            print(img["src"])
