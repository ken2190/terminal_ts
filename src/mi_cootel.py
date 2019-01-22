import uiautomator2 as u2
import time
import os
class Mi_CooTel():

    def __init__(self,d):
        self.d=d
    '''
    开启关闭mi cootel
    '''
    def start_mi_cootel(self):
        print('---------->开启mi cootel')
        print('进入mi cootel 后请手动切换最下面三个菜单栏切换一遍后，回到首页，等待脚本运行')
        self.d.app_start('com.xinwei.onlneHall')

    def stop_mi_cootel(self):
        print('---------->关闭mi cootel')
        self.d.app_stop('com.xinwei.onlneHall')

    def wait_first_page(self):
        '''
        判断首页是否出现
        :return:
        '''
        time.sleep(10)
        self.d(resourceId="title", description='Mi CooTel').wait()


    '''
    页面主功能操作
    '''

    def click_first_page(self):
        print('---------->点击首页')
        self.d(resourceId="tab_0").click()

    def click_product(self):
        print('---------->点击产品')
        self.d(resourceId="tab_1").click()

    def click_user(self):
        print('---------->点击用户中心')
        if self.d(resourceId="tab_2").wait()==True:
            self.d(resourceId="tab_2").click()


    '''
    以下是登录mi cootel的操作
    '''
    def assert_login(self):
        '''
        判断是否已经登录
        :return:
        '''
        if self.d(resourceId="loginBtn").wait(timeout=3)==True:
            self.d(resourceId="loginBtn").click()
            return True
        else:
            return False

    def input_us_pw(self,us='68824924',pw='203817'):
        '''
        输入账号和密码
        :return:
        '''
        print('---------->输入手机号码')
        time.sleep(2)
        self.d.set_fastinput_ime(True)
        self.d(className="android.view.View", instance=10).click()
        self.d.clear_text()
        self.d.send_keys(us)
        print('---------->输入密码')
        self.d(text=u"•••••").set_text(pw)

    def click_login(self):
        print('---------->点击登录')
        self.d(description=u"登录").click()

    '''
    登录的组合操作
    '''
    def start_and_login(self):
        '''
        开启并登陆
        :return:
        '''
        self.start_mi_cootel()
        time.sleep(20)
        self.wait_first_page()
        self.click_user()
        if self.assert_login()==True:
            self.input_us_pw()
            self.click_login()
        else:
            print('---------->已经登录')


    '''
    下面是首页的操作
    '''

    def click_network(self):
        print('---------->点击入网')
        self.d(description=u"入网", className="android.view.View", instance=1).click()
        if self.d(description=u"CooTel选号").wait(timeout=10)==True:
            return True
        else:
            return '进入入网界面错误'


    def click_set_meal(self):
        print('---------->点击套餐余量')
        self.d(description=u"套餐余量", className="android.view.View", instance=1).click()
        if self.d(description=u"套餐余量").wait(timeout=10)==True:
            return True
        else:
            return '进入套餐余量界面错误'

    def click_alteration(self):
        print('---------->点击变更产品')
        self.d(description=u"变更产品", className="android.view.View", instance=1).click()
        if self.d(description=u"业务查询").wait(timeout=10)==True:
            return True
        else:
            return '进入变更产品界面错误'

    def click_modification(self):
        print('---------->点击修改信息')
        self.d(description=u"修改信息", className="android.view.View", instance=1).click()
        if self.d(description=u"个人信息").wait(timeout=10)==True:
            return True
        else:
            return '进入修改信息界面错误'

    '''
    下面是用户中心界面
    '''
    def click_user_message(self):
        print('---------->点击用户信息')
        self.d(resourceId="my-info").click()
        if self.d(resourceId="title",description=u"个人信息").wait(timeout=10)==True:
            return True
        else:
            return '进入用户信息息界面错误'

    def click_update(self):
        print('---------->点击升级为后付费')
        self.d(resourceId="my-info", description=u" 升级为后付费").click()
        if self.d(description=u"升级为后付费").wait(timeout=10)==True:
            return True
        else:
            return '进入升级为后付费界面错误'

    def click_language(self):
        print('---------->点击语言设置')
        self.d(resourceId="chooseLang").click()
        if self.d(resourceId="android:id/text1", text=u"中文").wait(timeout=10)==True:
            return True
        else:
            return '进入语言设置界面错误'

    def click_quit(self):
        print('---------->点击退出登录')
        self.d(description=u"退出登录").click()
        if self.d(resourceId="android:id/message").wait(timeout=3)==True:
            self.d(resourceId="android:id/button1").click()
            return True
        else:
            return '没有点击到退出按钮'

    def click_back(self):
        print('---------->点击返回')
        time.sleep(3)
        self.d.press("back")
        time.sleep(3)

    '''
    下面是组合操作
    '''

    def Case_combination(self):
        '''
        组合操作
        :return:
        '''
        result_message=''
        self.start_and_login()
        self.click_first_page()
        network=self.click_network()
        if network!=True:
            result_message=result_message+network
        self.click_back()
        set_meal=self.click_set_meal()
        if set_meal!=True:
            result_message=result_message+set_meal
        self.click_back()
        alteration=self.click_alteration()
        if alteration!=True:
            result_message=result_message+alteration
        self.click_back()
        modification=self.click_modification()
        if modification!=True:
            result_message=result_message+modification
        self.click_back()
        self.click_product()
        time.sleep(3)
        self.click_user()
        time.sleep(2)
        user_message=self.click_user_message()
        if user_message!=True:
            result_message=result_message+user_message
        self.click_back()
        update=self.click_update()
        if update!=True:
            result_message=result_message+update
        self.click_back()
        language=self.click_language()
        if language!=True:
            result_message=result_message+language
        self.click_back()
        self.click_quit()
        self.stop_mi_cootel()
        return result_message






#
# d = u2.connect('164540b2')
# a=Mi_CooTel(d)
# print(a.combination())














