import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from pymongo.mongo_client import MongoClient


class TaobaoSpider:
    def __init__(self, username, password):
        #实现无可视化界面的操作
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        # 不加载图片，加快访问速度
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 设置为开发者模式，避免被识别(规避检测)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.web_driver = webdriver.Chrome(options=chrome_options)
        self.web_driver_wait = WebDriverWait(self.web_driver, 10)

        self.url = 'https://login.taobao.com/member/login.jhtml'
        self.username = username
        self.password = password

    def login(self):
        self.web_driver.get(self.url)
        try:
            # 切换为帐号密码登录
            login_method_switch = self.web_driver_wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="login"]/div[2]/div/div[1]/a[1]')))
            login_method_switch.click()

            # 找到用户名输入框并输入
            username_input = self.web_driver_wait.until(
                expected_conditions.presence_of_element_located((By.ID, 'fm-login-id')))#//*[@id="fm-login-id"]
            username_input.send_keys(self.username)

            # 找到密码输入框并输入
            password_input = self.web_driver_wait.until(
                expected_conditions.presence_of_element_located((By.ID, 'fm-login-password'))) #//*[@id="fm-login-password"]
            password_input.send_keys(self.password)

            # 找到登录按钮并点击
            login_button = self.web_driver_wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="login-form"]/div[4]/button'))) #//*[@id="login-form"]/div[4]/button
            login_button.click()

            # 找到名字标签并打印内容
            taobao_name_tag = self.web_driver_wait.until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="J_SiteNavLogin"]/div[1]/div[2]/a')))
            #//*[@id="J_SiteNavLogin"]/div[1]/div[2]/a
            print(f"登陆成功：{taobao_name_tag.text}")

            #点击购物车
            cart_click = self.web_driver_wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="mc-menu-hd"]')))
            cart_click.click()

            #获取购物车的信息
            # self.web_driver.get('https://cart.taobao.com/cart.htm?spm=a1z0d.6639537.1997525049.1.6ac87484zOijdK&from=mini&ad_id=&am_id=&cm_id=&pm_id=1501036000a02c5c3739')
            page_text = self.web_driver.page_source
            tree = etree.HTML(page_text)
            div_detail = tree.xpath('//*[@id="J_OrderList"]/div')
            print(div_detail)
            print(len(div_detail))
            time.sleep(1)
            # dic = {}
            for div in div_detail:
                #//*[@id="J_OrderList"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/ul/li[2]/div/div[2]/div[1]/a/text()
                #//*[@id="J_OrderList"]/div[17]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/ul/li[2]/div/div[2]/div[1]/a/text()
                #标题
                title = div.xpath('./div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/ul/li[2]/div/div[2]/div[1]/a/text()|./div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/ul/li[2]/div/div[2]/div[1]/a/text()')[0]
                #//*[@id="J_OrderList"]/div[18]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/ul/li[3]//p/text()
                #类型
                content = div.xpath('./div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/ul/li[3]//p/text()|./div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/ul/li[3]//p/text()')[0]
                #价格
                price = div.xpath('./div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/ul/li[6]//text()|./div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/ul/li[6]//text()')
                price = ''.join(price)
                dic = {'标题':title,
                       '类型':content,
                       '价格':price,
                    }
                print(dic)

                #存入mongodb中
                client = MongoClient("localhost", 27017)
                client['taobao']['infos'].save(dic)

            # 休息5秒钟，然后关闭浏览器
            time.sleep(5)
            self.web_driver.close()
        except Exception as e:
            print(e)
            self.web_driver.close()
            print("登陆失败")


if __name__ == "__main__":
    username = input("请输入用户名：")
    password = input("请输入密码：")
    spider = TaobaoSpider(username, password)
    spider.login()