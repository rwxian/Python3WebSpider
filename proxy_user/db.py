"""
存储模块，把代理以ip:端口的形式存储到redis中
"""

MAX_SCORE = 100                 # 最大分数
MIN_SCORE = 0                   # 最小分数
INITIAL_SCORE = 10              # 初始分数
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_PASSWORD = '123456'
REDIS_KEY = 'proxies'           # 所有代理的键名

from random import choice
import redis


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        print('redis连接成功'.center(30, '-'))

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return:      添加结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果最高分不存在，按排名获取
        :return:
        """
        result = self.db.zrangebyscore(REDIS_KEY, 0, 100)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrangebyscore(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise Exception('代理池为空！')

    def decrease(self, proxy):
        """
        代理值减一分，分数小于最小值，则代理删除
        :param proxy:
        :return:
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1!')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '被移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断代理是否存在
        :param proxy:
        :return:
        """
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy:
        :return:
        """
        print('代理', proxy, '可用， 分数设置为', MAX_SCORE)
        # return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)
        return self.db.zadd(REDIS_KEY, {proxy, MAX_SCORE})

    def count(self):
        """
        获取数量
        :return:
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)


if __name__ == '__main__':
    redis = RedisClient()
    redis.add('123.232.12.23:8080')
    a = redis.all()
    print(a)

