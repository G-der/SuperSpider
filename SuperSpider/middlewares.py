# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from ProxyPool.db import RedisClient
from scrapy import signals


class SuperspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SuperspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self, crawler):
        print('[' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())) + ']', "【init】")
        self.proxy = None  # 默认代理为空，使用真实IP
        self.db = RedisClient()

    def infoprint(self, message):
        print('[' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())) + ']【Info】' + message)

    def get_proxy(self):
        """随机获取代理"""
        try:
            proxy = self.db.get_random().decode('utf-8')
            return "http://{}".format(proxy)
        except Exception as e:
            print('[' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())) + ']', '【获取代理失败!】')
            return None

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        """处理请求"""
        self.infoprint('【是否重试】:' + ('是' if request.meta.get('retry') else '否'))
        old_proxy = request.meta.get('proxy')
        if self.proxy is None or old_proxy is None or self.proxy == request.meta.get('proxy'):
            # 请求被重来，更换代理
            proxy = self.get_proxy()
            self.infoprint('更换代理为:{}'.format(proxy))
            if proxy:
                self.proxy = proxy
        request.meta['proxy'] = self.proxy
        spider.info('【request】' + self.proxy + ' URL:' + request.url)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        """处理响应"""
        if response.status != 200:
            if response.status == 302:
                self.infoprint('【被拦截】:' + self.proxy)
                spider.logger.warning('【被拦截】:' + self.proxy)
            elif response.status == 404:
                self.infoprint('【无法找到文件】:' + self.proxy + ' URL:' + request.url)
                spider.logger.warning('【无法找到文件】:' + self.proxy + ' URL:' + request.url)
            else:
                self.infoprint('【未知】' + self.proxy + ' ' + str(response.status) + ' URL:' + request.url)
                spider.logger.warning('【未知】' + self.proxy + ' ' + str(response.status) + ' URL:' + request.url)

            return self.get_retry_request(request)
        elif '用户访问安全认证' in response.text:
            self.infoprint('【出现安全认证】' + response.url)
            spider.logger.warning('【出现安全认证】' + response.url)
            return self.get_retry_request(request)

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        try:
            oserror = str(exception.osError)
            if oserror == "10060" or oserror == "10061":
                self.infoprint('【exception】' + request.url + ' ' + str(exception.args))
                spider.logger.error('【exception】' + request.url + ' ' + str(exception.args))
            else:
                self.infoprint('【exception】' + request.url + ' ' + str(exception.osError))
                spider.logger.error('【exception】' + request.url + ' ' + str(exception.osError))
        except:
            try:
                self.infoprint('【exception】' + request.url + ' ' + str(exception))
                spider.logger.error('【exception】' + request.url + ' ' + str(exception))
            except:
                pass
            pass

        self.infoprint('【请求错误】重试')
        spider.logger.info('【请求错误】重试')

        # 重试
        return self.get_retry_request(request)

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def get_retry_request(self, request):
        """获取要重试的请求"""
        try:
            self.proxy = None  # 重置代理
            retry_request = request.copy()
            retry_request.dont_filter = True  # 禁止去重
            retry_request.meta['retry'] = time.time()
            return retry_request
        except Exception as e:
            self.infoprint('【get_retry_request】【获取要重试的请求出错】' + str(e))
            return None
