import time
import requests
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from ProxyPool.db import RedisClient
from lxml import etree
from selenium import webdriver


chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=chrome_options)


def scroll_until_loaded():
    check_height = browser.execute_script("return document.body.scrollHeight;")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        if browser.execute_script("return document.body.scrollHeight;") > check_height:
            check_height = browser.execute_script("return document.body.scrollHeight;")
        else:
            break


def get_qrcode_img_link_address():
    if browser.find_element_by_id("J_QRCodeImg"):
        print('get the QRCodeImgUrl.....')
        print(browser.find_element_by_id("J_QRCodeImg").find_element_by_tag_name("img").get_attribute("src"))
        # use_chrome_open_url(browser.find_element_by_id("J_QRCodeImg").find_element_by_tag_name("img").get_attribute("src"))


def login():
    # try:
    #     print("检测是否登录页面")
    #     login_button = browser.find_element_by_link_text("亲，请登录")
    #     if login_button:
    #         login_button.click()
    #         time.sleep(1)
    #         print("等待扫码登录")
    while True:
        try:
            if browser.find_element_by_link_text("密码登录"):
                time.sleep(1)
                try:
                    if browser.find_element_by_link_text("请点击刷新"):
                        browser.find_element_by_link_text("请点击刷新").click()
                        print("二维码失效，已刷新")
                        time.sleep(1)
                        get_qrcode_img_link_address()
                except NoSuchElementException:
                    time.sleep(1)
                    continue

        except NoSuchElementException:
            print("成功登录...")
            print(browser.current_url)
            break

    # except NoSuchElementException:
    #     print("已登录")
    #     time.sleep(1)

    # get_qrcode_img_link_address()


def taobaospider():
    url = "https://s.taobao.com/search?spm=a230r.1.1998181369.d4919860.5b226a03GQKkpM&q=%E6%B2%99%E5%8F%91&refpid=430266_1006&source=tbsy&style=grid&pvid=e6aa81065d35b34a8e3377a2d5ea8f10&clk1=6704192874a526dcb24faacded1f59cf&tab=mall&sort=sale-desc"
    browser.get(url)
    # browser.maximize_window()
    login()
    while True:
        scroll_until_loaded()
        time.sleep(5)
        html_str = browser.page_source
        with open("html_1.html", "wb") as f:
            f.write(html_str.encode())
        html = etree.HTML(html_str)
        try:
            each = html.xpath('//div[@class="item J_MouserOnverReq"]')
            print(each)
            if each:
                # for each in selector:
                price = each.xpath('.//strong/text()').extract_first()
                volume = each.xpath('.//div[@class="deal-cnt"]/text()').extract_first()
                title = each.xpath('.//a[@class="J_ClickStat"]/text()').extract_first()
                url = each.xpath('.//a[@class="J_ClickStat"]/@href')[0]
                shopname = each.xpath(
                    './/a[@class="shopname J_MouseEneterLeave J_ShopInfo"]/span[2]/text()').extract_first()
                shopurl = each.xpath('.//a[@class="shopname J_MouseEneterLeave J_ShopInfo"]/@href')[0]
                location = each.xpath('.//div[@class="location"]/text()').extract_first()
                print(price, volume, title, url, shopname, shopurl, location)
            try:
                browser.find_element_by_xpath('//li[@class="item next"]/a/span[1]').click()
            except Exception as e:
                print("点击下一页出错:{}".format(e))
                break
        except Exception as e:
            print(e)
            break


if __name__ == '__main__':
    taobaospider()
