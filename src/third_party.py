import datetime
import random
from time import sleep
import uiautomator2 as u2
from src.general import adb
from src.general import get_config as config


def install_third_app():
    adb.install_app("aiqiyi.apk")
    adb.install_app("TencentVideo.apk")
    adb.install_app("QQ.apk")
    # adb.install_app("360Browser.apk")
    adb.install_app("UCBrowser.apk")
    # adb.install_app("DataFillerS_v2.1.apk")



class Aiqiyi:
    def __init__(self,d):
        self.d = d



    def start(self):
        print(">>>启动第三方APK： 爱奇艺")
        self.d.app_start("com.qiyi.video")
        if self.d(resourceId="com.android.packageinstaller:id/dialog_container").wait(timeout=1):
            print("首次进入爱奇艺，点击允许授权")
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
        if self.d(resourceId="com.qiyi.video:id/wr").wait(timeout=1):
            print("进入爱奇艺，弹出提示框点击X")
            self.d(resourceId="com.qiyi.video:id/wr").clcik()
        if self.d(resourceId="com.qiyi.video:id/ah9", text="暂不升级").wait(timeout=10):
            print("进入爱奇艺，弹出升级提示，点击：暂不升级")
            self.d(resourceId="com.qiyi.video:id/ah9", text="暂不升级").click()

    def stop(self):
        print(">>>关闭第三方APK： 爱奇艺")
        self.d.app_stop("com.qiyi.video")

    def aiqiyi_play_video(self,time=5):
        self.stop()
        self.start()
        sleep(4)
        starttime = datetime.datetime.now()
        if self.d(className="android.widget.ImageView", instance=12).wait(timeout=2):
            print("爱奇艺，点击播放视频")
            print("开始播放时间：", starttime)
            self.d(className="android.widget.ImageView", instance=12).click()
            while True:
                sleep(5)
                endtime = datetime.datetime.now()
                if (endtime - starttime).seconds >= time * 60:
                    print("结束播放时间：", endtime)
                    self.d.press("home")
                    break
        else:
            print("爱奇艺视频，播放视频失败")


class Tx_Video:
    def __init__(self, d):
        self.d = d

    def start(self):
        print(">>>启动第三方APK： 腾讯视频")
        self.d.app_start("com.tencent.qqlive")
        sleep(3)
        if self.d(resourceId="com.tencent.qqlive:id/cvz", text=u"同意协议开始使用").wait(timeout=2):
            self.d(resourceId="com.tencent.qqlive:id/cvz", text=u"同意协议开始使用").click()
        if self.d(resourceId="com.tencent.qqlive:id/czj", text=u"暂不升级").wait(timeout=10):
            self.d(resourceId="com.tencent.qqlive:id/czj", text=u"暂不升级").click()
        if self.d(resourceId="com.tencent.qqlive:id/cvv", text=u"允许").wait(timeout=2):
            self.d(resourceId="com.tencent.qqlive:id/cvv", text=u"允许").click()
        if self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").wait(timeout=2):
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()


    def tx_play_video(self,time=5):
        self.stop()
        self.start()
        sleep(4)
        starttime = datetime.datetime.now()
        if self.d(resourceId="com.tencent.qqlive:id/aa7").wait(timeout=2):
            print("腾讯视频，点击播放视频")
            print("开始播放时间：", starttime)
            self.d(resourceId="com.tencent.qqlive:id/aa7").click()
            while True:
                sleep(5)
                endtime = datetime.datetime.now()
                if (endtime - starttime).seconds >= time * 60:
                    print("结束播放时间：", endtime)
                    self.d.press("home")
                    break
        else:
            print("腾讯视频，播放视频失败")

    def stop(self):
        print(">>>关闭第三方APK： 腾讯视频")
        self.d.app_stop("com.tencent.qqlive")

class Tx_QQ:
    def __init__(self, d):
        self.d = d
        self.name = config.get_config("QQ", "name")
        self.password = config.get_config("QQ", "password")


    def start(self):
        print(">>>启动第三方APK： QQ")
        self.d.app_start("com.tencent.mobileqq")

    def login_qq(self):
        qq = self.name
        password = self.password
        try:
            self.start()
            if self.d(resourceId="com.tencent.mobileqq:id/conversation_head").wait(timeout=5):
                print("qq已登录，切换到后台")
            elif self.d(resourceId="com.tencent.mobileqq:id/btn_login").wait(timeout=30):
                print("QQ 执行登录操作")
                self.d(resourceId="com.tencent.mobileqq:id/btn_login").click()
                self.d(text=u"QQ号/手机号/邮箱").set_text(qq)
                self.d(resourceId="com.tencent.mobileqq:id/password").set_text(password)
                self.d(resourceId="com.tencent.mobileqq:id/login").click()
                sleep(3)
                if self.d(resourceId="com.tencent.mobileqq:id/dialogLeftBtn").wait(timeout=20):
                    self.d(resourceId="com.tencent.mobileqq:id/dialogLeftBtn").click()
                if self.d(resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").wait(timeout=2):
                    self.d(resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").click()
                if self.d(resourceId="com.tencent.mobileqq:id/conversation_head").wait(timeout=5):
                    print("qq登录成功，切换到后台")
                else:
                    print("qq登录异常，可能需要手动执行验证码操作；切换到后台")
            self.d.press("home")
        except BaseException as e:
            print("后台挂qq出现异常:", e)
            self.d.app_stop("com.tencent.mobileqq")
            self.d.press("home")

    def wait_update_qq(self):
        '''
        判断qq的数据更新
        :return:
        '''
        if self.d(resourceId="com.tencent.mobileqq:id/name", className="android.widget.ProgressBar").wait(
                timeout=3) == True:
            print('---------->正在更新数据')
            self.d(resourceId="com.tencent.mobileqq:id/name", className="android.widget.ProgressBar").wait_gone(
                timeout=200)



    def stop(self):
        self.d.app_stop("com.tencent.mobileqq")
        print(">>>关闭第三方APK： QQ")



class Browser_360:
    def __init__(self, d):
        self.d = d
        self.d_size = self.d.window_size()


    def start(self):
        print(">>>启动第三方APK： 360浏览器")
        self.d.app_start("com.qihoo.browser")
        sleep(10)
        self.d.swipe(0.9, 0.5, 0.2, 0.5)
        sleep(1)
        if self.d(resourceId="com.qihoo.browser:id/ft").wait(timeout=2):
            self.d(resourceId="com.qihoo.browser:id/ft").click()
        while True:
            if self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").wait(timeout=2):
                self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
            else:
                break
        if self.d(resourceId="com.qihoo.browser:id/o7").wait(timeout=2):
            self.d(resourceId="com.qihoo.browser:id/o7").click()

    def open_browser(self,url=["www.baidu.com","www.sina.com.cn","news.qq.com","m.qidian.com"]):
        self.stop()
        self.start()
        num = random.randint(0, 4)
        print("360浏览器打开网页，输入url：",url[num])
        for i in range(3):
            if self.d(resourceId="com.qihoo.browser:id/tu").wait(timeout=1):
                self.d(resourceId="com.qihoo.browser:id/tu").click()
                self.d(resourceId="com.qihoo.browser:id/in").set_text(url[num])
                break
            elif self.d(resourceId="com.qihoo.browser:id/in").wait(timeout=1):
                self.d(resourceId="com.qihoo.browser:id/in").click()
                self.d(resourceId="com.qihoo.browser:id/in").set_text(url[num])
                break
            else:
                self.d.press("back")
        self.d(resourceId="com.qihoo.browser:id/aiy").click()
        sleep(2)
        self.d.press("home")


    def stop(self):
        self.d.app_stop("com.qihoo.browser")
        print(">>>关闭第三方APK： 360浏览器")



class Browser_UC:
    def __init__(self, d):
        self.d = d
        self.d_size = self.d.window_size()


    def start(self):
        print(">>>启动第三方APK： UC浏览器")
        self.d.app_start("com.UCMobile")
        if self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").wait(timeout=2):
            for i in range(6):
                if self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").wait(timeout=2):
                    self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
                else:
                    break
            if self.d(resourceId="com.UCMobile:id/agree").wait(timeout=2):
                self.d(resourceId="com.UCMobile:id/agree").click()
            if self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").wait(timeout=5):
                self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
            if self.d(text=u"跳过").wait(timeout=2):
                self.d(text=u"跳过").click()
            if self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").wait(timeout=5):
                self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
            if self.d(resourceId="com.UCMobile:id/navi_site_content", className="android.widget.LinearLayout", instance=4).wait(timeout=2):
                self.d(resourceId="com.UCMobile:id/navi_site_content", className="android.widget.LinearLayout", instance=4).click()
        if self.d(text=u"新版本提示").wait(timeout=2):
            self.d(text=u"取消").click()


    def open_browser(self,url=["www.baidu.com","www.sina.com.cn","news.qq.com","m.qidian.com"]):
        self.stop()
        self.start()
        num = random.randint(0, 4)
        print("UC浏览器打开网页，输入url：",url[num])
        for i in range(3):
            if self.d(description=u"homepage_search").wait(timeout=1):
                self.d(description=u"homepage_search").click()
                break
            elif self.d(resourceId="com.UCMobile:id/titlebar_search").wait(timeout=2):
                self.d(resourceId="com.UCMobile:id/titlebar_search").click()
                break
            else:
                self.d.press("back")
        if self.d(resourceId="com.UCMobile:id/edittext").wait(timeout=2):
            self.d(resourceId="com.UCMobile:id/edittext").set_text(url[num])
            self.d(resourceId="com.UCMobile:id/cancel").click()
        else:
            self.d.press("back")
        sleep(2)
        self.d.press("home")


    def stop(self):
        self.d.app_stop("com.UCMobile")
        print(">>>关闭第三方APK： UC浏览器")

