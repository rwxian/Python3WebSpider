"""

"""

from .db import RedisClient
from .crawler import Crawler


POOL_UPPER_THRESHOLD = 10000


class Getter:
    """动态调用crawl开头到方法，获取抓取到到代理，将其加入到数据库存储起来"""
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        :return:
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print("获取器开始执行".center(20, '='))
        if not self.is_over_threshold():                # 未达到代理池限制
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:                   # 把代理保存到redis
                    self.redis.add(proxy)
