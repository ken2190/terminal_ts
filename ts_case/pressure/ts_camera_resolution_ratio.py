import uiautomator2 as u2
import time
from src.camera import *
from src.general.unlock import *
from src.general import adb
from src.general import image_comparison
class Pre_camera_resolution_ratio():

    def __init__(self,d):
        self.d=d
        self.camera=Camera(self.d)
        self.path = image_comparison.get_path()
        self.switchcamera=[]
        self.camera_report_details=[]



    def setup(self):
        self.facility = adb.read_adb("adb shell getprop ro.product.model")  # 获取设备的版本号
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>停止所有运行的app')
        self.d.app_stop_all()
        self.camera.CameraOff()
        self.camera.CameraOn()
        self.camera.Pop_Up()
        self.camera.PictureMode(facility=self.facility)
        time.sleep(5)
        print(start_time)
        return start_time

    def Case_Camera_Pixel(self):
        '''
        相机的每个分辨率测试
        :return:
        '''
        result='Pass'
        pixel_list=[]
        self.camera.open_set()
        self.camera.click_operation(operation='照片尺寸')
        acquire_picture_size_long=self.camera.acquire_picture_size_long()
        for i in range(int(acquire_picture_size_long)):
            picture_size_name=self.camera.acquire_picture_size_long(num=i)
            pixel_list.append(picture_size_name)
        self.d.swipe(0.818,0.852,0.709,0.193)
        acquire_picture_size_long1 = self.camera.acquire_picture_size_long()
        for i in range(int(acquire_picture_size_long1)):
            picture_size_name1 = self.camera.acquire_picture_size_long(num=i)
            pixel_list.append(picture_size_name1)
        set_pixel_list=set(pixel_list)
        print(set_pixel_list)
        self.d.press("back")
        time.sleep(3)
        self.d.press("back")
        for pixel_name in set_pixel_list:
            print('>>>>>>>>>>>>>>>>>>正在寻找这个像素：'+pixel_name)
            self.camera.open_set()
            time.sleep(1)
            self.camera.click_operation(operation='照片尺寸')
            wait_pixel=self.camera.wait_pixel(pixel=pixel_name)
            if wait_pixel==True:
                print('正在点击：'+pixel_name)
                self.camera.click_pixel(pixel=pixel_name)
                time.sleep(5)
                self.camera.Photograph()
            else:
                self.d.swipe(0.818, 0.852, 0.709, 0.193)
                wait_pixel1 = self.camera.wait_pixel(pixel=pixel_name)
                if wait_pixel1 == True:
                    print('正在点击：' + pixel_name)
                    self.camera.click_pixel(pixel=pixel_name)
                    time.sleep(5)
                    self.camera.Photograph()
        return result

    def Case_Camera_Quality(self):
        '''
        相机的每个质量拍照操作
        :return:
        '''
        result='Pass'
        quality_list=[]
        self.camera.open_set()
        time.sleep(1)
        self.camera.click_operation(operation='照片质量')
        time.sleep(1)
        quality_long=self.camera.acquire_picture_quality_long()
        for i in range(quality_long):
            quality_name=self.camera.acquire_picture_quality_long(num=i)
            quality_list.append(quality_name)
        print(quality_list)
        self.d.press("back")
        time.sleep(3)
        self.d.press("back")
        for quality_names in quality_list:
            time.sleep(2)
            print('>>>>>>>>>>>>>>>>>>>>>>正在寻找这个质量名称：'+quality_names)
            self.camera.open_set()
            time.sleep(1)
            self.camera.click_operation(operation='照片质量')
            time.sleep(2)
            self.camera.click_picture_quality(quality_name=quality_names)
            time.sleep(2)
            print('点击快门')
            self.camera.Photograph()
            time.sleep(5)
        return result




    def Case_Combination_Pixel_Quality(self):
        '''
        相机的像素和质量组合测试，拍照
        :return:
        '''
        result='Pass'
        pixel_list=[]
        self.camera.open_set()
        self.camera.click_operation(operation='照片尺寸')
        picture_size_long=self.camera.acquire_picture_size_long()
        for i in range(int(picture_size_long)):
            picture_size_name=self.camera.acquire_picture_size_long(num=i)
            pixel_list.append(picture_size_name)
        self.d.swipe(0.818,0.852,0.709,0.193)
        picture_size_long1 = self.camera.acquire_picture_size_long()
        for i in range(int(picture_size_long1)):
            picture_size_name1 = self.camera.acquire_picture_size_long(num=i)
            pixel_list.append(picture_size_name1)
        set_pixel_list=set(pixel_list)
        print(set_pixel_list)
        self.d.press("back")
        time.sleep(3)
        self.d.press("back")
        for pixel_name in set_pixel_list:
            print('>>>>>>>>>>>>>>>>>>正在寻找这个像素：'+pixel_name)
            self.camera.open_set()
            time.sleep(1)
            self.camera.click_operation(operation='照片尺寸')
            wait_pixel=self.camera.wait_pixel(pixel_name)
            if wait_pixel==True:
                print('正在点击：'+pixel_name)
                self.camera.click_pixel(pixel_name)
                time.sleep(3)
                print('>>>>>>>>>>>>>>>>>>开始选择照片质量')
                print ('######################################################')
                quality_list = []
                self.camera.open_set()
                time.sleep(1)
                self.camera.click_operation(operation='照片质量')
                time.sleep(1)
                picture_quality_long = self.camera.acquire_picture_quality_long()
                for j in range(picture_quality_long):
                    picture_quality_name = self.camera.acquire_picture_quality_long(num=j)
                    quality_list.append(picture_quality_name)
                print(quality_list)
                self.d.press("back")
                time.sleep(3)
                self.d.press("back")
                for quality_names in quality_list:
                    time.sleep(2)
                    print('>>>>>>>>>>>>>>>>>>>>>>正在寻找这个质量名称：' + quality_names)
                    self.camera.open_set()
                    time.sleep(1)
                    self.camera.click_operation(operation='照片质量')
                    time.sleep(2)
                    self.camera.click_picture_quality(quality_names)
                    time.sleep(2)
                    print('点击快门')
                    self.camera.Photograph()
                    time.sleep(5)
            else:
                self.d.swipe(0.818, 0.852, 0.709, 0.193)
                wait_pixel1 = self.camera.wait_pixel(pixel_name)
                if wait_pixel1 == True:
                    print('正在点击：' + pixel_name)
                    self.camera.click_pixel(pixel_name)
                    time.sleep(3)
                    print('>>>>>>>>>>>>>>>>>>开始选择照片质量')
                    print('######################################################')
                    quality_list1 = []
                    self.camera.open_set()
                    time.sleep(1)
                    self.camera.click_operation(operation='照片质量')
                    time.sleep(1)
                    picture_quality_long1 = self.camera.acquire_picture_quality_long()
                    for x in range(picture_quality_long1):
                        picture_quality_name1 = self.camera.acquire_picture_quality_long(num=x)
                        quality_list1.append(picture_quality_name1)
                    print(quality_list1)
                    self.d.press("back")
                    time.sleep(3)
                    self.d.press("back")
                    for quality_names in quality_list1:
                        time.sleep(2)
                        print('>>>>>>>>>>>>>>>>>>>>>>正在寻找这个质量名称：' + quality_names)
                        self.camera.open_set()
                        time.sleep(1)
                        self.camera.click_operation(operation='照片质量')
                        time.sleep(2)
                        print('>>>>>>>>>>>>>>>>>>>>>>选择这个质量：' + quality_names)
                        self.camera.click_picture_quality(quality_names)
                        time.sleep(2)
                        print('点击快门')
                        self.camera.Photograph()
                        time.sleep(5)
        return result




    def Case_Shoot_video(self):
        result='Pass'
        times=0
        video_time_name_list=[]
        self.camera.VideoMode()
        self.camera.open_set()
        self.camera.click_operation(operation='视频持续时间')
        video_time_long=self.camera.acquire_picture_quality_long()

        for long_num in range(video_time_long):
            video_time_names=self.camera.acquire_picture_quality_long(num=long_num)
            video_time_name_list.append(video_time_names)
        self.d.press("back")
        time.sleep(2)
        self.d.press("back")
        for video_time_name in video_time_name_list:
            self.camera.open_set()
            self.camera.click_operation(operation='视频持续时间')
            time.sleep(2)
            print('>>>>>>>>>>>>>>>>>>>>>点击选择视频的持续时间')
            self.camera.click_picture_quality(video_time_name)
            print(video_time_name)
            if video_time_name=='30 秒 (MMS)':
                times=33
            elif video_time_name=='10 分钟':
                times=603
            elif video_time_name=='30 分钟':
                times=1803
            else:
                break
            time.sleep(3)
            self.camera.open_set()
            self.camera.click_operation(operation='视频画质')
            video_image_quality=self.camera.acquire_picture_quality_long()
            self.d.press("back")
            time.sleep(2)
            self.d.press("back")
            for i in range(video_image_quality):
                self.camera.open_set()
                self.camera.click_operation(operation='视频画质')
                video_image_quality_name=self.camera.acquire_picture_quality_long(num=i)
                time.sleep(2)
                print('>>>>>>>>>>>>>>>>>>>>>点击选择视频画质:'+video_image_quality_name)
                self.camera.click_picture_quality(video_image_quality_name)
                print('>>>>>>>>>>>>>>>>>>>>>点击录制视频')
                self.camera.Photograph()
                time.sleep(times)
        return result

    def Teardown(self):
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.camera.CameraOff()
        return end_time

    def run(self):
        print('#######  现在开始跑测试照片质量的case  ######')
        start_time1=self.setup()
        actul_reselt=''
        path=''
        try:
            result1=self.Case_Camera_Quality()
        except BaseException as e:
            result1='Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：跑测试照片质量" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "跑测试照片质量" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.camera.CameraOff()
            self.d.app_stop_all()
        end_time1=self.Teardown()
        self.camera_report_details.append(
            {"t_module": "相机", "t_case": "压力测试", "t_steps": "打开相机，对所有照片质量点击拍照",
             "t_expected_result": "1.可以正常拍照，结果需要手工查看 \n 2.请手工验证照片质量",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})
        time.sleep(5)

        print('################  现在开始跑测试分辨率的case  #################')
        start_time2=self.setup()
        actul_reselt=''
        path=''
        try:
            result2=self.Case_Camera_Pixel()
        except BaseException as e:
            result2 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：跑测试照片尺寸" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\'+ "跑测试照片尺寸" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.camera.CameraOff()
            self.d.app_stop_all()

        end_time2=self.Teardown()
        self.camera_report_details.append(
            {"t_module": "相机", "t_case": "压力测试", "t_steps": "打开相机，对所有分辨率点击拍照",
             "t_expected_result": "1.可以正常拍照，结果需要手工查看 \n 2.请手工验证照片尺寸",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time2, "t_end_time": end_time2,
             "t_reference_result": result2, "t_result": ""})
        time.sleep(5)

        print('##########################  现在开始跑测试分辨率和照片质量组合的case  ##########################')
        start_time3=self.setup()
        actul_reselt=''
        path=''
        try:
            result3=self.Case_Combination_Pixel_Quality()
        except BaseException as e:
            result3 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：跑测试照片尺寸和照片质量组合" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "跑测试照片尺寸和照片质量组合" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.camera.CameraOff()
            self.d.app_stop_all()
        end_time3=self.Teardown()
        self.camera_report_details.append(
            {"t_module": "相机", "t_case": "压力测试", "t_steps": "打开相机，对分辨率和照片质量组合选择进行拍照",
             "t_expected_result": "1.可以正常拍照，结果需要手工查看 \n 2.请手工验证照片质量和照片尺寸的组合照片",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time3, "t_end_time": end_time3,
             "t_reference_result": result3, "t_result": ""})
        time.sleep(5)

        print('##########################  现在开始跑视频的不同画质不同时长的case  ##########################')
        print('##########################  这个case的时间很长，大概在五个小时左右  ##########################')
        start_time4=self.setup()
        actul_reselt=''
        path=''
        try:
            result4=self.Case_Shoot_video()
        except BaseException as e:
            result4 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：跑视频的不同画质不同时长" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "跑视频的不同画质不同时长" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.camera.CameraOff()
            self.d.app_stop_all()
        end_time4=self.Teardown()
        self.camera_report_details.append(
            {"t_module": "相机", "t_case": "压力测试", "t_steps": "打开相机，录制不同画质的视频和不同的时长",
             "t_expected_result": "1.视频可以正常播放，画质显示正确 \n 2.请手工验证拍摄的视频",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time4, "t_end_time": end_time4,
             "t_reference_result": result4, "t_result": ""})
        time.sleep(5)
        print('###############################  测试结束  ###############################')
        return self.camera_report_details


