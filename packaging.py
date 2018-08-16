from urllib import request, parse
from urllib.error import URLError, HTTPError
import json, hashlib, pymysql
from http import cookiejar

'''
封装request
* 传入URL
* user_agent
* headers
* data
* urlopen
* 返回bytes 数组
* get or post
'''

class Session():
    def __init__(self):
        cookie_object = cookiejar.CookieJar()
        handler = request.HTTPCookieProcessor(cookie_object)
        self.opener = request.build_opener(handler)

    def get(self, url, headers=None):
        return get(url, headers,self.opener)

    def post(self, url, form, headers=None):
        return post(url, form, headers, self.opener)

import requests
# from hashlib import md5

# 自动打码
class RClient(object):
    '''
    首先实例化
    rc = RClient('这里输入若快打码账号', '这里输入若快打码密码')
    im = open('图片name.jpg', 'rb').read()  # 读取验证码图片内容
    print (rc.rk_create(im, 3050)) # im 验证码图片内容   3050 验证码类型
    '''
    def __init__(self, username, password, soft_id= '107806', soft_key='e6ade28674094c9b801e9993d858269e'):
        self.username = username
        self.password = self.md5(password)
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def md5(self,value):
        m = hashlib.md5()
        m.update(bytes(value,encoding='utf-8'))
        return m.hexdigest()


    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


class Mysql_conn(object):
    # 魔术方法, 初始化, 构造函数
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', user='root', password='123456', port=3306, database='mysql')
        self.cursor = self.db.cursor()
    # 执行modify(修改)相关的操作
    def ins(self, sql):
        self.cursor.execute(sql)
        self.db.commit()
    # 魔术方法, 析构化 ,析构函数
    def __del__(self):
        self.cursor.close()
        self.db.close()


def md5(key):
    # 创建一个MD5对象
    md5_a = hashlib.md5()
    # 需要有bytes, 作为参数
    # 由str, 转换成 bytes encode-------str.encode('utf-8')
    # 由bytes转换成 str, decode---------bytes.decode('utf-8+')
    sign_bytes = key.encode('utf-8')
    # print(type(sign_bytes))
    # 更新md5 object的值
    md5_a.update(sign_bytes)
    sign_str = md5_a.hexdigest()
    return sign_str


def get(url, headers=None, opener=None):
    '''
    :param url: 必填,传入的Url
    :param headers: 可不填,如果用户需要自行传入headers, 则覆盖之前的headers
    :return:返回调用的urlrequest封装的方法
    '''
    return urlrequest(url, headers=headers, opener=opener)


def post(url, data, headers=None, opener=None):
    '''
    :param url: 必填, User传入的Url
    :param data: 必填, 这里为传递给服务器的参数
    :param headers:可不填
    :return:
    '''
    return urlrequest(url, data, headers=headers, opener=opener)


def urlrequest(url, data=None, headers=None, opener=None):
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    html = ''
    if headers == None:
        # 如果没有传递headers 则使用默认的headers
        headers = {
            'User-Agent': user_agent
        }
    # 这里使用try, except 捕获异常, Eg: HTTPError404错误等...  和 URLError连接超时,服务器不存在,网络无连接等错误
    try:
        if data:
            # 把data 参数转成Unicode编码 (一般浏览器都是采用Unicode编码传递中文参数)
            data_str = parse.urlencode(data)
            data_bytes = data_str.encode('utf-8')
            req = request.Request(url, data=data_bytes, headers=headers)
        else:
            req = request.Request(url, headers=headers)
        if opener:
            response = opener.open(req)
        else:
            response = request.urlopen(req)
        html = response.read()
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    return html


if __name__ == '__main__':
    # url = 'http://weibo.com'
    # html = urlrequest(url).decode('gb2312')
    # print(html)
    # 测试

    url = 'http://fanyi.baidu.com/sug'
    while True:
        data = input('请输入要翻译的词语,按Q返回:')
        if data == 'q' or data == 'Q':
            break
        form = {
            'kw': data
        }
        html_bytes = post(url, data=form).decode('utf-8')
        try:
            html = json.loads(html_bytes,encoding='utf-8')['data'][0]['v']
            print('翻译:', '\n\r\r', html)
        except IndexError as e:
            print('错误:',e)

