import uiautomator2 as u2
from src.nictalk import *
from src.camtalk import *
class Factory_Pattern():

    def __init__(self,d):
        self.d = d
        self.talk = None

    def set_up(self):
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        nictalk = NicTalk(self.d)
        camtalk = CamTalk(self.d)
        nictalk.stop()
        camtalk.stop()
        nictalk.start()
        camtalk.start()
        current = self.d.current_app()
        if current['package'] == "com.nictalk.start":
            self.talk = nictalk
        elif current['package'] == "com.camtalk.start":
            self.talk = camtalk

    def start(self):
        '''
        直接启动原生态安卓拨号盘，进入工厂模式
        :return:
        '''
        self.d.app_stop("com.android.dialer")
        self.d.app_start("com.android.dialer",activity="com.android.dialer.DialtactsActivity")
        if self.d(resourceId="com.android.dialer:id/floating_action_button").wait(timeout=1):
            self.d(resourceId="com.android.dialer:id/floating_action_button").click()
        number = "000000*"
        for i in number:
            self.d(resourceId="com.android.dialer:id/dialpad_key_number", text=i).click()



    def enter_facrory_pattern(self):
        '''
        进入工厂模式界面
        :return:
        '''
        self.talk.click_calls()
        self.talk.input_phone_number('000000lg')
        if self.d(resourceId="com.android.dialer:id/floating_action_button").wait(timeout=3)==True:
            self.d(resourceId="com.android.dialer:id/floating_action_button").click()
        self.talk.android_input_phone_number('000000*')

    def wait_facrory_pattern(self):
        '''
        判断是否进入工厂模式
        :return:
        '''

        if self.d(text=u"工厂测试").wait(timeout=3) and self.d(description=u"更多选项").wait(timeout=1)==True:
            print('正常进入工厂模式')
            return True
        else:
            self.d.press("back")


    def enter_log(self):
        '''
        进入log菜单
        :return:
        '''
        print('开始寻找：获取AP日志(该项不测试)')
        while True:
            if self.d(resourceId="com.qti.factory:id/text_center", text=u"获取AP日志(该项不测试)").wait(timeout=3)==True:
                self.d(resourceId="com.qti.factory:id/text_center", text=u"获取AP日志(该项不测试)").click()
                break
            else:
                self.d.swipe(0.729, 0.8, 0.808, 0.095)


    def mcwill_msg(self):
        '''
        进入log菜单
        :return:
        '''
        print('>>>>>>>>>> 开始获取Mcwill信息\n开始寻找：McWill信息')
        while True:
            if self.d(text=u"工厂测试").wait(timeout=2):
                if self.d(resourceId="com.qti.factory:id/text_center", text=u"McWiLL信息").wait(timeout=2):
                    self.d(resourceId="com.qti.factory:id/text_center", text=u"McWiLL信息").click()
                    break
                elif self.d(resourceId="com.qti.factory:id/text_center", text=u"McWiLL复位(该项不测试)").wait(timeout=2)==True:
                    for i in range(10):
                        self.d.swipe(0.729, 0.2, 0.808, 0.8)
                else:
                    self.d.swipe(0.729, 0.8, 0.808, 0.3)
            elif self.d(text=u"McWiLL信息"):
                break
            else:
                self.d.press("back")
        if self.d(text=u"McWiLL信息"):
            if self.d(resourceId="com.qti.factory:id/text_pid").wait(timeout=1):
                msg = self.d(resourceId="com.qti.factory:id/text_pid").get_text()
                mcu = self.d(resourceId="com.qti.factory:id/mcu_info").get_text()
                mca = self.d(resourceId="com.qti.factory:id/mac_address").get_text()

            else:
                msg = "WcWill信息为空\n"
                if self.d(resourceId="com.qti.factory:id/mcu_info").wait(timeout=1):
                    mcu = self.d(resourceId="com.qti.factory:id/mcu_info").get_text()
                else:
                    mcu = "信息为空"

                if self.d(resourceId="com.qti.factory:id/mac_address").wait(timeout=1):
                    mca = self.d(resourceId="com.qti.factory:id/mac_address").get_text()
                else:
                    mca = "信息为空"
            msg = msg+"MCU信息：%s\nMAC地址：%s\n\n" % (mcu, mca)
            self.d.press("back")
            return True,msg
        else:
            msg = ">>>>>>>>>> 获取Mcwill信息失败"
            print(msg)
            return False,msg

    def mcwill_restoration(self):
        '''
        进入log菜单
        :return:
        '''
        print('>>>>>>>>>> 进行McWill复位\n开始寻找：McWill复位')
        while True:
            if self.d(text=u"工厂测试").wait(timeout=2):
                if self.d(resourceId="com.qti.factory:id/text_center", text=u"McWiLL复位(该项不测试)").wait(timeout=2):
                    self.d(resourceId="com.qti.factory:id/text_center", text=u"McWiLL复位(该项不测试)").click()
                    break
                else:
                    self.d.swipe(0.729, 0.8, 0.808, 0.3)
            elif self.d(text=u"McWiLL复位(该项不测试)"):
                break
            else:
                self.d.press("back")
        if self.d(text=u"McWiLL复位(该项不测试)").wait(timeout=1) and self.d(resourceId="com.qti.factory:id/reset").wait(timeout=1):
            print('>>>>>>>>>> 点击：McWiLL复位(该项不测试)')
            self.d(resourceId="com.qti.factory:id/reset").click()
            self.d.press("back")
            print('>>>>>>>>>> McWill复位完成')
            return True
        else:
            msg = ">>>>>>>>>> McWill复位失败"
            print(msg)
            return False



    def start_log(self):
        print('>>>>>>>>>>开启日志')
        if self.d(resourceId="com.qti.factory:id/catch_switch").get_text()=='关闭':
            self.d(resourceId="com.qti.factory:id/catch_switch").click()
        self.d(resourceId="com.qti.factory:id/rb_log_at").click()
        self.d.press("home")

    def start_log_run(self):
        self.set_up()
        self.enter_facrory_pattern()
        self.wait_facrory_pattern()
        self.enter_log()
        self.start_log()





