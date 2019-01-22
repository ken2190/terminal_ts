import time
from src.general import image_comparison
import uiautomator2 as u2
from src.general import adb
from src.general import get_config as config


class Settings():
    def __init__(self, d):
        self.d = d
        self.path = image_comparison.get_path()
        self.name = config.get_config("WIFI", "name")
        self.password = config.get_config("WIFI", "password")


    def __sleep(func):
        def inner(self):
            time.sleep(1)
            self.d.screen_on()
            return func(self)
        return inner


    @__sleep
    def start(self):
        print(">>>>>>>>>>>>>>>>> 启动apk: 设置")
        self.d.app_start("com.android.settings")


    @__sleep
    def stop(self):
        print(">>>>>>>>>>>>>>>>> 停止apk: 设置")
        self.d.app_stop("com.android.settings")

    '''
    以下为 设置 列表界面
    '''
    @__sleep
    def list_mcwill(self):
        print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击McWiLL数据")
        self.d(resourceId="com.android.settings:id/title", text=u"McWiLL数据").click()


    @__sleep
    def list_wlan(self):
        if self.d(resourceId="com.android.settings:id/title", text=u"WLAN").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击WLAN")
            self.d(resourceId="com.android.settings:id/title", text=u"WLAN").click()
        else:
            self.stop()
            self.start()
            print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击WLAN")
            self.d(resourceId="com.android.settings:id/title", text=u"WLAN").click()

    @__sleep
    def list_bluetooth(self):
        print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击蓝牙")
        self.d(resourceId="com.android.settings:id/title", text=u"蓝牙").click()


    @__sleep
    def list_simcard(self):
        print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击 SIM卡")
        self.d(resourceId="com.android.settings:id/title", text=u"SIM卡").click()


    @__sleep
    def list_data_usage(self):
        print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击 流量使用情况")
        self.d(resourceId="com.android.settings:id/title", text=u"流量使用情况").click()

    @__sleep
    def list_more(self):
        print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击 更多")
        self.d(resourceId="com.android.settings:id/title", text=u"更多").click()

    @__sleep
    def list_display(self):
        if self.d(resourceId="com.android.settings:id/title", text=u"显示").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击 显示")
            self.d(resourceId="com.android.settings:id/title", text=u"显示").click()
            return True
        else:
            return False

    @__sleep
    def list_sound(self):
        if self.d(resourceId="com.android.settings:id/title", text=u"提示音和通知").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击 提示音和通知")
            self.d(resourceId="com.android.settings:id/title", text=u"提示音和通知").click()
            return True
        else:
            return False

    @__sleep
    def list_apps(self):
        if self.d(resourceId="com.android.settings:id/title", text=u"应用").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击 应用")
            self.d(resourceId="com.android.settings:id/title", text=u"应用").click()
            return True
        else:
            return False

    @__sleep
    def list_phone(self):
        if self.d(resourceId="com.android.settings:id/title", text=u"电话").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击 电话")
            self.d(resourceId="com.android.settings:id/title", text=u"电话").click()
            return True
        else:
            return False

    @__sleep
    def list_storage(self):
        if self.d(resourceId="com.android.settings:id/title", text=u"存储设备和 USB").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击 存储设备和 USB")
            self.d(resourceId="com.android.settings:id/title", text=u"存储设备和 USB").click()
            return True
        else:
            return False

    @__sleep
    def list_battery(self):
        if self.d(resourceId="com.android.settings:id/title", text=u"电池").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击 电池")
            self.d(resourceId="com.android.settings:id/title", text=u"电池").click()
            return True
        else:
            return False

    @__sleep
    def list_memory(self):
        if self.d(resourceId="com.android.settings:id/title", text=u"内存").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击 内存")
            self.d(resourceId="com.android.settings:id/title", text=u"内存").click()
            return True
        else:
            return False

    @__sleep
    def list_reset(self):
        if self.d(resourceId="com.android.settings:id/title", text=u"备份和重置").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 设置列表界面: 点击 备份和重置")
            self.d(resourceId="com.android.settings:id/title", text=u"备份和重置").click()
            return True
        else:
            return False



    '''
    一下为备份和重置界面
    '''

    def restore_factory(self):
        print('点击恢复出厂设置')
        self.d(resourceId="android:id/title", text=u"恢复出厂设置").click()

    def affirm_restore_factory(self):
        print('---------->点击确认恢复出厂设置')
        time.sleep(3)
        self.d(resourceId="com.android.settings:id/initiate_master_clear").click()
        self.d(resourceId="com.android.settings:id/execute_master_clear").click()



    '''
    以下为 WLAN 界面
    '''
    @__sleep
    def wlan_switch(self):
        print(">>>>>>>>>>>>>>>>> WLAN 界面: 点击 WIFI开关")
        self.d(resourceId="com.android.settings:id/switch_widget").click()

    def get_wlan_switch(self):
        return self.d(resourceId="com.android.settings:id/switch_text").get_text()


    '''
    以下为 更多 界面
    '''
    def more_aeroplane_mode(self):
        print(">>>>>>>>>>>>>>>>> 更多 界面: 点击 飞行模式")
        self.d(resourceId="android:id/title", text=u"飞行模式").click()

    def more_wifi_calling(self):
        print(">>>>>>>>>>>>>>>>> 更多 界面: 点击 WLAN 通话")
        self.d(resourceId="android:id/title", text=u"WLAN 通话").click()

    def more_hotspot(self):
        print(">>>>>>>>>>>>>>>>> 更多 界面: 点击 网络共享与便携式热点")
        self.d(resourceId="android:id/title", text=u"网络共享与便携式热点").click()

    def more_vpn(self):
        print(">>>>>>>>>>>>>>>>> 更多 界面: 点击 VPN")
        self.d(resourceId="android:id/title", text=u"VPN").click()

    def more_mobile_network(self):
        print(">>>>>>>>>>>>>>>>> 更多 界面: 点击 移动网络")
        self.d(resourceId="android:id/title", text=u"移动网络").click()

    def more_mobile_plan(self):
        print(">>>>>>>>>>>>>>>>> 更多 界面: 点击 手机套餐")
        self.d(resourceId="android:id/title", text=u"手机套餐").click()

    def more_broadcasts(self):
        print(">>>>>>>>>>>>>>>>> 更多 界面: 点击 紧急广播")
        self.d(resourceId="android:id/title", text=u"紧急广播").click()

    '''
    以下为更多- 移动网络 界面
    '''
    def more_mb_network_roaming(self):
        print(">>>>>>>>>>>>>>>>> 更多 移动网络界面: 点击 移动数据网络漫游")
        self.d(resourceId="android:id/title", text=u"移动数据网络漫游").click()

    def more_mb_network_type(self):
        print(">>>>>>>>>>>>>>>>> 更多 移动网络界面: 点击 首选网络类型")
        self.d(resourceId="android:id/title", text=u"首选网络类型").click()

    def more_mb_network_type_cut(self,text1="4G/3G/2G"):
        print(">>>>>>>>>>>>>>>>> 更多 移动网络 首选网络类型 界面: 点击 "+text1)
        if self.d(resourceId="android:id/text1", text=text1).wait(timeout=2):
            self.d(resourceId="android:id/text1", text=text1).click()
            return True
        else:
            return False
    def get_simcard_network_type(self):
        return self.d(resourceId="android:id/summary")[1].get_text()

    def more_mb_network_mode(self):
        print(">>>>>>>>>>>>>>>>> 更多 移动网络界面: 点击 增强4G LTE模式")
        self.d(resourceId="android:id/title", text=u"增强4G LTE模式").click()

    def more_mb_network_APNnames(self):
        print(">>>>>>>>>>>>>>>>> 更多 移动网络界面: 点击 接入点名称 (APN)")
        self.d(resourceId="android:id/title", text=u"接入点名称 (APN)").click()

    def more_mb_network_operators(self):
        print(">>>>>>>>>>>>>>>>> 更多 移动网络界面: 点击 网络运营商")
        self.d(resourceId="android:id/title", text=u"网络运营商").click()



    '''
    以下为蓝牙界面
    '''

    @__sleep
    def bluetooth_switch(self):
        print(">>>>>>>>>>>>>>>>> 蓝牙 界面: 点击 蓝牙开关")
        self.d(resourceId="com.android.settings:id/switch_widget").click()

    @__sleep
    def bluetooth_adt(self):
        msg = ''
        if self.d(resourceId="android:id/title"):
            print(">>>>>>>>>>>>>>>>> 蓝牙 界面: 正在搜索可用设备")
            if self.d(className="android.widget.RelativeLayout"):
                msg = ">>>>>>>>>>>>>>>>> 蓝牙 界面: 可正常搜索到可用设备"
                print(msg)
                return True, msg
            else :
                msg = ">>>>>>>>>>>>>>>>> 蓝牙 界面: 未搜索到可用设备"
                print(msg)
                return False,msg
        else:
            print(">>>>>>>>>>>>>>>>> 蓝牙 界面: 未搜索设备")
            return False, msg

    @__sleep
    def bluetooth_more(self):
        print(">>>>>>>>>>>>>>>>> 蓝牙 界面: 点击 更多选项")
        self.d(description=u"更多选项", className="android.widget.ImageButton").click()

    @__sleep
    def bluetooth_wait_more_refresh(self):
        print(">>>>>>>>>>>>>>>>> 蓝牙更多 界面: 等待 刷新 按钮出现")
        return self.d(resourceId="android:id/title", text=u"刷新").wait(timeout=30.0)

    @__sleep
    def bluetooth_more_refresh(self):
        print(">>>>>>>>>>>>>>>>> 蓝牙更多 界面: 点击 刷新 选项")
        self.d(resourceId="android:id/title", text=u"刷新").click()

    @__sleep
    def bluetooth_more_rename(self):
        print(">>>>>>>>>>>>>>>>> 蓝牙更多 界面: 点击 重命名此设备 选项")
        self.d(resourceId="android:id/title", text=u"重命名此设备").click()

    @__sleep
    def bluetooth_more_show(self):
        print(">>>>>>>>>>>>>>>>> 蓝牙更多 界面: 点击 显示收到的文件 选项")
        self.d(resourceId="android:id/title", text=u"显示收到的文件").click()

    '''
    以下为进入应用后的界面
    '''
    def click_operation_app(self):
        print('点击管理应用')
        self.d(resourceId="android:id/title").click()


    def acquire_page_app_name(self):
        '''
        获取当前页面app的名称
        :return:
        '''
        page_app_name=[]
        len_num=len(self.d(resourceId="android:id/title"))
        for i  in range(len_num):
            page_app_name.append(self.d(resourceId="android:id/title")[i].get_text())
        return page_app_name


    def acquire_app_versions(self):
        print('获取APP的版本信息')
        versions=self.d(resourceId="com.android.settings:id/widget_text1")[1].get_text()
        time.sleep(2)
        self.app_list_page_back()
        return versions



    def app_list_page_back(self):
        print('---------->点击返回按钮')
        self.d(description=u"向上导航").click()


    def click_app_name(self,i):
        print('---------->点击app的名字进入app详情')
        self.d(resourceId="android:id/title", text=i).click()

    def slide_page(self):
        len_num = len(self.d(resourceId="android:id/title"))
        start_app = self.d(resourceId="android:id/title")[len_num - 2].get_text()
        print('---------->拖动')
        self.d.swipe(0.275, 0.845, 0.377, 0.045)
        end_app = self.d(resourceId="android:id/title")[len_num - 2].get_text()
        if start_app==end_app:
            return True
        else:
            return False

    '''
    以下为显示界面
    '''
    def display_time(self, text='long'):
        self.d.screen_on()
        self.d(resourceId="android:id/title", text=u"休眠").click()
        if text=='long':
            if self.d(resourceId="android:id/text1", text=u"永不").wait(timeout=1):
                self.d(resourceId="android:id/text1", text=u"永不").click()
                print(">>>>>>>>>>>>>>>>> 设置显示界面: 设置休眠时间为 永不")
            elif self.d(resourceId="android:id/text1", text=u"30分钟").wait(timeout=1):
                self.d(resourceId="android:id/text1", text=u"30分钟").click()
                print(">>>>>>>>>>>>>>>>> 设置显示界面: 设置休眠时间为 30分钟")
            else:
                self.d(resourceId="android:id/text1", text=u"10分钟").click()
                print(">>>>>>>>>>>>>>>>> 设置显示界面: 设置休眠时间为 10分钟")
        else:
            if self.d(resourceId="android:id/text1", text=text).wait(timeout=1):
                self.d(resourceId="android:id/text1", text=text).click()
                print(">>>>>>>>>>>>>>>>> 设置显示界面: 设置休眠时间为 ",text)

            else:
                print("不支持的休眠时间：", text)

    '''
    以下为其他封装的操作
    '''

    def cut_simcard_network_type(self,data_type):
        if self.d(resourceId="com.android.settings:id/category_title").wait(timeout=1):
            pass
        else:
            self.stop()
            self.start()
        self.list_more()
        self.more_mobile_network()
        if data_type == "get":
            return self.get_simcard_network_type()
        else:
            self.more_mb_network_type()
            self.more_mb_network_type_cut(data_type)

    def check_mcwill_data_status(self):
        '''
          True为 已连接 状态
          False为 其他 状态
          :return:
          '''
        if self.d(resourceId="android:id/title",text=u'网络信息').wait(timeout=1):
            pass
        else:
            self.stop()
            self.start()
            self.list_mcwill()
        if self.d(resourceId="android:id/summary").get_text() == "已连接":
            return True
        else:
            return False

    def check_mcwill_data_switch(self):
        '''
        True为 开启 状态
        False为 关闭 状态
        :return:
        '''
        if self.d(resourceId="android:id/title", text=u'网络信息').wait(timeout=1):
            pass
        else:
            self.stop()
            self.start()
            self.list_mcwill()
        if self.d(resourceId="com.android.settings:id/switch_widget",text='开启').wait(timeout=2):
            return True
        else:
            return False


    def cut_mcwill_data_switch(self, switch="on"):
        '''
        on 为保持 开启 状态
        off 为保持 关闭 状态
        :return:
        '''
        if self.d(resourceId="android:id/title", text=u'网络信息').wait(timeout=1):
            pass
        else:
            self.stop()
            self.start()
            self.list_mcwill()
        if switch == "on":
            print(">>>>>>>>>>>>>>>>> McWill数据界面: 开启数据")
            if self.d(resourceId="com.android.settings:id/switch_widget",text='开启').wait(timeout=2):
                pass
            else:
                self.d(resourceId="com.android.settings:id/switch_widget", text='关闭').click()
                time.sleep(4)
        else:
            print(">>>>>>>>>>>>>>>>> McWill数据界面: 关闭数据")
            if self.d(resourceId="com.android.settings:id/switch_widget", text='开启').wait(timeout=2):
                self.d(resourceId="com.android.settings:id/switch_widget", text='开启').click()
                if self.d(resourceId="android:id/button1").wait(timeout=1):
                    self.d(resourceId="android:id/button1").click()
                if self.d(resourceId="android:id/button1").wait(timeout=1):
                    self.d(resourceId="android:id/button1").click()
        self.d.press("home")







    @__sleep
    def display_setting(self):
        print(">>>>>>>>>>>>>>>>> settings: 设置休眠时间为最长时间")
        self.stop()
        self.start()
        while True:
            if self.list_display():
                self.display_time()
                break
            else:
                self.d.swipe(0.6, 0.9, 0.6, 0.7)
        self.d.press("home")

    @__sleep
    def open_wifi(self):
        print(">>>>>>>>>>>>>>>>> settings: 检测wifi是否开启，并保持开启状态")
        if not(self.d(resourceId="com.android.settings:id/title", text=u"WLAN").wait(timeout=1)):
            self.stop()
            self.start()
        self.list_wlan()
        time.sleep(2)
        while True:
            if self.d(resourceId="com.android.settings:id/switch_text", text=u"开启").wait(timeout=2.0):
                if self.d(resourceId="android:id/summary", text="已连接").wait(timeout=3):
                    print("WIFI已连接")
                    return True
                else:
                    print("WIFI连接异常")
                    return False
                break
            elif self.d(resourceId="com.android.settings:id/switch_text", text=u"关闭").wait(timeout=2.0):
                self.wlan_switch()
            else :
                print("WIFI连接出现异常")
        self.d.press("home")

    def close_wifi(self):
        print(">>>>>>>>>>>>>>>>> settings: 检测wifi是否关闭，并保持关闭状态")
        if not(self.d(resourceId="com.android.settings:id/title", text=u"WLAN").wait(timeout=1)):
            self.stop()
            self.start()
        self.list_wlan()
        time.sleep(2)
        if self.d(resourceId="com.android.settings:id/switch_text", text=u"开启").wait(timeout=2.0):
            self.wlan_switch()
        if self.d(resourceId="com.android.settings:id/switch_text", text=u"关闭").wait(timeout=2.0):
            print("WIFI已关闭")
        self.d.press("home")


    @__sleep
    def open_bluetooth(self):
        print(">>>>>>>>>>>>>>>>> settings: 检测蓝牙是否开启，将蓝牙打开")
        self.stop()
        self.start()
        self.list_bluetooth()
        blurtooth=self.d(resourceId="com.android.settings:id/switch_text",text='关闭').wait(timeout=2)
        if blurtooth==True:
            self.d(resourceId="com.android.settings:id/switch_widget").click()
            blurtooth1 = self.d(resourceId="com.android.settings:id/switch_text",text='开启').wait(timeout=2)
            if blurtooth1==True:
                print('已经开启了蓝牙')
            else:
                print('蓝牙开启失败')
        else:
            print('蓝牙处于开启状态')


    def auto_connect_wifi(self):
        wifi_name = self.name
        wifi_password = self.password
        print(">>>>>>>>>>>>>>>>> settings: 自动连接wifi "+wifi_name)
        if not(self.d(resourceId="com.android.settings:id/title", text=u"WLAN").wait(timeout=1)):
            self.stop()
            self.start()
        self.list_wlan()
        while True:
            if self.d(resourceId="com.android.settings:id/switch_text", text=u"开启").wait(timeout=2.0):
                time.sleep(5)
                self.d.screen_on()
                if self.d(resourceId="android:id/summary", text="已连接").wait(timeout=5):
                    print("WIFI已连接")
                    break
                else:
                    print("WIFI已开启，连接异常，自动连接wifi "+wifi_name)
            elif self.d(resourceId="com.android.settings:id/switch_text", text=u"关闭").wait(timeout=2.0):
                self.wlan_switch()
                time.sleep(5)
                self.d.screen_on()
            if self.d(resourceId="android:id/title", text=wifi_name).wait(timeout=15):
                self.d(resourceId="android:id/title", text=wifi_name).click()
                print("成功找到wifi，开始连接")
                time.sleep(2)
                if self.d(resourceId="com.android.settings:id/password"):
                    self.d(resourceId="com.android.settings:id/password").send_keys(wifi_password)
                    if self.d(resourceId="android:id/button1").wait(timeout=2):
                        self.d(resourceId="android:id/button1").click()
                    else :
                        self.d.click(0.91, 0.9)
                    print("成功输入wifi密码并连接")
                elif self.d(resourceId="com.android.settings:id/value", text="已连接").wait(timeout=2):
                    print("wifi处于已连接状态")
                    self.d(resourceId="android:id/button2").click()
                else:
                    self.d.press("back")
                    print("自动连接wifi("+wifi_name+")失败")
            else:
                print("未找到WIFIwifi("+wifi_name+")，自动连接失败")
            break
        self.d.press("home")

    def change_language_Chinese(self):
        '''
        进入语言菜单后，点击选择语言，找到中文点击
        :return:
        '''
        self.d(resourceId="android:id/title").click()
        print('开始寻找中文按钮')
        for i in range(0,8):
            if self.d(resourceId="android:id/locale", text=u"中文 (简体)").wait(timeout=2)==True:
                self.d(resourceId="android:id/locale", text=u"中文 (简体)").click()
                break
            else:
                self.d.screen_on()
                self.d.swipe(0.729, 0.8, 0.808, 0.095)

    def change_language_A(self):
        '''
        更改语言原始语言为西班牙语
        :return:
        '''
        print('开始寻找语言设置菜单')
        for i in range(0,4):
            if self.d(resourceId="com.android.settings:id/title", text=u"Teclado e idioma").wait(timeout=2)==True:
                self.d(resourceId="com.android.settings:id/title", text=u"Teclado e idioma").click()
                break
            else:
                self.d.screen_on()
                self.d.swipe(0.729, 0.8, 0.808, 0.095)
        self.change_language_Chinese()

    def change_language_B(self):
        '''
        更改语言，原始语言为柬埔寨语
        :return:
        '''
        print('开始寻找语言设置菜单')
        for i in range(0, 4):
            if self.d(resourceId="com.android.settings:id/title",text=u"ភាសា & ការ​បញ្ចូល").wait(timeout=2)==True:
                self.d(resourceId="com.android.settings:id/title",text=u"ភាសា & ការ​បញ្ចូល").click()
                break
            else:
                self.d.screen_on()
                self.d.swipe(0.729, 0.8, 0.808, 0.095)
        self.change_language_Chinese()

    def change_language(self):
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        self.stop()
        self.start()
        if self.d(text=u"ការ​កំណត់").wait(timeout=2)==True:
            self.d.screen_on()
            self.change_language_B()
            self.stop()
            return '柬埔寨'
        elif self.d(text=u"Configuración").wait(timeout=2)==True:
            self.d.screen_on()
            self.change_language_A()
            self.stop()
            return '尼加拉瓜'
        elif self.d(text=u"设置").wait(timeout=2)==True:
            self.d.screen_on()
            print('已经是中文')
            self.stop()
            return '中国'


    def wait_app_list(self):
        self.stop()
        self.start()
        for i in range(0,3):
            if self.list_apps()==False:
                self.d.swipe(0.729, 0.8, 0.808, 0.095)
            else:
                break




    '''
    下面是关于手机界面的操作
    '''

    def enter_about_phone(self):
        '''
        进入关于手机界面
        :return:
        '''
        self.stop()
        self.start()
        for i in range(0,6):
            if self.d(resourceId="com.android.settings:id/title", text=u"关于手机").wait(timeout=2)==True:
                self.d(resourceId="com.android.settings:id/title", text=u"关于手机").click()
                break
            else:
                self.d.swipe(0.729, 0.8, 0.808, 0.095)
        if self.d(resourceId="android:id/title", text=u"型号").wait(timeout=3) == True:
            return True
        else:
            return False


    def click_system_upgrade(self):
        '''
        点击系统升级
        :return:
        '''
        self.d(resourceId="android:id/title").click()



    def click_status_message(self):
        '''
        点击状态信息
        :return:
        '''
        self.d(resourceId="android:id/title", text=u"状态信息").click()

        '''
        下面是系统升级界面
        '''

    def click_system_update_set(self):
        print('---------->点击系统升级界面的设置')
        self.d(resourceId="com.redstone.ota.ui:id/ll_main_setting").click()

    def click_system_update_update(self):
        print('---------->点击系统升级界面的检查更新')
        self.d(resourceId="com.redstone.ota.ui:id/main_btn_check").click()

    '''
    下面是进入系统升级设置界面的操作
    '''

    def click_SD_update(self):
        print('---------->点击系统升级界面的本地升级')
        self.d(resourceId="com.redstone.ota.ui:id/tv_local_update").click()
        return self.d(resourceId="com.redstone.ota.ui:id/install_button_install").wait(timeout=3)

    def click_folder(self):
        print('---------->点击选择存储的文件夹')
        self.d(resourceId="com.redstone.ota.ui:id/imgFilebrowser").click()

    def select_updete_file(self,file):
        print('---------->寻找升级文件')
        while True:
            time.sleep(3)
            if self.d(resourceId="com.redstone.ota.ui:id/txtItemFilebrowser",text=file).wait(timeout=3)==True:
                time.sleep(5)
                self.d(resourceId="com.redstone.ota.ui:id/txtItemFilebrowser", text=file).click()
                break
            else:
                page_number = len(self.d(resourceId="com.redstone.ota.ui:id/txtItemFilebrowser"))
                start_file_name = self.d(resourceId="com.redstone.ota.ui:id/txtItemFilebrowser")[page_number - 1].get_text()
                self.d.swipe(0.729, 0.8, 0.808, 0.095)
                page_number = len(self.d(resourceId="com.redstone.ota.ui:id/txtItemFilebrowser"))
                end_file_name = self.d(resourceId="com.redstone.ota.ui:id/txtItemFilebrowser")[page_number - 1].get_text()
                if start_file_name==end_file_name:
                    break

    def click_install(self):
        '''
        点击立即安装按钮
        :return:
        '''
        print('---------->点击立即安装按钮')
        self.d(resourceId="com.redstone.ota.ui:id/install_button_install").click()

    def recover_factory_set(self):
        print('---------->开始恢复出厂设置')
        self.stop()
        self.start()
        for i in range(0,4):
            if self.list_reset()==True:
                break
            else:
                self.d.swipe(0.729, 0.8, 0.808, 0.095)
        self.restore_factory()
        self.affirm_restore_factory()


    def acquire_about_phone_message(self):
        '''
        获取关于手机的详细信息
        :return: phone_message <dic>类型
        '''
        if self.enter_about_phone()==True:
            self.d.swipe(0.729, 0.8, 0.808, 0.095)
            key_list=[]
            values_list=[]
            key_num=len(self.d(resourceId="android:id/title"))
            for i in range(1,key_num):
                key_name=self.d(resourceId="android:id/title")[i].get_text()
                key_list.append(key_name)
            values_num=len(self.d(resourceId="android:id/summary"))
            for i in range(values_num):
                values_name=self.d(resourceId="android:id/summary")[i].get_text()
                values_list.append(values_name)
            phone_message=dict(zip(key_list,values_list))
            return phone_message
        else:
            return False

    def click_datatime(self):
        for i in range(5):
            if self.d(resourceId="com.android.settings:id/title", text=u"日期和时间").wait(timeout=2) == True:
                print(">>>>>>>>>>>>>>>>> 点击进入时间与日期")
                self.d(resourceId="com.android.settings:id/title", text=u"日期和时间").click()
                break
            else:
                self.d.swipe(0.729, 0.8, 0.808, 0.095)

    def get_timezone(self):
        '''
        获取时区时间
        :return: timezone 时区时间
        '''
        if not(self.d(text=u"日期和时间").wait(timeout=2)):
            self.start()
            self.click_datatime()
        time.sleep(1)
        timezone = self.d(resourceId="android:id/summary")[4].get_text()
        return timezone

    def get_date(self):
        '''
        获取日期
        :return: timezone 时区时间
        '''
        if not(self.d(text=u"日期和时间").wait(timeout=2)):
            self.start()
            self.click_datatime()
        time.sleep(1)
        date = self.d(resourceId="android:id/summary")[2].get_text()
        return date

    def get_date_format(self):
        '''
        获取 24小时格式开关
        :return: date_format shiy 24小时格式开关，True = 开启，False = 关闭
        '''
        if not(self.d(text=u"日期和时间").wait(timeout=2)):
            self.start()
            self.click_datatime()
        time.sleep(1)
        date_format = self.d(resourceId="android:id/switchWidget")[2].get_text()
        if date_format == "关闭":
            date_format = False
        else:
            date_format = True
        return date_format

    def open_24date_format(self):
        '''
        获取 24小时格式开关
        :return: date_format shiy 24小时格式开关，True = 开启，False = 关闭
        '''
        if not(self.d(text=u"日期和时间").wait(timeout=2)):
            self.start()
            self.click_datatime()
        time.sleep(1)
        date_format = self.d(resourceId="android:id/switchWidget")[2].get_text()
        if date_format == "开启":
            pass
        else:
            self.d(resourceId="android:id/switchWidget", text=u"关闭").click()


    def get_sims_number(self):
        self.stop()
        self.start()
        self.list_simcard()
        sim_status = self.d(resourceId="android:id/summary").get_text()
        if sim_status == "未插入SIM卡":
            return "未插入SIM卡"
        else:
            return sim_status[-11:]
        self.stop()

    def get_mcwill_number(self):
        self.stop()
        self.start()
        self.list_simcard()
        sim_status = self.d(resourceId="android:id/summary")[1].get_text()
        if sim_status == "未插入SIM卡":
            return "未插入SIM卡"
        else:
            return sim_status[-13:]
        self.stop()
