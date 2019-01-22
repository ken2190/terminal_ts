import os
import time
import uiautomator2 as u2
import operator as op
from src.general.unlock import *
from src.general import adb
from src.settings import *
from src.nictalk import NicTalk
from src.camtalk import CamTalk
from ts_case.init_operation import Init_Operation
from src.message import Message1
from src.camera import Camera
from src.chrome import Chrome
class Case_SIM_Enter():

    def __init__(self,d,phong_number):
        self.d=d
        self.chrome=Chrome(d)
        self.camera=Camera(self.d)
        self.settings = Settings(self.d)
        self.message=Message1(self.d)
        self.path = os.path.abspath(os.path.join(os.getcwd(), "../..")) + "\\enter_resource\\"
        self.init_operation=Init_Operation()
        self.language = self.settings.change_language()

        self.phone_numebr = phong_number

    def set_up(self,test_time):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>停止所有运行的app')
        self.d.app_stop_all()
        self.settings.display_setting()
        self.d.press("home")
        print(start_time)
        return start_time

    def Case_send_message(self):
        '''
        发送短信和彩信的case需要人工输入接收号码，人工检测发送是否正确
        人工再次向测试机发送一条短信
        :return:
        '''
        #发送短信
        result='pass'
        result_message=''
        M_reception = self.settings.get_mcwill_number()
        if '+855' not in M_reception:
            M_reception = input('请输入M网接收者的电话号码：')
        G_reception = self.settings.get_sims_number()
        if '1' or '+86' not in G_reception:
            G_reception = input('请输入本机号码，G网测试本机：')
        G_message=input('请输入G和M网发送的内容')
        self.d.set_fastinput_ime(True)#获取输入法
        #G网新建短信
        self.message.stop_message()
        self.message.start_message()
        self.message.new_message()
        self.message.receiver(text=G_reception)
        self.message.enter_message(text=G_message)
        self.message.G_send()
        #判断短信有没有正常发送
        for i in range(0,5):
            if '接收时间：' in self.message.acquire_message(message='status'):
                print('---------->已经接收到短信')
                if G_message in self.message.acquire_message(message='content'):
                    print('短信内容验证正确')
                    break
                else:
                    print('---------->短信内容显示错误')
                    result='fail'
                    result_message=result_message+'接收到的短信内容显示错误'
                    break
            else:
                time.sleep(20)
        if '接收时间：' not in self.message.acquire_message(message='status'):
            print('---------->没有接收到短信，短信发送失败')
            result = 'fail'
            result_message = result_message + '没有接收到短信，短信发送失败'
        self.message.stop_message()
        time.sleep(3)
        # G网新建彩信发送视频
        self.message.start_message()
        self.message.new_message()
        self.message.receiver(text=G_reception)
        self.message.enter_message(text=G_message)
        self.message.add_accessory()
        self.message.add_accessory_video()
        self.message.start_transcribe_cideo()
        self.message.G_send_mms()
        error_message=self.message.contrast_message(self.path)
        #判断彩信有没有正常发送，判断彩信的详情显示是否正确
        if error_message!='':
            print('彩信对比失败')
            result='fail'
            result_message=result_message+error_message+'\n'
        self.message.stop_message()
        # G网新建彩信发送图片
        self.message.start_message()
        self.message.new_message()
        self.message.receiver(text=G_reception)
        self.message.enter_message(text=G_message)
        self.message.add_accessory()
        self.message.add_accessory_photograph()
        self.message.G_send_mms()
        error_message1 = self.message.contrast_message(self.path)
        # 判断彩信有没有正常发送，判断彩信的详情显示是否正确
        if error_message1!='':
            print('彩信对比失败')
            result='fail'
            result_message=result_message+error_message1+'\n'
        self.message.stop_message()
        # M网新建短信
        if self.settings.check_mcwill_data_status() == True:
            self.message.start_message()
            self.message.new_message()
            self.message.receiver(text=M_reception)
            self.message.enter_message(text=G_message)
            self.message.M_send()
            for i in range(0,5):
                if '接收时间：' in self.message.acquire_message(message='status'):
                    print('---------->已经接收到短信')
                    if G_message in self.message.acquire_message(message='content'):
                        print('短信内容验证正确')
                        break
                    else:
                        print('---------->短信内容显示错误')
                        result='fail'
                        result_message=result_message+'接收到的短信内容显示错误'
                        break
                else:
                    time.sleep(20)
            if '接收时间：' not in self.message.acquire_message(message='status'):
                print('---------->没有接收到短信，短信发送失败')
                result = 'fail'
                result_message = result_message + '没有接收到短信，短信发送失败'
            self.message.stop_message()
        else:
            print('----------->M网没有连接')
            result_message = result_message + 'M网没有连接'
        return result,result_message

    def sim_call_112(self):
        '''
        未插卡时进行一次紧急通话
        :return:
        '''
        result = "pass"
        actual_result = ""
        nictalk = NicTalk(self.d)
        camtalk = CamTalk(self.d)

        nictalk.stop()
        camtalk.stop()

        nictalk.start()
        current = self.d.current_app()
        if current['package'] == "com.nictalk.start":
            talk = nictalk
        else:
            camtalk.start()
            talk = camtalk
        talk.click_calls()
        talk.input_phone_number("112g")
        if talk.check_is_android():
            talk.android_click_call()
        time.sleep(5)
        if talk.check_call_show():
            talk.click_audio()
            msg = talk.get_call_state()
            if msg != "":
                pass
            print(msg)
            if talk.get_call_number() != "紧急电话号码":
                result = "fail"
                err_msg = "已插卡时拨号界面显示非紧急电话号码"
                img_name = self.path + "call\\" + err_msg + ".jpg"
                self.d.screenshot(img_name)
                actual_result = actual_result + "\n" + err_msg
                print(err_msg)
            talk.click_end_call()
        else:
            result = "fail"
            err_msg = "已插卡时紧急呼叫拨号失败"
            print(err_msg)
            img_name = self.path + "call\\" + err_msg + ".jpg"
            self.d.screenshot(img_name)
            actual_result = actual_result + "\n" + err_msg
        return actual_result, result

    def phone_book_add(self, name="移动", surname="中国", phone="10086"):
        result = "pass"
        actual_result = ""
        nictalk = NicTalk(self.d)
        camtalk = CamTalk(self.d)

        nictalk.stop()
        camtalk.stop()

        nictalk.start()
        current = self.d.current_app()
        if current['package'] == "com.nictalk.start":
            talk = nictalk
        else:
            camtalk.start()
            talk = camtalk
        # 测试新增联系人
        talk.click_contacts()
        talk.contacts_right_drawable()
        talk.right_drawable_add_contact()
        talk.add_one_contacts(name, surname, phone)
        time.sleep(2)
        self.d.press("back")
        # 检测新增联系人 并使用G网拨号
        end, getname, getphone = talk.search_one_contacts("移动")
        if end:
            if getname == surname + " " + name:
                if getphone == phone:
                    talk.one_contacts_call()
                    if talk.click_G():
                        time.sleep(6)
                        if talk.check_call_show():
                            talk.click_audio()
                            time.sleep(2)
                            if talk.get_call_state() != "正在拨号":
                                print("G网拨打电话成功")
                            else:
                                result = "fail"
                                err_msg = "G网拨打电话失败，出现一直拨号的现象"
                                img_name = self.path + "call\\" + err_msg + ".jpg"
                                self.d.screenshot(img_name)
                                actual_result = actual_result + "\n" + err_msg
                                print(err_msg)
                            time.sleep(2)
                            talk.click_end_call()
                        else:
                            result = "fail"
                            err_msg = "G网拨打电话失败，出现直接挂断的现象"
                            img_name = self.path + "call\\" + err_msg + ".jpg"
                            self.d.screenshot(img_name)
                            actual_result = actual_result + "\n" + err_msg
                            print(err_msg)
                    else:
                        err_msg = "无G网拨号方式"
                        if talk.check_call_show:
                            talk.click_end_call()
                        img_name = self.path + "call\\" + err_msg + ".jpg"
                        self.d.screenshot(img_name)
                        actual_result = actual_result + "\n" + err_msg
                        print(err_msg)
                else:
                    result = "fail"
                    err_msg = "搜索到的联系人，与添加的联系人信息不一致"
                    img_name = self.path + "call\\" + err_msg + ".jpg"
                    self.d.screenshot(img_name)
                    actual_result = actual_result + "\n" + err_msg
                    print(err_msg)
            # 执行删除联系人
            time.sleep(2)
            talk.contacts_del()
            end, getname, getphone = talk.search_one_contacts("移动")
            if end:
                if getname == surname + " " + name and getphone == phone:
                    result = "fail"
                    err_msg = "删除联系人失败"
                    img_name = self.path + "call\\" + err_msg + ".jpg"
                    self.d.screenshot(img_name)
                    actual_result = actual_result + "\n" + err_msg
                    print(err_msg)
                else:
                    print("删除联系人成功")
            else:
                print("删除联系人成功")
        self.d.press("back")

        # 使用M网拨打8888
        talk.click_calls()
        talk.input_phone_number("8888g")
        if talk.click_cootel():
            time.sleep(6)
            if talk.check_call_show():
                talk.click_audio()
                time.sleep(2)
                if talk.get_call_state() != "正在拨号":
                    talk.click_end_call()
                    print("cootel拨打电话成功")
                else:
                    talk.click_end_call()
                    result = "fail"
                    err_msg = "cootel拨打电话失败，出现一直拨号的现象"
                    img_name = self.path + "call\\" + err_msg + ".jpg"
                    self.d.screenshot(img_name)
                    actual_result = actual_result + "\n" + err_msg
                    print(err_msg)
            else:
                result = "fail"
                err_msg = "cootel拨打电话失败，出现直接挂断的现象"
                img_name = self.path + "call\\" + err_msg + ".jpg"
                self.d.screenshot(img_name)
                actual_result = actual_result + "\n" + err_msg
                print(err_msg)
        else:
            err_msg = "无cootel拨号方式"
            if talk.check_call_show:
                talk.click_end_call()
            img_name = self.path + "call\\" + err_msg + ".jpg"
            self.d.screenshot(img_name)
            actual_result = actual_result + "\n" + err_msg
            print(err_msg)
        time.sleep(2)
        talk.calls_del_edit()
        # 使用VOIP拨打8888
        talk.input_phone_number("8888g")
        if talk.click_voip():
            time.sleep(6)
            if talk.check_call_show():
                talk.click_audio()
                time.sleep(2)
                if talk.get_call_state() != "正在拨号":
                    talk.click_end_call()
                    print("VOIP拨打电话成功")
                else:
                    talk.click_end_call()
                    result = "fail"
                    err_msg = "VOIP拨打电话失败，出现一直拨号的现象"
                    img_name = self.path + "call\\" + err_msg + ".jpg"
                    self.d.screenshot(img_name)
                    actual_result = actual_result + "\n" + err_msg
                    print(err_msg)

            else:
                result = "fail"
                err_msg = "VOIP拨打电话失败，出现直接挂断的现象"
                img_name = self.path + "call\\" + err_msg + ".jpg"
                self.d.screenshot(img_name)
                actual_result = actual_result + "\n" + err_msg
                print(err_msg)
        else:
            err_msg = "无VOIP拨号方式"
            if talk.check_call_show:
                talk.click_end_call()
            img_name = self.path + "call\\" + err_msg + ".jpg"
            self.d.screenshot(img_name)
            actual_result = actual_result + "\n" + err_msg
            print(err_msg)
        return actual_result, result

    def data_connection(self):
        actual_result = ""
        result = "pass"
        chrome = Chrome(self.d)
        self.settings.close_wifi()
        for i in range(2):
            if self.settings.check_mcwill_data_switch():
                if self.settings.check_mcwill_data_status():
                    self.d.press("home")
                    chrome.start()
                    if chrome.check_open_baidu() == False:
                        err_msg = "McWill数据已连接时打开百度失败"
                        print(err_msg)
                        actual_result = actual_result + "\n" + err_msg
                        result = "fail"
                        err_screenshot = self.path + "data_connection\\" + err_msg + ".png"
                        self.d.screenshot(err_screenshot)
                    else:
                        print("McWill数据已连接时打开百度成功")
                    break
                else:
                    err_msg = "McWill数据状态为未连接"
                    print(err_msg)
                    actual_result = actual_result + "\n" + err_msg
                    result = "fail"
                    err_screenshot = self.path + "data_connection\\" + err_msg + ".png"
                    self.d.screenshot(err_screenshot)
                    break
            else:
                result = "fail"
                err_msg = "默认McWill数据为关闭状态"
                actual_result = actual_result + "\n" + err_msg
                err_screenshot = self.path + "data_connection\\" + err_msg + ".png"
                self.d.screenshot(err_screenshot)
                print(err_msg)
                self.settings.cut_mcwill_data_switch()
        self.d.press("home")

        # 关闭McWill，使用默认网络类型访问网络
        self.settings.cut_mcwill_data_switch("off")
        network_type = self.settings.cut_simcard_network_type("get")
        if "4G/3G/2G" in network_type:
            pass
        else:
            result = "fail"
            err_msg = "默认首选网络类型错误"
            actual_result = actual_result + "\n" + err_msg
            err_screenshot = self.path + "data_connection\\" + err_msg + ".png"
            self.d.screenshot(err_screenshot)
            print(err_msg)
            self.settings.cut_simcard_network_type("4G/3G/2G")
        self.d.press("home")
        chrome.start()
        if chrome.check_open_baidu() == False:
            err_msg = "默认网络模式时打开百度失败"
            print(err_msg)
            actual_result = actual_result + "\n" + err_msg
            result = "fail"
            err_screenshot = self.path + "data_connection\\" + err_msg + ".png"
            self.d.screenshot(err_screenshot)
        else:
            print(network_type + "网络模式时打开百度成功")

        # 切换网络类型访问网络
        network_type = ["4G", "3G/2G", "2G"]
        for i in network_type:
            self.settings.cut_simcard_network_type(i)
            self.d.press("home")
            chrome.start()
            if i == "2G":
                adb_msg = adb.read_adb("adb shell ping -c 100 www.baidu.com")
                print(adb_msg)
                if "0%" in adb_msg or "1%" in adb_msg or "2%" in adb_msg or "3%" in adb_msg or "4%" in adb_msg or "5%" in adb_msg:
                    print("pass")
                elif "unknown host" in adb_msg:
                    result = "fail"
                    err_msg = "网络模式2G时连接异常"
                    print(err_msg)
                    actual_result = actual_result + "\n" + err_msg
                else:
                    result = "fail"
                    err_msg = "网络模式2G时存在丢包的现象"
                    print(err_msg)
                    actual_result = actual_result + "\n" + err_msg
            else:
                if chrome.check_open_baidu() == False:
                    if i == "3G/2G":
                        i = "3G2G"
                    err_msg = i + "网络模式时打开百度失败"
                    print(err_msg)
                    actual_result = actual_result + "\n" + err_msg
                    result = "fail"
                    err_screenshot = self.path + "data_connection\\" + err_msg + ".png"
                    self.d.screenshot(err_screenshot)
                else:
                    print(i + "网络模式时打开百度成功")

        # 测试完毕，将设置恢复到初始
        self.settings.cut_mcwill_data_switch()
        self.settings.cut_simcard_network_type("4G/3G/2G")
        self.d.press("home")
        return actual_result, result

    def Case_detection_operator(self):
        '''
        将连接的设备重启，插卡，然后检测运营商显示是否正确
        :return:
        '''
        result = 'pass'
        result_message = ''
        print('1分钟时间请先插卡。。。。')
        time.sleep(10)
        operator = input('请手动输入插卡的运营商名称：')
        M = input('请手动输入M网名称：')
        adb.reboot_device()
        # 判断设备是否连接
        while True:
            if adb.detection_terminal_connect() == True:
                print('成功连接上设备')
                time.sleep(30)
                self.d = u2.connect()
                self.d.screen_on()
                if self.d(resourceId="com.android.systemui:id/emergency_call_button").wait() == True:
                    break
            else:
                time.sleep(30)
        self.d.screen_on()
        # 判断运营商显示是否正确
        if operator and M in self.d(resourceId="com.android.systemui:id/keyguard_carrier_text").get_text():
            print('运营商显示正确')
        else:
            print('运营商显示错误')
            result = 'fail'
            result_message = '手机显示的运营商与输入的运营不相符'
        return result, result_message

    def teardown(self,text):
        print(text)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return end_time

    def run(self):
        self.enter_sim_test_report = []
        start_time1 = self.set_up(test_time='开始测试：一次短信，一次彩信')
        actul_reselt = ''
        path = ''
        try:
            result1, result_message1= self.Case_send_message()
        except BaseException as e:
            result1 = 'Fail'
            print("except:", e)
            actul_reselt = str(e)[7:]
            result_message1 = '发送、编辑、接收，一次短信，一次彩信出现异常'
            print(
                "=====>>>>>执行测试：发送、编辑、接收，一次短信，一次彩信出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'message_img\\' + "发送、编辑、接收，一次短信，一次彩信出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time1 = self.teardown('发送、编辑、接收，一次短信，一次彩信')
        self.enter_sim_test_report.append(
            {"t_module": "B13/B14:SMS/MMS", "t_case": "入口测试",
             "t_steps": "发送、编辑、接收一次短信，一次彩信",
             "t_expected_result": "1.能够正常编辑常用语句；\n2.能够新建/编辑/发送/接收，短信/彩信.",
             "t_actual_result": actul_reselt + '\n' + path + '\n' + result_message1 ,
             "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})
        time.sleep(5)



        starttime = self.set_up("插入SIM卡时拨打112")
        try:
            t_actual_result, t_reference_result = self.sim_call_112()
        except BaseException as e:
            print("except:", e)
            t_reference_result = "fail"
            t_actual_result = str(e)[7:]
            print(t_actual_result)
            err_msg = "插入SIM卡时拨打112时出现异常"
            print(err_msg)
            err_screenshot = self.path + "call\\" + err_msg + ".png"
            self.d.screenshot(err_screenshot)
            self.d.press("home")
        endtime = self.teardown("插入SIM卡时拨打112")
        self.enter_sim_test_report.append({"t_module": "紧急电话", "t_case": "入口测试-已插卡", "t_steps": "一次紧急通话",
                               "t_expected_result": "插卡，拨打紧急电话112，正常可打通",
                               "t_actual_result": t_actual_result, "t_start_time": starttime, "t_end_time": endtime,
                               "t_reference_result": t_reference_result, "t_result": ""})

        starttime1 = self.set_up("联系人增加、拨打、删除")
        try:
            t_actual_result1, t_reference_result1 = self.phone_book_add()
        except BaseException as e:
            print("except:", e)
            t_reference_result1 = "fail"
            t_actual_result1 = str(e)[7:]
            print(t_actual_result1)
            err_msg = "联系人增加拨打删除时出现异常"
            print(err_msg)
            err_screenshot = self.path + "call\\" + err_msg + ".png"
            self.d.screenshot(err_screenshot)
            self.d.press("home")
        endtime1 = self.teardown("联系人增加、拨打、删除")
        self.enter_sim_test_report.append({"t_module": "电话簿", "t_case": "入口测试-已插卡", "t_steps": "记录添加、删除、拨打电话",
                               "t_expected_result": "记录添加、删除及拨打电话等功能正常",
                               "t_actual_result": t_actual_result1, "t_start_time": starttime1, "t_end_time": endtime1,
                               "t_reference_result": t_reference_result1, "t_result": ""})

        starttime1 = self.set_up("一次数据连接浏览器")
        try:
            t_actual_result2, t_reference_result2 = self.data_connection()
        except BaseException as e:
            print("except:", e)
            t_reference_result2 = "fail"
            t_actual_result2 = str(e)[7:]
            print(t_actual_result2)
            err_msg = "一次数据连接浏览器出现异常"
            print(err_msg)
            err_screenshot = self.path + "data_connection\\" + err_msg + ".png"
            self.d.screenshot(err_screenshot)
            self.d.press("home")
        endtime1 = self.teardown("一次数据连接浏览器")
        self.enter_sim_test_report.append({"t_module": "数据连接", "t_case": "入口测试-已插卡", "t_steps": "一次数据连接浏览器",
                               "t_expected_result": "1.能够正常启动数据连接；\n2.能够正常使用内置浏览器访问网络.\n3.移动和联通2G、3G数据连接都可以连接上网，不支持的频段可不验证。",
                               "t_actual_result": t_actual_result2, "t_start_time": starttime1, "t_end_time": endtime1,
                               "t_reference_result": t_reference_result2, "t_result": ""})

        start_time2 = self.set_up(test_time='开始测试：正常开/关机功能')
        actul_reselt = ''
        path = ''
        try:
            result2, result_message2 = self.Case_detection_operator()
        except BaseException as e:
            result2 = 'Fail'
            print("except:", e)
            actul_reselt = str(e)[7:]
            result_message2 = '正常开/关机功能出现异常'
            print(
                "=====>>>>>执行测试：正常开/关机功能出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'swish_facility_img\\' + "正常开/关机功能出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time2 = self.teardown('正常开/关机功能')
        self.enter_sim_test_report.append(
            {"t_module": "B07开机检查", "t_case": "入口测试",
             "t_steps": "正常开/关机功能",
             "t_expected_result": "1.插入SIM卡和TF卡，能够正常开机，正常检测设备，正常关机；\n2.能够正确注册对应运营商网络.",
             "t_actual_result": actul_reselt + '\n' + path + '\n' + result_message2,
             "t_start_time": start_time2, "t_end_time": end_time2,
             "t_reference_result": result2, "t_result": ""})
        time.sleep(5)

        return self.enter_sim_test_report





