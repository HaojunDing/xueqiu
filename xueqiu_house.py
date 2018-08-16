import requests as r
from packaging import Mysql_conn
import json


def xueqiu(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "device_id=79072ababd6b2d3ec7eae2fa55e81ade; _ga=GA1.2.1570603786.1530942589; s=f212kth48o; __utmz=1.1530942601.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=1.1570603786.1530942589.1530942601.1531224799.2; aliyungf_tc=AQAAAJPIRUfrhQAA7P5o37od1PLm1k/S; xq_a_token=584d0cf8d5a5a9809761f2244d8d272bac729ed4; xq_a_token.sig=x0gT9jm6qnwd-ddLu66T3A8KiVA; xq_r_token=98f278457fc4e1e5eb0846e36a7296e642b8138a; xq_r_token.sig=2Uxv_DgYTcCjz7qx4j570JpNHIs; u=571534297870908; Hm_lvt_1db88642e346389874251b5a1eded6e3=1534297871; _gid=GA1.2.1868096006.1534297871; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1534311974",
        "Host": "xueqiu.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    }
    a = r.get(url, headers=headers).json()
    return a


if __name__ == '__main__':
    m = Mysql_conn()
    url = 'https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=%d&count=10&category=111'
    j = -1
    for i in range(3):
        json_qiu = xueqiu(url%j)
        xueqiu_list = json_qiu['list']
        for p in xueqiu_list:
            # print(type(p['data']),p)
            dict_qiu = json.loads(p['data'])
            # print(type(dict_qiu),dict_qiu)
            xueqiu_title = dict_qiu['title']
            xueqiu_description = dict_qiu['description']
            xueqiu_target = dict_qiu['target']
            xueqiu_id = dict_qiu['id']
            print(xueqiu_description)
            print(xueqiu_target)
            print(xueqiu_title)
            print(xueqiu_id)
            sql = "insert into xueqiu values ('%s','%s','%s','%s')"%(xueqiu_id,xueqiu_title,xueqiu_target,xueqiu_description)
            m.ins(sql)

