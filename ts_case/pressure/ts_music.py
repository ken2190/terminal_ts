import random
from time import sleep
from src.general import image_comparison
from src.general import adb
from src.music import Music
import datetime
from src import loginfo
import os

class Ts_Music():
    def __init__(self, d):
        self.d = d
        self.music = Music(self.d)
        self.path = image_comparison.get_path()
        self.log_data = []
        self.music_report_details = []

    def set_up(self, casename):
        print(casename)
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        self.music.stop()
        self.d.app_stop_all()
        self.music.start()
        self.d.screen_on()
        adb.get_meminfo(self.d)
        adb.get_battery(self.d)
        adb.get_cpuinfo(self.d)
        startTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.d.screenshot(self.path + "image\\music\\"+casename+startTime+".jpg")
        return time


    def ts_case1(self, time=60):
        '''
        数量较多的音乐文件填充T卡，再播放音乐  2.选择播放
        '''
        self.music.list_option_music()
        file_dir = self.path + "resource\\music"
        for root, dirs, files in os.walk(file_dir):
            for i in files:
                self.d.push(root+"\\"+i, '/sdcard/Music/'+i)
                print("push文件：",i)
        pull_dir = self.path +"resource\\pull_music"
        pull_music = "adb pull /sdcard/Music " + pull_dir + " >" + pull_dir + "\\pull_music.log"

        adb.chmod_adb(pull_music)

        self.music.stop()
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        self.music.start()
        self.d.screen_on()
        self.music.list_shuffle_all()
        sleep(1)
        self.music.list_playing()
        sleep(1)
        starttime = datetime.datetime.now()
        while True:
            # 执行随机点击上一首或下一首
            if random.randint(0, 1) == 0:
                self.music.play_nexticon()
            else:
                self.music.play_previcon()
                self.music.play_previcon()
            sleep(1)
            endtime = datetime.datetime.now()
            if (endtime - starttime).seconds >= time * 60:
                break
        return "pass"

    def ts_case2(self, time=60):
        '''
        开启长时间背景播放音乐，背景放音乐，20分钟后再点亮屏，检查能否正常点亮屏
        '''
        self.music.list_option_music()
        self.music.list_shuffle_all()
        self.d.press("home")
        time = time * 60
        sleep(time)
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        self.music.start()
        if self.d.info.get('screenOn'):
            return "pass"
        else:
            return "fail"


    def ts_case3(self, time=60):
        '''
        连续播放MP3，在播放过程中不断的切换MP3/快进/快退/进入/退出，1小时
        '''
        self.music.list_option_music()
        if self.d.info.get('screenOn'):
            pass
        else:
            self.d.screen_on()
        self.music.list_shuffle_all()
        sleep(1)
        self.music.list_playing()
        sleep(1)
        starttime = datetime.datetime.now()  # 现在
        while True:
            num = random.randint(0, 3)
            if num == 0:
                self.music.play_nexticon()
            elif num == 1:
                self.music.play_previcon()
            elif num == 2:
                self.music.play_long_nexticon()
            else:
                self.music.play_long_previcon()
            endtime =  datetime.datetime.now()
            if (endtime - starttime).seconds >= time * 60:
                break
        return "pass"

    def ts_case4(self, num=201):
        '''
        音频文件能正确的跳转/列表显示/播放
        预置条件：
            1. SD卡中有100多个音频文件（每个文件大小至少3M）
            注：限于智能机
            界定切换时间间隔5s
        测试步骤：
            1. 打开音乐随身听的本地音乐
            2. 播放一个音频文件5秒
            3. 随机播放开启时跳转到下一个/上一个音频文件100次
            4. 随机播放关闭时跳转到下一个/上一个音频文件100次
        :return:
        '''
        self.music.list_option_music()
        if self.d.info.get('screenOn'):
            pass
        else:
            self.d.screen_on()
        self.music.list_shuffle_all()
        sleep(1)
        self.music.list_playing()
        sleep(1)
        for i in range(2):
            for j in range(num):
                sleep(10)
                self.d.screen_on()
                if random.randint(0, 1) == 0:
                    self.music.play_nexticon()
                else:
                    self.music.play_previcon()
            self.music.play_randomicon()
        return "pass"




    def tear_down(self, casename):
        downTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.d.screenshot(self.path + "image\\music\\"+casename+downTime+".jpg")
        adb.get_meminfo(self.d )
        adb.get_battery(self.d )
        adb.get_cpuinfo(self.d )
        self.music.stop()
        print(casename)
        return time



    def run(self):
        path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
        path = path+"\\resource\\log\\music.log"

        time= 2

        actual_result = ""
        err_path = ""
        starttime1 = self.set_up("开始测试：数量较多的音乐文件填充T卡，再播放音乐，选择播放"+str(time)+"分钟")
        try:
            t_reference_result1 = self.ts_case1(time)
        except BaseException as e:
            t_reference_result1 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：数量较多的音乐文件填充T卡，再播放音乐，选择播放"+str(time)+"分钟；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\music\\数量较多的音乐文件填充T卡，再播放音乐，选择播放"+str(time)+"分钟；出现异常.jpg"
            self.d.screenshot(err_path)
            self.music.stop()
            self.d.app_stop_all()
        endtime1 = self.tear_down("结束测试:数量较多的音乐文件填充T卡 ")
        self.music_report_details.append({"t_module": "音乐", "t_case": "压力测试", "t_steps": "数量较多的音乐文件填充T卡，再播放音乐\n选择播放"+str(time)+"分钟 ", "t_expected_result": "1.可正常播放音乐文件 \n 2.界面显示正常 ",
         "t_actual_result": actual_result + "\n" + err_path, "t_start_time": starttime1, "t_end_time": endtime1, "t_reference_result": t_reference_result1, "t_result": ""})
        sleep(2)


        actual_result = ""
        err_path = ""
        starttime2 = self.set_up("开始测试：开始长时间背景播放音乐"+str(time)+"分钟")
        try:
            t_reference_result2 = self.ts_case2(time)
        except BaseException as e:
            t_reference_result2 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：开始长时间背景播放音乐"+str(time)+"分钟；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\music\\开始长时间背景播放音乐"+str(time)+"分钟；出现异常.jpg"
            self.d.screenshot(err_path)
            self.music.stop()
            self.d.app_stop_all()
        endtime2 =self.tear_down("结束测试：结束长时间背景播放音乐"+str(time)+"分钟")
        self.music_report_details.append({"t_module": "音乐", "t_case": "压力测试", "t_steps": "开启长时间背景播放音乐，背景放音乐，\n"+str(time)+"分钟后再点亮屏，检查能否正常点亮屏 ", "t_expected_result": "无破音，杂音，死机等异常现象\n屏可以正常点亮",
         "t_actual_result": actual_result + "\n" + err_path, "t_start_time": starttime2, "t_end_time": endtime2, "t_reference_result": t_reference_result2, "t_result": ""})
        sleep(2)


        actual_result = ""
        err_path = ""
        starttime3 = self.set_up("开始测试：开始连续播放MP3 "+str(time)+"分钟")
        try:
            t_reference_result3 = self.ts_case3(time)
        except BaseException as e:
            t_reference_result3 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：开始连续播放MP3 "+str(time)+"分钟；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\music\\开始连续播放MP3 "+str(time)+"分钟；出现异常.jpg"
            self.d.screenshot(err_path)
            self.music.stop()
            self.d.app_stop_all()
        endtime3 = self.tear_down("结束测试：结束连续播放MP3 "+str(time)+"分钟")
        self.music_report_details.append({"t_module": "音乐", "t_case": "压力测试", "t_steps": "连续播放MP3\n在播放过程中不断的切换MP3/快进/快退/进入/退出，"+str(time)+"分钟", "t_expected_result": "频繁切换操作不会出现异常退出，奔溃等现象\n能够保持一直正常播放",
         "t_actual_result": actual_result + "\n" + err_path, "t_start_time": starttime3, "t_end_time": endtime3, "t_reference_result": t_reference_result3, "t_result": ""})



        count = 10
        actual_result = ""
        err_path = ""
        starttime4 = self.set_up("开始测试：开启或关闭随机播放时连续播放音乐，切换上下首"+str(count)+"次")
        try:
            t_reference_result4 = self.ts_case4(count)
        except BaseException as e:
            t_reference_result4 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：开启或关闭随机播放时连续播放音乐，切换上下首"+str(count)+"次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\music\\开启或关闭随机播放时连续播放音乐，切换上下首"+str(count)+"次；出现异常.jpg"
            self.d.screenshot(err_path)
            self.music.stop()
            self.d.app_stop_all()
        endtime4 = self.tear_down("结束测试：开启或关闭随机播放时连续播放音乐，切换上下首"+str(count)+"次")
        self.music_report_details.append({"t_module": "音乐", "t_case": "压力测试",
                                          "t_steps": "1. SD卡中有100多个音频文件（每个文件大小至少3M）\n注：限于智能机\n界定切换时间间隔5s\n测试步骤：\n1. 打开音乐随身听的本地音乐\n2. 播放一个音频文件5秒\n3. 随机播放开启时跳转到下一个/上一个音频文件100次\n4. 随机播放关闭时跳转到下一个/上一个音频文件"+str(count)+"次", "t_expected_result": "频繁切换操作不会出现异常退出，奔溃等现象\n能够保持一直正常播放",
                                        "t_actual_result": actual_result + "\n" + err_path, "t_start_time": starttime4, "t_end_time": endtime4, "t_reference_result": t_reference_result4, "t_result": ""})
        loginfo.writer_log(path, self.log_data)
        sleep(2)
        return self.music_report_details
