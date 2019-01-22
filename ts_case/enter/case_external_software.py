
import time
import os
from src.settings import Settings
from src.cootv import KHM_Cootv
from src.cootv import NCA_Cootv
from src.coo_clean import Coo_Clean
from src.coobill import KHM_CooBill
from src.coobill import NCA_CooBill
from src.mi_cootel import Mi_CooTel
from src.camtalk import CamTalk
from src.nictalk import NicTalk
from src.general import adb
class External_software():

    def __init__(self,d):
        self.d=d
        self.settings=Settings(d)
        self.ncacootv=NCA_Cootv(d)
        self.khmcootv = KHM_Cootv(d)
        self.cooclean=Coo_Clean(d)
        self.ncacoobill=NCA_CooBill(d)
        self.khmcoobill = KHM_CooBill(d)
        self.mi_cootel=Mi_CooTel(d)
        self.camtalk=CamTalk(d)
        self.nictalk=NicTalk(d)
        self.path = os.path.abspath(os.path.join(os.getcwd(), "../..")) + "\\enter_resource\\"
        self.NCA_test_report=[]
        self.KHM_test_report=[]
        self.test_report=[]

    def set_up(self,test_time):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>停止所有运行的app')
        self.d.app_stop_all()
        self.d.press("home")
        print(start_time)
        return start_time


    def teardown(self):
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return end_time



    def NCA_run(self):
        start_time1 = self.set_up(test_time='开始测试：内置应用运行：CooTv')
        actul_reselt = ''
        path = ''
        result1='pass'
        result_message1=''
        try:
            self.ncacootv.Case_menu_traversal()
        except BaseException as e:
            if self.d(resourceId="android:id/message").wait(timeout=5)==True:
                self.d(resourceId="android:id/button1").click()
            result1 = 'Fail'
            print("except:", e)
            actul_reselt = str(e)[7:]
            result_message1 = '内置应用运行：CooTv.出现异常'
            print("=====>>>>>执行测试：内置应用运行：CooTv出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'cootv_img\\' + "内置应用运行：CooTv-出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time1 = self.teardown()
        self.NCA_test_report.append(
            {"t_module": "B37-软件配置", "t_case": "入口测试",
             "t_steps": "内置应用运行及版本信息-cootv",
             "t_expected_result": "1.点击应用所有菜单执行正常",
             "t_actual_result": actul_reselt + '\n' + path + '\n' + result_message1,
             "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})
        time.sleep(5)


        start_time2 = self.set_up(test_time='开始测试：内置应用运行：CooBill')
        actul_reselt = ''
        path = ''
        result2='pass'
        try:
            result_message2 =self.ncacoobill.Case_all_operation()
        except BaseException as e:
            if self.d(resourceId="android:id/message").wait(timeout=5)==True:
                self.d(resourceId="android:id/button1").click()
            result2 = 'Fail'
            print("except:", e)
            actul_reselt = str(e)[7:]
            result_message2 = '内置应用运行：CooBill-出现异常'
            print(
                "=====>>>>>执行测试：内置应用运行：CooBill-出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'coobill_img\\' + "内置应用运行：CooBill-出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time2 = self.teardown()
        self.NCA_test_report.append(
            {"t_module": "B37-软件配置", "t_case": "入口测试",
             "t_steps": "内置应用运行及版本信息-CooBill",
             "t_expected_result": "1.点击应用所有菜单执行正常",
             "t_actual_result": actul_reselt + '\n' + path + '\n' + result_message2,
             "t_start_time": start_time2, "t_end_time": end_time2,
             "t_reference_result": result2, "t_result": ""})
        time.sleep(5)

        start_time3 = self.set_up(test_time='开始测试：内置应用运行：酷管家')
        actul_reselt = ''
        path = ''
        result3 = 'pass'
        try:
            result_message3 = self.cooclean.Case_menu_traversal()
        except BaseException as e:
            if self.d(resourceId="android:id/message").wait(timeout=5)==True:
                self.d(resourceId="android:id/button1").click()
            result3 = 'Fail'
            print("except:", e)
            actul_reselt = str(e)[7:]
            result_message3 = '内置应用运行：酷管家-出现异常'
            print(
                "=====>>>>>执行测试：内置应用运行：CooBill-出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'cooclean_img\\' + "内置应用运行：酷管家-出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time3 = self.teardown()
        self.NCA_test_report.append(
            {"t_module": "B37-软件配置", "t_case": "入口测试","t_steps": "内置应用运行及版本信息-酷管家",
             "t_expected_result": "1.点击应用所有菜单执行正常",
             "t_actual_result": actul_reselt + '\n' + path + '\n' + result_message3,
             "t_start_time": start_time3, "t_end_time": end_time3,
             "t_reference_result": result3, "t_result": ""})
        time.sleep(5)



        start_time4 = self.set_up(test_time='开始测试：内置应用运行：mi_cootel')
        actul_reselt = ''
        path = ''
        result4 = 'pass'
        try:
            result_message4 = self.mi_cootel.Case_combination()
        except BaseException as e:
            if self.d(resourceId="android:id/message").wait(timeout=5)==True:
                self.d(resourceId="android:id/button1").click()
            result4 = 'Fail'
            print("except:", e)
            actul_reselt = str(e)[7:]
            result_message4 = '内置应用运行：mi_cootel-出现异常'
            print(
                "=====>>>>>执行测试：内置应用运行：mi_cootel-出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'mi_cootel_img\\' + "内置应用运行：mi_cootel-出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time4 = self.teardown()
        self.NCA_test_report.append(
            {"t_module": "B37-软件配置", "t_case": "入口测试","t_steps": "内置应用运行及版本信息-mi_cootel",
             "t_expected_result": "1.点击应用所有菜单执行正常",
             "t_actual_result": actul_reselt + '\n' + path + '\n' + result_message4,
             "t_start_time": start_time4, "t_end_time": end_time4,
             "t_reference_result": result4, "t_result": ""})
        time.sleep(5)

        return self.NCA_test_report

    def KHM_run(self):
        start_time1 = self.set_up(test_time='开始测试：内置应用运行：CooTv')
        actul_reselt = ''
        path = ''
        result1 = 'pass'
        result_message1 = ''
        try:
            self.khmcootv.Case_menu_traversal()
        except BaseException as e:
            if self.d(resourceId="android:id/message").wait(timeout=5)==True:
                self.d(resourceId="android:id/button1").click()
            result1 = 'Fail'
            print("except:", e)
            actul_reselt = str(e)[7:]
            result_message1 = result_message1 + '内置应用运行：CooTv.出现异常'
            print(
                "=====>>>>>执行测试：内置应用运行：CooTv出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'cootv_img\\' + "内置应用运行：CooTv-出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time1 = self.teardown()
        self.KHM_test_report.append(
            {"t_module": "B37-软件配置", "t_case": "入口测试",
             "t_steps": "内置应用运行及版本信息-cootv",
             "t_expected_result": "1.点击应用所有菜单执行正常",
             "t_actual_result": actul_reselt + '\n' + path + '\n' + result_message1,
             "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})
        time.sleep(5)

        start_time2 = self.set_up(test_time='开始测试：内置应用运行：CooBill')
        actul_reselt = ''
        path = ''
        result2 = 'pass'
        try:
            result_message2 = self.khmcoobill.Case_all_operation()
        except BaseException as e:
            if self.d(resourceId="android:id/message").wait(timeout=5)==True:
                self.d(resourceId="android:id/button1").click()
            result2 = 'Fail'
            print("except:", e)
            actul_reselt = str(e)[7:]
            result_message2 = '内置应用运行：CooBill-出现异常'
            print(
                "=====>>>>>执行测试：内置应用运行：CooBill-出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'coobill_img\\' + "内置应用运行：CooBill-出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time2 = self.teardown()
        self.KHM_test_report.append(
            {"t_module": "B37-软件配置", "t_case": "入口测试","t_steps": "内置应用运行及版本信息-CooBill",
             "t_expected_result": "1.点击应用所有菜单执行正常","t_actual_result": actul_reselt + '\n' + path + '\n' + result_message2,
             "t_start_time": start_time2, "t_end_time": end_time2,"t_reference_result": result2, "t_result": ""})
        time.sleep(5)

        start_time3 = self.set_up(test_time='开始测试：内置应用运行：酷管家')
        actul_reselt = ''
        path = ''
        result3 = 'pass'
        try:
            result_message3 = self.cooclean.Case_menu_traversal()
        except BaseException as e:
            if self.d(resourceId="android:id/message").wait(timeout=5)==True:
                self.d(resourceId="android:id/button1").click()
            result3 = 'Fail'
            print("except:", e)
            actul_reselt = str(e)[7:]
            result_message3 = '内置应用运行：酷管家-出现异常'
            print(
                "=====>>>>>执行测试：内置应用运行：酷管家-出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'cooclean_img\\' + "内置应用运行：酷管家-出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time3 = self.teardown()
        self.KHM_test_report.append(
            {"t_module": "B37-软件配置", "t_case": "入口测试", "t_steps": "内置应用运行及版本信息-酷管家",
             "t_expected_result": "1.点击应用所有菜单执行正常",
             "t_actual_result": actul_reselt + '\n' + path + '\n' + result_message3,
             "t_start_time": start_time3, "t_end_time": end_time3,
             "t_reference_result": result3, "t_result": ""})
        time.sleep(5)
        return self.KHM_test_report

    def acquire_facility(self):
        '''
        获取当前手机的国家版本
        :return: NCA：尼加拉瓜   KHM：柬埔寨
        '''
        versions = adb.read_adb('adb shell getprop ro.build.display.id')
        if 'KHM' in versions:
            return 'KHM'
        elif 'NCA' in versions:
            return 'NCA'

    def run(self):
        if self.acquire_facility()=='KHM':
            self.test_report=self.KHM_run()
        elif self.acquire_facility() == 'NCA':
            self.test_report=self.NCA_run()
        return self.test_report

