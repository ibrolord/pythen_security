import urllib3

http = urllib3.PoolManager()

response = http.request('GET',urlopen("https://www.nostarch.com"))

print(body.read())