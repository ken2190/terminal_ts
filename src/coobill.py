import uiautomator2 as u2
import time

class KHM_CooBill():

    def __init__(self,d):
        self.d=d

    '''
    开启关闭和登录的操作
    '''

    def start_coobill(self):
        print('---------->开启coobill')
        self.d.app_start(pkg_name='com.mcwill.coopay',activity='.ui._new.SplashActivity')
        time.sleep(2)

    def stop_coobill(self):
        print('---------->关闭coobill')
        self.d.app_stop(pkg_name='com.mcwill.coopay')


    '''
    下面是登录界面的操作
    '''



    def select_state(self,state='柬埔寨'):
        time.sleep(2)
        self.d.set_fastinput_ime(True)
        print('---------->点击选择国家')
        self.d(resourceId="com.mcwill.coopay:id/countryName").click()
        print('---------->点击搜索')
        self.d(resourceId="android:id/search_button").click()
        print('---------->输入国家')
        self.d(resourceId="android:id/search_src_text").click()
        self.d.send_keys(state)
        print('---------->点击选择国家')
        self.d(resourceId="com.mcwill.coopay:id/countryName",text=state).click()
        time.sleep(2)

    def input_user_pw(self,us=383097143,pw=123456):
        self.d.set_fastinput_ime(True)
        print('---------->输入账号')
        self.d(resourceId="com.mcwill.coopay:id/phoneNumber").set_text(us)
        time.sleep(2)
        print('---------->输入密码')
        self.d(resourceId="com.mcwill.coopay:id/password").set_text(pw)

    def click_login(self):
        print('---------->点击确认登录')
        self.d(resourceId="com.mcwill.coopay:id/toLogIn").click()
        time.sleep(2)


    '''
    开启并登录的组合
    '''

    def start_and_login(self):
        self.start_coobill()
        if self.wait_first_page()==True:
            print('---------->已经登录')
        else:
            self.select_state()
            self.input_user_pw()
            self.click_login()
            for i in range(0,10):
                self.pop_up()
                if self.wait_first_page() == True:
                    print('---------->已经登录')
                    break
                else:
                    time.sleep(10)
            if self.wait_first_page() == False:
                print('登录失败')
                return False


    '''
    下面是首页面的操作
    '''

    def wait_first_page(self):
        print('---------->判断首页面是否出现')
        return self.d(text=u"CooBill").wait(timeout=3)

    def click_transfer_accounts(self):
        print('---------->点击转账按钮')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"转账").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/batText", text='转账').wait(timeout=300) == True:
            return True
        else:
            return '进入转账界面出现异常'

    def click_select_balance(self):
        print('---------->点击余额查询按钮')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"余额查询").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/batText", text='余额查询').wait(timeout=300) == True:
            return True
        else:
            return '进入余额查询界面出现异常'

    def click_request_payment(self):
        print('---------->点击请求支付按钮')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"请求支付").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/batText", text='请求支付').wait(timeout=300) == True:
            return True
        else:
            return '进入请求支付界面出现异常'

    def click_recharge(self):
        print('---------->点击充值按钮')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"充值").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/batText",text='充值').wait(timeout=300)==True:
            return True
        else:
            return '进入充值界面出现异常'

    def click_scan_code(self):
        print('---------->点击扫描二维码')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"二维码").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/batText",text='二维码').wait(timeout=300)==True:
            return True
        else:
            return '进入二维码界面出现异常'

    def click_set(self):
        print('---------->点击设置')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"设置").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/batText",text='设置').wait(timeout=300)==True:
            return True
        else:
            return '进入设置界面出现异常'

    def click_payment(self):
        print('---------->点击支付好友')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"支付好友").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/batText",text='支付好友').wait(timeout=300)==True:
            return True
        else:
            return '进入支付好友界面出现异常'

    def click_exchange_record(self):
        print('---------->点击交易记录')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"交易记录").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/batText",text='现金账户记录').wait(timeout=300)==True:
            return True
        else:
            return '进入现金账户记录界面出现异常'

    def click_integral(self):
        print('---------->点击购买积分')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"购买积分").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/batText",text='购买积分').wait(timeout=300)==True:
            return True
        else:
            return '进入购买积分界面出现异常'

    def click_shift_to(self):
        print('---------->点击转入')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"转入").click()
        toast=self.d.toast.get_message(5.0, 10.0)
        if toast != '请先完成实名认证':
            if self.d(resourceId="com.mcwill.coopay:id/batText", text='转入').wait(timeout=300) == True:
                self.back()
                return True

            else:
                return '进入转入界面出现异常'
        else:
            return toast

    def click_shift_out(self):
        print('---------->点击转出')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"转出").click()
        toast = self.d.toast.get_message(5.0, 10.0)
        if toast != '请先完成实名认证':
            if self.d(resourceId="com.mcwill.coopay:id/batText", text='转出').wait(timeout=300) == True:
                self.back()
                return True
            else:
                return '进入转出界面出现异常'
        else:
            return toast

    def click_more(self):
        print('---------->点击更多')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"更多").click()


    '''
    下面是设置界面的操作
    '''

    def set_click_autonym(self):
        print('----->点击设置界面的实名认证')
        if self.d(resourceId="com.mcwill.coopay:id/status").wait(timeout=300)==True:
            print('----->已认证')
            return True
        else:
            self.d(resourceId="com.mcwill.coopay:id/itemText",text='实名认证').click()
            if self.d(resourceId="com.mcwill.coopay:id/batText", text='身份认证').wait(timeout=100) == True:
                return True
            else:
                return '----->没有进入实名认证界面'

    def set_click_language(self):
        print('----->点击设置界面的语言选择/Language')
        self.d(resourceId="com.mcwill.coopay:id/itemText", text='语言选择/Language').click()
        if self.d(resourceId="com.mcwill.coopay:id/batText",text='语言选择').wait(timeout=100)==True:
            return True
        else:
            return '----->没有进入语言选择界面'

    def set_click_password(self):
        print('----->点击设置界面的密码管理')
        self.d(resourceId="com.mcwill.coopay:id/itemText", text='密码管理').click()
        if self.d(resourceId="com.mcwill.coopay:id/batText",text='密码管理').wait(timeout=100)==True:
            return True
        else:
            return '----->没有进入密码管理界面'

    def set_click_facility(self):
        print('----->点击设置界面的设备管理')
        self.d(resourceId="com.mcwill.coopay:id/itemText", text='设备管理').click()
        if self.d(resourceId="com.mcwill.coopay:id/batText", text='设备管理').wait(timeout=100) == True:
            return True
        else:
            return '----->没有进入设备管理界面'

    def set_click_versions(self):
        print('----->点击设置界面的版本信息')
        self.d(resourceId="com.mcwill.coopay:id/itemText", text=u"版本信息").click()
        if self.d(resourceId="com.mcwill.coopay:id/title", text=u"版本信息").wait(timeout=100):
            return True
        else:
            return '----->没有进入版本信息界面'

    def set_click_stop(self):
        print('----->点击设置界面的退出账户')
        self.d(resourceId="com.mcwill.coopay:id/itemText", text='退出账户').click()
        if self.pop_up()==True:
            return True
        else:
            return '----->点击退出账户失败，没有弹框确认'


    '''
    下面是对于弹框的操作
    '''

    def pop_up(self,operation='取消'):
        '''
        处理弹框，默认操作为点击取消
        :param operation:选择操作：取消 确认
        :return:
        '''
        print('---------->处理弹框')
        if self.d(resourceId="com.mcwill.coopay:id/alertTitle").wait(timeout=30)==True:
            if operation=='取消':
                self.d(resourceId="com.mcwill.coopay:id/button2").click()
            else:
                self.d(resourceId="com.mcwill.coopay:id/button1").click()
            return True
        else:
            return False



    '''
    下面是拖动的操作
    '''

    def up_drag_page(self):
        '''
        在coobill界面，向上拖动
        :return:
        '''
        print('>>>>>>>>>>向上拖动')
        self.d.swipe(0.329,0.723,0.331,0.531)

    def down_drag_page(self):
        '''
        在coobill界面，向下拖动
        :return:
        '''
        print('>>>>>>>>>>向下拖动')
        self.d.swipe(0.331,0.531,0.329,0.723)

    '''
    下面是返回的操作
    '''

    def back(self):
        print('>>>>>>>>>>点击返回')
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/back").wait(timeout=30)==True:
            self.d(resourceId="com.mcwill.coopay:id/back").click()
        time.sleep(3)

    def accomplish(self):
        print('>>>>>>>>>>点击完成')
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/titlebar_complete").wait(timeout=30)==True:
            self.d(resourceId="com.mcwill.coopay:id/titlebar_complete").clilck()
        time.sleep(3)



    '''
    下面是组合操作
    '''

    def first_page_operation(self):
        '''
        首页的组合操作
        :return:
        '''
        result_message=''
        transfer_accounts = self.click_transfer_accounts()
        if transfer_accounts != True:
            result_message = result_message + transfer_accounts
        self.back()
        select_balance = self.click_select_balance()
        if select_balance != True:
            result_message = result_message + select_balance
        self.back()
        request_payment = self.click_request_payment()
        if request_payment != True:
            result_message = result_message + request_payment
        self.back()
        recharge = self.click_recharge()
        if recharge != True:
            result_message = result_message + recharge
        self.back()
        scan_code = self.click_scan_code()
        if scan_code != True:
            result_message = result_message + scan_code
        self.back()
        set = self.click_set()
        if set != True:
            result_message = result_message + set
        self.back()
        payment = self.click_payment()
        if payment != True:
            result_message = result_message + payment
        self.back()
        exchange_record = self.click_exchange_record()
        if exchange_record != True:
            result_message = result_message + exchange_record
        self.back()
        integral = self.click_integral()
        if integral != True:
            result_message = result_message + integral
        self.back()
        self.up_drag_page()
        shift_to = self.click_shift_to()
        if shift_to != True:
            result_message = result_message + shift_to
        shift_out = self.click_shift_out()
        if shift_out != True:
            result_message = result_message + shift_out
        self.down_drag_page()
        return result_message

    def set_page_operation(self):
        '''
        设置页面的操作
        :return:
        '''
        result_message=''
        autonym = self.set_click_autonym()
        print(autonym)
        if autonym != True:
            result_message = result_message + autonym
        self.accomplish()
        language = self.set_click_language()
        if language != True:
            result_message = result_message + language
        self.back()
        password = self.set_click_password()
        if password != True:
            result_message = result_message + password
        self.back()
        facility = self.set_click_facility()
        if facility != True:
            result_message = result_message + facility
        self.back()
        versions = self.set_click_versions()
        if versions != True:
            result_message = result_message + versions
        self.back()
        stop = self.set_click_stop()
        if stop != True:
            result_message = result_message + stop
        self.back()
        return result_message

    def Case_all_operation(self):
        result_message=''
        self.start_and_login()
        time.sleep(3)
        result_message=result_message+self.first_page_operation()
        time.sleep(5)
        self.click_set()
        time.sleep(2)
        result_message = result_message +self.set_page_operation()
        time.sleep(2)
        self.stop_coobill()
        return result_message


class NCA_CooBill():

    def __init__(self,d):
        self.d=d

    '''
    开启关闭和登录的操作
    '''

    def start_coobill(self):
        print('---------->开启coobill')
        self.d.app_start(pkg_name='com.mcwill.coopay',activity='.ui._new.SplashActivity')
        time.sleep(2)

    def stop_coobill(self):
        print('---------->关闭coobill')
        self.d.app_stop(pkg_name='com.mcwill.coopay')

    '''
    下面是登录界面的操作
    '''

    def wait_login(self):
        print('开启后的登录按钮')
        if self.d(resourceId="com.mcwill.coopay:id/act_splash_sign_in").wait(timeout=3)==True:
            self.d(resourceId="com.mcwill.coopay:id/act_splash_sign_in").click()

    def select_state(self,state='柬埔寨'):
        time.sleep(2)
        self.d.set_fastinput_ime(True)
        print('---------->点击选择国家')
        self.d(resourceId="com.mcwill.coopay:id/toSelectCountryCode").click()
        print('---------->输入国家')
        self.d(resourceId="com.mcwill.coopay:id/searchView").click()
        self.d.send_keys(state)
        print('---------->点击选择国家')
        self.d(resourceId="com.mcwill.coopay:id/countryName",text=state).click()
        time.sleep(2)

    def input_user_pw(self,us=383097143,pw=123456):
        self.d.set_fastinput_ime(True)
        print('---------->输入账号')
        self.d(resourceId="com.mcwill.coopay:id/phoneNumber").set_text(us)
        time.sleep(2)
        print('---------->输入密码')
        self.d(resourceId="com.mcwill.coopay:id/password").set_text(pw)

    def click_login(self):
        print('---------->点击确认登录')
        self.d(resourceId="com.mcwill.coopay:id/toLogIn").click()
        time.sleep(2)


    '''
    开启并登录的组合
    '''

    def start_and_login(self):
        self.start_coobill()
        self.wait_login()
        if self.wait_first_page()==True:
            print('---------->已经登录')
        else:
            self.select_state()
            self.input_user_pw()
            self.click_login()
            for i in range(0,10):
                self.pop_up()
                if self.wait_first_page() == True:
                    print('---------->已经登录')
                    break
                else:
                    time.sleep(10)
            if self.wait_first_page() == False:
                print('登录失败')
                return False



    '''
    下面是首页面的操作
    '''

    def wait_first_page(self):
        print('---------->判断首页面是否出现')
        return self.d(resourceId="com.mcwill.coopay:id/tv_userName").wait(timeout=3)

    def click_scan_code(self):
        print('---------->点击扫一扫')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"扫一扫").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/btn_switch").wait(timeout=300)==True:
            return True
        else:
            return '进入扫一扫界面出现异常'

    def click_gathering_code(self):
        print('---------->点击收款码')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"收款码").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/title",text='收款码').wait(timeout=300) == True:
            return True
        else:
            return '进入收款码界面出现异常'

    def click_transfer_accounts(self):
        print('---------->点击转账按钮')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"转账").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/title", text='转账').wait(timeout=300) == True:
            return True
        else:
            return '进入转账界面出现异常'

    def click_select_balance(self):
        print('---------->点击余额查询按钮')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"余额").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/title", text='账户查询').wait(timeout=300) == True:
            return True
        else:
            return '进入余额查询界面出现异常'

    def click_exchange_record(self):
        print('---------->点击交易记录')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"交易记录").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/title",text='现金账户记录').wait(timeout=300)==True:
            return True
        else:
            return '进入现金账户记录界面出现异常'

    def click_recharge(self):
        print('---------->点击充值按钮')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"话费充值").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/title", text='选择充值类型').wait(timeout=300) == True:
            return True
        else:
            return '进入充值界面出现异常'

    def click_payment(self):
        print('---------->点击联系人')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"联系人").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/title",text='选择联系人').wait(timeout=300)==True:
            return True
        else:
            return '进入联系人界面出现异常'

    def click_exchange_tate(self):
        print('---------->点击汇率转换按钮')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"汇率转换").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/title",text=u"汇率").wait(timeout=300) == True:
            return True
        else:
            return '进入汇率转换界面出现异常'

    def click_set(self):
        print('---------->点击设置')
        self.d(resourceId="com.mcwill.coopay:id/text", text=u"设置").click()
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/title",text='设置').wait(timeout=300)==True:
            return True
        else:
            return '进入设置界面出现异常'

    '''
       下面是设置界面的操作
       '''

    def set_click_facility(self):
        print('----->点击设置界面的设备管理')
        self.d(resourceId="com.mcwill.coopay:id/itemText",text='设备管理').click()
        if self.d(resourceId="com.mcwill.coopay:id/title", text='设备管理').wait(timeout=200) == True:
            return True
        else:
            return '----->没有进入设备管理界面'

    def set_click_password(self):
        print('----->点击设置界面的密码管理')
        self.d(resourceId="com.mcwill.coopay:id/itemText", text=u"密码管理").click()
        if self.d(resourceId="com.mcwill.coopay:id/title", text='密码管理').wait(timeout=200) == True:
            return True
        else:
            return '----->没有进入密码管理界面'

    def set_click_language(self):
        print('----->点击设置界面的语言选择/Language')
        self.d(resourceId="com.mcwill.coopay:id/itemText", text=u"语言选择/Language").click()
        if self.d(resourceId="com.mcwill.coopay:id/title", text='语言选择').wait(timeout=200) == True:
            return True
        else:
            return '----->没有进入语言选择界面'

    def set_click_clear_cache(self):
        print('----->点击设置界面的清除缓存缓存')
        self.d(resourceId="com.mcwill.coopay:id/itemText", text=u"清除缓存").click()

    def set_click_versions(self):
        print('----->点击设置界面的版本信息')
        self.d(resourceId="com.mcwill.coopay:id/itemText", text=u"版本信息").click()
        if self.d(resourceId="com.mcwill.coopay:id/title", text='版本信息').wait(timeout=100) == True:
            return True
        else:
            return '----->没有进入版本信息界面'

    def set_click_stop(self):
        print('----->点击设置界面的退出账户')
        self.d(resourceId="com.mcwill.coopay:id/logOut", text='退出账户').click()
        if self.pop_up() == True:
            return True
        else:
            return '----->点击退出账户失败，没有弹框确认'


    '''
    下面是返回的操作
    '''

    def back(self):
        print('>>>>>>>>>>点击返回')
        time.sleep(3)
        if self.d(resourceId="com.mcwill.coopay:id/title_back").wait(timeout=30) == True:
            self.d(resourceId="com.mcwill.coopay:id/title_back").click()

        time.sleep(3)

    '''
    下面是对于弹框的操作
    '''

    def pop_up(self,operation='取消'):
        '''
        处理弹框，默认操作为点击取消
        :param operation:选择操作：取消 确认
        :return:
        '''
        print('---------->处理弹框')
        if self.d(resourceId="com.mcwill.coopay:id/alertTitle").wait(timeout=30)==True:
            if operation=='取消':
                self.d(resourceId="com.mcwill.coopay:id/button2").click()
            else:
                self.d(resourceId="com.mcwill.coopay:id/button1").click()
            return True
        else:
            return False


    '''
    下面是组合操作
    '''

    def first_page_operation(self):
        '''
        首页的组合操作
        :return:
        '''
        result_message=''
        scan_code=self.click_scan_code()
        if scan_code!=True:
            result_message=result_message+scan_code+'\n'
        self.back()
        gathering_code=self.click_gathering_code()
        if gathering_code!=True:
            result_message=result_message+gathering_code+'\n'
        self.back()
        transfer_accounts=self.click_transfer_accounts()
        if transfer_accounts!=True:
            result_message=result_message+transfer_accounts+'\n'
        self.back()
        select_balance=self.click_select_balance()
        if select_balance!=True:
            result_message=result_message+select_balance+'\n'
        self.back()
        exchange_record=self.click_exchange_record()
        if exchange_record!=True:
            result_message=result_message+exchange_record+'\n'
        self.back()
        recharge=self.click_recharge()
        if recharge!=True:
            result_message=result_message+recharge+'\n'
        self.back()
        payment=self.click_payment()
        if payment!=True:
            result_message=result_message+payment+'\n'
        self.back()
        exchange_tate=self.click_exchange_tate()
        if exchange_tate!=True:
            result_message=result_message+exchange_tate+'\n'
        self.back()
        set=self.click_set()
        if set!=True:
            result_message=result_message+set+'\n'
        self.back()
        return result_message

    def set_page_operation(self):
        '''
        设置页面的操作
        :return:
        '''
        result_message=''
        facility=self.set_click_facility()
        if facility != True:
            result_message = result_message + facility + '\n'
        self.back()
        password=self.set_click_password()
        if password != True:
            result_message = result_message + password + '\n'
        self.back()
        language=self.set_click_language()
        if language != True:
            result_message = result_message + language + '\n'
        self.back()
        self.set_click_clear_cache()
        versions=self.set_click_versions()
        if versions != True:
            result_message = result_message + versions + '\n'
        self.back()
        stop=self.set_click_stop()
        if stop != True:
            result_message = result_message + stop + '\n'
        self.back()
        return result_message

    def Case_all_operation(self):
        result_message=''
        self.start_and_login()
        time.sleep(3)
        self.click_set()
        time.sleep(2)
        result_message = result_message + self.set_page_operation()
        time.sleep(5)
        result_message = result_message + self.first_page_operation()
        time.sleep(2)
        self.stop_coobill()
        return result_message




if __name__=='__main__':
    d=u2.connect()
    a=KHM_CooBill(d)
