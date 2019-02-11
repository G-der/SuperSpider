from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from SuperSpider import webmodel
import time
from SuperSpider.items import BaseItem

global model
model = webmodel.set_model()


def link_cath():
    rules = []
    try:
        pages = LinkExtractor(allow=model.page_link_Re,
                              restrict_xpaths=model.page_link_path)
        rules.append(Rule(pages, callback=None, follow=True))
    except:
        pass
    links = LinkExtractor(allow=model.comment_link_Re,
                          restrict_xpaths=model.comment_link_path)
    rules.append(Rule(links, callback="web_parse"))
    return rules


class SuperSpider(CrawlSpider):
    name = "CS"
    allowed_domains = model.allow_domains
    start_urls = model.start_urls
    rules = link_cath()

    def info(self, message, isPrint=True):
        # 控制台显示消息
        if isPrint == True:
            print('[' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())) + '][INFO]' + message)

        # Log文件输出
        self.logger.info(message)

    def warning(self, message, logOutput=True):
        # 控制台显示消息
        print('[' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())) + '][WARNING]' + message)

        # Log文件输出
        if logOutput == True:
            self.logger.warning(message)

    def error(self, message, logOutput=True):
        # 控制台显示消息
        print('[' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())) + '][ERROR]' + message)

        # Log文件输出
        if logOutput == True:
            self.logger.error(message)

    def web_parse(self, response):
        try:
            title = response.xpath(model.title_path).extract_first()
            for each in response.xpath(model.eath_path):
                username = each.xpath(model.username_path).extract_first()
                pushtime = each.xpath(model.pushtime_path).extract_first()
                comtpath = each.xpath(model.comment_path)
                comtstr = comtpath.xpath('string(.)').extract_first()
                # dic = {"username":username,"pushtime":pushtime,"comtstr":comtstr}
                # for item in dic:
                #     if dic[item] is None:
                #         print("获取元素【{}】失败：请检查网页内容或xpath".format(item))
                usergender = None
                userlocation = None
                try:
                    usergender = each.xpath(model.usergend_path).extract_first()
                except:
                    pass
                try:
                    userlocation = each.xpath(model.userloct_path).extract_first()
                except:
                    pass
                item = BaseItem()
                item['title'] = title
                item['collection'] = model.collection
                item['username'] = username
                item['usergender'] = usergender
                item['userlocation'] = userlocation
                item['comment_detail'] = comtstr
                item['comment_url'] = response.url
                item['push_time'] = pushtime
                item['catch_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['data_from'] = model.webname
                yield item
        except Exception as e:
            self.error('【parse_detail出错】{},{}'.format(response.url, e))
