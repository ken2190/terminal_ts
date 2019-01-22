import random
import time
from src.general import image_comparison
import uiautomator2 as u2


class Video:
    def __init__(self, d):
        self.d = d
        self.path = image_comparison.get_path()
        self.d_size = self.d.window_size()


    def __sleep(func):
        def inner(self):
            time.sleep(1)
            self.d.screen_on()
            return func(self)
        return inner


    def start(self):
        print(">>>>>>>>>>>>>>>>> 启动apk: 视频")
        self.d.app_start("com.android.music", activity=".VideoBrowserActivity")


    def stop(self):
        print(">>>>>>>>>>>>>>>>> 停止apk: 视频")
        self.d.app_stop("com.android.music")


    '''
    以下为视频列表界面
    '''
    @__sleep
    def get_video_list(self):
        print(">>>>>>>>>>>>>>>>> 视频列表界面： 获取当前界面视频个数")
        number = self.d(resourceId="android:id/text1")
        return len(number)


    def click_list_void(self, number=0):
        time.sleep(1)
        self.d.screen_on()
        print(">>>>>>>>>>>>>>>>> 视频列表界面： 打开视频")
        while True:
            self.d(resourceId="android:id/text1")[number].click()
            current = self.d.current_app()
            if current['package'] != "com.android.gallery3d":
                if self.d(resourceId="android:id/title").wait(timeout=1):
                    self.d.swipe(0.5, 0.8, 0.5, 0.5)
                if self.d(resourceId="android:id/text2",text=u"图库").wait(timeout=2):
                    self.d(resourceId="android:id/text2", text=u"图库").click()
                    self.d(resourceId="android:id/button_once").click()
                    break
                elif self.d(resourceId="android:id/title", text="使用视频播放器打开").wait(timeout=2):
                    self.d(resourceId="android:id/button_once").click()
                    break
                elif self.d(resourceId="android:id/text1", text=u"视频播放器", className="android.widget.TextView", instance=0).wait(timeout=2):
                    self.d(resourceId="android:id/text1", text=u"视频播放器", className="android.widget.TextView", instance=0).click()
                    self.d(resourceId="android:id/button_once").click()
                    break
                else:
                    self.d.press("back")
            else:
                break


    def longclick_list_void(self, number=0):
        time.sleep(1)
        self.d.screen_on()
        print(">>>>>>>>>>>>>>>>> 视频列表界面： 长按视频")
        self.d(resourceId="android:id/text1")[number].long_click(duration=2)


    def get_list_void_name(self, number=0):
        time.sleep(1)
        self.d.screen_on()
        print(">>>>>>>>>>>>>>>>> 视频列表界面： 获取视频名称")
        name = self.d(resourceId="android:id/text1")[number].get_text()
        return name

    @__sleep
    def list_void_share(self):
        print(">>>>>>>>>>>>>>>>> 视频列表界面： 点击分享")
        self.d(resourceId="android:id/title").click()

    '''
    下列是播放界面
    '''
    def videoplay_pop(self, decide=2):
        time.sleep(1)
        self.d.screen_on()
        # decide 为2时为重新开始播放，为1时为继续播放 #
        if self.d(resourceId="android:id/alertTitle",text='继续播放视频').wait(timeout=2):
            if decide == 2:
                print(">>>>>>>>>>>>>>>>> 视频播放界面： 弹出继续播放视频选择框，【选择重新播放】")
                self.d(resourceId="android:id/button2").click()
            else:
                print(">>>>>>>>>>>>>>>>> 视频播放界面： 弹出继续播放视频选择框，【选择继续播放】")
                self.d(resourceId="android:id/button1").click()

    @__sleep
    def videoplay_pause(self):
        self.d.click(0.500, 0.500)
        if not(self.d(description=u"播放视频").wait(timeout=1)):
            self.d.click(0.500, 0.500)
        if self.d(description=u"播放视频").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 视频播放界面： 点击播放/暂停")
            self.d(description=u"播放视频").click()

    @__sleep
    def videoplay_full(self):
        self.d.click(0.500, 0.500)
        if not(self.d(className="android.widget.ImageView", instance=1).wait(timeout=1)):
            self.d.click(0.500, 0.500)
        if self.d(className="android.widget.ImageView", instance=1).wait(timeout=1):
            self.d(className="android.widget.ImageView", instance=1).click()
            print(">>>>>>>>>>>>>>>>> 视频播放界面： 点击全屏")
    @__sleep
    def videoplay_back(self):
        self.d.click(0.500, 0.500)
        if not(self.d(description=u"向上导航").wait(timeout=1)):
            self.d.click(0.500, 0.500)
        if self.d(description=u"向上导航").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 视频播放界面： 点击返回图标")
            self.d(description=u"向上导航").click()

    @__sleep
    def videoplay_share(self):
        if not(self.d(resourceId="android:id/image").wait(timeout=1)):
            self.d.click(0.500, 0.500)
        if self.d(resourceId="android:id/image").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 视频播放界面： 点击分享图标")
            self.d(resourceId="android:id/image").click()

    @__sleep
    def videoplay_more(self):
        if not(self.d(description=u"更多选项").wait(timeout=1)):
            self.d.click(0.500, 0.500)
        if self.d(description=u"更多选项").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 视频播放界面： 点击更多选项图标")
            self.d(description=u"更多选项").click()

    @__sleep
    def videoplay_progress(self):
        if not(self.d(description=u"视频播放器时间栏").wait(timeout=1)):
            self.d.click(0.500, 0.500)
        time.sleep(0.2)
        if self.d_size == (1080, 1920):
            print(">>>>>>>>>>>>>>>>> 视频播放界面： 点击进度条")
            if random.randint(0, 1) == 0:
                x = random.randint(190, 750) * 0.001
                self.d.click(x, 0.909)
        else:
            print(">>>>>>>>>>>>>>>>> 视频播放界面： 屏幕尺寸未做兼容，点击进度条失败")

