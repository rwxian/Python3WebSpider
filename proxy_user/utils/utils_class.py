"""
工具类
"""

import requests

headers = {
        'Content-Type': 'text/html;charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 '
                      'Safari/537.36 '
    }


def get_page(url):
    """通过requests来请求网页"""
    html = ''
    try:
        with requests.get(url, headers=headers, timeout=60) as response:
            if response.status_code == requests.codes.OK:
                print(response.status_code)
                # print(response.text)
                print('success')
                html = response.text
            else:
                print("请求出错，状态码：{}".format(response.status_code))
    except Exception as e:
        print('抓取网页{}失败！info: {}'.format(url, e))
    return html
