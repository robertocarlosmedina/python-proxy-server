import requests

url = 'http://192.168.1.40:3001/example.html'
myobj = {'email': 'eej@uta.cv', 'password':'pasojno32'}

x = requests.post(url, data = myobj)

print(x.json)