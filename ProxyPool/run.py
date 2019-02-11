from catch import IPSpider
from db import RedisClient
from settings import *


class Runner(object):
    def __init__(self):
        self.crawl = IPSpider()
        self.db = RedisClient()

    def catch_ip(self):
        """抓取代理并保存"""
        proxies = self.crawl.crawl_89ip()
        for proxy in proxies:
            result = self.db.save(proxy)
            if not result:
                print('保存失败')
                break

    def del_all(self):
        """慎用：删除所有代理"""
        try:
            result = self.db.del_all()
            if result:
                print('清理成功')
            else:
                print('清理失败')
        except Exception as e:
            print('数据库为空')


def main():
    r = Runner()
    if DBINIT:  # 设置中选择清空数据库
        r.del_all()
    r.catch_ip()


if __name__ == '__main__':
    main()
