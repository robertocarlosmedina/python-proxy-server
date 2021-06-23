import requests

url = 'http://192.168.88.18:3002/example.html'
myobj = {'email': 'eej@uta.cv', 'password':'pasojno32'}

x = requests.post(url, data = myobj)

print(x.text)