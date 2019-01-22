import uiautomator2 as u2
import time
import datetime
import os
from src.general.image_comparison import *
import random
from src.general import adb
from src.general import image_comparison

class Camera():

    def __init__(self,d):
        self.d=d
        self.path = image_comparison.get_path()

    def __sleep(func):
        def inner(self):
            time.sleep(1)
            return func(self)
        return inner

    def ScreenShot(self, name, count):
        '''
        :param name: 传入图片的名称
        :param count: 传入int类型帮助截图去重,定义截图文件的编号
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>开始截图')
        path = self.path+'image\\picture\\' + name +str(count)+ '.jpg'
        self.d.screenshot(path)

    def Pop_Up(self,select='是'):
        '''
        针对首次打开相机的弹窗
        :param select:
        :return:
        '''
        pop = self.d(resourceId="android:id/alertTitle").wait(timeout=2)
        hint3 = self.d(text=u"OK").wait(timeout=2)
        if pop==True:
            if select=='是':
                self.d(resourceId="android:id/button1").click()
                hint3=self.d(text=u"OK").wait(timeout=2)
                if hint3==True:
                    self.d(text=u"OK").click()
            else:
                self.d(resourceId="android:id/button2").click()
                hint3 = self.d(text=u"OK").wait(timeout=2)
                if hint3 == True:
                    self.d(text=u"OK").click()
        else:
            if hint3==True:
                self.d(text=u"OK").click()

    @__sleep
    def ClikeCentre(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>点击中心')
        self.d.click(0.502,0.474)

    @__sleep
    def CameraOn(self):         #开启相机
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>打开相机')
        self.d.app_start('org.codeaurora.snapcam',activity='com.android.camera.CameraLauncher')

    @__sleep
    def CameraOff(self):        #关闭相机
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>关闭相机')
        self.d.app_stop('org.codeaurora.snapcam')

    def PictureMode(self,facility):      #切换到拍照模式
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>切换到拍照模式')
        wait = self.d(resourceId="org.codeaurora.snapcam:id/camera_switcher", description=u"相机、视频、全景模式选择器",className="android.widget.ImageView").wait(timeout=10)
        if wait == True:
            self.d(resourceId="org.codeaurora.snapcam:id/camera_switcher", description=u"相机、视频、全景模式选择器",
                   className="android.widget.ImageView").click()
            # self.facility=self.d.adb_shell('getprop ro.product.model')
            if 'C8' in facility:
                self.d(description=u"切换到拍照模式", className="android.widget.ImageView").click()
            else:
                self.d(description=u"切换到拍照模式", className="android.widget.ImageView", instance=1).click()
        else:
            self.d.click(0.798, 0.482)
            self.wait = self.d(resourceId="org.codeaurora.snapcam:id/camera_switcher", description=u"相机、视频、全景模式选择器",
                               className="android.widget.ImageView").wait(timeout=10)
            if self.wait == True:
                self.d(resourceId="org.codeaurora.snapcam:id/camera_switcher", description=u"相机、视频、全景模式选择器",
                       className="android.widget.ImageView").click()
                self.d(description=u"切换到拍照模式", className="android.widget.ImageView", instance=1).click()
            else:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>切换到相机模式失败，可能没有进入相机界面')

    @__sleep
    def VideoMode(self):        #切换到视频模式
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>切换到视频模式')
        self.wait=self.d(resourceId="org.codeaurora.snapcam:id/camera_switcher", description=u"相机、视频、全景模式选择器",className="android.widget.ImageView").wait(timeout=10)
        if self.wait==True:
            self.d(resourceId="org.codeaurora.snapcam:id/camera_switcher", description=u"相机、视频、全景模式选择器",className="android.widget.ImageView").click()
            self.d(description=u"切换到视频模式").click()
        else:
            self.d.click(0.798, 0.482)
            if self.wait==True:
                self.d(resourceId="org.codeaurora.snapcam:id/camera_switcher", description=u"相机、视频、全景模式选择器",
                       className="android.widget.ImageView").click()
                self.d(description=u"切换到视频模式").click()
            else:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>切换到视频模式失败，可能没有进入相机界面')

    '''
    下面是视频模式下面的操作
    '''

    def open_set(self):
        '''
        点击视频模式下的设置
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>点击设置')
        self.d(resourceId="org.codeaurora.snapcam:id/menu").click()

    def click_operation(self,operation):
        '''
        点击菜单选项
        :param operation: 输入操作的菜单
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>点击'+operation)
        self.d(resourceId="org.codeaurora.snapcam:id/title", text=operation).click()

    def select_video_time(self,time='30 秒 (MMS)'):
        '''
        选择视频的持续时间
        :param time: 传入时间：30 秒 (MMS)、10 分钟、30 分钟
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>点击选择视频的持续时间'+time)
        self.d(resourceId="org.codeaurora.snapcam:id/text", text=time).click()

    def select_video_quality(self,quality='HD 1080p'):
        '''
        选择视频画质
        :param quality: 输入视频画质
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>点击选择视频画质'+quality)
        self.d(resourceId="org.codeaurora.snapcam:id/text", text=quality).click()


    '''
    以下是照片和拍照的操作
    '''

    def wait_photo_album(self):
        album=self.d(resourceId="org.codeaurora.snapcam:id/preview_thumb").wait(timeout=3)
        return album



    @__sleep
    def Photograph(self):       #拍照
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>正在拍照/正在录制视频')
        self.d(resourceId="org.codeaurora.snapcam:id/shutter_button").click()


    @__sleep
    def EnterInto(self):       #进入查看图片
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>打开相册')
        wait=self.d(description=u"胶卷视图").wait(timeout=2)
        if wait==True:
            self.d(description=u"胶卷视图").click()
        else:
            self.Photograph()
            wait = self.d(description=u"胶卷视图").wait(timeout=2)
            if wait == True:
                self.d(description=u"胶卷视图").click()

    @__sleep
    def Quit(self):             #退出查看图片
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>退出相册')
        self.wait=self.d(description=u"back", className="android.widget.ImageButton").wait(timeout=2)
        if self.wait==True:
            self.d(description=u"back", className="android.widget.ImageButton").click()
        else:
            self.d.click(0.785, 0.446)
            self.wait = self.d(description=u"back", className="android.widget.ImageButton").wait(timeout=2)
            if self.wait == True:
                self.d(description=u"back", className="android.widget.ImageButton").click()

    @__sleep
    def Last_Picture(self):            #切换到上一张
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>切换照片到上一张')
        self.d.drag(0.079, 0.308, 0.915, 0.329,0.01)
        # self.ScreenShot('switch_picture_next',count)

    @__sleep
    def Next_picture(self):             #切换到下一张
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>切换照片到下一张')
        self.d.drag(0.915, 0.272, 0.089, 0.256,0.01)
        # self.ScreenShot('switch_picture_last',count)

    @__sleep
    def Menu(self):                                 #点击菜单按钮
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>点击菜单按钮')
        if self.d(description=u"菜单按钮").wait(timeout=3)==True:
            self.d(description=u"菜单按钮").click()
        else:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>没有菜单按钮')
            return False

    @__sleep
    def Menu_picture(self):                         #验证是否进入相机模式
        self.Menu()
        picture_menu=self.d(resourceId="org.codeaurora.snapcam:id/title", text=u"照片尺寸").wait(timeout=10)
        picture_menu1=self.d(resourceId="org.codeaurora.snapcam:id/title", text=u"照片质量").wait(timeout=10)
        if picture_menu and picture_menu1==True:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>成功进入到相机模式')
            self.d.click(0.795, 0.255)
        else:
            print('没有进入到相机模式')
            return False

    @__sleep
    def Menu_video(self):                           #验证是否进入了视频模式
        self.Menu()
        self.video_menu=self.d(resourceId="org.codeaurora.snapcam:id/title", text=u"视频画质").wait(timeout=10)
        self.video_menu1=self.d(resourceId="org.codeaurora.snapcam:id/title", text=u"视频持续时间").wait(timeout=10)
        if self.video_menu and self.video_menu1==True:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>成功进入到视频模式')
            self.d.click(0.795, 0.255)
        else:
            print('没有进入到视频模式')
            return False

    @__sleep
    def Camera_Set(self):#分辨率
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>点击设置')
        self.d(resourceId="org.codeaurora.snapcam:id/menu").click()

    def Delete_picture(self):
        '''
        删除图片
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>删除图片')
        self.delete=self.d(resourceId="com.android.gallery3d:id/photopage_bottom_control_delete").wait(timeout=1)
        if self.delete==True:
            self.d(resourceId="com.android.gallery3d:id/photopage_bottom_control_delete").click()
            self.d(resourceId="android:id/button1",text='确定').click()
        else:
            self.d.click(0.191,0.482)
            self.d(resourceId="com.android.gallery3d:id/photopage_bottom_control_delete").click()
            self.d(resourceId="android:id/button1", text='确定').click()

    @__sleep
    def Picture_Number_Name(self):
        '''
        获取照片编号
        :return:
        '''
        picture_number = self.d(className='android.widget.TextView').wait(timeout=2)
        if picture_number == True:
            picture_number_name = self.d(className='android.widget.TextView').get_text()
        else:
            self.d.click(0.191, 0.482)
            picture_number_name = self.d(className='android.widget.TextView').get_text()
        return picture_number_name


    '''
    下面是等待元素出现
    '''
    def wait_picture_size(self):
        '''
        等待照片尺寸按钮出现
        :return: 返回：True 或 False
        '''
        picture_size=self.d(resourceId="org.codeaurora.snapcam:id/title", text=u"照片尺寸").wait(timeout=10)
        return picture_size

    def wait_picture_quality(self):
        '''
        等待照片质量的出现
        :return: 返回：True 或 False
        '''
        picture_quality = self.d(resourceId="org.codeaurora.snapcam:id/title", text=u"照片质量").wait(timeout=10)
        return picture_quality

    def wait_video_quality(self):
        '''
        等待视频画质的出现
        :return: 返回：True 或 False
        '''
        video_quality = self.d(resourceId="org.codeaurora.snapcam:id/title", text=u"视频画质").wait(timeout=10)
        return video_quality

    def wait_video_time(self):
        '''
        等待视频持续时间出现
        :return: 返回：True 或 False
        '''
        video_time = self.d(resourceId="org.codeaurora.snapcam:id/title", text=u"视频持续时间").wait(timeout=10)
        return video_time

    def wait_flashlight(self):
        '''
        等待菜单栏的闪光灯出现
        :return:
        '''
        self.Menu()
        return self.d(text='闪光灯模式').wait(timeout=3)





    '''
    以下是进入图库需要的判断
    '''

    def wait_mp_depot(self):
        '''
        等待进入图库的按钮出现
        :return:  返回：True 或 False
        '''
        mp_depot = self.d(resourceId="com.android.gallery3d:id/photopage_bottom_control_edit").wait(timeout=10)
        return mp_depot

    def wait_share(self):
        '''
        等待分享的按钮出现
        :return:  返回：True 或 False
        '''
        share = self.d(resourceId="com.android.gallery3d:id/photopage_bottom_control_share").wait(timeout=10)
        return share

    def wait_delete(self):
        '''
        等待删除的按钮出现
        :return:  返回：True 或 False
        '''
        delete = self.d(resourceId="com.android.gallery3d:id/photopage_bottom_control_delete").wait(timeout=10)
        return delete

    def wait_camera_page(self):
        '''
        等待退出相机页面
        :return: 返回：True 或 False
        '''
        quit_photo = self.d(resourceId="org.codeaurora.snapcam:id/camera_switcher", description=u"相机、视频、全景模式选择器",
                            className="android.widget.ImageView").wait(timeout=10)
        return quit_photo


    '''
    下面是对拍照设置的操作
    '''
    def acquire_picture_size_long(self,num=None):
        '''
        获取照片尺寸的长度
        :return: 返回照片尺寸的长度
        '''
        if num==None:
            long=len(self.d(resourceId="org.codeaurora.snapcam:id/text", className='android.widget.TextView'))
            return long
        else:
            picture_size_name=self.d(resourceId="org.codeaurora.snapcam:id/text", className='android.widget.TextView')[num].get_text()
            return picture_size_name

    def wait_pixel(self,pixel):
        '''
        等待照片尺寸出现
        :param pixel: 传入尺寸名称
        :return:返回：True 或 False
        '''
        pixel = self.d(resourceId="org.codeaurora.snapcam:id/text", className='android.widget.TextView',
                       text=pixel).wait(timeout=3)
        return pixel


    def click_pixel(self,pixel):
        '''
        点击照片尺寸
        :param pixel:传入尺寸名称
        :return:
        '''
        self.d(resourceId="org.codeaurora.snapcam:id/text", className='android.widget.TextView', text=pixel).click()


    def acquire_picture_quality_long(self,num=None):
        '''
        获取照片质量的长度
        :return: 返回照片质量的长度
        '''
        if num==None:
            quality_long = len(self.d(resourceId="org.codeaurora.snapcam:id/text"))
            return quality_long
        else:
            quality_name = self.d(resourceId="org.codeaurora.snapcam:id/text")[num].get_text()
            return quality_name

    def click_picture_quality(self,quality_name):
        '''
        点击选择照片质量
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>>选择这个质量：' + quality_name)
        self.d(resourceId="org.codeaurora.snapcam:id/text", text=quality_name).click()

    def switch_camera(self):
        '''
        切换前后摄
        :return:
        '''
        if self.d(resourceId="org.codeaurora.snapcam:id/front_back_switcher").wait(timeout=3)==True:
            self.d(resourceId="org.codeaurora.snapcam:id/front_back_switcher").click()









if __name__=='__main__':
    d=u2.connect('148b4177')
    a=Camera(d)
    d(text='闪光灯模式').click()


