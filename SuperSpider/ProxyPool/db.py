import re
import redis
from settings import *


class RedisClient(object):
    def __init__(self, host=REDIES_HOST, port=REDIES_PORT, password=REDIES_PASSWORD, db=DB_NUMBER):
        """连接数据库"""
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db)

    def get_count(self):
        """查询代理总数"""
        count = self.db.scard(REDIES_KEY)
        # str = "当前代理总数为【{}】".format(count)
        return count

    def save(self, proxy):
        """保存代理"""
        if self.get_count() >= MAX_PROXIES:
            print("代理池已满，请删除或初始化")
            return None
        else:
            self.db.sadd(REDIES_KEY, proxy)

    def get_random(self):
        """随机获取代理"""
        return self.db.srandmember(REDIES_KEY)

    def del_one(self, proxy):
        """删除指定代理"""
        result = self.db.srem(REDIES_KEY, proxy)
        return result

    def del_all(self):
        """清空代理池"""
        members = self.db.smembers(REDIES_KEY)
        proxies = []
        for proxy in members:
            proxies.append(proxy.decode('utf-8'))
        # print(proxies)
        result = self.db.srem(REDIES_KEY, *proxies)
        return result


if __name__ == '__main__':
    db = RedisClient()
    db.get_count()
