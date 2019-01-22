import uiautomator2 as u2
import time
import os
from src.general.unlock import *
from src.camera import *
from src.record import *
from src.general.adb import *
from src.general import image_comparison

class Terminal_load():

    def __init__(self,d):
        self.d=d
        self.camera=Camera(d)
        self.record=Record(d)
        self.path = image_comparison.get_path()
        self.App_Load_Report_Details=[]
        self.error_list=[]

    def install_app(self):
        '''
        安装大量的apk
        :return:
        '''
        c = '\\resource\\APK'
        d = os.path.abspath(os.path.join(os.getcwd(), "../.."))
        path = d + c
        Install_Apk(path)



    def setup(self):
        self.facility = adb.read_adb("adb shell getprop ro.product.model")  # 获取设备的版本号
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>停止所有运行的app')
        self.d.app_stop_all()
        time.sleep(5)
        self.d.press("home")
        print(start_time)
        return start_time


    def Case_App_Load(self,num=31):
        '''
        在内存满的情况下进行，首先安装apk
        满负载测试，测试视频的录制，录音，相机的拍照和删除图片
        :param num:
        :return:
        '''
        times=15                    #录音和录制视频的时间后期可以修改尽量改成要设置的时间往后延长几秒
        result='Pass'
        for all_num in range(num):
            print('##########  第%s次相机操作  ##########'%all_num)
            self.camera.CameraOn()
            self.camera.VideoMode()
            self.camera.open_set()
            self.camera.click_operation(operation='视频持续时间')
            time.sleep(2)
            self.camera.select_video_time(time='10 分钟')
            time.sleep(2)
            self.camera.open_set()
            self.camera.click_operation(operation='视频画质')
            self.camera.select_video_quality()
            self.camera.Photograph()
            time.sleep(10)
            self.camera.PictureMode(self.facility)
            for picture_num in range(num):
                time.sleep(1)
                self.camera.Photograph()
            self.camera.EnterInto()
            for delete_picture in range(int(num/2-1)):
                self.d.click(0.191, 0.482)
                pictuer_number_name=self.camera.Picture_Number_Name()
                print('这是开始的图片编号'+pictuer_number_name)
                self.d.click(0.191, 0.482)
                self.camera.Delete_picture()
                self.d.click(0.191, 0.482)
                new_pictuer_number_name = self.camera.Picture_Number_Name()
                print('这是滑动之后的图片编号'+new_pictuer_number_name)
                if pictuer_number_name!=new_pictuer_number_name:
                    print('>>>>>>>>>>第%s次删除图片成功'%delete_picture)
                else:
                    print('>>>>>>>>>>第%s次删除图片失败'%delete_picture)
                    result='Fail'
                    self.error_list.append('第%s次删除图片失败'%delete_picture)
                time.sleep(3)
            self.camera.CameraOff()
            time.sleep(2)
            print('##########  第%s次录音操作  ##########' % all_num)
            self.record.Packaging_one(times)
            self.record.Packaging_two(times)
            self.record.Packaging_three(times)
            for screen_operation_num in range(num):
                screen_operation=self.d.info.get('screenOn')
                if screen_operation==True:
                    print('>>>>>>>>>>当前屏幕状态正确处于亮屏状态')
                else:
                    print('>>>>>>>>>>当前屏幕状态错误，应该处于亮屏状态')
                    result='Fail'
                    self.error_list.append('当前屏幕状态错误，应该处于亮屏状态')
                time.sleep(3)
                print('>>>>>>>>>>正在灭屏')
                self.d.screen_off()
                screen_operation = self.d.info.get('screenOn')
                if screen_operation == False:
                    print('>>>>>>>>>>当前屏幕状态正确处于熄屏状态')
                else:
                    print('>>>>>>>>>>当前屏幕状态错误，应该处于亮屏状态')
                    result='Fail'
                    self.error_list.append('当前屏幕状态错误，应该处于熄屏状态')
                time.sleep(5)
                print('>>>>>>>>>>正在亮屏')
                self.d.screen_on()
                print('>>>>>>>>>>正在解锁')
                self.d.unlock()
        print('开始执行待机3小时。。。。。')
        time.sleep(10800)                           #待机3小时，测试时间为1秒，正式跑是改成10800

        return result


    def Teardown(self):
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return end_time


    def run(self):
        start_time1=self.setup()
        actul_reselt=''
        path=''
        result1 = self.Case_App_Load()
        # try:
        #     result1=self.Case_App_Load()
        # except BaseException as e:
        #     result1 = 'Fail'
        #     print("except:", e)
        #     actul_reselt=str(e)[7:]wo
        #     print("=====>>>>>执行测试：满负载测试" + "；出现异常<<<<<=====")
        #     self.d.screen_on()
        #     # 判断是否锁屏状态
        #     if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
        #         self.d.unlock()
        #     path=self.path+'image\\error_picture\\' + "满负载测试" + "；出现异常.jpg"
        #     self.d.screenshot(path)
        #     self.d.app_stop_all()
        end_time1=self.Teardown()
        self.App_Load_Report_Details.append(
            {"t_module": "满负载测试", "t_case": "压力测试", "t_steps": "1. 进行录像和拍照。2. 进行录音等基本功能  d验证。3. 休眠唤醒4. 待机3小时5. 图库删除图片",
             "t_expected_result": "1.录像和拍照提示信息正确。\n 2.录音功能正常。\n 3.休眠唤醒正常。\n 4.待机无异常重启等。\n 5.能正常删除图片。\n 6.请手工验证录制的视频",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})
        return self.App_Load_Report_Details


