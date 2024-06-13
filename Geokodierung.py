import urllib.parse
import requests

params = urllib.parse.quote_plus("(Bad Lippspringe), Auguste-Viktoria-Allee 25")
print(params)
params = params.replace("+", "%20")
print(params)

url = 'https://geocoder.fbg-hsbo.de/geocoder/geocode/query-string?q='
url = url + params
geocoder = requests.get(url)

result = geocoder.json()
print(result)