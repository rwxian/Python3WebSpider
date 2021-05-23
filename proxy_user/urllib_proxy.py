from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener


proxy = '127.0.0.1:8001'
proxy_handler = ProxyHandler({
    'http': 'http://' + proxy,
    'https:': 'https://' + proxy
})
opener = build_opener(proxy_handler)
try:
    response = opener.open('https://www.google.com/')
    print(response.read().decode('utf-8'))
except Exception as e:
    print(e.reason)
