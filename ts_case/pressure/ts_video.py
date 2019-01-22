import random
from datetime import datetime
from time import sleep
from src.general import image_comparison
from src.general import adb
from src.video import Video
from src.third_party import *
import datetime
from src.settings import Settings

from src.youtube import YouTube


class Ts_Video:
    def __init__(self, d):
        self.d = d
        self.video = Video(self.d)
        self.path = image_comparison.get_path()
        self.log_data = []
        self.video_report_details = []

    def set_up(self, casename):
        print(casename)
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        self.video.stop()
        self.d.app_stop_all()
        self.video.start()
        self.d.screen_on()
        adb.get_meminfo(self.d)
        adb.get_battery(self.d)
        adb.get_cpuinfo(self.d)
        startTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.d.screenshot(self.path + "image\\video\\" + casename + startTime + ".jpg")
        return time

    def case1(self, time=240):
        '''
        长时间播放视频列表中的视频
        '''
        result = "pass"
        starttime = datetime.datetime.now()
        print(">>>>开始测试长时间播放视频列表中的视频：", starttime)
        video_number = self.video.get_video_list()
        if video_number != 0:
            while True:
                video_number = self.video.get_video_list()
                for i in range(0, video_number):
                    name = self.video.get_list_void_name(number=i)
                    self.video.click_list_void(number=i)
                    self.video.videoplay_pop()
                    print(">>>>播放视频：", name)
                    print("播放开始时间：",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    while True:
                        sleep(10)
                        self.d.screen_on()
                        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                            self.d.unlock()
                        current = self.d.current_app()
                        if current['package'] == "com.android.gallery3d":
                            endtime = datetime.datetime.now()
                            if (endtime - starttime).seconds >= time * 60:
                                current = self.d.current_app()
                                if current['package'] == "com.android.gallery3d":
                                    self.d.press("back")
                                print("播放结束时间：", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                break
                        else:
                            endtime = datetime.datetime.now()
                            print("播放结束时间：", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                            break
                    if (endtime - starttime).seconds >= time * 60:
                        break
                self.d.swipe(0.729, 0.8, 0.808, 0.095)
                endtime = datetime.datetime.now()
                if (endtime - starttime).seconds >= time*60:
                    break
        else:
            print(">>>视频列表为空")
            result = "fail"
        endtime = datetime.datetime.now()
        print(">>>>结束测试长时间播放视频列表中的视频：", endtime)
        return result

    def case2(self, time=240):
        '''
        播放大容量的视频文件，反复播放暂停视频，检查是否会出现无法播放现象
        '''
        result = "pass"
        runtime = random.randint(1, time/5)
        starttime = datetime.datetime.now()
        print(">>>>开始测试播放大容量的视频文件，反复播放暂停视频：", starttime)
        while True:
            swipenum= random.randint(0, 2)
            if swipenum == 0:
                self.d.swipe(0.729, 0.8, 0.808, 0.095)
            elif swipenum == 1:
                self.d.swipe(0.5, 0.3, 0.5, 0.6)
            video_number = self.video.get_video_list()
            if video_number != 0:
                while video_number:
                    number = random.randint(0, video_number-1)
                    name = self.video.get_list_void_name(number=number)
                    self.video.click_list_void(number=number)
                    self.video.videoplay_pop()
                    print(">>>>播放视频：", name)
                    run_starttime = datetime.datetime.now()
                    while True:
                        endtime = datetime.datetime.now()
                        num = random.randint(0, 2)
                        if num == 0:
                            self.video.videoplay_progress()
                        elif num == 1:
                            self.video.videoplay_pause()
                        else:
                            self.video.videoplay_full()
                        sleep(5)
                        current = self.d.current_app()
                        if (endtime - run_starttime).seconds >= runtime * 60:
                            runtime = random.randint(1, time)
                            print(">>>>>>>>>>>>>>>>> 视频列表界面： 点击返回")
                            self.d.press("back")
                            break
                        elif (endtime - starttime).seconds >= time * 60:
                            break
                        elif not(current['package'] == "com.android.gallery3d"):
                            break
                    if (endtime - starttime).seconds >= time * 60:
                        break
                if (endtime - starttime).seconds >= time * 60:
                    break
            else:
                print(">>>视频列表为空")
                result = "fail"
                break
        endtime = datetime.datetime.now()
        print(">>>>结束测试播放大容量的视频文件，反复播放暂停视频：", endtime)
        return result

    def case3(self,time=240,onetime=10):
        '''
        播放本地视频与播放在线视频，反复切换视频播放器，返回主界面等
        :return:
        '''
        aiqiyi = Aiqiyi(self.d)
        tx_video = Tx_Video(self.d)
        youtube = YouTube(self.d)
        setting = Settings(self.d)
        if setting.open_wifi():
            pass
        else :
            setting.auto_connect_wifi()
        self.video.start()
        starttime = datetime.datetime.now()
        video_number = self.video.get_video_list()
        print(">>>>开始测试播放本地视频与播放在线视频：", starttime)
        if video_number != 0:
            while video_number:
                swipenum = random.randint(0, 2)
                if swipenum == 0:
                    self.d.swipe(0.729, 0.8, 0.808, 0.095)
                elif swipenum == 1:
                    self.d.swipe(0.5, 0.3, 0.5, 0.6)
                video_number = self.video.get_video_list()

                number = random.randint(0, video_number - 1)
                name = self.video.get_list_void_name(number=number)
                self.video.click_list_void(number=number)
                self.video.videoplay_pop()
                print(">>>>播放视频：", name)
                run_starttime = datetime.datetime.now()
                print(">>>>开始播放视频：", run_starttime)
                while True:
                    num = random.randint(0, 10)
                    if num == 0:
                        self.video.videoplay_progress()
                    elif num == 1:
                        self.video.videoplay_pause()
                    elif num == 2:
                        self.video.videoplay_full()
                    sleep(5)
                    endtime = datetime.datetime.now()
                    current = self.d.current_app()
                    if (endtime - run_starttime).seconds >= onetime * 60:
                        current = self.d.current_app()
                        if current['package'] == "com.android.gallery3d":
                            print(">>>>>>>>>>>>>>>>> 视频列表界面： 点击返回")
                            self.d.press("back")
                        print(">>>>结束播放视频：", endtime)
                        break
                    elif (endtime - starttime).seconds >= time * 60:
                        current = self.d.current_app()
                        if current['package'] == "com.android.gallery3d":
                            print(">>>>>>>>>>>>>>>>> 视频列表界面： 点击返回")
                            self.d.press("back")
                        print(">>>>结束播放视频：", endtime)
                        break
                    elif current['package'] != "com.android.gallery3d":
                        print(">>>>结束播放视频：", endtime)
                        break
                while True:
                    num = random.randint(0, 2)
                    if (endtime - starttime).seconds >= time * 60:
                        break
                    try:
                        if num == 0:
                            aiqiyi.aiqiyi_play_video(time=onetime)
                        elif num == 1:
                            tx_video.tx_play_video(time=onetime)
                        else:
                            youtube.youtube_random_play(time=onetime)
                    except BaseException as e:
                        print("第三方app出现异常:", e)
                        self.d.app_stop_all()
                    self.video.start()
                    break
                if (endtime - starttime).seconds >= time * 60:
                    print(">>>>结束测试播放本地视频与播放在线视频")
                    break
        else:
            print(">>>视频列表为空")
            result = "fail"
        return result

    def tear_down(self, casename):
        downTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.d.screenshot(self.path + "image\\video\\"+casename+downTime+".jpg")
        adb.get_meminfo(self.d )
        adb.get_battery(self.d )
        adb.get_cpuinfo(self.d )
        self.video.stop()
        print(casename)
        return time

    def run(self):
        time = 5


        actual_result = ""
        err_path = ""
        starttime1 = self.set_up("开始测试：长时间播放视频测试"+str(time)+"分钟")
        try:
            t_reference_result1 = self.case1(time)
        except BaseException as e:
            t_reference_result1 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：长时间播放视频测试"+str(time)+"分钟；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\video\\长时间播放视频测试"+str(time)+"分钟；出现异常.jpg"
            self.d.screenshot(err_path)
            self.video.stop()
            self.d.app_stop_all()
        endtime1 = self.tear_down("结束测试：长时间播放测试"+str(time)+"分钟")
        self.video_report_details.append(
            {"t_module": "视频", "t_case": "压力测试", "t_steps": "长时间播放视频"+str(time)+"分钟",
             "t_expected_result": "视频正常播放，无死机等异常 ",
             "t_actual_result": actual_result + "\n" + err_path,  "t_start_time": starttime1, "t_end_time": endtime1,
             "t_reference_result": t_reference_result1, "t_result": ""})


        actual_result = ""
        err_path = ""
        starttime2 = self.set_up("开始测试：反复播放暂停视频"+str(time)+"分钟。检查是否会出现无法播放现象")
        try:
            t_reference_result2 = self.case2(time)
        except BaseException as e:
            t_reference_result2 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：反复播放暂停视频"+str(time)+"分钟。检查是否会出现无法播放现象；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\video\\反复播放暂停视频"+str(time)+"分钟。检查是否会出现无法播放现象；出现异常.jpg"
            self.d.screenshot(err_path)
            self.video.stop()
            self.d.app_stop_all()
        endtime2 = self.tear_down("结束测试：反复播放暂停视频"+str(time)+"分钟。检查是否会出现无法播放现象")
        self.video_report_details.append(
            {"t_module": "视频", "t_case": "压力测试", "t_steps": "反复播放暂停视频"+str(time)+"分钟检查是否会出现无法播放现象 ",
             "t_expected_result": "播放正常",
             "t_actual_result": actual_result + "\n" + err_path,  "t_start_time": starttime2, "t_end_time": endtime2,
             "t_reference_result": t_reference_result2, "t_result": ""})


        actual_result = ""
        err_path = ""
        starttime3 =self.set_up("开始测试：反复切换视频播放器，在线播放高清视频"+str(time)+"分钟")
        try:
            t_reference_result3 = self.case3(time,1)
        except BaseException as e:
            t_reference_result3 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：反复切换视频播放器，在线播放高清视频"+str(time)+"分钟；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\video\\反复切换视频播放器，在线播放高清视频"+str(time)+"分钟；出现异常.jpg"
            self.d.screenshot(err_path)
            self.video.stop()
            self.d.app_stop_all()
        endtime3 = self.tear_down("结束测试：反复切换视频播放器，在线播放高清视频"+str(time)+"分钟")
        self.video_report_details.append(
            {"t_module": "视频", "t_case": "压力测试", "t_steps": "反复切换视频播放器，在线播放高清视频"+str(time)+"分钟检查是否会出现无法播放现象 ",
             "t_expected_result": "播放正常",
             "t_actual_result": actual_result + "\n" + err_path,  "t_start_time": starttime3, "t_end_time": endtime3,
             "t_reference_result": t_reference_result3, "t_result": ""})

        return self.video_report_details