from src.settings import Settings
import random
from datetime import datetime
from time import sleep
from src.general import image_comparison
from src.general import adb
import datetime
import os
from src import loginfo



class Ts_Setting_Bluetooth():
    def __init__(self, d):
        self.d = d
        self.setting = Settings(self.d)
        self.path = image_comparison.get_path()

        self.log_data = []
        self.st_blue_report_data = []



    def set_up(self, casename):
        print(casename)

        self.d.screen_on()

        # 判断是否锁屏状态
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()

        # 停止并启动设置
        self.setting.stop()
        self.setting.start()
        self.setting.list_bluetooth()

        # 获取设置的内存、cpu等信息
        adb.get_meminfo(self.d)
        adb.get_battery(self.d)
        adb.get_cpuinfo(self.d)

        # 获取当前时间，并保存测试开始前的截图
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.d.screenshot(self.path + "image\\setting\\"+casename + nowTime+".jpg")
        return time


    def case1(self, num=201):
        '''
        反复开启关闭蓝牙50次，检查是否会出现蓝牙无法开启等其它异常现象
        :param num:
        :return:
        '''
        result = "pass"
        self.d.screen_on()
        original = self.path + "image\\setting\\bluetoot_反复开启关闭蓝牙.png"
        count = 1
        err_count = 2

        while True:
            sleep(1)
            self.d.screen_on()
            if self.d(resourceId="com.android.settings:id/switch_text").get_text() == "关闭":
                adb.chmod_adb("adb shell screencap -p /sdcard/Screenshot.png")
                adb.chmod_adb("adb pull /sdcard/Screenshot.png " + original)
                break
            else:
                self.setting.bluetooth_switch()
                err_count = err_count - 1
                if err_count == 0:
                    self.d.screenshot(self.path + "image\\setting\\error反复开启关闭蓝牙初始化出现异常.png")
                    self.setting.stop()
                    self.setting.start()
                    self.setting.list_bluetooth()
                    break
        for i in range(num):
            self.d.screen_on()
            self.setting.bluetooth_switch()
            if self.d(resourceId="com.android.settings:id/switch_text").get_text() == "开启":
                sleep(2)
                if self.d(resourceId="android:id/title")[1].get_text() != '':
                    print(">>>蓝牙已开启时， 可正常搜索到蓝牙设备")
                    print(self.d(resourceId="android:id/title")[1].get_text())
                else:
                    print(">>>蓝牙已开启时， 等待2秒；未搜索到可用蓝牙设备")
                    self.d.screenshot(self.path + "image\\setting\\error蓝牙已开启时等待2秒未搜索到可用蓝牙.png")
                    result="fail"
            else:
                sleep(2)
                comparison = self.path + "image\\setting\\bluetoot_反复开启关闭蓝牙" + str(count) + ".jpg"
                count = count + 1
                self.d.screenshot(comparison)
                sleep(1)
                print()
                if image_comparison.compare_image_with_histogram(original, comparison):
                    print(">>>蓝牙关闭时， 显示正常")
                else:
                    print("ERROR MSG -- 蓝牙关闭时， 显示异常")
                    self.d.screenshot(self.path + "image\\setting\\error蓝牙关闭时显示异常.png")
                    msg = "case：反复开启关闭WIFI\n图片对比：蓝牙关闭时，显示异常\n" + "原始图：" + original + "\n" + "对比图：" + comparison + "\n"
                    self.log_data.append(msg)
                    result = "fail"
        return result

    def case2(self, num=201):
        '''
        蓝牙已激活 ，反复进入搜索蓝牙装置然后取消搜索50次；检查是否会出现异常
        :param num:
        :return:
        '''
        result = "pass"
        err_count = 2
        while True:
            self.d.screen_on()
            if self.d(resourceId="com.android.settings:id/switch_text").get_text() == "开启":
                break
            else:
                self.setting.bluetooth_switch()
                err_count = err_count - 1
                if err_count == 0:
                    self.d.screenshot(self.path + "image\\setting\\error反复进入搜索蓝牙装置然后取消搜索初始化出现异常.png")
                    self.setting.stop()
                    self.setting.start()
                    self.setting.list_bluetooth()
                    break
        for i in range(num):
            sleep(3)
            self.d.screen_on()
            if self.d(resourceId="android:id/title")[1].get_text() != '':
                print(">>>反复搜索蓝牙装置然后取消搜索， 可正常搜索到蓝牙设备")
                print(self.d(resourceId="android:id/title")[1].get_text())
                self.setting.bluetooth_more()
                if self.setting.bluetooth_wait_more_refresh():
                    self.d.screen_on()
                    self.setting. bluetooth_more_refresh()
            else:
                print(">>>反复搜索蓝牙装置然后取消搜索，等待3秒未，搜索到可用蓝牙")
                comparison = self.path + "image\\setting\\error反复搜索蓝牙装置然后取消搜索等待3秒未搜索到可用蓝牙.png"
                self.d.screenshot(comparison)
                msg = "case：反复开启关闭WIFI\n图片对比：蓝牙关闭时，显示异常\n" +  comparison + "\n"
                self.log_data.append(msg)
                result = "fail"
        return result

    def tear_down(self, casename):
        self.d.screen_on()
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.d.screenshot(self.path + "image\\setting\\" + casename + nowTime + ".jpg")
        adb.get_meminfo(self.d)
        adb.get_battery(self.d)
        adb.get_cpuinfo(self.d)
        self.setting.stop()
        print(casename)
        return time

    def run(self):
        path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
        path = path+"\\resource\\log\\setting_wifi.log"

        count = 2

        actual_result = ""
        err_path = ""
        starttime1 = self.set_up("开始测试：反复开启关闭蓝牙"+str(count)+"次")
        try:
            t_reference_result1 = self.case1(count)
        except BaseException as e:
            t_reference_result1 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：反复开启关闭蓝牙"+str(count)+"次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\setting\\反复开启关闭蓝牙"+str(count)+"次出现异常.jpg"
            self.d.screenshot(err_path)
            self.setting.stop()
            self.d.app_stop_all()
        endtime1 = self.tear_down("结束测试：反复开启关闭蓝牙"+str(count)+"次，检查是否会出现蓝牙无法开启等其它异常现象")
        self.st_blue_report_data.append(
            {"t_module": "设置-蓝牙", "t_case": "压力测试", "t_steps": "反复开启关闭蓝牙"+str(count)+"次\n检查是否会出现蓝牙无法开启等其它异常现象",
             "t_expected_result": "应可以正常关闭及开启",
             "t_actual_result": actual_result + "\n" + err_path, "t_start_time": starttime1, "t_end_time": endtime1,
             "t_reference_result": t_reference_result1, "t_result": ""})


        actual_result = ""
        err_path = ""
        starttime2 = self.set_up("开始测试：蓝牙已激活,反复进入搜索蓝牙装置然后取消搜索"+str(count)+"次")
        try:
            t_reference_result2 = self.case2(count)
        except BaseException as e:
            t_reference_result2 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：蓝牙已激活 ，反复进入搜索蓝牙装置然后取消搜索"+str(count)+"次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\setting\\蓝牙已激活,反复进入搜索蓝牙装置然后取消搜索"+str(count)+"次；出现异常.jpg"
            self.d.screenshot(err_path)
            self.setting.stop()
            self.d.app_stop_all()
        endtime2 = self.tear_down("结束测试：蓝牙已激活 ，反复进入搜索蓝牙装置然后取消搜索"+str(count)+"次")
        self.st_blue_report_data.append(
            {"t_module": "设置-蓝牙", "t_case": "压力测试", "t_steps": "蓝牙已激活 ，反复进入搜索蓝牙装置然后取消搜索"+str(count)+"次\n检查是否会出现异常，",
             "t_expected_result": "可以正常搜索，取消搜索；无异常",
             "t_actual_result": actual_result + "\n" + err_path, "t_start_time": starttime2, "t_end_time": endtime2,
             "t_reference_result": t_reference_result2, "t_result": ""})
        loginfo.writer_log(path, self.log_data)
        return self.st_blue_report_data