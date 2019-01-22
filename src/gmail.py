import uiautomator2 as u2
import time
from src.general import image_comparison
from src.settings import Settings
from src.general import get_config as config


class Gmail():

    def __init__(self,d):
        self.d = d
        self.path = image_comparison.get_path()
        self.settings = Settings(d)
        self.name = config.get_config("GMAIL", "name")
        self.password = config.get_config("GMAIL", "password")


    def __sleep(func):
        def inner(self):
            time.sleep(1)
            self.d.screen_on()
            return func(self)
        return inner

    @__sleep
    def start(self):
        print(">>>>>>>>>>>>>>>>> 启动apk: Gmail")
        self.d.app_start("com.google.android.gm")

    @__sleep
    def stop(self):
        print(">>>>>>>>>>>>>>>>> 停止apk: Gmail")
        self.d.app_stop("com.google.android.gm")


    '''
    以下为启动页
    '''

    @__sleep
    def got_it(self):
        print(">>>>>>>>>>>>>>>>> Gmail启动界面：点击知道了")
        self.d(resourceId="com.google.android.gm:id/welcome_tour_got_it").click()

    @__sleep
    def click_addresses(self):
        print(">>>>>>>>>>>>>>>>> Gmail启动界面：点击添加电子邮件地址")
        self.d(resourceId="com.google.android.gm:id/setup_addresses_add_another").click()


    @__sleep
    def goto_gmail(self):
        print(">>>>>>>>>>>>>>>>> Gmail启动界面：点击转至 Gmail")
        self.d(resourceId="com.google.android.gm:id/action_done").click()

    def goto_addGoogle(self):
        self.d(resourceId="com.google.android.gm:id/account_setup_label", text=u"Google").click()   # 点击Google





    '''
    以下为已登录邮箱的个人邮箱界面
    '''

    @__sleep
    def write_gmail(self):
        print(">>>>>>>>>>>>>>>>> Gmail 个人首页：点击写邮箱")
        self.d(resourceId="com.google.android.gm:id/compose_button").click()


    @__sleep
    def navbar(self):
        if self.d(resourceId="com.google.android.gm:id/conversation_tip_text",text=u"帐号同步设置已关闭。请在帐号设置中开启。").wait(timeout=2):
            self.d.swipe(0.5, 0.3, 0.5, 0.8)
            time.sleep(5)
        if self.d(description=u"打开抽屉式导航栏").wait(timeout=5):
            print(">>>>>>>>>>>>>>>>> Gmail 个人首页：点击导航栏")
            self.d(description=u"打开抽屉式导航栏").click()

    @__sleep
    def search(self):
        print(">>>>>>>>>>>>>>>>> Gmail 个人首页：点击查询")
        self.d(resourceId="com.google.android.gm:id/search").click()


    '''
    以下为导航栏详情界面
    '''
    def inbox(self):
        print(">>>>>>>>>>>>>>>>> Gmail 导航栏：点击收件箱")
        self.d(resourceId="com.google.android.gm:id/name", text=u"收件箱").click()

    def unread(self):
        print(">>>>>>>>>>>>>>>>> Gmail 导航栏：点击未读")
        self.d(resourceId="com.google.android.gm:id/name", text=u"未读").click()

    def asterisk(self):
        print(">>>>>>>>>>>>>>>>> Gmail 导航栏：点击已加星标")
        self.d(resourceId="com.google.android.gm:id/name", text=u"已加星标").click()

    def delayed(self):
        print(">>>>>>>>>>>>>>>>> Gmail 导航栏：点击已延后")
        self.d(resourceId="com.google.android.gm:id/name", text=u"已延后").click()

    def importance(self):
        print(">>>>>>>>>>>>>>>>> Gmail 导航栏：点击重要邮件")
        self.d(resourceId="com.google.android.gm:id/name", text=u"重要邮件").click()

    def sent(self):
        print(">>>>>>>>>>>>>>>>> Gmail 导航栏：点击已发邮件")
        self.d(resourceId="com.google.android.gm:id/name", text=u"已发邮件").click()

    def outbox(self):
        print(">>>>>>>>>>>>>>>>> Gmail 导航栏：点击发件箱")
        self.d(resourceId="com.google.android.gm:id/name", text=u"发件箱").click()

    def draft(self):
        print(">>>>>>>>>>>>>>>>> Gmail 导航栏：点击草稿")
        self.d(resourceId="com.google.android.gm:id/name", text=u"草稿").click()




    '''
    以下为已登录邮箱的 写邮箱界面
    '''

    @__sleep
    def gmail_click_pop(self):
        if self.d(resourceId="android:id/button1").wait(timeout=2):
            print(">>>>>>>>>>>>>>>>> Gmail 写邮件：点击弹框")
            self.d(resourceId="android:id/button1").click()
        else:
            pass

    @__sleep
    def gmail_add_addressee(self, addressee="Strongboxman@gmail.com"):
        print(">>>>>>>>>>>>>>>>> Gmail 写邮件：输入收件人")
        self.d(resourceId="com.google.android.gm:id/to").set_text(addressee)


    def gmail_add_subject(self, subject="测试邮件主题"):
        print(">>>>>>>>>>>>>>>>> Gmail 写邮件：输入主题")
        self.d(resourceId="com.google.android.gm:id/subject").set_text(subject)

    def gmail_add_details(self, details="测试邮件内容"):
        print(">>>>>>>>>>>>>>>>> Gmail 写邮件：输入内容")
        self.d(description=u"撰写电子邮件").set_text(details)


    @__sleep
    def gmail_attachment(self):
        print(">>>>>>>>>>>>>>>>> Gmail 写邮件：点击附件")
        self.d(resourceId="com.google.android.gm:id/add_attachment").click()

    @__sleep
    def gmail_add_attachment(self):
        print(">>>>>>>>>>>>>>>>> Gmail 写邮件：选择添加附件")
        self.d(resourceId="com.google.android.gm:id/title", text=u"添加附件").click()

    @__sleep
    def gmail_send(self):
        print(">>>>>>>>>>>>>>>>> Gmail 写邮件：点击发送")
        self.d(resourceId="com.google.android.gm:id/send").click()

    '''
    以下为打开附件后进入的打开文件界面
    '''

    @__sleep
    def attachment_open_file(self):
        print(">>>>>>>>>>>>>>>>> Gmail 添加附件：最近附件")
        if self.d(description=u"显示根目录").wait(timeout=2):
            self.d(description=u"显示根目录").click()
        self.d(resourceId="android:id/title", text=u"最近").click()                       # 打开文件界面，选择 最近
        if self.d(resourceId="android:id/empty",text=u"无任何文件").wait(timeout=2):
            print("最近 目录中无任何文件\n切换到图片，选择一张图片")
            self.d(description=u"显示根目录").click()
            if self.d(resourceId="android:id/title", text=u"图片").wait(timeout=2):
                self.d(resourceId="android:id/title", text=u"图片").click()
                time.sleep(1)
                self.d(className="android.widget.ImageView", instance=3).click()
                time.sleep(1)
                self.d(className="android.widget.ImageView", instance=2).click()
            elif self.d(resourceId="android:id/title", text=u"图库").wait(timeout=2):
                self.d(resourceId="android:id/title", text=u"图库").click()
                time.sleep(2)
                self.d.click(0.125, 0.185)
                time.sleep(1)
                self.d.click(0.149, 0.189)
        else:
            time.sleep(1)
            self.d(resourceId="android:id/title")[0].click()               # 选择最近的第一个文件


    '''
    以下为其他检测
    '''

    def check_outbox(self):
        print(">>>>>>>>>>>>>>>>> 检测发件箱是否有未发送的邮件 ")
        if not(self.d(text=u"发件箱").wait(timeout=1)):
            self.navbar()
            self.outbox()
        if self.d(resourceId="com.google.android.gm:id/empty_text").wait(timeout=1):
            if self.d(resourceId="com.google.android.gm:id/empty_text").get_text() == '“发件箱”中没有任何内容':
                return True
            else:
                return False
        else:
            return False


    def get_unread(self):
        if not(self.d(resourceId="com.google.android.gm:id/unread").wait(timeout=2)):
            self.navbar()
        print(">>>>>>>>>>>>>>>>> 获取未读邮件的个数")
        number = self.d(resourceId="com.google.android.gm:id/unread").get_text()
        self.d.press("back")
        return number


    def detection_got_it(self):
        print(">>>>>>>>>>>>>>>>> Gmail检测是否已登录用户 ")
        if self.d(text=u"主要").wait(timeout=2.0) or self.d(resourceId="com.google.android.gm:id/compose_button").wait(timeout=2):
            print(">已登录邮箱")
            return True
        else :
            self.got_it()
            time.sleep(1)
            if self.d(resourceId="com.google.android.gm:id/account_address").wait(timeout=2):
                self.d(resourceId="com.google.android.gm:id/action_done").click()
                if self.d(text=u"主要").wait(timeout=2.0) or self.d(resourceId="com.google.android.gm:id/compose_button").wait(timeout=2):
                    print(">>已登录邮箱")
                    return True
            else:
                print("未登录邮箱")
                return False


    '''
    自动登录固定账户与密码
    '''

    def add_google_gmail(self):
        gmail_address = self.name
        gmail_password = self.password
        if self.d(resourceId="identifierId").wait(timeout=30):
            self.d(resourceId="identifierId").set_text(gmail_address)
            if self.d(resourceId="com.kikaoem.qisiemoji.inputmethod:id/keyboard_view").wait(timeout=1):
                self.d.press("back")
            time.sleep(1)
            self.d(resourceId="identifierNext").click()
            time.sleep(3)
            if not(self.d(text=u"输入您的密码").wait(timeout = 2)):
                self.d(resourceId="identifierNext").click()
            self.d(text=u"输入您的密码").set_text(gmail_password)
            if self.d(resourceId="com.kikaoem.qisiemoji.inputmethod:id/keyboard_view").wait(timeout=1):
                self.d.press("back")
            time.sleep(1)
            self.d(resourceId="passwordNext").click()
            self.d(resourceId="signinconsentNext").click()

            time.sleep(5)
            if self.d(resourceId="com.google.android.gms:id/suw_navbar_more").wait(timeout=180):
                self.d(resourceId="com.google.android.gms:id/suw_navbar_more").click()
                self.d(resourceId="com.google.android.gms:id/suw_navbar_next").click()
                for i in range(6):
                    if self.d(resourceId="com.google.android.gm:id/account_address").wait(timeout=1):
                        self.goto_gmail()
                        return True
                    else:
                        time.sleep(5)
        else :
            print("连接google服务异常")
            return False


    '''
    自动添加google账户
    '''

    def add_oth_addresses(self):
        print(">>>>>>>>>>>>>>>>> Gmail设置电子邮件：添加 google 电子邮件地址")
        self.click_addresses()
        time.sleep(2)
        self.goto_addGoogle()
        # 判断是否有网络连接
        while True:
            if self.d(resourceId="com.google.android.gms:id/suw_layout_title").wait(timeout=1):
                text = self.d(resourceId="com.google.android.gms:id/suw_layout_title").get_text()
                if text == "无法登录":
                    self.d(resourceId="com.google.android.gms:id/suw_navbar_next").click()
                    self.goto_addGoogle()
                    if self.d(resourceId="com.google.android.gms:id/suw_layout_title").wait(timeout=3):
                        text2 = self.d(resourceId="com.google.android.gms:id/suw_layout_title").get_text()
                        if text2 == '正在核对信息…':
                            time.sleep(3)
                        else:
                            return False
                    elif self.d(resourceId="identifierId").wait(timeout=1):
                        if self.add_google_gmail():
                            return True
                        else:
                            return False
                elif text == '正在核对信息…':
                    time.sleep(3)
            elif self.d(resourceId="identifierId").wait(timeout=1):
                if self.add_google_gmail():
                    return True
                else:
                    return False





