import uiautomator2 as u2
from src.camera import Camera
from src.general.adb import *
from src.general.image_comparison import *
from src.general.unlock import *
from src.loginfo import writer_log
import time
import os
import xlwt
from src.general import adb
from src.general import image_comparison
from xlutils.copy import copy





class PressureCamera():


    def __init__(self,d):
        self.d=d
        self.camera=Camera(self.d)
        self.switchcamera=[]
        self.camera_report_details=[]
        self.path = image_comparison.get_path()
        self.facility = adb.read_adb("adb shell getprop ro.product.model")


    def setup(self):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>停止所有运行的app')
        self.d.app_stop_all()
        self.camera.CameraOff()
        self.d.press("home")
        time.sleep(5)
        print(start_time)
        return start_time


    def screenshot(self,picture_name,picture_name1,count):
        print(picture_name1)
        '''
        对比截图，传入两张图片的名称，对比的是两张不同名称的图片
        :param picture_name: 传入图片1的名称
        :param picture_name1: 传入图片2的名称
        :param count: 传入要对比的次数
        :return: 返回True或False
        '''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>开始对比图片')
        soucepath1 = self.path +'image\\picture\\'+ picture_name + '.jpg'
        for i in range(count):
            comparison1 = self.path +'image\\picture\\'+ picture_name + str(i) + '.jpg'
            print('第%s张图片对比，对比结果为：' % i)
            asserts = compare_image_with_hash(comparison1, soucepath1, max_dif=6)  # 对比图片
            if asserts == True:
                print('根据选择的精度对比图片，对比成功，图片相似度达到要求精度')
            elif asserts == False:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('根据选择的精度对比图片，对比失败，图片相似度没有达到要求精度')
                self.switchcamera.append('在第%s次切换图片到下一张时图片对比没有达到要求的精度：'%i+now_time + picture_name + str(i) + '.jpg')
                writer_log(self.path+'log\\'+ picture_name + '.txt', self.switchcamera)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>开始对比图片')
        soucepath = self.path+'image\\picture\\' + picture_name1 + '.jpg'
        for i in range(count):
            comparison = self.path+'image\\picture\\'+ picture_name1 + str(i) + '.jpg'
            print(soucepath,comparison)
            print('第%s张图片对比，对比结果为：' % i)
            asserts = compare_image_with_hash(comparison, soucepath, max_dif=6)  # 对比图片
            if asserts == True:
                print('根据选择的精度对比图片，对比成功，图片相似度达到要求精度')
            elif asserts == False:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('根据选择的精度对比图片，对比失败，图片相似度没有达到要求精度')
                self.switchcamera.append('在第%s次切换图片到上一张后，图片对比没有达到要求的精度：'%i+now_time + picture_name1 + str(i) + '.jpg')
                writer_log(self.path+'log\\' + picture_name1 + '.txt', self.switchcamera)


    def Case_Pre_SwitchCamera(self,count=100,picture_name='oncamera'):
        result = 'Pass'
        '''
        重复进入相机的压力测试
        :param count: 传入操作的次数。默认100次
        :param picture_name: 传入截图后的截图名称
        :return:
        '''
        self.camera.CameraOn()
        self.camera.Pop_Up()
        self.camera.PictureMode(facility=self.facility)
        self.camera.ClikeCentre()
        path = self.path+'image\\picture\\' + picture_name + '.jpg'
        self.d.screenshot(path)
        self.camera.CameraOff()
        for i in range(count):
            self.camera.CameraOn()
            self.camera.Pop_Up()
            time.sleep(1)
            self.camera.ClikeCentre()
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>开始截图')
            path = self.path+'image\\picture\\' + picture_name + str(i) + '.jpg'
            self.d.screenshot(path)
            time.sleep(1)
            self.camera.CameraOff()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>开始对比图片')
        soucepath = self.path+'image\\picture\\'+picture_name+'.jpg'
        for i in range(count):
            comparison = self.path+'image\\picture\\'+ picture_name + str(i) + '.jpg'
            print('第%s张图片对比，对比结果为：' % i)
            asserts=compare_image_with_hash(comparison, soucepath, max_dif=6)  # 对比图片
            if asserts==True:
                print('根据选择的精度对比图片，对比成功，图片相似度达到要求精度')

            elif asserts==False:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('根据选择的精度对比图片，对比失败，图片相似度没有达到要求精度')
                self.switchcamera.append('Case_Pre_SwitchCamera:'+'图片对比失败，图片没有达到要求的精度'+'\t'+now_time+picture_name+str(i)+'.jpg'+'\n')
                writer_log(self.path+'log\\'+picture_name+'.txt',self.switchcamera)
                result = 'fail'
        return result


    def Case_Pre_Photograph(self,count=100,picture_name='start_picturemode_photograph'):

        '''
        打开相机后，截图，然后重复拍照后在截图
        检测相机拍照之后的取景界面是否正常显示
        拍照完成之后将资源使用率获取
        '''
        result = 'Pass'
        self.camera.CameraOn()
        self.camera.Pop_Up()
        self.camera.PictureMode(facility=self.facility)
        time.sleep(2)
        self.camera.ScreenShot(picture_name,0)
        for i in range(count):
            self.camera.Photograph()
        self.camera.ScreenShot(picture_name,1)
        time.sleep(2)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>开始对比图片')
        soucepath = self.path + 'image\\picture\\' +picture_name +'0.jpg'
        print(soucepath)
        comparison = self.path+'image\\picture\\'+picture_name  + '1.jpg'
        print(comparison)
        print('第%s张图片对比，对比结果为：' % 1)
        asserts = compare_image_with_hash(comparison, soucepath, max_dif=5)  # 对比图片
        if asserts == True:
            print('根据选择的精度对比图片，对比成功，图片相似度达到要求精度')

        elif asserts == False:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('根据选择的精度对比图片，对比失败，图片相似度没有达到要求精度')
            self.switchcamera.append(' Case_Pre_Photograph:'+'图片精度对比失败，两张图片对比没有达到要求的精度'+now_time + picture_name + str(1) + '.jpg')
            writer_log(self.path+'log\\' + picture_name + '.txt', self.switchcamera)
            print(self.switchcamera)
            result='Fail'
        return result


    def Case_Pre_Switchover(self,count=100,):

        '''
        反复切换相机的照相模式和录像模式
        每一次切换都会进行截图
        做完操作后打印出资源使用率
        '''
        result = 'Pass'
        self.camera.CameraOn()
        self.camera.Pop_Up()
        for i in range(count):
            self.camera.PictureMode(facility=self.facility)
            self.camera.Menu()
            time.sleep(2)
            picture_size =self.camera.wait_picture_size()
            picture_quality = self.camera.wait_picture_quality()
            if picture_size and picture_quality  == True:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>成功进入到相机模式')
                self.d.click(0.757,0.459)
            else:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>没有进入到相机模式')
                self.camera.ScreenShot(' not_enter_camera_mode',i)
                error='在切换相机的操作中，第%s次没有进入相机模式'%i
                self.switchcamera.append(error)
                writer_log(self.path+'log\\' + 'picture_mode' + '.txt',self.switchcamera)
                result = 'Fail'
            self.camera.VideoMode()
            self.camera.Menu()
            video_quality = self.camera.wait_video_quality()
            video_time = self.camera.wait_video_time()
            if video_quality and video_time == True:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>成功进入到视频模式')
                self.d.click(0.757,0.459)
            else:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>没有进入到视频模式')
                self.camera.ScreenShot(' not_enter_video_mode', i)
                error1 = '在切换相机的操作中，第%s次没有进入视频模式' % i
                self.switchcamera.append(error1)
                writer_log(self.path+'log\\' + 'video_mode' + '.txt', self.switchcamera)
                result = 'Fail'
        return result


    def Case_Pre_SwitchMapdepot(self,count=100):

        '''
        重复进入退出图库，每次操作后进行截图
        默认进行100次，做完操作后打印资源使用率
        :return:
        '''
        result = 'Pass'
        self.camera.CameraOn()
        self.camera.Pop_Up()
        for i in range(count):
            self.camera.EnterInto()
            mp_depot=self.camera.wait_mp_depot()
            share=self.camera.wait_share()
            delete=self.camera.wait_delete()
            if mp_depot and share and delete==True:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>成功进入到图库')
            else:
                self.camera.ClikeCentre()
                mp_depot = self.camera.wait_mp_depot()
                share = self.camera.wait_share()
                delete = self.camera.wait_delete()
                if mp_depot and share and delete == True:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>成功进入到图库')
                else:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>没有进入到图库')
                    self.camera.ScreenShot(' not_enter_mopdepot', i)
                    error = '在切换图库的操作中，第%s次没有进入图库' % i
                    self.switchcamera.append(error)
                    writer_log(self.path+'log\\' + 'enterinto_photo' + '.txt', self.switchcamera)
            self.camera.Quit()
            quit_photo=self.camera.wait_camera_page()
            if quit_photo==True:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>成功退出图库')
            else:
                self.d.click(0.798,0.482)
                quit_photo = self.camera.wait_camera_page()
                if quit_photo == True:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>成功退出图库')
                else:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>没有退出图库')
                    self.camera.ScreenShot(' not_quit_mopdepot', i)
                    error1 = '在切换图库的操作中，第%s次没有退出图库' % i
                    self.switchcamera.append(error1)
                    writer_log(self.path+'log\\' + 'quit_photo' + '.txt', self.switchcamera)
                    result = 'Fail'
        return result


    def Case_Pre_SwitchImage(self,count=100):
        result = 'Pass'
        '''
        进入图库重复切换图片
        默认100次
        :param
        :return:
        '''
        self.camera.CameraOn()
        self.camera.Pop_Up()
        self.camera.EnterInto()
        delete = self.camera.wait_delete()
        if delete==True:
            self.d.click(0.757, 0.459)
        else:
            pass
        time.sleep(2)
        self.d.screenshot(self.path+'image\\picture\\'+'last_picture.jpg')
        time.sleep(2)
        self.camera.Next_picture()
        time.sleep(2)
        self.d.screenshot(self.path+'image\\picture\\' + 'next_picture.jpg')
        for i in range(count):
            self.camera.Last_Picture()
            time.sleep(1)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>开始截图')
            path = self.path+'image\\picture\\' + 'last_picture' + str(i) + '.jpg'
            self.d.screenshot(path)
            time.sleep(2)
            self.camera.Next_picture()
            time.sleep(1)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>开始截图')
            path = self.path+'image\\picture\\' + 'next_picture' + str(i) + '.jpg'
            self.d.screenshot(path)
            time.sleep(2)
        self.screenshot('last_picture','next_picture',count)
        return result


    def Case_Pre_Run_Out_Of_Memory(self):

        '''
        使用文件将手机内存填满
        使用相机拍照，检测拍照功能
        打印出资源的使用率
        :return:
        '''
        result = 'Pass'
        self.camera.CameraOn()
        self.camera.Pop_Up()
        self.camera.PictureMode(facility=self.facility)
        self.camera.Menu()
        picture_quality = self.camera.wait_picture_quality()
        picture_size = self.camera.wait_picture_size()
        if picture_quality and picture_size==True:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>内存满后相机界面正常')
            self.d.click(0.757, 0.459)
        else:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>内存满后没有正常进入相机界面')
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>开始截图')
            path = self.path+'image\\error_picture\\' + 'not_picturemode.jpg'
            self.d.screenshot(path)
            result = 'Fail'
        self.camera.VideoMode()
        self.camera.Menu()
        video_quality = self.camera.wait_video_quality()
        video_time = self.camera.wait_video_time()
        if video_quality and video_time==True:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>内存满后进入视频界面正常')
        else:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>内存满后没有正常进入视频界面')
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>开始截图')
            path = self.path+'image\\error_picture\\' + 'not_videomode.jpg'
            self.d.screenshot(path)
            result = 'Fail'
        return result

    def Teardown(self):
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.camera.CameraOff()
        get_meminfo(self.d)
        get_cpuinfo(self.d)
        get_battery(self.d)
        return end_time

    def run(self,i=100):
        '''
        每一条用例是默认次数100次
        在调用这个方法时可以传入运行次数，传入的次数是每条用例执行的次数
        如果想要单一调试某个需要在下面修改count的值
        :param i: 传入运行的次数
        :return:
        '''
        start_time1=self.setup()
        actul_reselt=''
        path=''
        try:
            result1=self.Case_Pre_SwitchCamera(count=i)
        except BaseException as e:
            result1='Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：打开相机，重复进入退出相机100次" + str(i) + "次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path + 'image\\error_picture\\' + "打开相机，重复进入退出相机100次" + str(i) + "次；出现异常.jpg"
            self.d.screenshot(path)
            self.camera.CameraOff()
            self.d.app_stop_all()
        end_time1=self.Teardown()
        self.camera_report_details.append(
            {"t_module": "相机", "t_case": "压力测试", "t_steps": "打开相机，重复进入退出相机100次",
             "t_expected_result": "1.可以正常进入或退出  \n 2.请手工验证是否正常进入退出相机，已截图",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})
        time.sleep(5)



        start_time2 = self.setup()
        actul_reselt=''
        path=''
        try:
            result2 =self.Case_Pre_Photograph(count=i)
        except BaseException as e:
            result2 = "fail"
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：打开相机截图，拍照100次截图" + str(i) + "次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\'+"打开相机截图，拍照100次截图" + str(i) + "次；出现异常.jpg"
            self.d.screenshot(path)
            self.camera.CameraOff()
            self.d.app_stop_all()
        end_time2 = self.Teardown()
        self.camera_report_details.append(
            {"t_module": "相机", "t_case": "压力测试", "t_steps": "打开相机截图，拍照100次截图",
             "t_expected_result": "1.界面显示正常，可正常拍照 \n 2.请手工验证相机的界面显示，已截图",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time2, "t_end_time": end_time2,
             "t_reference_result": result2, "t_result": ""})
        time.sleep(5)

        start_time3 = self.setup()
        actul_reselt=''
        path=''
        try:
            result3 =self.Case_Pre_Switchover(count=i)
        except BaseException as e:
            result3 = "fail"
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：打开相机，重复切换拍照和录像模式" + str(i) + "次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\'+"打开相机，重复切换拍照和录像模式" + str(i) + "次；出现异常.jpg"
            self.d.screenshot(path)
            self.camera.CameraOff()
            self.d.app_stop_all()
        end_time3 = self.Teardown()
        self.camera_report_details.append(
            {"t_module": "相机", "t_case": "压力测试", "t_steps": "打开相机，重复切换拍照和录像模式",
             "t_expected_result": "1.正常切换，相机录像机功能正常",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time3, "t_end_time": end_time3,
             "t_reference_result": result3, "t_result": ""})
        time.sleep(5)


        start_time4 = self.setup()
        actul_reselt=''
        path=''
        try:
            result4 =self.Case_Pre_SwitchMapdepot(count=i)
        except BaseException as e:
            result4 = "fail"
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：打开相机，重复进入退出相册" + str(i) + "次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\'+"打开相机，重复进入退出相册" + str(i) + "次;出现异常.jpg"
            self.d.screenshot(path)
            self.camera.CameraOff()
            self.d.app_stop_all()
        end_time4 = self.Teardown()
        self.camera_report_details.append(
            {"t_module": "相机", "t_case": "压力测试", "t_steps": "打开相机，重复进入退出相册",
             "t_expected_result": "1.每次查看图片都正常显示，无异常退出，报错等现象 \n 2.请手工验证是否正常进入退出相册，已截图",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time4, "t_end_time": end_time4,
             "t_reference_result": result4, "t_result": ""})
        time.sleep(5)


        start_time5 = self.setup()
        actul_reselt=''
        path=''
        try:
            result5 =self.Case_Pre_SwitchImage(count=i)
        except BaseException as e:
            result5 = "fail"
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：打开相机，重复切换照片" + str(i) + "次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\'+"打开相机，重复切换照片" + str(i) + "次；出现异常.jpg"
            self.d.screenshot(path)
            self.camera.CameraOff()
            self.d.app_stop_all()
        end_time5 = self.Teardown()
        self.camera_report_details.append(
            {"t_module": "相机", "t_case": "压力测试", "t_steps": "打开相机，重复切换照片",
             "t_expected_result": "1.每次查看图片都正常显示，无异常退出，报错等现象 \n 2.请手工切换图片是否正确，已截图",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time5, "t_end_time": end_time5,
             "t_reference_result": result5, "t_result": ""})
        time.sleep(5)


        start_time6 = self.setup()
        actul_reselt=''
        path=''
        try:
            result6 =self.Case_Pre_Run_Out_Of_Memory()
        except BaseException as e:
            result6 = "fail"
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：内存满时进入相机/拍照" + str(i) + "次；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\'+"内存满时进入相机拍照" + str(i) + "次；出现异常.jpg"
            self.d.screenshot(path)
            self.camera.CameraOff()
            self.d.app_stop_all()
        end_time6 = self.Teardown()
        self.camera_report_details.append(
            {"t_module": "相机", "t_case": "压力测试", "t_steps": "内存满时进入相机/拍照",
             "t_expected_result": "1.给出正确的提示内存满的信息 \n2.无花屏、死机等异常现象",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time6, "t_end_time": end_time6,
             "t_reference_result": result6, "t_result": ""})
        time.sleep(5)
        return self.camera_report_details


