import random
import time
from src.general import image_comparison


class Chrome:
    def __init__(self, d):
        self.d = d
        self.d_size = self.d.window_size()

    def __sleep(func):
        def inner(self):
            time.sleep(1)
            self.d.screen_on()
            return func(self)
        return inner


    def start(self):
        print(">>>>>>>>>>>>>>>>> 启动APP：Chrome")
        self.d.app_start("com.android.chrome")
        if self.d(resourceId="com.android.chrome:id/title",text="欢迎使用 Chrome").wait(timeout=2):
            print(">>>>>>>>>>>>>>>>> Chrome界面： 欢迎界面点击 接受并继续")
            self.d(resourceId="com.android.chrome:id/terms_accept").click()
            self.d.screen_on()
            if self.d(resourceId="com.android.chrome:id/signin_title").wait(timeout=2):
                self.d(resourceId="com.android.chrome:id/negative_button").click()
            if self.d(resourceId="com.android.chrome:id/negative_button").wait(timeout=2):
                self.d(resourceId="com.android.chrome:id/negative_button").click()
        if self.d(resourceId="com.android.chrome:id/title",text="节省数据流量，加快浏览速度").wait(timeout=2):
            print(">>>>>>>>>>>>>>>>> Chrome界面： 节省数据流量，加快浏览速度界面点击 下一步")
            self.d(resourceId="com.android.chrome:id/next_button").click()
            self.d(resourceId="com.android.chrome:id/negative_button").click()
        if self.d(resourceId="com.android.chrome:id/no_thanks_button").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> Chrome界面： 加载更快，流量更省界面点击 不，谢谢")
            self.d(resourceId="com.android.chrome:id/no_thanks_button").click()


    def stop(self):
        print(">>>>>>>>>>>>>>>>> 关闭APP：Chrome")
        self.d.app_stop("com.android.chrome")

    '''
    下面是查看历史记录的操作
    '''

    def click_more(self):
        print('---------->点击更多')
        self.d(resourceId="com.android.chrome:id/menu_button").click()

    def KHM_assert_browse_history(self):
        self.click_more()
        self.d(resourceId="com.android.chrome:id/menu_item_text", text=u"历史记录").click()
        return self.d(resourceId="results-header",description='未找到任何历史记录条目。').wait(timeout=3)

    def NCA_assert_browse_history(self):
        self.click_more()
        self.d(resourceId="com.android.chrome:id/menu_item_text", text=u"历史记录").click()
        return self.d(resourceId="com.android.chrome:id/empty_view").wait(timeout=3)



    def connect_url(self, url):
        print("打开网页：", url)
        if self.d(resourceId="com.android.chrome:id/search_box_text").wait(timeout=2):
            self.d(resourceId="com.android.chrome:id/search_box_text").click()
            self.d(resourceId="com.android.chrome:id/url_bar").set_text(url)
            time.sleep(1)
            self.d.press("enter")
        elif self.d(resourceId="com.android.chrome:id/url_bar").wait(timeout=2):
            self.d(resourceId="com.android.chrome:id/url_bar").set_text(url)
            time.sleep(1)
            self.d.press("enter")



    @__sleep
    def menu(self):
        print(">>>>>>>>>>>>>>>>> Chrome界面：点击菜单")
        self.d(resourceId="com.android.chrome:id/menu_button").clcik()

    @__sleep
    def switcher_window(self):
        self.d.swipe(0.5, 0.3, 0.5, 0.6)
        print(">>>>>>>>>>>>>>>>> Chrome窗口界面：窗口切换")
        if self.d(resourceId="android:id/button1",  text=u'允许').wait(timeout=1):
            self.d(resourceId="android:id/button1", text=u'允许').click()
        self.d(resourceId="com.android.chrome:id/tab_switcher_button").click()
        if not(self.d(resourceId="com.android.chrome:id/new_tab_button").wait(timeout=1)):
            self.d(resourceId="com.android.chrome:id/tab_switcher_button").click()

    @__sleep
    def window_add(self):
        self.pop_up()
        self.d.swipe(0.5, 0.3, 0.5, 0.6)
        if self.d(resourceId="com.android.chrome:id/new_tab_button").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> Chrome窗口界面：增加窗口")
            self.d(resourceId="com.android.chrome:id/new_tab_button").click()
        elif self.d(resourceId="com.android.chrome:id/tab_switcher_button").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> Chrome窗口界面：窗口切换")
            self.d(resourceId="com.android.chrome:id/tab_switcher_button").click()
            print(">>>>>>>>>>>>>>>>> Chrome窗口界面：增加窗口")
            self.d(resourceId="com.android.chrome:id/new_tab_button").click()


    def swipe_window(self):
        self.d.screen_on()
        # 判断是否锁屏状态
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        self.switcher_window()
        time.sleep(1)
        self.d.swipe(0.5, 0.3, 0.5, 0.6)
        time.sleep(1)
        self.d.click(0.506, 0.447)

    @__sleep
    def pop_up(self):
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        if self.d(resourceId="android:id/message",text="Chrome无响应。 要将其关闭吗？").wait(timeout=1):
            self.d(resourceId="android:id/button1").click()
            self.start()
        elif self.d(resourceId="android:id/message").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>异常弹框消息： ", self.d(resourceId="android:id/message").get_text())
            self.d(resourceId="android:id/button1").click()
            self.start()

    def check_home(self):
        if self.d(resourceId="com.android.chrome:id/search_provider_logo").wait(timeout=1):
            if self.d(resourceId="com.android.chrome:id/search_box_text").wait(timeout=1):
                return True
        else:
            return False

    def check_open_baidu(self):
        self.window_add()
        time.sleep(2)
        self.connect_url("www.baidu.com  ")
        time.sleep(5)
        if self.d(resourceId="android:id/button1").wait(timeout=1):
            self.d(resourceId="android:id/button1").click()
        if self.d(resourceId="index-kw").wait(timeout=3):
            return True
        else:
            if self.d(description=u"您处于离线状态。").wait(timeout=1):
                print("网络未连接或网络不稳定")
            return False
