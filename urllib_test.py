import urllib.request
import urllib.parse


# response = urllib.request.urlopen('https://www.python.org')
# print(response.read().decode('utf-8'))
# print(type(response))
# print(response.status)
# print(response.getheaders())
# print(response.getheader('Server'))
#
# data = bytes(urllib.parse.urlencode({'word':'hello'}), encoding='utf8')
# respnose2 = urllib.request.urlopen('https://httpbin.org/post', data=data)
# print(respnose2.read())
#
# request = urllib.request.Request('https://python.org')
# respnose3 = urllib.request.urlopen(request)
# print(respnose3.read().decode('utf8'))

url = 'http://httpbin.org/post'
headers = {
    'User-Agent': 'Mozilla/4.0(compatible; MSIE 5.5; Windows NT)',
    'Host': 'httpbin.org'
}
dict = {
    'name': 'Germey'
}
data = bytes(urllib.parse.urlencode(dict), encoding='utf8')
req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))


