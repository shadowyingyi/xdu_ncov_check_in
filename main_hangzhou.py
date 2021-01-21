import requests
import json
import time
import pytz
import datetime


def login(session, username, password):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://xxcapp.xidian.edu.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://xxcapp.xidian.edu.cn/uc/wap/login',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    data = {
        'username': username,
        'password': password
    }

    session.post('https://xxcapp.xidian.edu.cn/uc/wap/login/check',
                 headers=headers, data=data)


def submit(session):

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://xxcapp.xidian.edu.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://xxcapp.xidian.edu.cn/ncov/wap/default/index',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    data = {
    'szgjcs': '',
    'szcs': '',
    'szgj': '',
    'zgfxdq': '0',
    'mjry': '0',
    'csmjry': '0',
    'tw': '2',
    'sfcxtz': '0',
    'sfjcbh': '0',
    'sfcxzysx': '0',
    'qksm': '',
    'sfyyjc': '0',
    'jcjgqr': '0',
    'remark': '',
    'address': '浙江省杭州市上城区紫阳街道平安里江城路小区',
    'geo_api_info': '{"type":"complete","info":"SUCCESS","status":1,"$Da":"jsonp_745295_","position":{"Q":30.22961,"R":120.17371000000003,"lng":120.17371,"lat":30.22961},"message":"Get ipLocation success.Get address success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{"citycode":"0571","adcode":"330102","businessAreas":[{"name":"望江","id":"330102","location":{"Q":30.236908,"R":120.18526500000002,"lng":120.185265,"lat":30.236908}},{"name":"吴山","id":"330102","location":{"Q":30.241234,"R":120.16583700000001,"lng":120.165837,"lat":30.241234}},{"name":"紫阳","id":"330102","location":{"Q":30.235255,"R":120.16893900000002,"lng":120.168939,"lat":30.235255}}],"neighborhoodType":"商务住宅;住宅区;住宅小区","neighborhood":"平安里","building":"","buildingType":"","street":"江城路","streetNumber":"322幢","country":"中国","province":"浙江省","city":"杭州市","district":"上城区","township":"紫阳街道"},"formattedAddress":"浙江省杭州市上城区紫阳街道平安里江城路小区","roads":[],"crosses":[],"pois":[]}',
    'area': '浙江省 杭州市 上城区',
    'province': '浙江省',
    'city': '杭州市',
    'sfzx': '0',
    'sfjcwhry': '0',
    'sfjchbry': '0',
    'sfcyglq': '0',
    'gllx': '',
    'glksrq': '',
    'jcbhlx': '',
    'jcbhrq': '',
    'ismoved': '0',
    'bztcyy': '',
    'sftjhb': '0',
    'sftjwh': '0',
    'sfjcjwry': '0',
    'jcjg': ''
    }


    response = session.post('https://xxcapp.xidian.edu.cn/ncov/wap/default/save',
                            headers=headers, data=data)

    s = response.text
    j = json.loads(s)
    return j['m']


def get_hour_message():
    h = datetime.datetime.fromtimestamp(
        int(time.time()), pytz.timezone('Asia/Shanghai')).hour
    if 6 <= h <= 11:
        return '晨'
    elif 12 <= h <= 17:
        return '午'
    elif 18 <= h <= 24:
        return '晚'
    else:
        return '凌晨'


def server_jiang_push(SCKEY: str, message):
    requests.get(f'https://sc.ftqq.com/{SCKEY}.send?text={message}')


def main_handler(event, context):

    student_id = ''
    password = ''  # http://ids.xidian.edu.cn/authserver/login

    # https://sc.ftqq.com/3.version
    # 基于 Server 酱的推送服务,
    SCKEY = ''

    session = requests.session()
    login(session, student_id, password)
    message = submit(session)

    message = '疫情通丨' + message

    server_jiang_push(SCKEY, message)


if __name__ == '__main__':
    main_handler(None, None)
