import requests
import json

from sys import argv

url = 'http://0.0.0.0:5000/api/'

test = argv[1:]

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

r = requests.post(url, data=json.dumps(test), headers=headers)
print(r, r.text)
