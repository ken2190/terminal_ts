import random

import uiautomator2 as u2
import configparser
import time
import os
from src.message import *
from src.general.unlock import *
from src.general import image_comparison

class Pre_Message():

    def __init__(self,d):
        self.d=d
        self.path = image_comparison.get_path()
        self.message=Message1(self.d)
        self.message_Report_Details=[]
        self.error_list = []

    def Setup(self):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>停止所有运行的app')
        self.d.app_stop_all()
        self.message.start_message()
        time.sleep(5)
        print(start_time)
        return start_time

    def Storage_Message_SMS(self,num=500):
        '''
        新建短信，保存到终端
        :param num: 传入新建的数量
        :return:
        '''
        start_message_num = self.message.message_num()
        phone1=random.randint(10000, 90000)
        phone=139446
        result='Pass'
        for i in range(num):
            print('#####  第%s次新建短信  #####'%i)
            self.message.new_message()
            self.message.receiver(str(phone)+str(phone1))
            self.message.enter_message()
            if i%2==0:
                self.message.M_send()
            else:
                self.message.G_send()
            phone1+=1
            self.message.back()
        stop_message_num = self.message.message_num()
        if start_message_num+num==stop_message_num:
            print('添加短信成功')
        else:
            print('添加短信失败')
        return result

    def Storage_Message_MMS(self,num=250):
        start_message_num=self.message.message_num()
        phone1=random.randint(10000, 90000)
        phone=188446
        result='Pass'
        i=0
        while i<=num:
            print('#####  第%s次新建彩信  #####'%i)
            self.message.new_message()
            self.message.receiver(str(phone)+str(phone1))
            self.message.add_accessory()
            self.message.add_accessory_video()
            time.sleep(2)
            self.message.start_transcribe_cideo()
            self.message.back()
            time.sleep(3)
            toast = self.d.toast.get_message(5.0, 10.0)
            print('这是添加视频的toast：——' + toast)
            phone1+=1
            i+=1
            if i==num:
                break
            print('#####  第%s次新建彩信  #####' % i)
            self.message.new_message()
            self.message.receiver(str(phone) + str(phone1))
            self.message.add_accessory()
            self.message.add_accessory_music()
            self.message.select_music()
            self.message.add_accessory()
            self.message.add_accessory_music()
            self.message.select_music('Fluent')
            self.message.back()
            time.sleep(3)
            toast = self.d.toast.get_message(5.0, 10.0)
            print('这是添加音频的toast：——' + toast)
            phone1 += 1
            i+=1
            if i==num:
                break
            print('#####  第%s次新建彩信  #####' % i)
            self.message.new_message()
            self.message.receiver(str(phone) + str(phone1))
            for picture in range(6):
                self.message.add_accessory()
                self.message.add_accessory_picture()
                self.d(className="android.widget.ImageView", instance=3).click()
                time.sleep(2)
            self.message.back()
            time.sleep(3)
            toast = self.d.toast.get_message(5.0, 10.0)
            print('这是添加照片的toast：——' + toast)
            time.sleep(2)
            phone1 += 1
            i+=1
            if i==num:
                break
        stop_message_num = self.message.message_num()
        if start_message_num+num==stop_message_num:
            print('添加彩信数量正确')
        else:
            print('添加彩信数量错误')
            result='Fail'
        return result

    def delete_MMS_SMS(self,num=150):
        '''
        逐条删除信息
        :return:
        '''
        start_message_num = self.message.message_num()
        result = 'Pass'
        i=0
        while i<num:
            if self.message.wait_page_null() == True:
                print('##########  会话已为空  ##########')
                break
            print('---------->第%s次删除信息'%i)
            self.message.Longclick_message()
            self.message.click_delete()
            i+=1
        stop_message_num = self.message.message_num()
        print(start_message_num,i,stop_message_num)
        if start_message_num-i==stop_message_num:
            print('删除信息成功')
        else:
            print('删除信息失败')
            result='fail'
        return result

    def Delete_All(self):
        result='pass'
        print(">>>>>>>>>>>>>>>>>>>>删除所有短信")
        self.d(description=u"更多选项").click()
        delete_all=self.message.delete_all_message()
        if delete_all==True:
            self.message.delete_all_message(operation='click')
        else:
            print('>>>>>>>>>>>>>>>>>>>>会话已经为空')
        text=self.message.wait_page_null()
        if text==False:
            print('删除信息失败')
            result='FAIL'
        else:
            print('删除信息成功')

        return result

    def Teardown(self):
        self.message.stop_message()
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return end_time

    def run(self):
        start_time1 = self.Setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>开始添加彩信')
        try:
            result1 = self.Storage_Message_MMS()
        except BaseException as e:
            result1 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：添加彩信" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "添加彩信" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.message.stop_message()
            self.d.app_stop_all()
        end_time1 = self.Teardown()
        self.message_Report_Details.append(
            {"t_module": "信息", "t_case": "压力测试", "t_steps": "打开信息，添加250条彩信，彩信包含音频、视频和图片",
             "t_expected_result": "彩信可以正常添加",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})

        start_time2 = self.Setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>开始添加短信')
        try:
            result2 = self.Storage_Message_SMS()
        except BaseException as e:
            result2 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：添加短信" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "添加短信" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.message.stop_message()
            self.d.app_stop_all()
        end_time2 = self.Teardown()
        self.message_Report_Details.append(
            {"t_module": "信息", "t_case": "压力测试", "t_steps": "打开信息，添加500条短信，短信包含70个字符",
             "t_expected_result": "短信可以正常添加",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time2, "t_end_time": end_time2,
             "t_reference_result": result2, "t_result": ""})

        start_time3 = self.Setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>开始单条删除信息')
        try:
            result3 = self.delete_MMS_SMS()
        except BaseException as e:
            result3 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：单条删除信息" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "单条删除信息" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.message.stop_message()
            self.d.app_stop_all()
        end_time3 = self.Teardown()
        self.message_Report_Details.append(
            {"t_module": "信息", "t_case": "压力测试", "t_steps": "连续点击删除100条短信，50条彩信",
             "t_expected_result": "短信和彩信被删除",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time3, "t_end_time": end_time3,
             "t_reference_result": result3, "t_result": ""})

        start_time4 = self.Setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>开始删除所有信息')
        try:
            result4 = self.Delete_All()
        except BaseException as e:
            result4 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：删除所有信息" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "删除所有信息" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.message.stop_message()
            self.d.app_stop_all()
        end_time4 = self.Teardown()
        self.message_Report_Details.append(
            {"t_module": "信息", "t_case": "压力测试", "t_steps": " 删除所有短信和彩信",
             "t_expected_result": "所有短信和彩信同时被删除",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time4, "t_end_time": end_time4,
             "t_reference_result": result4, "t_result": ""})

        return self.message_Report_Details






































    # def Storage_Message(self,num):
    #     '''
    #     新建短信，保存到终端
    #     :param num: 传入新建的数量
    #     :return:
    #     '''
    #     result='Pass'
    #     config = configparser.ConfigParser()
    #     config.read(self.message.path())
    #     for add_message in range(num//4):
    #         print('#####  第%s组新建短信  #####'%add_message)
    #         for i in range(4):
    #             print('#####  第%s次新建短信  #####'%i)
    #             phone=config['message%s'%i]['phone']
    #             message=config['message%s'%i]['message']
    #             self.message.new_message()
    #             self.message.receiver(phone)
    #             self.message.enter_message(message)
    #             if i%2==0:
    #                 self.message.M_send()
    #             else:
    #                 self.message.G_send()
    #             self.message.back()
    #     return result
    #
    # def Storage_MMS(self,num):
    #     result = 'Pass'
    #     config = configparser.ConfigParser()
    #     config.read(self.message.path())
    #     for add_MMS in range(num//4):
    #         print('#####  第%s组新建彩信  #####' % add_MMS)
    #         for i in range(4):
    #             print('#####  第%s次新建彩信  #####' % i)
    #             self.message.new_message()
    #             phone = config['message%s' % i]['phone']
    #             message = config['message%s' % i]['message']
    #             self.message.receiver(phone)
    #             self.message.enter_message(message)
    #             for x in range(2):
    #                 self.message.add_accessory()
    #                 self.message.add_accessory_picture()
    #                 self.d(className="android.widget.ImageView", instance=3).click()
    #                 self.max=self.d(resourceId="android:id/alertTitle").wait(timeout=2)
    #                 if self.max==True:
    #                     self.d(resourceId="android:id/button1").click()
    #                     self.message.back()
    #                     break
    #             time.sleep(2)
    #             self.message.add_accessory()
    #             self.message.add_accessory_music()
    #             self.d(resourceId="android:id/text1", text='系统音频').click()
    #             self.d(resourceId="android:id/text1").click()
    #             self.d(resourceId="android:id/button1", text='确定').click()
    #             self.max = self.d(resourceId="android:id/alertTitle").wait(timeout=2)
    #             if self.max == True:
    #                 self.d(resourceId="android:id/button1").click()
    #                 self.message.back()
    #             time.sleep(2)
    #     return result
    #













# if i == 0:
#     for picture in range(6):
#         self.message.add_accessory()
#         self.message.add_accessory_picture()
#         self.d(className="android.widget.ImageView", instance=3).click()
#         time.sleep(2)
#         toast = self.d.toast.get_message(5.0, 10.0)
#         print('这是添加照片的toast：——' + toast)
#         time.sleep(2)
#     self.message.back()
# elif i == 1:
#     for music in range(3):
#         self.message.add_accessory()
#         self.message.add_accessory_music()
#         self.d(resourceId="android:id/text1", text='系统音频').click()
#         self.d(resourceId="android:id/text1").click()
#         self.d(resourceId="android:id/button1", text='确定').click()
#         time.sleep(2)
#         toast = self.d.toast.get_message(5.0, 10.0)
#         print('这是添加音频的toast：——' + toast)
#     self.message.back()
# elif i == 2:
#     self.message.add_accessory()
#     self.message.add_accessory_video()
#     time.sleep(2)
#     self.d(resourceId="org.codeaurora.snapcam:id/shutter_button").click()
#     self.play = self.d(resourceId="org.codeaurora.snapcam:id/btn_done", description='完成').wait(timeout=100)
#     if self.play == True:
#         self.d(resourceId="org.codeaurora.snapcam:id/btn_done", description='完成').click()
#         time.sleep(2)
#         toast = self.d.toast.get_message(5.0, 10.0)
#         print('这是添加视频的toast：——' + toast)
#     self.message.back()
# else:
#     pass