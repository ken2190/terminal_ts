from src.settings import Settings
import random

from time import sleep
from src.general import image_comparison
from src.general import adb
import datetime
import os
from src import loginfo



class Ts_Setting_Wifi():
    def __init__(self, d):
        self.d = d
        self.setting = Settings(self.d)
        self.path = image_comparison.get_path()

        self.log_data = []
        self.ts_wifi_report_data = []

    def set_up(self, casename):
        print(casename)
        self.d.screen_on()

        # 判断是否锁屏状态
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()

        # 停止并启动设置
        self.setting.stop()
        self.setting.start()
        self.setting.list_wlan()

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
        反复开启关闭WIFI50次，检查是否会出现WIFI无法开启等其它异常现象
        :param num:反复开关机的次数, 若执行50次，就填入51
        :return:
        '''
        self.d.screen_on()
        original = self.path + "image\\setting\\WIFI_反复开启关闭WIFI.png"
        count = 1
        err_count = 2
        image_count = 1
        result = "pass"
        while True:
            sleep(1)
            self.d.screen_on()
            if self.d(resourceId="com.android.settings:id/switch_text", text=u"关闭").wait(timeout=2.0):
                adb.chmod_adb("adb shell screencap -p /sdcard/Screenshot.png")
                adb.chmod_adb("adb pull /sdcard/Screenshot.png "+original)
                break
            else:
                self.setting.wlan_switch()
                err_count = err_count - 1
                if err_count == 0:
                    self.d.screenshot(self.path + "image\\setting\\error反复开启关闭wifi初始化出现异常.png")
                    self.setting.stop()
                    self.setting.start()
                    self.setting.list_wlan()
                    break

        for i in range(num):
            self.d.screen_on()
            self.setting.wlan_switch()
            if self.d(resourceId="com.android.settings:id/switch_text", text=u"开启").wait(timeout=2.0):
                sleep(3)
                if self.d(resourceId="android:id/title")[0].get_text() != '':
                    print(">>>WIFI已开启时， 可正常搜索到WIFI")
                    print(self.d(resourceId="android:id/title")[0].get_text())
                else:
                    print(">>>WIFI已开启时， 等待3秒；未搜索到可用WIFI")
                    self.d.screenshot(self.path + "image\\setting\\errorWIFI已开启时等待2秒未搜索到可用WIFI"+image_count+".png")
                    msg = "WIFI已开启时， 等待2秒；未搜索到可用WIFI\n图片地址："+self.path + "image\\setting\\errorWIFI已开启时等待3秒未搜索到可用WIFI"+image_count+".png"
                    image_count = image_count + 1
                    self.log_data.append(msg)
                    result = "fail"
            else:
                sleep(3)
                comparison = self.path + "image\\setting\\WIFI_反复开启关闭WIFI" + str(count) + ".jpg"
                count = count + 1
                self.d.screenshot(comparison)
                sleep(1)
                print()
                if image_comparison.compare_image_with_histogram(original,comparison):
                    print(">>>WIFI关闭时， 显示正常")
                else:
                    print("ERROR MSG -- WIFI关闭时， 显示异常")
                    self.d.screenshot(self.path + "image\\setting\\errorWIFI关闭时显示异常.png")
                    msg = "case：反复开启关闭WIFI\n图片对比：WIFI关闭时，显示异常\n"+"原始图：" +original + "\n" +"对比图："+ comparison +"\n"
                    result = "fail"
                    self.log_data.append(msg)
        return result


    def case2(self, num=201, ping_num=100):
        '''
        不断从数据连接与WIFI之前切换，检查是否会出现无法切换，无法上网等现象（默认已插入sim卡）
        :param num: 不断切换网络的次数, 若执行50次，就填入51
        :return:
        '''
        self.d.screen_on()
        self.setting.auto_connect_wifi()   # 自动连接wifi
        err_wifi_count = 1
        err_data_count = 1
        result = "pass"
        for i in range(num):
            sleep(2)
            self.d.screen_on()
            if self.d(resourceId="com.android.settings:id/switch_text", text=u"开启").wait(timeout=2.0):
                if self.d(resourceId="android:id/title")[0].get_text() != '':
                    print(">>>WIFI已开启时， 可正常搜索到WIFI")
                    print(self.d(resourceId="android:id/title")[0].get_text())
                    if self.d(resourceId="android:id/summary", text=u"已连接").wait(timeout=2.0):
                        wifi_name = self.d(resourceId="android:id/title")[0].get_text()
                        print(">>>WIFI已开启时，正常连接到WIFI：" + wifi_name)
                        adb_msg_wifi = adb.read_adb("adb shell ping -c "+str(ping_num)+" www.baidu.com")
                        print(adb_msg_wifi)
                        if "0% packet loss" in adb_msg_wifi or "1% packet loss" in adb_msg_wifi:
                            print("pass")
                        else :
                            print("WIFI存在丢包情况")
                            self.d.screen_on()
                            err_wifi_image = self.path + "image\\setting\\error不断从数据连接与WIFI之前切换WIFI存在丢包情况" + str(err_wifi_count) + ".png"
                            self.d.screenshot(err_wifi_image)
                            self.log_data.append(err_wifi_image + "\n" + adb_msg_wifi)
                            err_wifi_count = err_wifi_count+1
                            result = "fail"
                    else :
                        print("WIFI连接异常")

                        err_wifi_image = self.path + "image\\setting\\error不断从数据连接与WIFI之前切换WIFI连接异常" + str(err_wifi_count) + ".png"
                        self.d.screenshot(err_wifi_image)
                        self.log_data.append(err_wifi_image + "\n")
                        err_wifi_count = err_wifi_count + 1
                        self.setting.wlan_switch()
                        self.d.screen_on()
                        result = "fail"
                        continue
            else :
                self.d.screen_on()
                adb_msg_data = adb.read_adb("adb shell ping -c "+str(ping_num)+" www.baidu.com")
                print(adb_msg_data)
                if "0% packet loss" in adb_msg_data or "1% packet loss" in adb_msg_data:
                    print("pass")
                elif "unknown host www.baidu.com" in adb_msg_data :
                    print("数据连接异常")
                    err_data_image = self.path + "image\\setting\\error不断从数据连接与WIFI之前切换数据连接异常" + str(
                        err_data_count) + ".png"
                    self.d.screenshot(err_data_image)
                    self.log_data.append(err_data_image + "\n" + adb_msg_data)
                    err_data_count = err_data_count + 1
                    result = "fail"
                else:
                    print("数据存在丢包情况")
                    err_data_image = self.path + "image\\setting\\error不断从数据连接与WIFI之前切换数据存在丢包情况"+str(err_data_count)+".png"
                    self.d.screenshot(err_data_image)
                    self.log_data.append(err_data_image + "\n" + adb_msg_data)
                    err_data_count = err_data_count + 1
                    result = "fail"
            self.d.screen_on()
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            apk = self.d.current_app()
            packageName = apk['package']
            if packageName != "com.android.settings":
                self.setting.start()
                self.setting.list_wlan()
            self.setting.wlan_switch()
        return result

    def case3(self,num=201, ping_num=100):
        '''
        无线网络和移动网络中首选网络模式切换
        :param num: 不断切换网络的次数, 若执行50次，就填入51
        :return:
        '''
        self.setting.auto_connect_wifi()  # 自动连接wifi
        self.d.screen_on()
        result = "pass"
        result_data = "pass"
        err_wifi_count = 1
        err_data_count = 1

        for i in range(num):
            sleep(2)
            self.d.screen_on()
            if self.d(resourceId="com.android.settings:id/switch_text", text=u"开启").wait(timeout=3.0):
                print(">>>WIFI已开启")
                if self.d(resourceId="android:id/title")[0].wait(timeout=2):
                    print(">>>WIFI已开启时， 可正常搜索到WIFI")
                    print(self.d(resourceId="android:id/title")[0].get_text())
                    if self.d(resourceId="android:id/summary", text=u"已连接").wait(timeout=10.0):
                        self.d.screen_on()
                        wifi_name = self.d(resourceId="android:id/title")[0].get_text()
                        print(">>>WIFI已开启时，正常连接到WIFI：" + wifi_name)
                        adb_msg_wifi = adb.read_adb("adb shell ping -c "+str(ping_num)+" www.sina.com")
                        # print(adb_msg_wifi)
                        if "0% packet loss" in adb_msg_wifi or "1% packet loss" in adb_msg_wifi:
                            print("pass")
                        else:
                            print("WIFI存在丢包情况")
                            self.d.screen_on()
                            err_wifi_image = self.path + "image\\setting\\error无线网络和移动网络中首选网络模式切换WIFI存在丢包情况" + str(
                                err_wifi_count) + ".png"
                            self.d.screenshot(err_wifi_image)
                            self.log_data.append(err_wifi_image + "\n" + adb_msg_wifi)
                            err_wifi_count = err_wifi_count + 1
                            result = "fail"
                    else:
                        print("WIFI连接异常")
                        self.d.screen_on()
                        err_wifi_image = self.path + "image\\setting\\error无线网络和移动网络中首选网络模式切换WIFI连接异常" + str(
                            err_wifi_count) + ".png"
                        self.d.screenshot(err_wifi_image)
                        self.log_data.append(err_wifi_image + "\n")
                        err_wifi_count = err_wifi_count + 1
                        result = "fail"
                self.d.screen_on()
                if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                    self.d.unlock()
                    self.setting.start()
                    self.setting.list_wlan()
                self.setting.wlan_switch()
                self.d.press("back")
                self.d.screen_on()
            print("进入数据测试")
            for count in range(4):
                self.d.screen_on()
                if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                    self.d.unlock()
                apk = self.d.current_app()
                packageName = apk['package']
                if packageName != "com.android.phone":
                    self.setting.start()
                elif self.d(resourceId="com.android.settings:id/title", text=u"更多").wait(timeout=2) != True:
                    self.setting.start()
                self.setting.list_more()
                self.setting.more_mobile_network()
                # count = random.randint(0, 3)
                self.setting.more_mb_network_type()
                if count == 0:
                    data_type = "4G"
                elif count == 1:
                    data_type = "3G/2G"
                elif count == 2:
                    data_type = "2G"
                else:
                    data_type = "4G/3G/2G"
                if self.setting.more_mb_network_type_cut(data_type):
                    print("网络切换成功，等待10秒")
                    sleep(10)
                    adb_msg_data = adb.read_adb("adb shell ping -c " + str(ping_num) + " www.sina.com")
                    print(adb_msg_data)
                    if "unknown host www.sina.com" in adb_msg_data:
                        print("数据连接异常")
                        err_data_image = self.path + "image\\setting\\error无线网络和移动网络中首选网络模式切换数据连接异常" + str(
                            err_data_count) + ".png"
                        self.d.screenshot(err_data_image)
                        self.log_data.append(err_data_image + "\t " + data_type + "\n" + adb_msg_data)
                        err_data_count = err_data_count + 1
                        result_data = ""
                        result = "fail"
                        continue
                    elif "0% packet loss" in adb_msg_data or "1% packet loss" in adb_msg_data:
                        print(result_data)
                    else:
                        result_data = "fail"
                        print(result_data)

                    if result_data == "fail":
                        print("首选网络类型为：" + data_type + "时；数据存在丢包情况")
                        self.d.screen_on()
                        err_data_image = self.path + "image\\setting\\error无线网络和移动网络中首选网络模式切换数据存在丢包情况" + str(
                            err_data_count) + ".png"
                        self.d.screenshot(err_data_image)
                        self.log_data.append(err_data_image + "\n 连接方式为：" + data_type + "\n" + adb_msg_data)
                        err_wifi_count = err_data_count + 1
                        result = "fail"
                        result_data = "pass"
                else:
                    print("ERROR 切换 首选网络类型 失败，请检查是否插入sim卡")
                    self.d.screen_on()
                    err_data_image = self.path + "image\\setting\\error无线网络和移动网络中首选网络模式切换数据首选网络类型切换失败" + str(
                        err_data_count) + ".png"
                    self.d.screenshot(err_data_image)
                    self.log_data.append(err_data_image + "\n")
                    err_wifi_count = err_data_count + 1
                    result = "fail"
                    result_data = "pass"
                    break
            self.d.screen_on()
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            self.setting.start()
            self.setting.list_wlan()
            self.setting.wlan_switch()

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
        starttime1 = self.set_up("开始测试：重复开启WIFI开关200次")
        try:
            t_reference_result1 = self.case1(count)
        except BaseException as e:
            t_reference_result1 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：重复开启WIFI开关"+str(count)+"次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\setting\\重复开启WIFI开关"+str(count)+"次；出现异常.jpg"
            self.d.screenshot(err_path)
            self.setting.stop()
            self.d.app_stop_all()
        endtime1 = self.tear_down("结束测试：重复开启WIFI开关"+str(count)+"次")
        self.ts_wifi_report_data.append(
            {"t_module": "设置-WIFI", "t_case": "压力测试", "t_steps": "反复开启关闭WIFI "+str(count)+"次\n检查是否会出现WIFI无法开启等其它异常现象",
             "t_expected_result": "可以正常开启关闭",
             "t_actual_result":  actual_result + "\n" + err_path, "t_start_time": starttime1, "t_end_time": endtime1,
             "t_reference_result": t_reference_result1, "t_result": ""})
        sleep(2)


        actual_result = ""
        err_path = ""
        starttime2 = self.set_up("开始测试：不断从数据连接与WIFI之前切换"+str(count)+"次")
        try:
            t_reference_result2 = self.case2(count)
        except BaseException as e:
            t_reference_result2 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：不断从数据连接与WIFI之前切换"+str(count)+"次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\setting\\不断从数据连接与WIFI之前切换"+str(count)+"次；出现异常.jpg"
            self.d.screenshot(err_path)
            self.setting.stop()
            self.d.app_stop_all()
        endtime2 = self.tear_down("结束测试：不断从数据连接与WIFI之前切换"+str(count)+"次")
        self.ts_wifi_report_data.append(
            {"t_module": "设置-WIFI", "t_case": "压力测试", "t_steps": "不断从数据连接与WIFI之前切换"+str(count)+"次\n检查是否会出现无法切换，无法上网等现角",
             "t_expected_result": "可以正常切换及上网",
             "t_actual_result":  actual_result + "\n" + err_path, "t_start_time": starttime2, "t_end_time": endtime2,
             "t_reference_result": t_reference_result2, "t_result": ""})

        actual_result = ""
        err_path = ""
        starttime3 = self.set_up("开始测试：无线网络和移动网络中首选网络模式切换"+str(count)+"次")
        try:
            t_reference_result3 = self.case3(count)
        except BaseException as e:
            t_reference_result3 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：无线网络和移动网络中首选网络模式切换"+str(count)+"次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\setting\\无线网络和移动网络中首选网络模式切换"+str(count)+"次；出现异常.jpg"
            self.d.screenshot(err_path)
            self.setting.stop()
            self.d.app_stop_all()
        endtime3 = self.tear_down("结束测试：无线网络和移动网络中首选网络模式切换"+str(count)+"次")
        self.ts_wifi_report_data.append(
            {"t_module": "设置-WIFI", "t_case": "压力测试", "t_steps": "无线网络和移动网络中首选网络模式切换"+str(count)+"次\n检查是否会出现无法切换，无法上网等现角",
             "t_expected_result": "可以正常切换及上网",
             "t_actual_result":  actual_result + "\n" + err_path, "t_start_time": starttime3, "t_end_time": endtime3,
             "t_reference_result": t_reference_result3, "t_result": ""})


        loginfo.writer_log(path, self.log_data)
        return self.ts_wifi_report_data
