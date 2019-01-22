import random
import time
from src.general import image_comparison


class Music:
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

    @__sleep
    def start(self):
        print(">>>>>>>>>>>>>>>>> 启动apk: 音乐")
        self.d.app_start("com.android.music", activity=".MusicBrowserActivity")
        if self.d(resourceId="com.android.packageinstaller:id/permission_message").wait(timeout=1):
            print(">>>>>>>>>>>>>>>>> 弹出权限允许框，点击允许")
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()


    @__sleep
    def stop(self):
        print(">>>>>>>>>>>>>>>>> 停止apk: 音乐")
        self.d.app_stop("com.android.music")


    '''
    以下为音乐列表界面
    '''
    @__sleep
    def list_option_music(self):
        print(">>>>>>>>>>>>>>>>> 音乐列表界面: 点击选项")
        self.d(description=u"drawer").click()
        time.sleep(1)
        print(">>>>>>>>>>>>>>>>> 音乐列表界面: 选项切换到歌曲")
        self.d(resourceId = "com.android.music:id/title", text = u"歌曲").click()

    def acquire_music_list(self):
        music=self.d(resourceId="com.android.music:id/iconTabbedView").wait(timeout=3)
        return music



    @__sleep
    def list_option_album(self,):
        print(">>>>>>>>>>>>>>>>> 音乐列表界面: 点击选项")
        self.d(description=u"drawer").click()
        time.sleep(1)
        print(">>>>>>>>>>>>>>>>> 音乐列表界面: 选项切换到专辑")
        self.d(resourceId="com.android.music:id/title", text=u"专辑").click()

    @__sleep
    def list_search(self):
        print(">>>>>>>>>>>>>>>>> 音乐列表界面: 点击搜索")
        self.d(resourceId="com.android.music:id/action_search").click()


    @__sleep
    def list_shuffle_all(self):
        print(">>>>>>>>>>>>>>>>> 音乐列表界面: 点击全部随机播放")
        self.d(resourceId="com.android.music:id/shuffleAll").click()

    @__sleep
    def list_play_indicator(self):
        print(">>>>>>>>>>>>>>>>> 音乐列表界面: 点击音乐详情")
        self.d(resourceId="com.android.music:id/play_indicator").click()

    @__sleep
    def list_playing(self):
        print(">>>>>>>>>>>>>>>>> 音乐列表界面: 点击播放盘，进入播放界面")
        self.d(resourceId="com.android.music:id/header_layout").click()
        # self.d(className="android.widget.LinearLayout", instance=7).click()


    '''
    以下为音乐详情界面
    '''
    @__sleep
    def play_pause(self):
        print(">>>>>>>>>>>>>>>>> 音乐详情界面: 点击播放/暂停图标")
        self.d(resourceId="com.android.music:id/play_pause").click()

    @__sleep
    def play_nexticon(self):
        print(">>>>>>>>>>>>>>>>> 音乐详情界面: 点击下一首")
        self.d(resourceId="com.android.music:id/nexticon").click()

    @__sleep
    def play_long_nexticon(self):
        print(">>>>>>>>>>>>>>>>> 音乐详情界面: 长按快进")
        if self.d_size == (1080, 1920):
            if random.randint(0, 1) == 0:
                x = random.randint(2, 999) * 0.001
                self.d.click(x, 0.707)
            else:
                self.d(resourceId="com.android.music:id/nexticon").long_click(duration=random.randint(0, 5))
        else:
            self.d(resourceId="com.android.music:id/nexticon").long_click(duration=random.randint(0, 5))


    @__sleep
    def play_previcon(self):
        print(">>>>>>>>>>>>>>>>> 音乐详情界面: 点击上一首")
        self.d(resourceId="com.android.music:id/previcon").click()


    @__sleep
    def play_long_previcon(self):
        print(">>>>>>>>>>>>>>>>> 音乐详情界面: 快退")
        if self.d_size == (1080, 1920):
            if random.randint(0, 1) == 0:
                x = random.randint(2, 999) * 0.001
                self.d.click(x, 0.707)
            else:
                self.d(resourceId="com.android.music:id/previcon").long_click(duration=random.randint(0, 5))
        else:
            self.d(resourceId="com.android.music:id/previcon").long_click(duration=random.randint(0, 5))

    @__sleep
    def play_randomicon(self):
        print(">>>>>>>>>>>>>>>>> 音乐详情界面: 点击随机播放")
        self.d(resourceId="com.android.music:id/randomicon").click()
        print(self.d.toast.get_message(wait_timeout=5, cache_timeout=5))

    @__sleep
    def play_loop_view(self):
        print(">>>>>>>>>>>>>>>>> 音乐详情界面: 点击重复播放")
        self.d(resourceId="com.android.music:id/loop_view").click()
        print(self.d.toast.get_message(wait_timeout=5, cache_timeout=5))


    '''
    以下是封装的一些操作
    '''

    @__sleep
    def start_background_play(self):
        print(">>>>>>>>>>>>>>>>> 音乐: 启动后台播放音乐")
        self.stop()
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        self.start()
        self.list_option_music()
        self.list_shuffle_all()
        self.d.press("home")

