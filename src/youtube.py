import random
import datetime
from time import sleep


class YouTube:
    def __init__(self, d):
        self.d = d

    def start(self):
        print("启动APP： YouTube")
        self.d.app_start("com.google.android.youtube")
        if self.d(resourceId="com.google.android.youtube:id/later_button",text='以后再说').wait(timeout=2):
            self.d(resourceId="com.google.android.youtube:id/later_button",text='以后再说').click()

    def stop(self):
        print("停止APP： YouTube")
        self.d.app_stop("com.google.android.youtube")

    def click_video(self):
        if self.d(resourceId="com.google.android.youtube:id/thumbnail", className="android.widget.ImageView").wait(timeout=20):
            print("YouTube界面： 播放视频")
            self.d(resourceId="com.google.android.youtube:id/thumbnail", className="android.widget.ImageView", instance=0).click()

    def youtube_random_play(self,time=5):
        self.start()
        num = random.randint(0, 1)
        if num == 0:
            self.d.swipe(0.5, 0.8, 0.5, 0.095)
            self.click_video()
        else:
            self.click_video()
        starttime = datetime.datetime.now()
        print("开始播放时间：", starttime)
        while True:
            sleep(5)
            endtime = datetime.datetime.now()
            if (endtime - starttime).seconds >= time * 60:
                print("结束播放时间：", endtime)
                self.d.press("home")
                break
