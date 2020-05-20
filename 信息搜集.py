# -*- coding:utf-8 -*-
from selenium import webdriver
import time

#不启动浏览器
option = webdriver.ChromeOptions()
# option.add_argument('headless')

# 通过url访问浏览器
driver = webdriver.Chrome(r'C:\Python27\Scripts\chromedriver.exe',chrome_options=option)
url = 'http://whatweb.bugscaner.com/look'
try:
    driver.get(url=url)
    time.sleep(2)

    #在输入框中输入需要进行查询的网址并点击查询按钮
    # driver.find_elements_by_css_selector('//*[@id="inputurls"]')[0].clear()
    driver.find_element_by_id('//*[@id="inputurls"]').clear()
    driver.find_element_by_xpath('//*[@id="inputurls"]').send_keys("http://b2b.haier.com/")
    driver.find_element_by_xpath('//*[@id="start"]').click()
    time.sleep(2)

    #用正则表达式获取信息
    html=driver.page_source
    print(html.encode("utf8"))
    # 退出浏览器
    driver.quit()
except:
    1