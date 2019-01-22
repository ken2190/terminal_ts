import os
import time
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
from src.chrome import Chrome
from src.general import image_comparison
from src.settings import Settings
from src.gmail import Gmail




class Case_Enter():

    def __init__(self,d):
        self.d=d
        self.nictalk = NicTalk(self.d)
        self.camtalk = CamTalk(self.d)
        self.qq=Tx_QQ(self.d)
        self.clock=Clock(self.d)
        self.camera=Camera(self.d)
        self.settings = Settings(self.d)
        self.message=Message1(self.d)
        self.path = os.path.abspath(os.path.join(os.getcwd(), "../..")) + "\\enter_resource\\"
        self.language = self.settings.change_language()
        self.settings.display_setting()

    def set_up(self,test_time='1'):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>停止所有运行的app')
        self.d.app_stop_all()

        self.d.press("home")
        print("开始测试：" + test_time)
        print(start_time)
        return start_time

    def KHM_apk_dict(self):
        '''
        定义的预期存在的apk包名和activity
        :return:
        '''
        apk_dict = {'YouTube':['com.google.android.youtube','com.google.android.apps.youtube.app.WatchWhileActivity'],
                    '录音机':['com.android.soundrecorder', '.SoundRecorder'],
                    'GOOgle Play':['com.android.vending',''],
                    '电话':['com.camtalk.start','com.uip.start.activity.MainActivity'],
                    '联系人':['com.camtalk.start','com.uip.start.activity.MainActivity'],
                    '下载':['com.android.documentsui','.DocumentsActivity'],
                    'Google':['com.android.chrome',''],
                    'cooBill':['com.mcwill.coopay','.ui._new.SplashActivity'],
                    'cooTv':['com.tvata.tvaxw.mobile',''],
                    '地图':['com.google.android.apps.maps','com.google.android.maps.MapsActivity'],
                    '记事本':['com.example.android.notepad','.NotesList'],
                    'Gmail':['com.google.android.gm',''],
                    'CamTalk':['com.camtalk.start','com.uip.start.activity.MainActivity'],
                    '酷管家':['com.cootf.kuoperation','.MainActivity'],
                    '计算器':['com.android.calculator2','.Calculator'],
                    '视频':['com.android.music','.VideoBrowserActivity'],
                    '音乐':['com.android.music','.MusicBrowserActivity'],
                    '图库':['com.android.gallery3d','.app.GalleryActivity'],
                    '短信':['com.android.mms','.ui.ConversationList'],
                    '相机':[ 'org.codeaurora.snapcam', 'com.android.camera.CameraLauncher'],
                    '日历':['com.android.calendar','.AllInOneActivity'],
                    '时钟':['com.android.deskclock','.DeskClock'],
                    '文件管理器':['com.cyanogenmod.filemanager','.activities.NavigationActivity'],
                    '设置':['com.android.settings','.Settings']
                    }
        return apk_dict

    def NCA_apk_dict(self):
        '''
        定义的预期存在的apk包名和activity
        :return:
        '''
        apk_dict = {'YouTube':['com.google.android.youtube','com.google.android.apps.youtube.app.WatchWhileActivity'],
                    '录音机':['com.android.soundrecorder', '.SoundRecorder'],
                    'GOOgle Play':['com.android.vending',''],
                    '电话':['com.nictalk.start','com.uip.start.activity.MainActivity'],
                    '联系人':['com.nictalk.start','com.uip.start.activity.MainActivity'],
                    '下载':['com.android.documentsui','.DocumentsActivity'],
                    'Google':['com.android.chrome',''],
                    'cooBill':['com.mcwill.coopay','.ui._new.SplashActivity'],
                    'cooTv':['com.xinwei.ni.cootv',''],
                    '地图':['com.google.android.apps.maps','com.google.android.maps.MapsActivity'],
                    '记事本':['com.example.android.notepad','.NotesList'],
                    'Gmail':['com.google.android.gm',''],
                    'NicTalk':['com.nictalk.start','com.uip.start.activity.MainActivity'],
                    '酷管家':['com.cootf.kuoperation','.MainActivity'],
                    '计算器':['com.android.calculator2','.Calculator'],
                    '视频':['com.android.music','.VideoBrowserActivity'],
                    '音乐':['com.android.music','.MusicBrowserActivity'],
                    '图库':['com.android.gallery3d','.app.GalleryActivity'],
                    '短信':['com.android.mms','.ui.ConversationList'],
                    '相机':[ 'org.codeaurora.snapcam', 'com.android.camera.CameraLauncher'],
                    '日历':['com.android.calendar','.AllInOneActivity'],
                    '时钟':['com.android.deskclock','.DeskClock'],
                    '文件管理器':['com.cyanogenmod.filemanager','.activities.NavigationActivity'],
                    '设置':['com.android.settings','.Settings'],
                    'Mi Cootel': ['com.xinwei.onlneHall', 'io.dcloud.PandoraEntryActivity']
                    }
        return apk_dict

    def Case_root_test(self):
        '''
        判断当前用户有没有root
        :return:
        '''
        result='pass'
        result_message=''
        if 'Permission denied' in self.d.adb_shell('cd root'):
            print('当前没有root权限')
        else:
            print('当前用户有root权限')
            result='fail'
            result_message='当前用户可以进入root目录，有root权限'
        return result,result_message

    def Case_about_phone_versions_message(self):
        '''
        版本对比，使用adb获取版本和手机界面显示的版本对比
        将关于手机里面的版本信息写入文件
        :return:返回对比之后的结果
        '''
        result='pass'
        result_message=''
        phone_versions=self.settings.acquire_about_phone_message()
        if phone_versions==False:
            print('当前手机没有显示版本信息')
            result_message=result_message+'当前手机没有显示版本信息'
            self.settings.stop()
            return result, result_message, phone_versions
        else:
            adb.acquire_versions()
            #读取adb获取到的手机的版本号
            with open(self.path+'log_message\\adb_instruct.txt','r')as f:
                read=f.readline()
            print('这是adb获取的版本号：'+read)
            print('这是关于手机页面显示的版本号'+phone_versions['版本号'])
            if phone_versions['版本号'] in read:
                print('>>>>>>>>>>版本号对比成功')
            else:
                print('>>>>>>>>>>版本号对比失败')
                result='fail'
                result_message='adb获取手机的版本号和手机关于手机界面显示的版本号不对应'
            print('>>>>>>>>>>将关于手机页面信息写入文件')
            self.settings.stop()
            return result,result_message,phone_versions

    def Case_enter_camera(self):
        '''
        相机的切换前后摄拍照和摄像
        :return:
        '''
        result = 'pass'
        result_message = ''
        print('相机切换前后摄拍照，请手动查看')
        facility = adb.read_adb("adb shell getprop ro.product.model")
        self.camera.CameraOff()
        self.camera.CameraOn()
        self.camera.Pop_Up()
        self.camera.PictureMode(facility)
        if self.camera.Menu_picture() == False:
            self.d.screenshot(self.path+"camera_img\\进入相机模式出现异常.jpg")
            result = 'fail'
            result_message=result_message+'没有进入相机模式'
        else:
            self.camera.Photograph()
            time.sleep(2)
            self.camera.switch_camera()
            time.sleep(2)
            self.camera.Photograph()
        self.camera.VideoMode()
        if self.camera.Menu_video() == False:
            self.d.screenshot(self.path + "camera_img\\进入视频模式出现异常.jpg")
            result = 'fail'
            result_message=result_message+'没有进入视频模式'
        else:
            self.camera.Photograph()
            time.sleep(10)
            self.camera.Photograph()
            self.camera.switch_camera()
            time.sleep(3)
            self.camera.Photograph()
            time.sleep(10)
            self.camera.Photograph()
        self.camera.CameraOff()
        if self.camera.Menu() != False:
            self.d.screenshot(self.path + "camera_img\\退出相机模式出现异常.jpg")
            result = 'fail'
            result_message=result_message+'没有退出相机模式'
        self.camera.CameraOff()
        return result, result_message

    def Case_start_built_in_apk(self):
        '''
        开启所有内置app
        :return:
        '''
        num=0
        result='pass'
        result_message=''
        built_in_apk_list=[]
        #获取内置的apk信息
        apk=self.d.adb_shell('pm list packages -s ')
        #将内置apk信息写入文件
        with open(self.path+'log_message\\adb_instruct.txt','w')as f:
            f.write(apk)
        # 将内置apk信息读出处理换行符处理:'package:'
        #将处理后的信息加入list
        with open(self.path+'log_message\\adb_instruct.txt','r')as f:
            for j in f.readlines():
                i=j.strip('\n')
                built_in_apk_list.append(i.replace("package:", ''))
        #获取预期的apk信息
        apk_dict = self.KHM_apk_dict()
        #获取当前连接手机的版本信息
        versions = adb.read_adb('adb shell getprop ro.build.display.id')
        if 'KHM' in versions:
            apk_dict = self.KHM_apk_dict()
        elif 'NCA'in versions:
            apk_dict = self.NCA_apk_dict()
        #循环遍历出
        for apk_name in apk_dict:
            print('%s---------->正在执行'%num+apk_name)
            if apk_dict[apk_name][0] in built_in_apk_list:
                print('---------->这是一个内置apk')
                print('---------->开启'+apk_name)
                self.d.app_start(pkg_name=apk_dict[apk_name][0],activity=apk_dict[apk_name][1])
                time.sleep(3)
                print('---------->开始截图')
                self.d.screenshot(self.path+'built_in_apk_img\\开启'+apk_name+'的截图.jpg')
                time.sleep(3)
                print('---------->停止apk')
                if apk_name=='酷管家':
                    self.d.press("home")
                    continue
                elif apk_name=='cooTv':
                    self.d.press("back")
                    if self.d(resourceId="android:id/message").wait(timeout=3):
                        self.d(resourceId="android:id/button1").click()
                self.d.app_stop(pkg_name=apk_dict[apk_name][0])
                now_start_apk=self.d.current_app()
                if now_start_apk['package']==apk_dict[apk_name][0]:
                    print('---------->没有退出apk')
                    self.d.screenshot(self.path + 'built_in_apk_img\\没有退出'+apk_name+'apk.jpg')
                    result='fail'
                    result_message= result_message+'退出'+apk_name+'失败'
                    self.d.press("home")
                time.sleep(3)
                print('---------->开始截图')
                self.d.screenshot(self.path + 'built_in_apk_img\\关闭' + apk_name + '的截图.jpg')
                time.sleep(3)
            else:
                print('---------->这不是一个内置apk')
                result='fail'
                result_message= result_message+'这不是一个内置apk\n开启apk的截图目录为：'+self.path+'built_in_apk_img'
            num+=1
        return result,result_message

    def Case_install_apk(self):
        '''
        安装一个apk并运行
        在运行时截图
        :return:
        '''
        result='pass'
        result_message=''
        install_apk='adb install '+self.path+'package\\qq.apk >'+self.path+'log_message\\install-APK.log'
        print(install_apk)
        os.system(install_apk)
        print('----------->启动apk')
        self.qq.start()
        self.qq.wait_update_qq()
        window = self.d.current_app()
        if 'com.tencent.mobileqq'==window['package']:
            time.sleep(5)
            self.d.screenshot(self.path + 'install_apk_img\\打开qq.apk' + '的截图.jpg')
            print('成功运行安装的apk')
        else:
            result='fail'
            result_message=result_message+'apk没有正常打开'
            print('---------->apk无法打开')
        print('---------->关闭apk')
        self.d.app_stop(pkg_name='com.tencent.mobileqq')
        time.sleep(2)
        self.d.screenshot(self.path + 'install_apk_img\\关闭qq.apk' + '的截图.jpg')

        return result,result_message

    def Case_new_clock(self):
        '''
        新建闹钟
        :return:
        '''
        result='pass'
        result_message=''
        self.settings.open_24date_format()
        self.clock.stop_clock()
        self.clock.start_clock()
        self.clock.clock_menu('闹钟')
        self.clock.add_alarm()
        hour=self.clock.acquire_now_hour()
        minute=self.clock.acquire_now_minute()
        clock_time=self.clock.select_time(hour,minute)
        self.clock.click_confirm()
        print(clock_time)
        self.d.open_notification()
        suspend=self.clock.wait_suspend()
        cancle=self.clock.wait_cancel()
        print(suspend)
        print(cancle)
        if suspend and cancle==True:
            time.sleep(3)
            self.clock.click_cancel()
            phone_time=self.clock.acquare_phone_time()
            self.d(scrollable=True).fling()
            print(phone_time)
            if str(phone_time)==str(clock_time):
                print('闹钟功能正常')
            else:
                result='fail'
                result_message = result_message +'闹钟功能异常，没有在定义的时间响应'
        delete=self.clock.delete_clock()
        if delete==False:
            self.d.screenshot(self.path+"clock_img\\没有找到删除闹钟按钮.jpg")
            result = 'fail'
            result_message = result_message+ '没有找到删除闹钟按钮'
        self.clock.stop_clock()
        self.settings.stop()
        return result,result_message

    def Case_built_in_apk_versions(self):
        '''
        验证内置apk的版本是否正确
        :return:
        '''
        app_list=[]
        result='pass'
        apk_versions={}
        result_message=''
        versions=adb.read_adb('adb shell getprop ro.build.display.id')
        if 'KHM' in versions:
            app_list = ['CooBill', 'CooTV', 'CamTalk', '酷管家']
        elif 'NCA'in versions:
            app_list = ['CooBill', 'CooTV', 'Mi CooTel', 'NicTalk', '酷管家']
        self.settings.stop()
        self.settings.start()
        while True:
            if self.settings.list_apps() == True:
                self.settings.click_operation_app()
                while True:
                    for i in app_list:
                        page_app_name = self.settings.acquire_page_app_name()
                        if i in page_app_name:
                            self.settings.click_app_name(i)
                            time.sleep(2)
                            versions = self.settings.acquire_app_versions()
                            print(i + '的版本信息为：' + versions)
                            apk_versions[i]=versions
                    slide_page=self.settings.slide_page()
                    if slide_page==True:
                        break
                if slide_page == True:
                    break
            else:
                self.d.swipe(0.275, 0.845, 0.377, 0.045)
        for dict_apk_name in apk_versions:
            if dict_apk_name in app_list:
                app_list.remove(dict_apk_name)
        if app_list!=[]:
            print('没有找到这个apk的版本信息',app_list)
            self.d.screenshot(self.path+"apk_versions_img\\没有找到这个apk的版本信息.jpg")
            result='fail'
            result_message='没有找到这个apk的版本信息',app_list
        self.settings.stop()
        return result,result_message,apk_versions

    def teardown(self,text):
        print(text)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return end_time

    def enter_settings(self):
        '''
        一次默认时间格式和日期、语言的检测
        :return:
        '''
        actual_result = ""
        result = "pass"
        print("开始测试：一次默认时区检测")
        self.settings.stop()
        self.settings.start()
        timezone = self.settings.get_timezone()
        result_timezone = ""
        if self.language == "柬埔寨":
            result_timezone = "GMT+07:00 印度支那时间"
        elif self.language == "尼加拉瓜":
            result_timezone = "GMT-06:00 北美中部标准时间"
        elif self.language == "中国":
            result_timezone = "GMT+08:00 中国标准时间"
        if timezone != result_timezone:
            err_name = "默认时区检测默认语言" + str(self.language) + "与时区不一致"
            print(err_name)
            img_name = self.path + "settings\\" + err_name + ".jpg"
            self.d.screenshot(img_name)
            result = "fail"
            actual_result = err_name
        # 开始进行日期格式对比
        date = self.settings.get_date()
        try:
            time.strptime(date, "%Y年%m月%d日")
        except ValueError:
            err_name = "默认日期格式非《年月日》格式"
            print(err_name)
            img_name = self.path + "settings\\" + err_name + ".jpg"
            self.d.screenshot(img_name)
            result = "fail"
            actual_result = actual_result + "\n" + err_name
        # 开始进行默认24时间格式的检测
        if self.settings.get_date_format():
            err_name = "默认24时间格式的检测为开启状态"
            print(err_name)
            img_name = self.path + "settings\\" + err_name + ".jpg"
            self.d.screenshot(img_name)
            result = "fail"
            actual_result = actual_result + "\n" + err_name
        return actual_result, result

    def enter_chrome(self):
        '''
        一次浏览器主页检查 （google）
        共检测两次，首次检测通过，截图名为：《一次浏览器主页检查.png》，新增窗口检测通过，截图名为：《一次浏览器主页检查,新增一个新的窗口.png》；
        若检测失败，则截图名为：《一次浏览器主页检查,出现异常.jpg》
        :return:result为pass 即为通过
        '''
        actual_result = ""
        result = "pass"
        chrome = Chrome(self.d)
        chrome.start()
        for i in range(2):
            if chrome.check_home():
                if i == 0:
                    name = "一次浏览器主页检查"
                else:
                    name = "一次浏览器主页检查,新增一个新的窗口"
                img_name = self.path + "chrome\\" + name + ".jpg"
                self.d.screenshot(img_name)
                chrome_img = self.path + "picture\\chrome.jpg"
                if image_comparison.compare_image_with_histogram(chrome_img, img_name):
                    pass
                else:
                    err_msg = name + ":可正常检测到元素，但页面显示与期望不完全一致"
                    print(err_msg)
                    actual_result = actual_result + "\n" + err_msg
                    result = "fail"
                break
            else:
                result = "fail"
                err_msg = "一次浏览器主页检查,出现异常"
                img_name = self.path + "chrome\\" + err_msg + ".jpg"
                self.d.screenshot(img_name)
                actual_result = actual_result + "\n" + err_msg
                print(">>>>>>>>>>>> 新增一个新的窗口，检测是否正常")
                chrome.window_add()
        chrome.stop()
        return actual_result, result

    def enter_gmail(self):
        '''
        一次发送和接收G-mail
        :return:
        '''
        result = "pass"
        actual_result = ""
        gmail = Gmail(self.d)
        # self.settings.auto_connect_wifi()
        gmail.stop()
        gmail.start()
        if gmail.detection_got_it():
            err_msg = "入口测试，首次进入gmail时显示已登录账号"
            img_name = self.path + "gmail\\" + err_msg + ".jpg"
            self.d.screenshot(img_name)
            actual_result = err_msg
            print(err_msg)
        else:
            if gmail.add_oth_addresses():
                start_unread_number = gmail.get_unread()
                self.d.screen_on()
                if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                    self.d.unlock()
                    gmail.start()
                gmail.write_gmail()
                gmail.gmail_click_pop()
                gmail.gmail_add_addressee()
                gmail.gmail_add_subject("入口测试，主题内容填写")
                gmail.gmail_click_pop()
                gmail.gmail_send()
                for i in range(5):
                    if gmail.check_outbox():
                        end_unread_number = gmail.get_unread()
                        if end_unread_number == "99+":
                            pass
                        elif int(end_unread_number) - int(start_unread_number) == 1:
                            break
                    else:
                        if i == 4:
                            result = "fail"
                            err_msg = "邮件发送或接受异常"
                            img_name = self.path + "gmail\\" + err_msg + ".jpg"
                            self.d.screenshot(img_name)
                            actual_result = err_msg
                            print(err_msg)
                            break
                        time.sleep(60)
            else:
                result = "fail"
                err_msg = "连接到服务异常，请手动尝试"
                img_name = self.path + "gmail\\" + err_msg + ".jpg"
                self.d.screenshot(img_name)
                actual_result = err_msg
                print(err_msg)
                gmail.stop()
        return actual_result, result

    def call_112(self):
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
        time.sleep(5)
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
                err_msg = "拨号界面显示非紧急电话号码"
                img_name = self.path + "call\\" + err_msg + ".jpg"
                self.d.screenshot(img_name)
                actual_result = err_msg
                print(err_msg)
            talk.click_end_call()
        else:
            result = "fail"
            err_msg = "紧急呼叫拨号失败"
            img_name = self.path + "call\\" + err_msg + ".jpg"
            self.d.screenshot(img_name)
            actual_result = err_msg
        return actual_result, result

    def enter_Wlan(self):
        '''
        连接WLAN并使用WLAN启动chrome浏览器上网
        :return:
        '''
        result = "pass"
        actual_result = ""
        self.settings.start()
        self.settings.list_wlan()
        if self.settings.get_wlan_switch() == "开启":
            err_msg = "首次启动设置WLAN应为关闭状态！！"
            print(err_msg)
            actual_result = actual_result + "\n" + err_msg
            result = "fail"
            self.settings.wlan_switch()
        if self.settings.get_wlan_switch() == "关闭":
            off_original = self.path + "settings\\WLAN关闭时.png"
            self.d.screenshot(off_original)
            self.settings.wlan_switch()
        if self.settings.get_wlan_switch() == "开启":
            on_original = self.path + "settings\\WLAN开启时.png"
            self.d.screenshot(on_original)
            time.sleep(3)
            if self.d(resourceId="android:id/title")[0].get_text() != '':
                print(">>>WIFI已开启时， 可正常搜索到WIFI")
            else:
                err_msg = "WIFI已开启时，等待3秒未搜索到可用WIFI"
                print(err_msg)
                err_screenshot = self.path + "settings\\" + err_msg + ".png"
                self.d.screenshot(err_screenshot)
                actual_result = actual_result + "\n" + err_msg
                result = "fail"
            self.settings.wlan_switch()

        for i in range(3):
            if self.settings.get_wlan_switch() == "关闭":
                comparison = self.path + "settings\\WLAN关闭时" + str(i) + ".png"
                self.d.screenshot(comparison)
                if not (image_comparison.compare_image_with_histogram(off_original, comparison)):
                    err_msg = "WIFI关闭时" + str(i) + "对比失败"
                    print(err_msg)
                    actual_result = actual_result + "\n" + err_msg
                    result = "fail"
                self.settings.wlan_switch()
            time.sleep(2)
            if self.settings.get_wlan_switch() == "开启":
                comparison = self.path + "settings\\WLAN开启时" + str(i) + ".png"
                self.d.screenshot(comparison)
                if self.d(resourceId="android:id/title")[0].get_text() != '':
                    print(">>>WIFI已开启时， 可正常搜索到WIFI")
                    print(self.d(resourceId="android:id/title")[0].get_text())
                else:
                    err_msg = "WIFI已开启" + str(i) + "时，等待3秒未搜索到可用WIFI"
                    print(err_msg)
                    actual_result = actual_result + "\n" + err_msg
                    result = "fail"
                self.settings.wlan_switch()
        self.settings.auto_connect_wifi()
        self.d.press("home")
        chrome = Chrome(self.d)
        chrome.start()
        if chrome.check_open_baidu() == False:
            err_msg = "打开百度失败"
            print(err_msg)
            actual_result = actual_result + "\n" + err_msg
            result = "fail"
            err_screenshot = self.path + "settings\\" + err_msg + ".png"
            self.d.screenshot(err_screenshot)
        return actual_result, result



    def run(self):
        self.enter_test_report = []

        start_time1=self.set_up(test_time='验证软件版本号，和其他版本号')
        actul_reselt1=''
        path=''
        phone_versions=''
        try:
            result1,result_message,dict_phone_versions=self.Case_about_phone_versions_message()
            if dict_phone_versions!=False:
                for i, j in dict_phone_versions.items():  # 将字典的键和值遍历
                    phone_versions=phone_versions+i+':'+j+'\n'
        except BaseException as e:
            result1='Fail'
            print("except:", e)
            actul_reselt1=str(e)[7:]
            result_message='获取手机的版本信息出现异常'
            print("=====>>>>>执行测试：验证About Phone中，手机型号、Android版本、基带版本、内核版本、版本号，命名正确，且不含有个人和公司信息.有客户需求的要与需求一致；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path + 'error_versions_message_img\\' + "获取手机的版本信息出现异常.jpg"
            self.d.screenshot(path)
            self.settings.stop()
            self.d.app_stop_all()
        end_time1=self.teardown('获取手机的版本信息')
        self.enter_test_report.append(
            {"t_module": "B01,B02:软件版本号", "t_case": "入口测试", "t_steps": "验证About Phone中，手机型号、Android版本、基带版本、内核版本、版本号，命名正确，且不含有个人和公司信息.有客户需求的要与需求一致",
             "t_expected_result": "1.adb获取手机的版本号和手机关于手机界面显示的版本号相对应  \n 2.请手工验证关于手机页面其他的版本信息",
             "t_actual_result": actul_reselt1+'\n'+path+'\n'+result_message+phone_versions, "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})
        time.sleep(5)

        start_time2=self.set_up(test_time='验证内置apk的版本是否正确')
        actul_reselt2=''
        path=''
        apk_name=''
        try:
            result2,result_message2,dict_apk_name=self.Case_built_in_apk_versions()
            for i,j in dict_apk_name.items():
                apk_name=apk_name+i+':'+j+'\n'
        except BaseException as e:
            result2='Fail'
            print("except:", e)
            actul_reselt2=str(e)[7:]
            result_message2='获取内置apk版本信息出现异常'
            print("=====>>>>>执行测试：内置应用验证版本信息；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path + 'apk_versions_img\\' + "获取内置apk版本信息出现异常.jpg"
            self.d.screenshot(path)
            self.settings.stop()
            self.d.app_stop_all()
        end_time2=self.teardown('获取内置apk版本信息')
        self.enter_test_report.append(
            {"t_module": "B37：软件配置", "t_case": "入口测试", "t_steps": "内置应用验证版本信息",
             "t_expected_result": "1.内置apk版本信息，在详情中需要显示正确\n2.需要人工验证版本信息",
             "t_actual_result": actul_reselt2+'\n'+path+'\n'+result_message2+'\n'+apk_name, "t_start_time": start_time2, "t_end_time": end_time2,
             "t_reference_result": result2, "t_result": ""})
        time.sleep(5)

        start_time3 = self.set_up(test_time='查看user版本是否确认不可root')
        actul_reselt3 = ''
        try:
            result3, result_message3 = self.Case_root_test()
        except BaseException as e:
            result3 = 'Fail'
            print("except:", e)
            actul_reselt3 = str(e)[7:]
            result_message3 = '查看user版本是否确认不可root'
            print(
                "=====>>>>>执行测试：查看user版本是否确认不可root；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            self.d.app_stop_all()
        end_time3 = self.teardown('查看user版本是否确认不可root')
        self.enter_test_report.append(
            {"t_module": "B04:软件版本检查", "t_case": "入口测试",
             "t_steps": "查看user版本是否确认不可root",
             "t_expected_result": "1.执行adb root指令 ，确认user版本不可root；",
             "t_actual_result": actul_reselt3 + '\n' + result_message3,
             "t_start_time": start_time3, "t_end_time": end_time3,
             "t_reference_result": result3, "t_result": ""})
        time.sleep(5)



        start_time4 = self.set_up(test_time='内置应用启动/关闭')
        actul_reselt4 = ''
        path = ''
        try:
            result4, result_message4= self.Case_start_built_in_apk()
        except BaseException as e:
            result4 = 'Fail'
            print("except:", e)
            actul_reselt4 = str(e)[7:]
            result_message4 = '内置应用启动/关闭'
            print(
                "=====>>>>>执行测试：内置应用启动/关闭；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'built_in_apk_img\\' + "内置应用启动关闭出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time4 = self.teardown('内置应用启动关闭')
        self.enter_test_report.append(
            {"t_module": "B16:内置应用", "t_case": "入口测试",
             "t_steps": "内置应用启动/关闭",
             "t_expected_result": "1.能够正常启动/退出主菜单界面的所有内置应用.",
             "t_actual_result": actul_reselt4 + '\n' + path + '\n' + result_message4 ,
             "t_start_time": start_time4, "t_end_time": end_time4,
             "t_reference_result": result4, "t_result": ""})
        time.sleep(5)



        start_time5 = self.set_up(test_time='一次前后摄拍照和摄像')
        actul_reselt5 = ''
        path = ''
        try:
            result5, result_message5= self.Case_enter_camera()
        except BaseException as e:
            result5 = 'Fail'
            print("except:", e)
            actul_reselt5 = str(e)[7:]
            result_message5 = '一次前后摄拍照和摄像'
            print(
                "=====>>>>>执行测试：一次前后摄拍照和摄像；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'camera_img\\' + "一次前后摄拍照和摄像出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time5 = self.teardown('一次前后摄拍照和摄像')
        self.enter_test_report.append(
            {"t_module": "B21:拍照和录像", "t_case": "入口测试",
             "t_steps": "一次前后摄拍照和摄像",
             "t_expected_result": "1.可以正常打开退出相机；\n2.拍照和摄像成功，拍摄后浏览文件正常；\n3.前后摄切换无异常。",
             "t_actual_result": actul_reselt5 + '\n' + path + '\n' + result_message5 ,
             "t_start_time": start_time5, "t_end_time": end_time5,
             "t_reference_result": result5, "t_result": ""})
        time.sleep(5)


        start_time6 = self.set_up(test_time='一次安装应用成功')
        actul_reselt6 = ''
        path = ''
        try:
            result6, result_message6= self.Case_install_apk()
        except BaseException as e:
            result6 = 'Fail'
            print("except:", e)
            actul_reselt6 = str(e)[7:]
            result_message6 = '一次安装应用成功'
            print(
                "=====>>>>>执行测试：一次安装应用成功；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'install_apk_img\\' + "一次安装应用成功.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time6 = self.teardown('一次安装应用成功')
        self.enter_test_report.append(
            {"t_module": "B31:应用", "t_case": "入口测试",
             "t_steps": "一次安装应用成功",
             "t_expected_result": "1.安装任1个APK应用成功并可以运行；",
             "t_actual_result": actul_reselt6 + '\n' + path + '\n' + result_message6 ,
             "t_start_time": start_time6, "t_end_time": end_time6,
             "t_reference_result": result6, "t_result": ""})
        time.sleep(5)



        start_time7 = self.set_up(test_time='一次新建闹钟及删除闹钟')
        actul_reselt7 = ''
        path = ''
        try:
            result7, result_message7= self.Case_new_clock()
        except BaseException as e:
            result7 = 'Fail'
            print("except:", e)
            actul_reselt7 = str(e)[7:]
            result_message7 = '一次新建闹钟及删除闹钟'
            print(
                "=====>>>>>执行测试：一次新建闹钟及删除闹钟；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path = self.path + 'clock_img\\' + "一次新建闹钟及删除闹钟出现异常.jpg"
            self.d.screenshot(path)
            self.d.app_stop_all()
        end_time7 = self.teardown('一次新建闹钟及删除闹钟')
        self.enter_test_report.append(
            {"t_module": "B33:工具箱", "t_case": "入口测试",
             "t_steps": "一次新建闹钟及删除闹钟",
             "t_expected_result": "1.可以新建闹钟，正常响闹及删除闹钟。",
             "t_actual_result": actul_reselt7 + '\n' + path + '\n' + result_message7 ,
             "t_start_time": start_time7, "t_end_time": end_time7,
             "t_reference_result": result7, "t_result": ""})
        time.sleep(5)

        starttime8 = self.set_up("默认时间格式和日期、语言的检测")
        try:
            t_actual_result8, t_reference_result8 = self.enter_settings()
        except BaseException as e:
            print("except:", e)
            t_reference_result8 = "fail"
            t_actual_result8 = str(e)[7:]
            print(t_actual_result8)
            err_msg = "默认时间格式和日期语言的检测出现异常"
            print(err_msg)
            err_screenshot = self.path + "settings\\" + err_msg + ".png"
            self.d.screenshot(err_screenshot)
            self.d.press("home")
        endtime8 = self.teardown("默认时间格式和日期、语言的检测")
        self.enter_test_report.append({"t_module": "设置", "t_case": "入口测试", "t_steps": "一次默认时间格式和日期、语言的检测",
                               "t_expected_result": "检测默认语言与时区是否匹配\n默认日期格式为年月日格式\n默认时间为12小时格式",
                               "t_actual_result": t_actual_result8, "t_start_time": starttime8, "t_end_time": endtime8,
                               "t_reference_result": t_reference_result8, "t_result": ""})

        starttime9 = self.set_up("浏览器主页检查")
        try:
            t_actual_result9, t_reference_result9 = self.enter_chrome()
        except BaseException as e:
            print("except:", e)
            t_reference_result9 = "fail"
            t_actual_result9 = str(e)[7:]
            print(t_actual_result9)
            err_msg = "浏览器主页检查出现异常"
            print(err_msg)
            err_screenshot = self.path + "chrome\\" + err_msg + ".png"
            self.d.screenshot(err_screenshot)
            self.d.press("home")
        endtime9 = self.teardown("浏览器主页检查")
        self.enter_test_report.append(
            {"t_module": "chrome", "t_case": "入口测试", "t_steps": "一次浏览器主页检查", "t_expected_result": "检测默认主页是否为google",
             "t_actual_result": t_actual_result9, "t_start_time": starttime9, "t_end_time": endtime9,
             "t_reference_result": t_reference_result9, "t_result": ""})

        starttime10 = self.set_up("连接WLAN并使用WLAN上网")
        try:
            t_actual_result10, t_reference_result10 = self.enter_Wlan()
        except BaseException as e:
            print("except:", e)
            t_reference_result10 = "fail"
            t_actual_result10 = str(e)[7:]
            print(t_actual_result10)
            err_msg = "连接WLAN并使用WLAN上网出现异常"
            print(err_msg)
            err_screenshot = self.path + "settings\\" + err_msg + ".png"
            self.d.screenshot(err_screenshot)
            self.d.press("home")
        endtime10 = self.teardown("连接WLAN并使用WLAN上网")
        self.enter_test_report.append({"t_module": "WLAN", "t_case": "入口测试", "t_steps": "一次连接WLAN并使用WLAN上网",
                               "t_expected_result": "WLAN开关正常，成功连接WLAN热点并使用WLAN上网",
                               "t_actual_result": t_actual_result10, "t_start_time": starttime10, "t_end_time": endtime10,
                               "t_reference_result": t_reference_result10, "t_result": ""})

        starttime11 = self.set_up("一次发送和接收G-mail")
        try:
            t_actual_result11, t_reference_result11 = self.enter_gmail()
        except BaseException as e:
            print("except:", e)
            t_reference_result11 = "fail"
            t_actual_result11 = str(e)[7:]
            print(t_actual_result11)
            err_msg = "一次发送和接收G-mail出现异常"
            print(err_msg)
            err_screenshot = self.path + "gmail\\" + err_msg + ".png"
            self.d.screenshot(err_screenshot)
            self.d.press("home")
        endtime11 = self.teardown("一次发送和接收G-mail")
        self.enter_test_report.append(
            {"t_module": "gmail", "t_case": "入口测试", "t_steps": "一次发送和接收G-mail成功 ", "t_expected_result": "邮件发送和接收",
             "t_actual_result": t_actual_result11, "t_start_time": starttime11, "t_end_time": endtime11,
             "t_reference_result": t_reference_result11, "t_result": ""})

        starttime12 = self.set_up("未插卡时一次紧急通话")
        try:
            t_actual_result12, t_reference_result12 = self.call_112()
        except BaseException as e:
            print("except:", e)
            t_reference_result12 = "fail"
            t_actual_result12 = str(e)[7:]
            print(t_actual_result12)
            err_msg = "未插卡时一次紧急通话出现异常"
            print(err_msg)
            err_screenshot = self.path + "call\\" + err_msg + ".png"
            self.d.screenshot(err_screenshot)
            self.d.press("home")
        endtime12 = self.teardown("未插卡时一次紧急通话")
        self.enter_test_report.append(
            {"t_module": "紧急电话", "t_case": "入口测试", "t_steps": "一次紧急通话", "t_expected_result": "不插卡，拨打紧急电话112，正常可打通；",
             "t_actual_result": t_actual_result12, "t_start_time": starttime12, "t_end_time": endtime12,
             "t_reference_result": t_reference_result12, "t_result": ""})

        return self.enter_test_report





