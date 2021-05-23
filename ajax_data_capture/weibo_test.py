from urllib.parse import urlencode
import requests
from pyquery import PyQuery


base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_page(since_id):
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'since_id': since_id
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json):
    items = json.get('data').get('cards')
    for item in items:
        item = item.get('mblog')
        weibo = {'id': item.get('id'), 'text': PyQuery(item.get('text')).text(),
                 'attitudes': item.get('attitudes_count'), 'reposts': item.get('reposts_count')}
        yield weibo


if __name__ == '__main__':
    for page in range(1, 10):
        json = get_page('4622435985393057')
        results = parse_page(json)
        for result in results:
            print(result)
