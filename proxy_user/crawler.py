"""
获取模块，用于从各大网站抓取代理
pip命令使用方式：python3 -m pip install xxx--v2.x.x
"""

import warnings

from deprecated.sphinx import deprecated

from utils import utils_class
from pyquery import PyQuery
from lxml import etree


class ProxyMetaclass(type):
    """
    Crawler的元类，方便Crawler进行扩展，后期需要添加新的代理时，只用在Crawler中添加以craw_开头的方法即可
    metaclass是类的模板，所以必须从`type`类型派生
    """

    def __new__(cls, name, bases, attrs):
        """__new__继承自object类，用于创建和返回一个新的对象，它作用在构造方法建造实例之前。Python中存在于类中的构造方法__init__（）负责将类实例化，
        而在__init__（）执行之前，__new__（）负责制造这样的一个实例对象，以便__init__（）去让该实例对象更加的丰富（为其添加属性等）。
        同时：__new__() 方法还决定是否要使用该__init__() 方法，因为__new__()可以调用其他类的构造方法或者直接返回别的对象来作为本类 的实例。
        此处的__new__()是添加ProxyMetaclass的属性
        :param cls: 当前准备创建的类的对象；
        :param name: 类的名字；
        :param bases: 类继承的父类集合；
        :param attrs: 类的方法集合。
        :return:
        """
        count = 0
        attrs['__CraslFunc__'] = []
        # 遍历attrs，获取类的所有方法，添加到__CraslFunc__中，把crawl开头的方法定义成了一个属性
        for k, v in attrs.items():
            if 'crawl_' in k and not k.__antations__['deprecated']:  # 方法以crawl_开头且方法未弃用
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


# class Crawler(object, metaclass=ProxyMetaclass):
class Crawler(object):
    """
    定义到各大网站抓取代理的方法，抓取后以ip: 端口的形式返回
    """

    def get_proxies(self, callback):
        """
        讲所有以crawl开头的方法调用一遍，获取每个方法返回的代理并组合成列表形式返回
        :param callback:
        :return:
        """
        proxies = []
        for proxy in eval("self.{}()".format(callback)):  # callback为方法名称，方法名称拼接后，执行方法抓取对应的代理，eval()方法可以把字符串当做函数运行
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    @deprecated(version='1.0', reason="此代理网站已不可用!")
    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 
        :return:
        """
        warnings.warn("此代理已不可用，建议弃用方法", DeprecationWarning)
        start_url = 'http://www.66ip.cn/{}/html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]  # 构造前5页的url
        for url in urls:
            print('Crawling：', url.center(10, '='))
            html = utils_class.get_page(url)
            if html:
                doc = PyQuery(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = int(tr.find('td:nth-child(2)').text())
                    yield ':'.join([ip, port])

    @deprecated(version='1.0', reason="此代理网站已不可用!")
    def crawl_proxy360(self):
        """
        获取Proxy360
        :return:
        """
        warnings.warn("此代理已不可用，建议弃用方法", DeprecationWarning)
        start_url = 'http://www.proxy360.cn/Region/China'
        print('Crawling', start_url)
        html = utils_class.get_page((start_url))
        if html:
            doc = PyQuery(html)
            lines = doc('div[name="list_proxy_ip"]').items()
            for line in lines:
                ip = line.find('.tbBottomLine:nth-child(1)').text()
                port = line.find('.tbBottomLine:nth-child(2)').text()
                yield ':'.join([ip, port])

    @deprecated(version='1.0', reason="此代理网站已不可用!")
    def crawl_goubanjia(self):
        warnings.warn("此代理已不可用，建议弃用方法", DeprecationWarning)
        start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
        html = utils_class.get_page(start_url)
        print(start_url)
        if html:
            doc = PyQuery(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ', '')

    @staticmethod
    def crawl_ihua(self, page_count=5):
        """小幻http代理，目前可用"""
        start_url = 'https://ip.ihuan.me/?page={}'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]  # 构造前5页的url
        try:
            for url in urls:
                html = utils_class.get_page(url)
                xpath_obj = etree.HTML(html)  # 构造xpath解析对象
                res = xpath_obj.xpath('//div[@class="table-responsive"]/table/tbody/tr')  # 获取到所有代理tr
                for tr in res:  # 循环tr，解析出ip和端口
                    tr_html = etree.tostring(tr)
                    host = etree.HTML(tr_html).xpath('//tr/td[1]/a/text()')
                    port = etree.HTML(tr_html).xpath('//tr/td[2]/text()')
                    yield ':'.join([host[0], port[0]])
        except Exception as e:
            raise e

    @staticmethod
    def crawl_kuaidaili(self, page_count=5):
        """
        快代理
        :return:
        """
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]  # 构造前5页的url
        try:
            for url in urls:
                html = utils_class.get_page(url)
                if len(html) > 1:
                    xpath_obj = etree.HTML(html)  # 构造xpath解析对象
                    res = xpath_obj.xpath('//*[@id="list"]/table/tbody/tr')  # 获取到所有代理tr
                    for tr in res:  # 循环tr，解析出ip和端口
                        tr_html = etree.tostring(tr)
                        host = etree.HTML(tr_html).xpath('//tr/td[1]/text()')
                        port = etree.HTML(tr_html).xpath('//tr/td[2]/text()')
                        yield ':'.join([host[0], port[0]])
                        # print(host[0] + ":" + port[0])
        except Exception as e:
            raise e


# if __name__ == '__main__':
#     crawl = Crawler()
#     daili666 = crawl.crawl_kuaidaili()
#     # a = crawl.crawl_daili66()
#     # print(daili666)
#     for i in daili666:
#         print(i)
#         print('=======================')
