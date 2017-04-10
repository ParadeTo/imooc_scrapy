# -*- coding: utf-8 -*-

from selenium import webdriver

browser = webdriver.Firefox(executable_path="/Users/ayou/Documents/Soft/geckodriver")

browser.get("https://detail.tmall.com/item.htm?spm=a3211.0-7358991.mobileBanner_1491355178376_11.1.7bhltV&id=21595027010&rn=4fe6ceab69e6339a084572c47f29ddb1&abbucket=2")

print(browser.page_source)