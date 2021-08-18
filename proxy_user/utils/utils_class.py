"""
工具类
"""

import requests

def get_page(url):
    html = ''
    headers = {
        'Content-Type': 'text/html;charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    try:
        with requests.get(url, headers=headers, timeout=60) as response:
            print(response.status_code)
            if response.status_code == requests.codes.OK:
                # print(response.text)
                print('success')
                html = response.text
    except Exception as e:
        print('抓取网页{}失败！info: {}'.format(url, e))
    return html