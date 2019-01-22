import time
import uiautomator2 as u2
from src.general import get_config as config

class NicTalk:
    def __init__(self, d):
        self.d = d
        self.name = config.get_config("TALK", "name")
        self.password = config.get_config("TALK", "password")


    def __sleep(func):
        def inner(self):
            time.sleep(1)
            self.d.screen_on()
            return func(self)
        return inner

    def start(self):
        print(">>>>>>>>>>>>>>>>> 启动APP： NicTalk")
        self.d.app_start("com.nictalk.start")
        time.sleep(3)
        if self.d(resourceId="com.nictalk.start:id/title", text=u"通讯录").wait(timeout=2)==True:
            print('已经进入NicTalk')
        else:
            self.pop_up1()
            self.pop_up()
        self.pop_up1()
        login = self.wait_login()
        register = self.wait_register()
        if login and register == True:
            print('>>>>>>>>>>>>>>>>>>>>正在登陆')
            self.d(resourceId="com.nictalk.start:id/activity_login_country_name").click()
            self.d(resourceId="com.nictalk.start:id/country_et_search").set_text('柬埔寨')
            self.d(resourceId="com.nictalk.start:id/activity_country_name").click()
            self.d(resourceId="com.nictalk.start:id/activity_login_home_phone_num").set_text(self.name)
            self.d(resourceId="com.nictalk.start:id/activity_login_by_pw_pw").set_text(self.password)
            time.sleep(2)
            self.d.press("back")
            self.d(resourceId="com.nictalk.start:id/activity_login_home_next_step").click()
            pop_up = self.d(resourceId="com.nictalk.start:id/alertTitle").wait(timeout=2000000)
            if pop_up == True:
                self.d(resourceId="android:id/button2", text='取消').click()
        else:
            mine=self.d(resourceId="com.nictalk.start:id/title", text=u"我的").wait(timeout=3)
            if mine==True:
                self.d(resourceId="com.nictalk.start:id/title", text=u"我的").click()
                login=self.d(resourceId="com.nictalk.start:id/nick").get_text()
                if login=='未登录':
                    self.d.swipe(0.484, 0.809, 0.56, 0.082)
                    self.d(className="android.widget.LinearLayout", instance=12).click()
                    self.d(resourceId="android:id/button1").click()
                    self.d(resourceId="com.nictalk.start:id/activity_login_country_name").click()
                    self.d(resourceId="com.nictalk.start:id/country_et_search").set_text('柬埔寨')
                    self.d(resourceId="com.nictalk.start:id/activity_country_name").click()
                    print('>>>>>>>>>>>>>>>>>>>>正在登陆')
                    self.d(resourceId="com.nictalk.start:id/activity_login_home_phone_num").set_text(self.name)
                    self.d(resourceId="com.nictalk.start:id/activity_login_by_pw_pw").set_text(self.password)
                    time.sleep(2)
                    self.d.press("back")
                    self.d(resourceId="com.nictalk.start:id/activity_login_home_next_step").click()
                    pop_up = self.d(resourceId="com.nictalk.start:id/alertTitle").wait(timeout=20)
                    if pop_up == True:
                        self.d(resourceId="android:id/button2", text='取消').click()

    def stop(self):
        print(">>>>>>>>>>>>>>>>> 关闭APP： NicTalk")
        self.d.app_stop("com.nictalk.start")

    '''
       下面是处理弹框界面
       '''

    def pop_up(self):
        '''
        检测弹框
        :return:
        '''
        if self.d(resourceId="com.android.packageinstaller:id/permission_message").wait(timeout=20):
            while True:
                if self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").wait(timeout=5):
                    self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
                else:
                    break

    def pop_up1(self):
        '''
        等待欢迎使用talk
        :return:
        '''
        if self.d(resourceId="com.nictalk.start:id/title", text='欢迎使用Talk').wait(timeout=5):
            self.d(resourceId="com.nictalk.start:id/positiveButton").click()

    def wait_login(self):
        login = self.d(resourceId="com.nictalk.start:id/activity_login_home_next_step").wait(timeout=3)
        return login

    def wait_register(self):
        print('---------->等待注册出现')
        register = self.d(resourceId="com.nictalk.start:id/activity_login_home_register").wait(timeout=3)
        return register

    def acquire_state_name(self):
        state_name = self.d(resourceId="com.nictalk.start:id/activity_login_country_name").get_text()
        return state_name

    def assert_login(self):
        print(">>>>>>>>>>>>>>>>> 启动APP： NicTalk")
        self.d.app_start("com.nictalk.start")
        self.pop_up()
        self.pop_up1()
        login = self.wait_login()
        register = self.wait_register()
        if login and register == True:
            return True

    @__sleep
    def click_me(self):
        print(">>>>>>>>>>>>>>>>> NicTalk界面: 点击 我的")
        self.d(resourceId="com.nictalk.start:id/title", text=u"我的").click()

    @__sleep
    def click_contacts(self):
        print(">>>>>>>>>>>>>>>>> NicTalk界面: 点击 通讯录")
        self.d(resourceId="com.nictalk.start:id/title", text=u"通讯录").click()

    @__sleep
    def click_calls(self):
        print(">>>>>>>>>>>>>>>>> NicTalk界面: 点击 电话")
        self.d(resourceId="com.nictalk.start:id/title", text=u"电话").click()

    def input_phone_number(self,num):
        '''
        输入电话号码
        :param num:传入电话号码:l代表*  r代表#   g代表拨号
        :return:
        '''
        if not(self.d(resourceId="com.nictalk.start:id/del_edit").wait(timeout=1)):
            self.d(resourceId="com.nictalk.start:id/title", text=u"电话").click()
        print('>>>>>>>>>>>>>>>>>>>输入电话号码：'+str(num))
        for i in num:
            self.d(resourceId="com.nictalk.start:id/ibtn_key_"+str(i)).click()

    def android_input_phone_number(self,num):
        '''
        在android原生电话输入号码
        :param num: 传入电话号码
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>> 在android原生输入电话号码：'+str(num))
        for i in num:
            self.d(resourceId="com.android.dialer:id/dialpad_key_number", text=i).click()

    def android_click_call(self):
        print('>>>>>>>>>>>>>>>>>>> 在android原生拨号界面，点击G网拨打')
        self.d(resourceId="com.android.dialer:id/dialpad_floating_action_button").click()


    @__sleep
    def click_recent(self):
        print(">>>>>>>>>>>>>>>>> NicTalk界面: 点击 消息")
        self.d(resourceId="com.nictalk.start:id/title", text=u"消息").click()




    '''
    以下为通讯录界面
    '''

    @__sleep
    def contacts_all(self):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录界面: 点击 全部")
        self.d(resourceId="com.nictalk.start:id/friend_rb_all").click()

    @__sleep
    def contacts_cootalk(self):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录界面: 点击 NicTalk")
        self.d(resourceId="com.nictalk.start:id/friend_rb_cootalk").click()

    @__sleep
    def contacts_right_drawable(self):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录界面: 点击 右侧下拉栏")
        if self.d(resourceId="com.nictalk.start:id/right_drawable").wait(timeout=2):
            self.d(resourceId="com.nictalk.start:id/right_drawable").click()
        else:
            self.d(resourceId="com.nictalk.start:id/title", text=u"我的").click()
            self.d(resourceId="com.nictalk.start:id/title", text=u"通讯录").click()
            self.d(resourceId="com.nictalk.start:id/right_drawable").click()


    def contacts_search(self, search='null'):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录界面: 点击 搜索栏")
        self.d(resourceId="com.nictalk.start:id/contacts_et_search").click()
        if search != 'null' and search != 'get':
            print(">>>>>>>>>>>>>>>>> NicTalk 通讯录界面: 点击搜索栏，搜索",search)
            self.d(resourceId="com.nictalk.start:id/contacts_et_search").set_text(search)
        elif search == 'get':
            print(">>>>>>>>>>>>>>>>> NicTalk 通讯录界面: 获取搜索栏联系人总数")
            sum = self.d(resourceId="com.nictalk.start:id/contacts_et_search").get_text()
            return sum

    @__sleep
    def contacts_group_chat(self):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录界面: 点击 群聊")
        self.d(resourceId="com.nictalk.start:id/fragment_contact_list_head_item_contact_name", text=u"群聊").click()

    @__sleep
    def contacts_public_accounts(self):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录界面: 点击 公众号")
        self.d(resourceId="com.nictalk.start:id/fragment_contact_list_head_item_contact_name", text=u"公众号").click()

    def contacts_call(self, i=0):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录界面: 点击 联系人栏的拨号图标")
        self.d(resourceId="com.nictalk.start:id/fragment_contact_call_phone", className="android.widget.ImageView", instance=i).click()

    def contacts_sms(self, i=0):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录界面: 点击 联系人栏的短信图标")
        self.d(resourceId="com.nictalk.start:id/fragment_contact_send_message", className="android.widget.ImageView", instance=i).click()



    '''
    以下为右侧下拉栏界面
    '''

    @__sleep
    def right_drawable_search(self):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录右侧下拉栏界面: 点击 搜索")
        self.d(resourceId="com.nictalk.start:id/activity_add_friends_input").click()

    @__sleep
    def right_drawable_myphone(self):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录右侧下拉栏界面: 点击 我的手机号")
        number = self.d(resourceId="com.nictalk.start:id/activity_add_friends_my_number").get_text()
        return number

    @__sleep
    def right_drawable_add_contact(self):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录右侧下拉栏界面: 点击 添加手机联系人")
        self.d(resourceId="com.nictalk.start:id/title",text=u"添加手机联系人").click()


    def right_drawable_nearby(self):
        print(">>>>>>>>>>>>>>>>> CamLink 通讯录右侧下拉栏界面: 点击 面对面加好友")
        print(">>>>>>>>>>>>>>>>> CamLink 请将辅助机打开放到附近，等待测试机搜索")
        self.d(resourceId="com.nictalk.start:id/title", text=u"面对面加好友").click()
        if self.d(resourceId="com.nictalk.start:id/activity_add_friend_radar_item_text").wait(timeout=30)==True:
            print('成功搜索到面对面好友')
            self.d(resourceId="com.nictalk.start:id/activity_add_friend_radar_item_text").click()
            self.d(resourceId="com.nictalk.start:id/user_detail_add_friend").click()
            toast=self.d.toast.get_message(5.0, 10.0)
            if toast=='添加好友成功':
                return True
            else:
                return '添加好友失败'


    def right_drawable_scan(self):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录右侧下拉栏界面: 点击 扫一扫")
        self.d(resourceId="com.nictalk.start:id/title", text=u"扫一扫").click()
        if self.d(resourceId="com.nictalk.start:id/open_flashlight").wait(timeout=3)==True:
            return True
        else:
            return '没有进入扫一扫界面'


    def right_drawable_invite(self):
        print(">>>>>>>>>>>>>>>>> NicTalk 通讯录右侧下拉栏界面: 点击 邀请好友")
        self.d(resourceId="com.nictalk.start:id/title", text=u"邀请好友").click()

    '''
    以下为添加联系人界面
    '''
    def add_contact_name(self, name):
        print(">>>>>>>>>>>>>>>>> NicTalk 添加手机联系人界面: 输入 名:", name)
        self.d(resourceId="com.nictalk.start:id/activity_add_contact_first_name").set_text(name)

    def add_contact_surname(self, name):
        print(">>>>>>>>>>>>>>>>> NicTalk 添加手机联系人界面: 输入 姓:", name)
        self.d(resourceId="com.nictalk.start:id/activity_add_contact_last_name").set_text(name)

    @__sleep
    def add_contact_phone_add(self):
        print(">>>>>>>>>>>>>>>>> NicTalk 添加手机联系人界面: 点击 添加新号码")
        self.d(resourceId="com.nictalk.start:id/activity_modify_contact_phone_add").click()

    def add_contact_phone_del(self,i=0):
        print(">>>>>>>>>>>>>>>>> NicTalk 添加手机联系人界面: 点击 删除电话号码")
        self.d(resourceId="com.nictalk.start:id/iv_delete_info_item")[i].click()

    def add_contact_phone(self,phonenumber="13500000000",i=0):
        print(">>>>>>>>>>>>>>>>> NicTalk 添加手机联系人界面: 输入 电话号码:"+phonenumber+"，位置为:",i)
        self.d(resourceId="com.nictalk.start:id/et_info_input")[i].set_text(phonenumber)

    def add_contact_email(self,email="123456789@qq.com"):
        print(">>>>>>>>>>>>>>>>> NicTalk 添加手机联系人界面: 输入 邮箱:",email)
        self.d(resourceId="com.nictalk.start:id/activity_modify_contact_email").set_text(email)

    def add_contact_company(self, company="酷泰丰科技有限公司"):
        print(">>>>>>>>>>>>>>>>> NicTalk 添加手机联系人界面: 输入 公司:",company)
        self.d(resourceId="com.nictalk.start:id/activity_modify_contact_company").set_text(company)

    def add_contact_address(self, address="深圳市南山区朗峰大厦"):
        print(">>>>>>>>>>>>>>>>> NicTalk 添加手机联系人界面: 输入 地址:",address)
        self.d(resourceId="com.nictalk.start:id/activity_modify_contact_address").set_text(address)

    def add_contact_accomplish(self):
        print('>>>>>>>>>>>>>>>>>>>>点击完成')
        self.d(resourceId="com.nictalk.start:id/right_text").click()

    def add_contact_back(self):
        print('>>>>>>>>>>>>>>>>>>>>点击返回')
        self.d(resourceId="com.nictalk.start:id/back_drawable").click()


    def add_linkman_back(self):
        print('>>>>>>>>>>>>>>>>>>>>点击返回')
        self.d(resourceId="com.nictalk.start:id/contacts_iv_cleartext").click()

    def add_one_contacts(self, name, surname, phonenumber):
        self.add_contact_name(name)
        self.add_contact_surname(surname)
        self.add_contact_phone(phonenumber)
        self.add_contact_accomplish()

    def add_linkman(self,num=5):
        '''
        添加联系人
        :param num: 传入添加数量
        :return: 返回测试结果
        '''
        name='四'
        surname='李'
        number=10000
        phone=135000
        phone1=158000
        self.start()
        self.click_calls()
        self.click_contacts()
        for linkman_value in range(num) :
            self.contacts_right_drawable()
            self.right_drawable_add_contact()
            self.d.set_fastinput_ime(True)
            self.add_contact_name(name+str(linkman_value))
            self.add_contact_surname(surname)
            self.add_contact_phone_add()
            self.add_contact_phone(str(phone)+str(number))
            self.add_contact_phone(str(phone1) +str(number),1)
            self.add_contact_email()
            self.add_contact_address()
            self.add_contact_accomplish()
            self.add_contact_back()
            self.contacts_search(surname+name+str(linkman_value))
            names=self.linkman_text()
            print(names)
            if names==surname+name+str(linkman_value):
                print('>>>>>>>>>>>>>>>>>>>>添加联系人成功')
                number += 1
            else:
                print('>>>>>>>>>>>>>>>>>>>>添加联系人失败')
                number += 1
        self.stop()

    def verification_add_linkman(self,num=5):
        name = '四'
        surname = '李'
        number = 10000
        result=True
        self.start()
        self.click_calls()
        self.click_contacts()
        for linkman_value in range(num):
            self.contacts_search(surname + name + str(linkman_value))
            names=self.linkman_text()
            print(names)
            if names==surname+name+str(linkman_value):
                print('>>>>>>>>>>>>>>>>>>>>添加联系人成功')
                number += 1
            else:
                print('>>>>>>>>>>>>>>>>>>>>添加联系人失败')
                result=False
                number += 1
        self.stop()
        return result

    '''
    以下为联系人详情界面
    '''
    def get_contacts_name(self):
        print('>>>>>>>>>>>>>>>>>>>>联系人详情界面：获取联系人姓名')
        name = self.d(resourceId="com.nictalk.start:id/user_detail_nick").get_text()
        return name

    def get_contacts_number(self):
        print('>>>>>>>>>>>>>>>>>>>>联系人详情界面：获取联系人电话')
        number = self.d(resourceId="com.nictalk.start:id/detail_phone").get_text()
        return number

    def one_contacts_call(self):
        print('>>>>>>>>>>>>>>>>>>>>联系人详情界面：打电话')
        self.d(resourceId="com.nictalk.start:id/user_detail_call_phone_contact").click()

    def contacts_del(self, alert = "确认"):
        print('>>>>>>>>>>>>>>>>>>>>联系人详情界面：删除联系人')
        self.d(resourceId="com.nictalk.start:id/right_drawable").click()
        time.sleep(2)
        # 弹出确定框，选择确定或取消
        if alert == "确认":
            self.d(resourceId="com.nictalk.start:id/tvAlert").click()
        elif alert =="取消":
            self.d(resourceId="com.nictalk.start:id/tvAlertCancel").click()

######################################################################################
    def search_one_contacts(self, name):
        '''
        输入name，查找相关的联系人，进入联系人详情界面；返回查找到的联系人姓名与电话
        :param name:
        :param other:
        :return:
        '''
        getname = ""
        phone = ""
        self.contacts_search(name)
        if self.d(resourceId="com.nictalk.start:id/contact_icon").wait(timeout=1):
            print("点击联系人，进入联系人详情界面")
            self.d(resourceId="com.nictalk.start:id/contact_icon").click()
            getname = self.get_contacts_name()
            phone = self.get_contacts_number()
            return True, getname, phone
        else:
            return False, getname, phone



    def linkman_text(self):  # 获取联系人的文本信息
        name1 = self.d(resourceId="com.nictalk.start:id/fragment_contact_list_item_contact_name").get_text()
        names = name1.replace(" ", '')
        return names


    def select_linkman(self):
        print('单独删除联系人，一套操作')
        self.d(resourceId="com.nictalk.start:id/fragment_contact_list_item_contact_name").click()
        self.d(resourceId="com.nictalk.start:id/right_drawable").click()
        self.d(resourceId="com.nictalk.start:id/tvAlert").click()

    def long_click_linkman(self):
        print('>>>>>>>>>>>>>>>>>>>>长按文件夹')
        self.d(resourceId="com.nictalk.start:id/fragment_contact_list_item_contact_name").long_click(duration=1)

    def select_all_text(self):
        print('>>>>>>>>>>>>>>>>>>>>获取当前选择的文本，是全选还是全不选')
        select = self.d(resourceId="com.nictalk.start:id/right_text").get_text()
        return select

    def delete_linkman(self):
        print('>>>>>>>>>>>>>>>>>>>>删除全部联系人')
        self.d(resourceId="com.nictalk.start:id/activity_batch_delete_num").click()
        self.d(resourceId="com.nictalk.start:id/tvAlert").click()
        delete_pop_up = self.d(resourceId="com.nictalk.start:id/id_tv_loadingmsg").wait_gone(timeout=1000)
        return delete_pop_up

    def all_select(self):
        print('>>>>>>>>>>>>>>>>>>>>点击全选')
        self.d(resourceId="com.nictalk.start:id/right_text").click()

    '''
    拨号选择界面
    '''
    def click_voip(self):
        if self.d(resourceId="com.nictalk.start:id/tv_call_type", text=u"VoIP呼叫").wait(timeout=2):
            print('>>>>>>>>>>>>>>>>>>>>拨号界面选择 VoIP呼叫')
            self.d(resourceId="com.nictalk.start:id/tv_call_type", text=u"VoIP呼叫").click()
            return True
        else:
            return False

    def click_cootel(self):
        if self.d(resourceId="com.nictalk.start:id/tv_call_type", text=u"CooTel呼叫").wait(timeout=2):
            print('>>>>>>>>>>>>>>>>>>>>拨号界面选择 CooTel呼叫')
            self.d(resourceId="com.nictalk.start:id/tv_call_type", text=u"CooTel呼叫").click()
            return True
        else:
            return False


    def click_G(self):
        if self.d(resourceId="com.nictalk.start:id/tv_call_type", text=u"G网呼叫").wait(timeout=2):
            print('>>>>>>>>>>>>>>>>>>>>拨号界面选择 G网呼叫')
            self.d(resourceId="com.nictalk.start:id/tv_call_type", text=u"G网呼叫").click()
            return True
        else:
            return False

    '''
    通话界面检测
    '''
    def check_call_show(self):
        if self.d(resourceId="com.android.dialer:id/floating_end_call_action_button").wait(timeout=1):
            return True
        else:
            return False

    def click_end_call(self):
        if self.d(resourceId="com.android.dialer:id/floating_end_call_action_button").wait(timeout=1):
            print('>>>>>>>>>>>>>>>>>>>>拨号界面点击挂断')
        self.d(resourceId="com.android.dialer:id/floating_end_call_action_button").click()

    def get_call_number(self):
        number = self.d(resourceId="com.android.dialer:id/name").get_text()
        return number

    def click_audio(self):
        if self.d(resourceId="com.android.dialer:id/audioButton").wait(timeout=1):
            print('>>>>>>>>>>>>>>>>>>>>拨号界面点击免提')
            self.d(resourceId="com.android.dialer:id/audioButton").click()

    def click(self):
        if self.d(resourceId="com.android.dialer:id/swapButton").wait(timeout=1):
            print('>>>>>>>>>>>>>>>>>>>>拨号界面点击蓝牙')
            self.d(resourceId="com.android.dialer:id/swapButton").click()

    def click_mute(self):
        if self.d(resourceId="com.android.dialer:id/muteButton").wait(timeout=1):
            print('>>>>>>>>>>>>>>>>>>>>拨号界面点击静音')
            self.d(resourceId="com.android.dialer:id/muteButton").click()

    def click_parameter(self):
        if self.d(resourceId="com.android.dialer:id/parameterButton").wait(timeout=1):
            print('>>>>>>>>>>>>>>>>>>>>拨号界面点击统计')
            self.d(resourceId="com.android.dialer:id/parameterButton").click()

    def click_dialpad(self):
        if self.d(resourceId="com.android.dialer:id/dialpadButton").wait(timeout=1):
            print('>>>>>>>>>>>>>>>>>>>>拨号界面点击拨号盘')
            self.d(resourceId="com.android.dialer:id/dialpadButton").click()

    def get_callpop_msg(self):
        '''
        获取挂断后的弹框提示拨号时长，不一定能获取到！
        :return:msg
        '''
        msg = ''
        if self.d(className="android.widget.FrameLayout").wait(timeout=5):
            msg = self.d(resourceId="android:id/message").get_text()
        return msg

    def get_call_state(self):
        # 获取 拨打状态
        msg = ""
        if self.d(resourceId="com.android.dialer:id/callStateLabel").wait(timeout=1):
            msg = self.d(resourceId="com.android.dialer:id/callStateLabel").get_text()
            return msg
        else:
            return msg

    def check_is_android(self):
        '''
        检查是不是安卓拨号盘界面，是就返回True
        :return:
        '''
        if self.d(resourceId="com.android.dialer:id/dialpad_floating_action_button_mcwill").wait(timeout=1) or self.d(resourceId="com.android.dialer:id/dialpad_floating_action_button").wait(timeout=1):
            return True
        else:
            return False

    '''
    下面是添加联系人的操作
    '''

    def add_linkman_num(self,num=5):
        '''
        添加联系人
        :param num: 传入添加数量
        :return: 返回测试结果
        '''
        name='四'
        surname='李'
        number=10000
        phone=135000
        phone1=158000
        self.start()
        self.click_calls()
        self.click_contacts()
        for linkman_value in range(num) :
            self.contacts_right_drawable()
            self.right_drawable_add_contact()
            self.d.set_fastinput_ime(True)
            self.add_contact_name(name+str(linkman_value))
            self.add_contact_surname(surname)
            self.add_contact_phone_add()
            self.add_contact_phone(str(phone)+str(number))
            self.add_contact_phone(str(phone1) +str(number),1)
            self.add_contact_email()
            self.add_contact_address()
            self.add_contact_accomplish()
            self.add_contact_back()
            self.contacts_search(surname+name+str(linkman_value))
            names=self.linkman_text()
            print(names)
            if names==surname+name+str(linkman_value):
                print('>>>>>>>>>>>>>>>>>>>>添加联系人成功')
                number += 1
            else:
                print('>>>>>>>>>>>>>>>>>>>>添加联系人失败')
                number += 1
        self.stop()

    def verification_add_link_man(self,num=5):
        name = '四'
        surname = '李'
        number = 10000
        result=True
        self.start()
        self.click_calls()
        self.click_contacts()
        for linkman_value in range(num):
            self.contacts_search(surname + name + str(linkman_value))
            names=self.linkman_text()
            print(names)
            if names==surname+name+str(linkman_value):
                print('>>>>>>>>>>>>>>>>>>>>添加联系人成功')
                number += 1
            else:
                print('>>>>>>>>>>>>>>>>>>>>添加联系人失败')
                result=False
                number += 1
        self.stop()
        return result

    '''
    下面是消息界面的所有操作
    '''

    def message_page_click_more(self):
        print('---------->消息界面-点击更多')
        self.d(resourceId="com.nictalk.start:id/popup_drawable").click()
        if self.d(resourceId="android:id/text1", text='发起群聊').wait(timeout=3)==True:
            return True
        else:
            return '在消息界面，点击左上角[更多]-点击失败'


    '''
    下面是【更多】界面
    '''

    def more_page_click_group_chat(self):
        print('---------->消息界面-点击更多-发起群聊')
        self.d(resourceId="android:id/text1", text='发起群聊').click()
        if self.d(resourceId="com.nictalk.start:id/tv_group_face_to_face").wait(timeout=3)==True:
            return True
        else:
            return '在[更多]操作中点击发起群聊，点击失败'

    '''
    下面是发起群聊界面
    '''

    def group_chat_page_search(self,operation,name='李 四'):
        '''
        搜索框的操作
        :param operation: 传入：输入 or 文本
        :param name: 如果operation传入的是输入name就是需要传入输入的内容,请在姓和名中间加上空格
        :return:  如果operation传入的是文本那就返回获取的文本  <int>类型
        '''
        if operation=='输入':
            self.d(resourceId="com.nictalk.start:id/activity_add_group_search").set_text(name)
            if name in self.group_chat_page_acquire_link_man():
                return True
            else:
                return '没有找到要搜索的联系人'
        elif operation=='文本':
            x=self.d(resourceId="com.nictalk.start:id/activity_add_group_search").get_text()
            search_text = str(x)[(str(x).index("索") + 1):str(x).index("位")]
            return int(search_text)

    def group_chat_page_acquire_link_man(self):
        '''
        获取第一个联系人的name
        :return:
        '''
        if self.d(resourceId="com.nictalk.start:id/fragment_contact_list_item_contact_name").wait(timeout=5)==True:
            end_link_man_name = self.d(resourceId="com.nictalk.start:id/fragment_contact_list_item_contact_name").get_text()
            print(end_link_man_name)
            return end_link_man_name
        else:
            return '没有该联系人'

    def group_chat_page_face_to_face(self,number='1234'):
        '''
        面对面建群传入群号，群号不能大于四位
        :param number:传入四位群号
        :return:
        '''
        print('---------->消息界面-点击更多-发起群聊-面对面建群')
        self.d(resourceId="com.nictalk.start:id/tv_group_face_to_face").click()
        for i in number:
            self.d(resourceId="com.nictalk.start:id/key_"+str(i)).click()
        self.d(text=u"进入该群").click()
        time.sleep(10)
        if self.d(resourceId="com.nictalk.start:id/text", text=u"你通过面对面建群进入群聊").wait(timeout=5)==True:
            return True
        else:
            return '没有正常进入群聊，进入群聊过程失败'

    def group_chat_page_select_group_chat(self):
        print('---------->消息界面-点击更多-发起群聊-选择一个群')
        self.d(resourceId="com.nictalk.start:id/tv_group_select_one").click()
        if self.d(resourceId="com.nictalk.start:id/activity_group_list_name").wait(timeout=3)==True:
            self.d(resourceId="com.nictalk.start:id/activity_group_list_name").click()
            return True
        else:
            return '账号没有群,无法选择'

    def group_chat_page_add_group_chat(self):
        print('---------->消息界面-点击更多-发起群聊-增加一个群')
        if self.group_chat_page_search(operation='文本')>0:
            self.d(resourceId="com.nictalk.start:id/fragment_contact_item_check").click()
            self.d(resourceId="com.nictalk.start:id/right_text").click()
            time.sleep(10)
            if self.d(resourceId="com.nictalk.start:id/text", text=u"你创建了群组").wait(timeout=5)==True:
                return True
            else:
                return '创建群组失败'
        else:
            return '当前手机没有联系人'

    def group_chat_page_back(self,operation='back'):
        print('---------->消息界面-点击更多中的返回按钮')
        if operation=='back':
            time.sleep(5)
            self.d(resourceId="com.nictalk.start:id/back_drawable").click()
            time.sleep(3)
        else:
            time.sleep(5)
            self.d.press("back")
            time.sleep(3)

    '''
    发起群聊界面操作结束
    '''

    def more_page_add_friend(self):
        print('---------->消息界面-点击更多-添加朋友')
        self.d(resourceId="android:id/text1", text=u"添加朋友").click()
        if self.d(resourceId="com.nictalk.start:id/text").wait(timeout=3)==True:
            return True
        else:
            return '在[更多]操作中点击添加朋友，没有进入添加朋友界面'

    '''
    下面是添加朋友界面
    '''


    '''
    下面是搜索操作界面
    '''
    def add_friend_page_search(self,phone_number='0383033701'):
        '''
        搜索服务器上的好友，输入手机联系人无效
        :param phone_number:
        :return:
        '''
        self.right_drawable_search()
        print('---------->消息界面-点击更多-添加朋友-点击搜索框-输入要搜索的联系人')
        self.d(resourceId="com.nictalk.start:id/friend_et_search").set_text(phone_number)
        print('---------->消息界面-点击更多-添加朋友-点击搜索框-输入要搜索的联系人-点击搜索')
        self.d(resourceId="com.nictalk.start:id/activity_add_friends_home_text").click()
        if self.d(resourceId="com.nictalk.start:id/detail_phone").wait()==True:
            return True
        else:
            return '没有搜索出联系人，搜索失败'


    '''
    搜索操作界面结束
    '''



    '''
    下面是邀请好友的操作
    '''

    def address_book_invite(self):
        print('---------->通讯录邀请好友')
        self.d(resourceId="com.nictalk.start:id/activity_add_friends_home_text").click()

    def invite_friend(self, phone_number):
        self.right_drawable_invite()
        self.address_book_invite()
        print('---------->通讯录搜索:', phone_number)
        self.d(resourceId="com.nictalk.start:id/contacts_et_search").set_text(phone_number)
        print('---------->选中联系人')
        self.d(resourceId="com.nictalk.start:id/lv_item_addcontact_check").click()
        self.group_chat_page_back('null')
        print('---------->点击邀请好友')
        self.d(resourceId="com.nictalk.start:id/activity_invite_add_tv_invite_num").click()
        toast = self.d.toast.get_message(5.0, 10.0)
        if toast == '邀请成功':
            return True
        else:
            return '邀请好友失败'


    '''
    邀请好友的操作完成
    '''


    '''
    添加朋友操作结束
    '''

    def more_page_scan(self):
        print('---------->消息界面-点击更多-扫一扫')
        self.d(resourceId="android:id/text1", text=u"扫一扫").click()
        if self.d(text=u"将二维码对入取景框，即可自动扫描").wait(timeout=3)==True:
            return True
        else:
            return '在[更多]操作中点击扫一扫，没有进入扫一扫界面'

    def more_page_gathering(self):
        print('---------->消息界面-点击更多-收款')
        self.d(resourceId="android:id/text1", text=u"收款").click()
        if self.d(text=u"扫一扫，向我付钱").wait(timeout=3)==True:
            return True
        else:
            return '在[更多]操作中点击收款，没有进入收款界面'

    def message_page_click_search(self,message):
        print('---------->消息界面-点击搜索-输入搜索内容')
        self.d.set_fastinput_ime(True)
        self.d(resourceId="com.nictalk.start:id/contacts_et_search").click()
        self.d.send_keys(message)
        if self.d(resourceId="com.nictalk.start:id/fragment_contact_list_item_contact_name").wait(timeout=3)==True:
            self.search_page_cancle_button()
            return True
        else:
            self.search_page_cancle_button()
            return '没有搜索到联系人'


    def search_page_cancle_button(self):
        print('---------->输入搜索内容后点击取消按钮')
        self.d(resourceId="com.nictalk.start:id/tv_cancel").click()

    '''
    下面是聊天界面的操作
    '''
    def click_chat_window(self):
        print('---------->点击一个聊天窗口')
        if self.d(resourceId="com.nictalk.start:id/chat_name").wait(timeout=2)==True:
            self.d(resourceId="com.nictalk.start:id/chat_name").click()

    '''
    下面是聊天界面的操作
    '''

    def click_send(self):
        print('---------->聊天页面--下面的发送选项--点击发送')
        self.d(resourceId="com.nictalk.start:id/send").click()

    def send_text(self,text='测试'):
        print('---------->聊天页面--下面的发送选项--聊天界面发送文字')
        self.d(resourceId="com.nictalk.start:id/input").set_text(text)

    def switch_voice(self):
        print('---------->聊天页面--下面的发送选项--聊天界面文字切换语音')
        self.d(resourceId="com.nictalk.start:id/voice").click()

    def switch_text(self):
        print('---------->聊天页面--下面的发送选项--聊天界面语音切换文字')
        self.d(resourceId="com.nictalk.start:id/keyboard").click()

    def send_voice(self):
        print('---------->聊天页面--下面的发送选项--聊天界面发送语音')
        self.d(resourceId="com.nictalk.start:id/voiceInput").long_click(duration=2)

    def click_picture(self):
        print('---------->聊天页面--下面的发送选项--点击图片按钮')
        self.d(resourceId="com.nictalk.start:id/photo").click()

    def click_camera(self):
        print('---------->聊天页面--下面的发送选项--点击相机按钮')
        self.d(resourceId="com.nictalk.start:id/camera").click()

    def click_expression(self):
        print('---------->聊天页面--下面的发送选项--点击表情按钮')
        self.d(resourceId="com.nictalk.start:id/expression").click()

    def click_plus(self):
        print('---------->聊天页面--下面的发送选项--点击加号按钮')
        self.d(resourceId="com.nictalk.start:id/plus").click()

    def click_chat_page_more(self):
        print('---------->聊天页面--右上角--点击更多按钮')
        self.d(resourceId="com.nictalk.start:id/right_drawable").click()

    '''
    下面是发送图片的操作
    '''
    def picture_send(self):
        print('---------->图片的发送')
        self.d(resourceId="com.nictalk.start:id/swipe_send").click()

    def select_picture(self):
        print('---------->选择要发送的图片')
        self.d(resourceId="com.nictalk.start:id/recycler_item_rb").click()

    def click_source_picture(self):
        print('---------->点击原图按钮')
        self.d(resourceId="com.nictalk.start:id/swipe_image_compress").click()

    def click_scrawl(self):
        print('---------->点击涂鸦按钮')
        self.d(resourceId="com.nictalk.start:id/swipe_drawing_board").click()

    '''
    下面是涂鸦的操作
    '''
    def select_red(self):
        print('---------->选择涂鸦红色')
        self.d(resourceId="com.nictalk.start:id/activity_drawing_broad_color_red").click()
        self.d.swipe(0.084, 0.216, 0.931, 0.2)

    def select_orange(self):
        print('---------->选择涂鸦橙色')
        self.d(resourceId="com.nictalk.start:id/activity_drawing_broad_color_orange").click()
        self.d.swipe(0.071, 0.316, 0.892, 0.313)

    def select_yellow(self):
        print('---------->选择涂鸦黄色')
        self.d(resourceId="com.nictalk.start:id/activity_drawing_broad_color_yellow").click()
        self.d.swipe(0.037, 0.436, 0.918, 0.421)

    def select_green(self):
        print('---------->选择涂鸦绿色')
        self.d(resourceId="com.nictalk.start:id/activity_drawing_broad_color_green").click()
        self.d.swipe(0.056, 0.524, 0.943, 0.521)

    def select_blue(self):
        print('---------->选择涂鸦蓝色')
        self.d(resourceId="com.nictalk.start:id/activity_drawing_broad_color_blue").click()
        self.d.swipe(0.068, 0.663, 0.966, 0.671)

    def select_violet(self):
        print('---------->选择涂鸦紫色')
        self.d(resourceId="com.nictalk.start:id/activity_drawing_broad_color_pink").click()
        self.d.swipe(0.022, 0.797, 0.982, 0.786)

    def click_clear(self):
        print('---------->点击清除按钮')
        self.d(resourceId="com.nictalk.start:id/activity_drawing_broad_color_image").click()

    def click_affirm(self):
        print('---------->点击确定按钮')
        self.d(resourceId="com.nictalk.start:id/activity_chat_photo_ensure").click()

    def click_cancel(self):
        print('---------->点击取消按钮')
        self.d(resourceId="com.nictalk.start:id/activity_chat_photo_cancel").click()

    '''
    涂鸦的操作结束
    '''

    '''
    发送图片的操作结束
    '''

    '''
    下面是拍照的操作
    '''
    def click_photogtaph(self):
        print('---------->点击拍照')
        self.d(resourceId="org.codeaurora.snapcam:id/shutter_button").click()

    def click_accomplish(self):
        print('---------->点击完成')
        self.d(resourceId="org.codeaurora.snapcam:id/btn_done").click()

    '''
    拍照的操作完成
    '''

    '''
    下面是表情的操作
    '''
    def select_expression(self,i=0):
        print('---------->选择一个表情')
        self.d(resourceId="com.nictalk.start:id/emojicon_icon")[i].click()

    '''
    表情的操作完成
    '''

    '''
    下面操作其他附件
    '''

    def click_location(self):
        print('---------->点击位置')
        self.d(resourceId="com.nictalk.start:id/picture", className="android.widget.ImageView", instance=0).click()

    def click_location_send(self):
        print('---------->点击发送位置')
        self.d(resourceId="com.nictalk.start:id/right_text").click()

    def click_input_location(self,location='北京'):
        print('---------->点击输入位置')
        self.d(resourceId="com.nictalk.start:id/et_search").set_text(location)
        print('---------->点击选择输入的位置')
        self.d(resourceId="com.nictalk.start:id/tv_name").click()

    def click_calling_card(self):
        print('---------->点击名片')
        self.d(resourceId="com.nictalk.start:id/picture", className="android.widget.ImageView", instance=1).click()

    def select_calling_card(self):
        print('---------->点击选择名片')
        self.d(resourceId="com.nictalk.start:id/lv_item_delete_contact_name").click()

    def input_calling_card(self,name='李四'):
        print('---------->输入要选择名片')
        self.d(resourceId="com.nictalk.start:id/contacts_et_search").set_text(name)

    def click_background(self):
        print('---------->点击背景图')
        self.d(resourceId="com.nictalk.start:id/picture", className="android.widget.ImageView", instance=2).click()

    def click_select_background(self):
        print('----------选择背景图')
        self.d(resourceId="com.nictalk.start:id/select_from_bg").click()

    def select_background(self):
        print('---------->选择一张背景图')
        self.d(resourceId="com.nictalk.start:id/iv_default").click()

    def plus_page_click_scrawl(self):
        print('---------->点击更多附件中的涂鸦按钮')
        self.d(resourceId="com.nictalk.start:id/picture", className="android.widget.ImageView", instance=3).click()

    def scrawl_page_click_easel(self):
        print('---------->涂鸦界面点击画板')
        self.d(resourceId="com.nictalk.start:id/tvAlert").click()

    def scrawl_page_click_photo(self):
        print('---------->涂鸦界面点击相册')
        self.d(resourceId="com.nictalk.start:id/tvAlert", text=u"从相册选择").click()

    def scrawl_page_click_cancle(self):
        print('---------->涂鸦界面点击取消')
        self.d(resourceId="com.nictalk.start:id/tvAlertCancel").click()

    def click_red_packet(self):
        print('---------->点击红包')
        self.d(resourceId="com.nictalk.start:id/picture", className="android.widget.ImageView", instance=4).click()
    def input_red_packet_number(self,number):
        print('---------->输入红包数量')
        self.d(resourceId="bonusNum").set_text(number)

    def input_red_packet_money(self,number):
        print('---------->输入红包金额')
        self.d(resourceId="totalMoney").set_text(number)

    def input_red_packet_remark(self,remark):
        print('---------->输入红包祝福语')
        self.d(resourceId="remark").set_text(remark)

    def send_red_packet(self):
        print('---------->点击塞钱进红包')
        self.d(resourceId="postBtn").click()

    def red_packet_page_click_back(self):
        print('---------->红包界面点击返回')
        self.d(resourceId="closeBtn").click()

    def click_file(self):
        print('---------->点击文件')
        self.d(resourceId="com.nictalk.start:id/picture", className="android.widget.ImageView", instance=5).click()

    def select_folder(self):
        print('---------->选择文件夹')
        self.d(resourceId="com.nictalk.start:id/fname", text=u"sdcard").click()

    def select_file(self,i=0):
        print('---------->选择一个文件')
        self.d(scrollable=True).fling()
        self.d(resourceId="com.nictalk.start:id/file_mark")[i].click()

    def file_page_click_confirm(self):
        print('---------->选择文件界面点击确定')
        self.d(resourceId="com.nictalk.start:id/select").click()

    def file_page_click_cancle(self):
        print('---------->选择文件界面点击取消')
        self.d(resourceId="com.nictalk.start:id/cancel").click()

    '''
    操作其他附件结束
    '''


    '''
    下面是右上角更多界面的操作
    '''

    def more_page_enter_user_details(self):
        print('---------->进入用户详情界面')
        self.d(resourceId="com.nictalk.start:id/right_drawable").click()
        user_name = self.d(resourceId="com.nictalk.start:id/activity_chat_detail_group_text").get_text()
        self.d(resourceId="com.nictalk.start:id/activity_chat_detail_group_image").click()
        # 获取用户详情界面的名称
        enter_user = self.d(resourceId="com.nictalk.start:id/user_detail_nick").get_text()
        self.group_chat_page_back()
        if enter_user == user_name:
            return True
        else:
            return '进入用户详情界面，用户名称显示错误'

    def click_add_user(self):
        print('---------->点击添加一个用户')
        self.d(resourceId="com.nictalk.start:id/activity_chat_detail_group_add").click()

    def select_add_user(self):
        print('----------->选择一个要添加的用户')
        self.d(resourceId="com.nictalk.start:id/fragment_contact_item_check", className="android.widget.CheckBox", instance=1).click()

    def click_confirm(self):
        if self.d(resourceId="com.nictalk.start:id/right_text",text='确认(1)').wait():
            self.d(resourceId="com.nictalk.start:id/right_text", text='确认(1)').click()
            self.d(resourceId="com.nictalk.start:id/loadingImageView").wait_gone(timeout=10000)
        else:
            return '没有选择上用户'

    def click_delete_user(self):
        print('---------->点击删除一个用户')
        self.d(resourceId="com.nictalk.start:id/activity_chat_detail_group_delete").click()

    def delete_page_click_compile(self):
        print('---------->删除用户界面点击编辑')
        self.d(resourceId="com.nictalk.start:id/right_text").click()

    def select_delete_user(self):
        print('---------->选择要删除的用户')
        self.d(resourceId="com.nictalk.start:id/chat_group_delete_item_name").click()

    def delete_page_click_confirm(self):
        print('---------->删除用户界面点击确定')
        self.d(resourceId="com.nictalk.start:id/right_text",text='确认(1)').click()

    def acquire_personnel_number(self):
        print('---------->获取全部群成员数量')
        persionnel=self.d(resourceId="com.nictalk.start:id/title").get_text()
        return persionnel

    def avquire_group_name_status(self):
        print('---------->获取当前组名称的状态')
        status=self.d(resourceId="com.nictalk.start:id/description").get_text()
        return status

    def click_group_name(self):
        print('---------->点击群聊名称')
        self.d(resourceId="com.nictalk.start:id/title", text=u"群聊名称").click()

    def set_group_name(self,name='测试群'):
        print('---------->设置群聊名称')
        self.d(resourceId="com.nictalk.start:id/activity_update_chat_group_detail_content").set_text(name)

    def update_group_name(self,new_name='高级测试群'):
        print('---------->修改群聊名称')
        self.d.set_fastinput_ime(True)
        self.d(resourceId="com.nictalk.start:id/activity_update_chat_group_detail_content").click()
        self.d.clear_text()
        self.d.send_keys(new_name)

    def play_voice(self):
        print('---------->自动播放语音')
        self.d(resourceId="com.nictalk.start:id/activity_add_friends_home_switch_button").click()

    def click_group_code(self):
        print('---------->点击群二维码')
        self.d(resourceId="com.nictalk.start:id/title", text=u"群二维码").click()

    def group_code_page_click_more(self):
        print('---------->在二维码界面点击更多')
        self.d(resourceId="com.nictalk.start:id/right_drawable").click()

    def group_code_save_phone(self):
        print('将群二维码保存到手机')
        self.d(resourceId="com.nictalk.start:id/tvAlert").click()

    def click_group_message(self):
        print('---------->点击群公告')
        self.d(resourceId="com.nictalk.start:id/title", text=u"群公告").click()

    def set_group_message(self,message):
        print('---------->设置群公告')
        self.d(resourceId="com.nictalk.start:id/activity_update_chat_group_detail_content").set_text(message)

    def common_click_accomplish(self):
        print('---------->在群公告界面点击完成')
        self.d(resourceId="com.nictalk.start:id/right_text").click()

    def click_my_name_in_the_group(self):
        print('---------->点击我在群中的名称')
        self.d(resourceId="com.nictalk.start:id/title", text=u"我在本群的昵称").click()

    def set_my_name_in_the_gtoup(self,new_name):
        print('---------->设置我在群中的昵称')
        self.d.set_fastinput_ime(True)#切换输入法
        self.d(resourceId="com.nictalk.start:id/activity_update_chat_group_detail_content").click()
        self.d.clear_text()#清空输入框
        self.d.send_keys(new_name)

    def click_message_disturbing(self):
        print('---------->点击消息免打扰')
        self.d(resourceId="com.nictalk.start:id/key").click()
        toast=self.d.toast.get_message(5.0, 10.0)
        if toast=='修改成功':
            return True
        else:
            return '修改失败'

    def stick_chat(self):
        print('---------->点击置顶聊天')
        self.d(resourceId="com.nictalk.start:id/key", className="android.widget.CheckBox", instance=1).click()
        toast=self.d.toast.get_message(5.0, 10.0)
        if toast=='修改成功':
            return True
        else:
            return '修改失败'

    def click_chat_file(self):
        print('---------->点击聊天文件')
        self.d(resourceId="com.nictalk.start:id/title", text=u"聊天文件").click()

    def click_clear_message(self):
        print('---------->点击清空聊天记录')
        self.d(resourceId="com.nictalk.start:id/title", text=u"清空聊天记录").click()

    def clear_message_pop_up(self,operation='确认'):
        print('--------->处理清空聊天记录的弹框')
        if self.d(resourceId="com.nictalk.start:id/alertTitle").wait(timeout=4):
            if operation=='确认':
                self.d(resourceId="android:id/button1").click()
            else:
                self.d(resourceId="android:id/button2").click()

    def click_quit(self):
        print('---------->点击退出按钮')
        self.d(resourceId="com.nictalk.start:id/delete_and_exit").click()
        if self.d(resourceId="com.nictalk.start:id/alertTitle").wait(timeout=3):
            self.d(resourceId="android:id/button1").click()

    '''
   更多界面的操作结束
    '''



    '''
    聊天界面操作结束
    '''

    '''
    下面是组合的操作
    '''
    def Case_run1(self,phone_number='13500010000'):
        result_message=''
        self.add_linkman(num=1)
        self.start()
        self.click_recent()
        click_more=self.message_page_click_more()
        if click_more!=True:
            result_message=result_message+click_more+'\n'
        click_group_chat=self.more_page_click_group_chat()
        if click_group_chat!=True:
            result_message=result_message+click_group_chat+'\n'
        search=self.group_chat_page_search(operation='输入')
        if search!=True:
            result_message=result_message+search+'\n'
        self.group_chat_page_back()
        self.message_page_click_more()
        self.more_page_click_group_chat()
        print('---------->',self.group_chat_page_search(operation='文本'))
        face_to_face=self.group_chat_page_face_to_face()
        if face_to_face!=True:
            result_message=result_message+face_to_face+'\n'
        self.group_chat_page_back()
        select_group_chat=self.group_chat_page_select_group_chat()
        if select_group_chat!=True:
           result_message=result_message+select_group_chat+'\n'
        self.group_chat_page_back()
        self.group_chat_page_back()
        self.message_page_click_more()
        self.more_page_click_group_chat()
        add_group_chat=self.group_chat_page_add_group_chat()
        if add_group_chat!=True:
            result_message=result_message+add_group_chat+'\n'
        self.group_chat_page_back()
        self.message_page_click_more()
        add_friend=self.more_page_add_friend()
        if add_friend!=True:
            result_message=result_message+add_friend+'\n'
        search=self.add_friend_page_search()
        if search!=True:
            result_message=result_message+search+'\n'
        self.group_chat_page_back()
        self.group_chat_page_back('null')
        self.right_drawable_scan()
        self.group_chat_page_back()
        self.invite_friend(phone_number)
        self.group_chat_page_back()
        self.group_chat_page_back()
        self.group_chat_page_back()
        self.message_page_click_more()
        scan=self.more_page_scan()
        if scan != True:
            result_message = result_message + scan+'\n'
        self.group_chat_page_back()
        self.message_page_click_more()
        gathering=self.more_page_gathering()
        if gathering != True:
            result_message = result_message + gathering+'\n'
        self.group_chat_page_back()
        search=self.message_page_click_search(phone_number)
        if search != True:
            result_message = result_message + search+'\n'
        return result_message

    def Case_run2(self):
        #进入一个聊天窗口
        self.click_chat_window()
        #输入文本
        self.send_text()
        #点击发送
        self.click_send()
        #切换语音
        self.switch_voice()
        #发送语音
        self.send_voice()
        #切换成文本
        self.switch_text()
        #点击相机
        self.click_camera()
        #点击拍照
        self.click_photogtaph()
        #点击完成
        self.click_accomplish()
        #点击图片
        self.click_picture()
        #选择图片
        self.select_picture()
        #点击原图
        self.click_source_picture()
        #点击涂鸦
        self.click_scrawl()
        #选择颜色
        # -----------
        self.select_red()
        self.select_orange()
        self.select_yellow()
        self.select_green()
        self.select_blue()
        self.select_violet()
        self.click_affirm()
        #------------------
        #选择表情
        self.click_expression()
        #选择表情
        for i in range(0,10):
            self.select_expression(i)
        self.click_send()
        #点击加号
        self.click_plus()
        #点击位置
        # self.click_location()
        # self.click_input_location()
        # self.click_location_send()
        #点击名片
        self.click_calling_card()
        self.input_calling_card()
        self.select_calling_card()
        #点击背景图
        self.click_background()
        self.click_select_background()
        self.select_background()
        #点击加号中的涂鸦
        self.plus_page_click_scrawl()
        self.scrawl_page_click_easel()
        self.select_red()
        self.select_orange()
        self.select_yellow()
        self.select_green()
        self.select_blue()
        self.select_violet()
        self.click_affirm()
        #点击红包
        self.click_red_packet()
        self.input_red_packet_number(1000)
        self.input_red_packet_money(1000)
        self.input_red_packet_remark('你好')
        self.red_packet_page_click_back()
        #点击文件
        self.click_file()
        self.select_folder()
        self.select_file()
        self.file_page_click_confirm()

    def Case_run3(self):
        self.more_page_enter_user_details()
        #添加一个用户
        self.click_add_user()
        self.select_add_user()
        self.click_confirm()
        #删除一个用户
        self.click_delete_user()
        self.delete_page_click_compile()
        self.select_delete_user()
        self.delete_page_click_confirm()
        print(self.acquire_personnel_number())
        print(self.avquire_group_name_status())
        #点击群聊名称
        self.click_group_name()
        self.set_group_name()
        self.update_group_name()
        self.add_contact_accomplish()
        #点击群二维码
        self.click_group_code()
        self.group_code_page_click_more()
        self.group_code_save_phone()
        self.group_chat_page_back()
        #点击群公告
        self.click_group_message()
        self.set_group_message('你好')
        self.common_click_accomplish()

        #点击我在 本群的名称
        self.click_my_name_in_the_group()
        self.set_my_name_in_the_gtoup('你好')
        self.add_contact_accomplish()
        #点击免打扰
        self.click_message_disturbing()
        #点击置顶聊天
        self.stick_chat()
        self.d.swipe(0.553, 0.769, 0.507, 0.329)
        #点击群聊文件
        self.click_chat_file()
        self.group_chat_page_back()
        self.d.swipe(0.553,0.769,0.507,0.329)
        #点击清空聊天记录
        self.click_clear_message()
        self.clear_message_pop_up()
        #点击退出按钮
        self.click_chat_window()
        self.more_page_enter_user_details()
        self.d.swipe(0.553, 0.769, 0.507, 0.329)
        self.click_quit()







    '''
    组合操作结束
    '''

