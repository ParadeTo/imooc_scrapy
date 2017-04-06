# -*- coding: utf-8 -*-

import requests
import re

import time

from PIL import Image

try: # py3
    import cookielib
except: # py2
    import http.cookiejar as cookielib

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")

try:
    session.cookies.load(ignore_discard=True)
except:
    print ('cookie 未能加载')

agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
header = {
    "HOST": "www.zhihu.com",
    "Referer": "www.zhihu.com",
    "User-Agent": agent
}

def is_login():
    # 通过个人中心页面返回状态码来判断是否为登录状态
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True

def get_xsrf():
    # 获取xsrf
    response = session.get('https://www.zhihu.com', headers=header)
    text = response.text
    match_obj = re.match('[\s\S]*name="_xsrf" value="(.*?)"', text)
    if match_obj:
        print (match_obj.group(1))
        return match_obj.group(1)
    else:
        return ""

def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=header)
    with open("captcha.jpg", "wb") as f:
        f.write(t.content)
        f.close()
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        pass

    captcha = input("输入验证码\n>")
    return captcha

def get_index():
    response = session.get('https://www.zhihu.com', headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf8"))
    print ("ok")

def zhihu_login(account, password):
    """知乎登录"""

    captcha = get_captcha()

    if re.match("1\d{10}", account):
        print ("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": captcha
        }

    else:
        if "@" in account:
            print("邮箱登录")
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": get_xsrf(),
                "phone_num": account,
                "password": password,
                "captcha": captcha
            }

    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save()


# get_xsrf()
zhihu_login("18611112949", "81051766")
# get_index()
# get_captcha()