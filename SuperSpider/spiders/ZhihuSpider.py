import scrapy
import time
from selenium import webdriver
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
import re
from SuperSpider.items import BaseItem

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('–disable-images')  # 禁止加载图片
chrome_options.add_argument('--headless')  # 无头浏览（无界面模式）
chrome_options.add_argument('--ignore-certificate-errors')  # 忽略网络错误
browser = webdriver.Chrome(options=chrome_options)  # 设置浏览器为无头模式

def scroll_until_loaded():
    check_height = browser.execute_script("return document.body.scrollHeight;")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        if browser.execute_script("return document.body.scrollHeight;") > check_height:
            check_height = browser.execute_script("return document.body.scrollHeight;")
        else:
            break


def parse_urls(args):
    """解析该关键词下所有问题的URL"""
    url = "https://www.zhihu.com/search?q={}".format(args)
    browser.get(url)
    scroll_until_loaded()
    html_str = browser.page_source
    html = etree.HTML(html_str)
    selector = html.xpath('//div[@class="Card SearchResult-Card"]')
    url_list = []
    if selector:
        for each in selector:
            url = each.xpath('.//div[@itemprop="zhihu:question"]/meta[1]/@content')
            # question = each.xpath('.//div[@itemprop="zhihu:question"]/meta[2]/@content')
            if url:
                url_list.append(url[0])
    return url_list


class ZhihuSpider(scrapy.Spider):
    global kw
    kw = "冈本"  # 修改关键字
    name = 'zhihu'
    allowed_domains = ["www.zhihu.com"]
    url_list = parse_urls(kw)
    print(url_list)
    start_urls = url_list

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

    def parse(self, response):
        """滚动到页面最底部并提取元素"""
        url = response.url
        browser.get(url)
        scroll_until_loaded()

        # # 计算滚动次数
        # answer_count = 0
        # try:
        #     answer_count_str = html.xpath('//h4[@class="List-headerText"]/span/text()[1]')[0]
        #     answer_count_str_re = answer_count_str.replace(',', '')
        #     print(answer_count_str_re)
        #     # pattern = re.compile(r'\d+')
        #     # answer_count_re = re.search(pattern,answer_count_str_re)
        #     answer_count = int(answer_count_str_re)
        # except Exception as e:
        #     self.error('回答条数过少，无需滚动:{}'.format(e))
        # print('answer_count:{}'.format(answer_count))
        # scroll_count = 0
        # if answer_count:
        #     scroll_count = answer_count // 5 + 1
        #
        # # 页面滚动
        # k = 0
        # while k < scroll_count:
        #     time.sleep(1)
        #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        #     k += 1

        # 开始解析页面元素
        try:
            html_str = browser.page_source
            html = etree.HTML(html_str)
            selector = html.xpath('//*[@class="List-item"]')
            questionname = html.xpath('//*[@id="root"]/div/main/div/div[1]/div[2]/div[1]/div[1]/h1/text()')[0]
            print(questionname)
            for each in selector:
                username = each.xpath(
                    './/*[@class="AuthorInfo AnswerItem-authorInfo AnswerItem-authorInfo--related"]/meta[1]/@content')[
                    0]
                # print('[1]:username' + username)
                # userurl = each.xpath(
                #     './/*[@class="AuthorInfo AnswerItem-authorInfo AnswerItem-authorInfo--related"]/meta[3]/@content')[
                #     0]
                # print('[2]:userurl' + userurl)
                # userfans = each.xpath(
                #     './/*[@class="AuthorInfo AnswerItem-authorInfo AnswerItem-authorInfo--related"]/meta[4]/@content')[
                #     0]
                # print('[3]:userfans' + userfans)
                anserurl = each.xpath('.//*[@class="ContentItem AnswerItem"]/meta[3]/@content')[0]
                # print('[4]:anserurl' + anserurl)
                # upvoteCount = each.xpath('.//*[@class="ContentItem AnswerItem"]/meta[2]/@content')[0]
                # print('[5]:upvoteCount' + upvoteCount)
                modifiedtime = each.xpath('.//*[@class="ContentItem AnswerItem"]/meta[5]/@content')[0]
                # print('[6]:modifiedtime' + modifiedtime)
                # commentcount = each.xpath('.//*[@class="ContentItem AnswerItem"]/meta[6]/@content')[0]
                # print('[7]:commentcount' + commentcount)
                # answerPath = each.xpath('.//div[@class="RichContent-inner"]')
                # answerdetail = answerPath.xpath('string(.)').extract_first()
                # .xpath('string(.)').extract_first()
                answerdetail = each.xpath(
                    './/div[@class="RichContent-inner"]/span/p/text() | .//div[@class="RichContent-inner"]/span/text()')
                if isinstance(answerdetail, list) is True:
                    answerdetail = ''.join(answerdetail)
                else:
                    answerdetail = each.xpath('.//div[@class="RichContent-inner"]/span/text()').extract_first()

                item = BaseItem()
                item['collection'] = kw+"(知乎-2次)"
                item['title'] = questionname
                item['username'] = username
                item['usergender'] = None
                item['userlocation'] = None
                # item['userfans'] = userfans
                # item['user_url'] = userurl
                item['comment_url'] = anserurl
                item['push_time'] = modifiedtime
                item['comment_detail'] = answerdetail
                # item['follower'] = upvoteCount
                # item['anscommt'] = commentcount
                item['catch_time'] = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
                item['data_from'] = "知乎"
                yield item
        except Exception as e:
            self.error('【parse_detail出错】{},{}'.format(response.url, e))
