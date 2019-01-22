import random

from src.chrome  import Chrome
from src.general import image_comparison
from src.general import adb
import datetime
from time import sleep
from src.music import Music
from src.third_party import Tx_QQ
from src.third_party import Browser_UC
from src.third_party import Browser_360


class Ts_Chrome():
    def __init__(self, d):
        self.d = d
        self.chrome = Chrome(self.d)
        self.path = image_comparison.get_path()
        self.log_data = []
        self.chrome_report_details = []


    def set_up(self, casename):
        print(casename)
        self.d.screen_on()

        # 判断是否锁屏状态
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()

        # 停止并启动设置
        self.chrome.stop()
        self.d.app_stop_all()
        self.chrome.start()

        # 获取设置的内存、cpu等信息
        adb.get_meminfo(self.d)
        adb.get_battery(self.d)
        adb.get_cpuinfo(self.d)

        # 获取当前时间，并保存测试开始前的截图
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.d.screenshot(self.path + "image\\chrome\\"+casename + nowTime+".jpg")
        return time


    def case1(self, window=100, num=30):
        '''
        多次切换浏览器中的窗口,打开window个窗口；切换num次窗口，并打开sina.com 网页
        '''
        result = "pass"
        for i in range(window):
            print(">>Chrome窗口界面：第"+str(i)+"次添加窗口")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            self.chrome.switcher_window()
            self.chrome.window_add()
        for i in range(num):
            self.chrome.connect_url("www.sina.com.cn")
            self.chrome.swipe_window()
        return result

    def case2(self,window=100,url=["www.baidu.com","www.sina.com.cn","www.iqiyi.com","news.qq.com","m.qidian.com"]):
        '''
        后台播放音乐，挂QQ进入网页，反复退出进入网络，检查是否会出现异
        '''
        music = Music(self.d)
        qq = Tx_QQ(self.d)
        browser_uc = Browser_UC(self.d)


        qq.login_qq()
        music.start_background_play()
        result = "pass"
        self.chrome.start()
        for i in range(window):
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            num = random.randint(0, 3)
            if num == 0:
                self.chrome.switcher_window()
                self.chrome.window_add()
            elif num == 1:
                url_num = random.randint(0, len(url)-1)
                self.chrome.connect_url(url[url_num])
            elif num == 2:
                self.chrome.swipe_window()
            elif num == 3:
                try:
                    browser_uc.open_browser()
                except BaseException as e:
                    print("第三方app出现异常:", e)
                    self.d.app_stop_all()
                self.chrome.start()
        return result




    def tear_down(self, casename):
        self.d.screen_on()
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.d.screenshot(self.path + "image\\chrome\\" + casename + nowTime + ".jpg")

        adb.get_meminfo(self.d)
        adb.get_battery(self.d)
        adb.get_cpuinfo(self.d)
        self.chrome.stop()

        print(casename)
        return time

    def run(self):
        window = 100

        actual_result = ""
        err_path = ""
        starttime1 = self.set_up("开始测试：Chrome切换"+str(window)+"次浏览器中的窗口")
        try:
            t_reference_result1 = self.case1()
        except BaseException as e:
            t_reference_result1 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：Chrome切换"+str(window)+"次浏览器中的窗口；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\chrome\\Chrome切换" + str(window) + "次浏览器中的窗口；出现异常.jpg"
            self.d.screenshot(err_path)

            self.chrome.stop()
            self.d.app_stop_all()
        endtime1 = self.tear_down("结束测试：Chrome切换"+str(window)+"次浏览器中的窗口")
        self.chrome_report_details.append({"t_module": "Chrome", "t_case": "压力测试", "t_steps": "多次切换浏览器中的窗口", "t_expected_result": "每次均能成功切换，无异常发生",
         "t_actual_result": actual_result + "\n" + err_path, "t_start_time": starttime1, "t_end_time": endtime1, "t_reference_result": t_reference_result1, "t_result": ""})
        sleep(2)

        actual_result = ""
        err_path = ""
        starttime2 = self.set_up("开始测试：后台播放音乐，挂QQ进入网页，反复退出进入网络"+str(window)+"次，检查是否会出现异常")
        try:
            t_reference_result2 = self.case2()
        except BaseException as e:
            t_reference_result2 = "c"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：后台播放音乐，挂QQ进入网页，反复退出进入网络"+str(window)+"次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\chrome\\Chrome后台播放音乐，挂QQ进入网页，反复退出进入网络"+str(window)+"次；出现异常.jpg"
            self.d.screenshot(err_path)
            self.chrome.stop()
            self.d.app_stop_all()
        endtime2 = self.tear_down("结束测试：后台播放音乐，挂QQ进入网页，反复退出进入网络"+str(window)+"次，检查是否会出现异常")
        self.chrome_report_details.append({"t_module": "Chrome", "t_case": "压力测试", "t_steps": "后台播放音乐，挂QQ进入网页，反复退出进入网络"+str(window)+"次", "t_expected_result": "检查是否会出现异常",
         "t_actual_result": actual_result + "\n" + err_path, "t_start_time": starttime2, "t_end_time": endtime2, "t_reference_result": t_reference_result2, "t_result": ""})

        return self.chrome_report_details