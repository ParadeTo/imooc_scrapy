# -*- coding: utf-8 -*-

from selenium import webdriver
from scrapy.selector import Selector

# browser = webdriver.Chrome(executable_path="e://soft/selenium/chromedriver.exe")

# browser.get("https://detail.tmall.com/item.htm?spm=a3211.0-7358991.mobileBanner_1491355178376_11.1.7bhltV&id=21595027010&rn=4fe6ceab69e6339a084572c47f29ddb1&abbucket=2")

# print(browser.page_source)
#
# t_selector = Selector(text=browser.page_source)
# print(t_selector.css(".tm-promo-price .tm-price::text").extract())


# browser.get("https://www.zhihu.com/#signin")
# browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys('18611112949')
# browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys('81051766')
# browser.find_element_by_css_selector(".view-signin button.sign-button").click()

# browser.get('https://www.weibo.com')
# browser.maximize_window()
# import time
# time.sleep(5)
# browser.find_element_by_css_selector("#loginname").send_keys("18611112949")
# browser.find_element_by_css_selector(".info_list.password input[node-type='password']").send_keys("woshiyxz12")
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()
# browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")


# 不加载图片
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chrome_opt.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path="e://soft/selenium/chromedriver.exe", chrome_options=chrome_opt);
browser.get("https://detail.tmall.com/item.htm?spm=a3211.0-7358991.mobileBanner_1491355178376_11.1.7bhltV&id=21595027010&rn=4fe6ceab69e6339a084572c47f29ddb1&abbucket=2")
