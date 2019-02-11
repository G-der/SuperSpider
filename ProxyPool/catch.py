import re
import time

import requests


class IPSpider(object):
    def __init__(self):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

    def crawl_89ip(self):
        for i in range(1, 8):
            time.sleep(0.5)
            url = 'http://www.89ip.cn/index_{}.html'.format(i)
            print('正在抓取第{}页:{}'.format(i, url))
            response = requests.get(url, headers=self.headers)
            html = response.text
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                    re_port = find_port.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                    print(address_port)
                    yield address_port
