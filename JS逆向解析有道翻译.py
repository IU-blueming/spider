import requests
import time
import random
import hashlib

# 1. 确定要爬取链接 : http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
# 2 .请求方式  :  post
# 3 . 构建 data 参数

# 获取参数
def get_parm(word):
    # 时间戳   1604392098660
    lts = str(int(time.time()*1000))
    # 盐值 :r + parseInt(10 * Math.random(), 10)
    salt = lts + str(random.randint(1,10))
    # 签名 : n.md5("fanyideskweb" + e + i + "]BjuETDhU)zqSxf-=B#7m")  d76b30c019a8bcaf1f6415a16a3eea6e
    # 签名 = MD5 加密 ("fanyideskweb" + 要翻译的单词 + 盐值 + "]BjuETDhU)zqSxf-=B#7m")
    sign = hashlib.md5(("fanyideskweb"+word+salt+"]BjuETDhU)zqSxf-=B#7m").encode('utf-8')).hexdigest()
    # bv = MD5加密 (浏览器的标识 ): n.md5(navigator.appVersion)
    us = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    bv = hashlib.md5(us.encode('utf-8')).hexdigest()
    # print((lts,salt,sign,bv))
    return  {"lts":lts,"salt":salt,"sign":sign,"bv":bv,"word":word}


def get_conent(data):
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    # url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    headers ={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '244',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-532941148@10.169.0.82; JSESSIONID=aaaRm2oJxjMzF8HaSbnwx; OUTFOX_SEARCH_USER_ID_NCOO=1595231732.1175306; ___rl__test__cookies=1604391991434',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'i':data['word'],    # 需要翻译单词
        'from':'AUTO',
        'to':'AUTO',
        'smartresult':'dict',
        'client':'fanyideskweb',
        'salt':data['salt'],   # 盐值
        'sign':data['sign'],   # 签名
        'lts':data['lts'],    # 时间戳
        'bv':data["bv"],  # 浏览器标识
        'doctype':'json',
        'version':'2.1',
        'keyfrom':'fanyi.web',
        'action':'FY_BY_REALTlME',
    }
    response = requests.post(url=url,data=data,headers=headers).json()
    # print(response)
    print(response['translateResult'][0][0]['tgt'])

#处理翻译
def fanyi(word):
    connmet = get_parm(word)
    get_conent(connmet)


if __name__ == '__main__':
    word = input("请输入你要翻译的单词:")
    fanyi(word)
