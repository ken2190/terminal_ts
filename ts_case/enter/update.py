import os
import time
import uiautomator2 as u2
from src.general.unlock import *
from src.general import adb
from src.settings import *
from ts_case.init_operation import Init_Operation
from src.message import Message1
from src.camera import Camera
from src.clock import Clock
from src.third_party import Tx_QQ
from src.camtalk import CamTalk
from src.nictalk import NicTalk
from src.music import Music
from src.chrome import Chrome



class Update():


    def __init__(self,d):
        self.d=d
        self.chrome=Chrome(d)
        self.music=Music(d)
        self.init_operation=Init_Operation()
        self.nictalk = NicTalk(self.d)
        self.camtalk = CamTalk(self.d)
        self.qq=Tx_QQ(self.d)
        self.clock=Clock(self.d)
        self.camera=Camera(self.d)
        self.settings = Settings(self.d)
        self.message=Message1(self.d)
        self.path = os.path.abspath(os.path.join(os.getcwd(), "../..")) + "\\enter_resource\\"
        self.init_operation=Init_Operation()

    def set_up(self, test_time='1'):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>停止所有运行的app')
        self.d.app_stop_all()
        self.settings.display_setting()
        self.settings.auto_connect_wifi()
        self.d.press("home")
        print("开始测试：" + test_time)
        print(start_time)
        return start_time

    def Case_SD_update(self):
        result='pass'
        result_message=''
        print('---------->请将升级包放到指定的目录；\n请保证目录只有一个升级包；\n尼加拉瓜版本升级目录：NCA_update；\n柬埔寨版本升级目录：KHM_update；')
        if adb.acquire_battery_message(self.path)>31:
            versions = adb.read_adb('adb shell getprop ro.build.display.id')
            update_file = ""
            if 'KHM' in versions:
                files = os.listdir(self.path + 'update_file\\KHM_update')
                if files == []:
                    print('没有升级包不执行升级')
            elif 'NCA' in versions:
                files = os.listdir(self.path+'update_file\\NCA_update')
                if files==[]:
                    print('没有升级包不执行升级')
            print("\n\n####################\n请在10分钟内，在"+self.path+"update_file\ 路径下根据版本放入指定目录\n请保证目录只有一个升级包；\n尼加拉瓜版本升级文件夹：NCA_update；\n柬埔寨版本升级文件夹：KHM_update；\n\n")
            time.sleep(60*10)
            self.message.start_message()
            message_num = self.message.message_num()
            self.message.stop_message()
            if 'KHM' in versions:
                files = os.listdir(self.path + 'update_file\\KHM_update')
                if files==[]:
                    print('没有找到升级包，升级失败')
                else:
                    self.camtalk.add_linkman()
                    for i in files:
                        print(i)
                        update_file=i
                        adb.read_adb('adb push '+self.path+'update_file\\KHM_update\\'+i+' /sdcard/')
                        os.remove(self.path+'update_file\\KHM_update\\'+i)
                    self.settings.enter_about_phone()
                    self.settings.click_system_upgrade()
                    self.settings.click_system_update_set()
                    if self.settings.click_SD_update()==True:
                        self.settings.click_install()
                        time.sleep(400)
                        self.d = u2.connect()
                        self.__init__(self.d)
                        for i in range(0, 10):
                            if adb.detection_terminal_connect() == True:
                                break
                            else:
                                time.sleep(20)
                        self.d.screen_on()
                        if self.camtalk.verification_add_linkman()==False:
                            result='fail'
                            result_message = result_message + '验证联系人失败\n'
                        self.message.start_message()
                        message_num1 = self.message.message_num()
                        self.message.stop_message()
                        if message_num!=message_num1:
                            result = 'fail'
                            result_message = result_message + '验证短信数量失败\n'

                    else:
                        self.settings.click_folder()
                        self.settings.select_updete_file(update_file)
                        self.settings.click_install()
                        time.sleep(400)
                        self.d = u2.connect()
                        self.__init__(self.d)
                        for i in range(0,10):
                            if adb.detection_terminal_connect()==True:
                                break
                            else:
                                time.sleep(20)
                        self.d.screen_on()
                        if self.camtalk.verification_add_linkman()==False:
                            result='fail'
                            result_message=result_message+'验证联系人失败\n'
                        self.message.start_message()
                        message_num1 = self.message.message_num()
                        self.message.stop_message()
                        if message_num!=message_num1:
                            result = 'fail'
                            result_message = result_message + '验证短信数量失败\n'
            elif 'NCA' in versions:
                files = os.listdir(self.path+'update_file\\NCA_update')
                if files==[]:
                    print('没有找到升级包，升级失败')
                else:
                    self.nictalk.add_linkman()
                    for i in files:
                        adb.read_adb('adb push '+self.path+'update_file\\NCA_update\\'+i+' /sdcard/')
                        os.remove(self.path + 'update_file\\NCA_update\\' + i)
                    self.settings.enter_about_phone()
                    self.settings.click_system_upgrade()
                    self.settings.click_system_update_set()
                    if self.settings.click_SD_update()==True:
                        self.settings.click_install()
                        time.sleep(400)
                        self.d = u2.connect()
                        self.__init__(self.d)
                        for i in range(0,10):
                            if adb.detection_terminal_connect()==True:
                                break
                            else:
                                time.sleep(20)
                        self.d.screen_on()
                        if self.nictalk.verification_add_linkman()==False:
                            result = 'fail'
                            result_message = result_message + '验证联系人失败\n'
                        self.message.start_message()
                        message_num1 = self.message.message_num()
                        self.message.stop_message()
                        if message_num!=message_num1:
                            result = 'fail'
                            result_message = result_message + '验证短信数量失败\n'
                    else:
                        self.settings.click_folder()
                        self.settings.select_updete_file(update_file)
                        self.settings.click_install()
                        time.sleep(400)
                        self.d = u2.connect()
                        self.__init__(self.d)
                        for i in range(0,10):
                            if adb.detection_terminal_connect()==True:
                                break
                            else:
                                time.sleep(20)
                        self.d.screen_on()
                        if self.nictalk.verification_add_linkman()==False:
                            result = 'fail'
                            result_message = result_message + '验证联系人失败\n'
                        self.message.start_message()
                        message_num1 = self.message.message_num()
                        self.message.stop_message()
                        if message_num!=message_num1:
                            result = 'fail'
                            result_message = result_message + '验证短信数量失败\n'
        else:
            print('当前手机电量无法完成升级')
        return result,result_message

    def Case_recover_factory(self):
        result = 'pass'
        result_message = ''
        self.settings.recover_factory_set()
        print("\n\n已进行恢复出厂设置，请在手机重启成功后手动选择与电脑的连接\n\n")
        time.sleep(60*5)
        for i in range(0, 20):
            if adb.detection_terminal_connect() == True:
                break
            else:
                time.sleep(30)
        time.sleep(20)
        print("\n\n开始执行安装uiautomator，请手动勾选允许安装\n\n")
        self.init_operation.init_equipment()
        time.sleep(50)
        self.d=u2.connect()
        self.__init__(self.d)

        versions = adb.read_adb('adb shell getprop ro.build.display.id')
        if 'KHM' in versions:
            if self.settings.change_language()=='柬埔寨':
                print('---------->恢复出厂设置语言恢复正确')
            else:
                result='fail'
                print('---------->恢复出厂设置，语言没有正确恢复')
                result_message=result_message+'语言没有恢复出厂设置\n'
            self.settings.display_setting()
            self.settings.auto_connect_wifi()
            if self.camtalk.assert_login() == True:
                if  '柬埔寨' in self.camtalk.acquire_state_name():
                    print('---------->talk恢复出厂设置正确')
                else:
                    result = 'fail'
                    print('---------->talk恢复出厂设置国家显示错误')
                    result_message = result_message + 'talk恢复出厂设置国家显示错误\n'
            else:
                result = 'fail'
                print('---------->talk没有进入登录界面')
                result_message = result_message + 'talk没有进入登录界面\n'
            self.chrome.start()
            if self.chrome.KHM_assert_browse_history() == True:
                print('---------->浏览器没有访问记录，恢复出厂设置正常')
            else:
                result = 'fail'
                print('---------->浏览器还有访问记录，恢复出厂设置失败')
                result_message = result_message + '浏览器还有访问记录，恢复出厂设置失败\n'
        elif 'NCA' in versions:
            if self.settings.change_language() == '尼加拉瓜':
                print('---------->恢复出厂设置语言恢复正确')
            else:
                result='fail'
                print('---------->恢复出厂设置，语言没有正确恢复')
                result_message = result_message + '恢复出厂设置，语言没有正确恢复\n'
            self.settings.display_setting()
            self.settings.auto_connect_wifi()
            if self.nictalk.assert_login() == True:
                if  '尼加拉瓜' in self.nictalk.acquire_state_name():
                    print('---------->talk恢复出厂设置正确')
                else:
                    result = 'fail'
                    print('---------->talk恢复出厂设置国家显示错误')
                    result_message = result_message + 'talk恢复出厂设置国家显示错误\n'
            else:
                result = 'fail'
                print('---------->talk没有进入登录界面')
                result_message = result_message + 'talk没有进入登录界面'
            if self.chrome.KHM_assert_browse_history() == True:
                print('---------->浏览器没有访问记录，恢复出厂设置正常')
            else:
                result = 'fail'
                print('---------->浏览器还有访问记录，恢复出厂设置失败')
                result_message = result_message + '浏览器还有访问记录，恢复出厂设置失败\n'
        self.message.start_message()
        if self.message.message_num()==0:
            print('短信成功恢复出厂设置')
        else:
            result = 'fail'
            print('短信没有恢复出厂设置')
            result_message = result_message + '短信没有恢复出厂设置\n'
        self.camera.CameraOn()
        if self.camera.Pop_Up()==False:
            result='fail'
            print('---------->相机没有恢复出厂设置')
            result_message=result_message+'相机没有恢复出厂设置\n'
        else:
            print('相机恢复出厂设置正常')
        self.music.start()
        if self.music.acquire_music_list()==True:
            result = 'fail'
            print('---------->音乐没有恢复出厂设置')
            result_message = result_message + '音乐没有恢复出厂设置\n'
        else:
            print('音乐恢复出厂设置正常')
        return result,result_message

    def teardown(self):
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return end_time

    def run(self):
        self.update_report = []
        start_time1 = self.set_up(test_time='开始测试：一次SD卡升级')
        actul_reselt = ''
        path = ''
        try:
            result1, result_message1 = self.Case_SD_update()
        except BaseException as e:
            result1 = 'Fail'
            print("except:", e)
            actul_reselt = str(e)[7:]
            result_message1 = '一次SD卡升级出现异常'
            print(
                "=====>>>>>执行测试：一次SD卡升级出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'built_in_apk_img\\' + "一次SD卡升级出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time1 = self.teardown()
        self.update_report.append(
            {"t_module": "B34:SD卡升级", "t_case": "入口测试","t_steps": "一次SD卡升级",
             "t_expected_result": "1.手机能过SD卡正确升级，检查联系人和短信是否丢失",
             "t_actual_result": actul_reselt + '\n' + path + '\n' + result_message1,
             "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})
        time.sleep(5)

        start_time2 = self.set_up(test_time='入口测试完成后恢复出厂设置')
        actul_reselt = ''
        path = ''
        try:
            result2, result_message2 = self.Case_recover_factory()
        except BaseException as e:
            result2 = 'Fail'
            print("except:", e)
            actul_reselt = str(e)[7:]
            result_message2 = '入口测试完成后恢复出厂设置'
            print(
                "=====>>>>>执行测试：入口测试完成后恢复出厂设置,出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'built_in_apk_img\\' + "入口测试完成后恢复出厂设置出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time2 = self.teardown()
        self.update_report.append(
            {"t_module": "B38恢复出厂设置", "t_case": "入口测试",
             "t_steps": "入口测试完成后恢复出厂设置",
             "t_expected_result": "1.系统还原为默认状况，语音，设置等信息都为默认，之前操作记录和保存信息都被删除，无网页浏览痕迹，通话记录，拍摄相片，录音文件等",
             "t_actual_result": actul_reselt + '\n' + path + '\n' + result_message2,
             "t_start_time": start_time2, "t_end_time": end_time2,
             "t_reference_result": result2, "t_result": ""})
        time.sleep(5)
        return self.update_report



if __name__=='__main__':
    d=u2.connect()
    a=Update(d)
    a.Case_SD_update()
    a.Case_recover_factory()
