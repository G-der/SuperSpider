class BaseModel(object):
    def __init__(self):
        self.allow_domains = [""]  # 允许的域名
        self.start_urls = [""]  # 起始页面
        self.comment_link_Re = None  # 帖子链接正则
        self.comment_link_path = ''  # 帖子链接xpath
        self.title_path = ''  # 标题xpath
        self.eath_path = ''  # 遍历对象xpath
        self.username_path = ''  # 用户名xpath
        self.pushtime_path = ''  # 发表时间xpath
        self.comment_path = ''  # 评论内容xpath
        self.collection = ""  # 数据保存的集合名
        self.webname = ""  # 网页名称

        # 存在用户性别和所在地时设置
        self.userloct_path = ''  # 用户所在地xpath
        self.usergend_path = ''  # 用户性别xpath
        # 存在多页时设置
        self.page_link_Re = None  # 分页链接正则
        self.page_link_path = ''  # 分页链接xpath


class BBS591Moto(BaseModel):
    """591摩托论坛"""
    def __init__(self):
        self.allow_domains = ["bbs.591moto.com"]  # 允许的域名
        self.start_urls = ["http://bbs.591moto.com/forum-135-1.html"]  # 起始页面
        self.comment_link_Re = 'thread-'  # 帖子链接正则
        self.comment_link_path = '//table[@summary="forum_135"]'  # 帖子链接xpath
        self.title_path = '//h1/span/text()'  # 标题xpath
        self.eath_path = '//div[@id="postlist"]/div[starts-with(@id,"post_")]'  # 遍历对象xpath
        self.username_path = './/div[@class="authi"]/a[@class="xw1"]/text()'  # 用户名xpath
        self.pushtime_path = './/div[@class="authi"]/em/text()'  # 发表时间xpath
        self.comment_path = './/td[@class="t_f"]'  # 评论内容xpath
        self.collection = "测试数据"  # 数据保存的集合名
        self.webname = "591论坛"  # 网页名称


def set_model():
    model = BBS591Moto()  # 设置要抓取的网页模型
    return model
