import uiautomator2 as u2
import os
import time
from src.camera import Camera
class Message1():

    def __init__(self,d):
        self.d=d
        self.camera=Camera(d)

    def __sleep(func):
        def inner(self):
            time.sleep(1)
            return func(self)
        return inner


    @__sleep
    def start_message(self):
        print('>>>>>>>>>>>>>>>>>>>>开启短信')
        self.d.app_start('com.android.mms',activity='.ui.ConversationList')

    @__sleep
    def stop_message(self):
        print('>>>>>>>>>>>>>>>>>>>>停止短信')
        self.d.app_stop('com.android.mms')

    @__sleep
    def new_message(self):
        print('>>>>>>>>>>>>>>>>>>>>点击新建短信')
        self.d(resourceId="com.android.mms:id/action_compose_new",description='新信息').click()


    def receiver(self,text='13033255568'):
        print('>>>>>>>>>>>>>>>>>>>>点击输入接收者')
        self.d(resourceId="com.android.mms:id/recipients_editor").set_text(text)

    def enter_message(self,text='fasongduanxin发送短信#￥……%&……*GFDVXZCZC215564d4s5a2fd5sa4fd2dc5发送短信发送短信发送短信发送短信发送短信发送短信'):
        print('>>>>>>>>>>>>>>>>>>>>点击输入短信内容')
        self.d(resourceId="com.android.mms:id/embedded_text_editor_btnstyle",text='键入信息').set_text(text)

    @__sleep
    def address_book(self):
        print('>>>>>>>>>>>>>>>>>>>>点击点击通讯录')
        self.d(resourceId="com.android.mms:id/recipients_picker").click()

    @__sleep
    def M_send(self):
        print('>>>>>>>>>>>>>>>>>>>>点击M网发送')
        self.d(resourceId="com.android.mms:id/second_send_button_sms_view",description='发送').click()

    @__sleep
    def G_send(self):
        print('>>>>>>>>>>>>>>>>>>>>点击G网发送')
        self.d(resourceId="com.android.mms:id/first_send_button_sms_view").click()

    def G_send_mms(self):
        print('>>>>>>>>>>>>>>>>>>>>点击G网发送彩信')
        self.d(resourceId="com.android.mms:id/first_send_button_mms_view").click()


    @__sleep
    def back(self):
        print('>>>>>>>>>>>>>>>>>>>>点击返回')
        self.d(resourceId="android:id/up").click()

    @__sleep
    def Longclick_message(self):
        print('>>>>>>>>>>>>>>>>>>>>长按信息')
        if self.d(resourceId="com.android.mms:id/empty").wait(timeout=2)==True:
            pass
        else:
            self.d(resourceId="com.android.mms:id/from").long_click(duration=1)

    def click_delete(self):
        print('>>>>>>>>>>>>>>>>>>>>点击删除')
        self.d(resourceId="com.android.mms:id/delete").click()
        if self.d(resourceId="android:id/alertTitle").wait(timeout=2)==True:
            print('>>>>>>>>>>>>>>>>>>>>确认删除')
            self.d(resourceId="android:id/button1").click()

    def message_num(self):
        print('>>>>>>>>>>>>>>>>>>>>获取当前信息数量')
        self.Longclick_message()
        if self.d(resourceId="com.android.mms:id/delete").wait(timeout=2)==False:
            return 0
        else:
            self.d(resourceId="com.android.mms:id/selection_menu").click()
            self.d(resourceId="com.android.mms:id/popup_list_title").click()
            message_num=self.d(resourceId="com.android.mms:id/selection_menu").get_text()
            str1 = str(message_num)[str(message_num).index(''):str(message_num).index(' 项')]
            self.d.press("back")
            return int(str1)




###########################################################################################################

    @__sleep
    def add_accessory(self):
        print('>>>>>>>>>>>>>>>>>>>>点击添加附件')
        self.d(resourceId="com.android.mms:id/add_attachment_second",description='附件').click()

    @__sleep
    def add_accessory_picture(self):
        print('>>>>>>>>>>>>>>>>>>>>点击添加附件照片')
        self.d(resourceId="com.android.mms:id/attachment_selector_text",text='照片').click()
        if self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").wait(timeout=2):
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()

    def add_accessory_photograph(self):
        '''
        点击添加附件拍照
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>点击添加附件拍照')
        self.d(resourceId="com.android.mms:id/attachment_selector_text", text=u"拍摄照片").click()
        self.camera.Pop_Up()
        self.d(resourceId="org.codeaurora.snapcam:id/shutter_button").click()
        time.sleep(3)
        self.d(resourceId="org.codeaurora.snapcam:id/btn_done").click()

    @__sleep
    def add_accessory_video(self):
        print('>>>>>>>>>>>>>>>>>>>>点击添加附件视频(录制视频)')
        self.d(resourceId="com.android.mms:id/attachment_selector_text", text=u"拍摄视频").click()


    def start_transcribe_cideo(self):
        print('>>>>>>>>>>开始录制视频')
        self.d(resourceId="org.codeaurora.snapcam:id/shutter_button").click()
        play = self.d(resourceId="org.codeaurora.snapcam:id/btn_done", description='完成').wait(timeout=100)
        if play == True:
            self.d(resourceId="org.codeaurora.snapcam:id/btn_done", description='完成').click()
    @__sleep
    def add_accessory_music(self):
        print('>>>>>>>>>>>>>>>>>>>>点击添加附件音频')
        self.d(resourceId="com.android.mms:id/attachment_selector_text", text=u"音频").click()


    def select_music(self,music='Brisk'):
        '''
        选择系统音频
        :param music: 传入音频名称
        :return:
        '''
        self.d(resourceId="android:id/text1", text='系统音频').click()
        self.d(resourceId="android:id/text1",text=music).click()
        self.d(resourceId="android:id/button1", text='确定').click()


    def wait_page_null(self):
        '''
        等待页面出现无会话
        :return:
        '''
        page=self.d(resourceId="com.android.mms:id/empty").wait(timeout=2)
        return page


    def delete_all_message(self,operation='wait'):
        '''
        删除所有的短信
        :return: 返回：True 或 False
        '''
        if operation=='wait':
            delete_all = self.d(resourceId="android:id/title", text=u"删除所有会话").wait(timeout=2)
            return delete_all
        elif operation=='click':
            self.d(resourceId="android:id/title", text=u"删除所有会话").click()
            if self.d(resourceId="android:id/alertTitle").wait(timeout=2) == True:
                print('>>>>>>>>>>>>>>>>>>>>确认删除')
                self.d(resourceId="android:id/button1").click()


    '''
    下面是短信的页面显示操作
    '''

    def page_message_number(self):
        '''
        获取当前短信页面的显示数量
        :return:
        '''
        number=self.d(resourceId="com.android.mms:id/unread_conv_count").get_text()
        return int(number)

    def acquire_message(self,message):
        '''
        获取短信状态
        :return:
        '''
        time.sleep(3)
        #获取新建短信状态信息
        if message=='status':
            len1=len(self.d(resourceId="com.android.mms:id/date_view"))
            get_text=self.d(resourceId="com.android.mms:id/date_view")[len1-1].get_text()
            return get_text
        #获取新建短信的内容信息
        elif message=='content':
            len2=len(self.d(resourceId="com.android.mms:id/text_view_buttom"))
            get_text=self.d(resourceId="com.android.mms:id/text_view_buttom")[len2-1].get_text()
            return get_text

    def acquire_MMS_message(self,i):
        print('---------->获取彩信的内容')
        message=self.d(resourceId="com.android.mms:id/text_view_buttom", className="android.widget.TextView", instance=i).get_text()
        return message

    def acquire_message_size(self,i):
        '''
        点击最后一条信息的详情
        :return:
        '''
        self.d(resourceId="com.android.mms:id/text_view_buttom", className="android.widget.TextView",instance=i).long_click(duration=1)
        self.d(description=u"更多选项").click()
        self.d(resourceId="android:id/title", text=u"信息详情").click()
        text=self.d(resourceId="com.android.mms:id/message_details").get_text()
        self.d.press("back")
        return text

    def wait_reception_time(self):
        for j in range(0,20):
            if '接收时间：' in self.acquire_message(message='status'):
                print('---------->已经接收到彩信')
                if self.acquire_MMS_message(i=0)==self.acquire_MMS_message(i=1):
                    print('---------->彩信内容验证正确')
                else:
                    print('---------->彩信内容验证错误')
                    return 'error'
                break
            else:
                time.sleep(10)
        if '接收时间：'not in self.acquire_message(message='status'):
            self.stop_message()
            return False

    def contrast_message(self,path):
        result_message=''
        result=True#self.wait_reception_time()
        if result==False:
            return '没有接收到短信'
        elif result=='error':
            return '彩信内容验证错误'
        else:
            time.sleep(5)
            # send_message_size = self.acquire_message_size(i=0)
            # reception_message_size=self.acquire_message_size(i=1)
            # self.write_file(path+'log_message\\adb_instruct.txt',send_message_size)
            # self.write_file(path + 'log_message\\adb_instruct2.txt', reception_message_size)
            file1=self.read_file(path+'log_message\\adb_instruct.txt')
            file2 = self.read_file(path + 'log_message\\adb_instruct2.txt')
            file2.pop(2)
            file2.pop(2)
            file1.pop(2)
            for i in range(len(file1)):
                if '接收者' not in file1[i]:
                    if file2[i] == file1[i]:
                        print('对比成功')
                    else:
                        print('对比失败')
                        result_message=result_message+file1[i]+'和'+file2[i]+'对比失败'
                else:
                    message_text1=file1[i].replace("接收者： ", '')
                    message_text2=file2[i].replace("发送者： ", '')
                    if message_text2 in message_text1:
                        print('对比成功')
                    else:
                        result_message = result_message + file1[i].replace("接收者： ", '') + '和' + file2[i].replace("发送者： ", '') + '对比失败'
            return result_message

    '''
    下面是文件的操作
    '''

    def write_file(self,path,file):
        '''
        写入文件
        :param path: 传入路径
        :param file: 传入文件
        :return:
        '''
        with open(path, 'w')as f:
            f.write(file+'\n')

    def read_file(self,path):
        '''
        读取文件
        :param path: 传入路径
        :return: 返回文件的内容 <-list->
        '''
        with open(path, 'r')as f:
            file1 = f.readlines()
            return file1



    '''
    下面是添加短信和验证短信的操作
    '''

    def Storage_Message_SMS(self,num=4):
        '''
        新建短信，保存到终端
        :param num: 传入新建的数量
        :return:
        '''
        start_message_num = self.message_num()
        phone1=10000
        phone=139446
        for i in range(num):
            print('#####  第%s次新建短信  #####'%i)
            self.new_message()
            self.receiver(str(phone)+str(phone1))
            self.enter_message()
            if i%2==0:
                self.M_send()
            else:
                self.G_send()
            self.back()
            phone1+=1
        time.sleep(5)
        stop_message_num = self.message_num()
        if start_message_num+num==stop_message_num:
            print('添加短信成功')
        else:
            print('添加短信失败')














    '''
    下面是更多选项操作
    '''


    @__sleep
    def more_select(self):
        print('>>>>>>>>>>>>>>>>>>>>点击更多选项')
        self.d(description=u"更多选项").click()

    @__sleep
    def add_theme(self):
        print('>>>>>>>>>>>>>>>>>>>>点击添加主题')
        self.d(resourceId="android:id/title",text='添加主题').click()

    @__sleep
    def Import_Template(self):
        print('>>>>>>>>>>>>>>>>>>>>点击导入模板')
        self.d(resourceId="android:id/title",text='导入模板').click()

    @__sleep
    def give_up(self):
        print('>>>>>>>>>>>>>>>>>>>>点击舍弃')
        self.d(resourceId="android:id/title",text='舍弃').click()

    @__sleep
    def set(self):
        print('>>>>>>>>>>>>>>>>>>>>点击设置')
        self.d(resourceId="android:id/title",text='设置').click()

    @__sleep
    def impute_theme(self,text):
        print('>>>>>>>>>>>>>>>>>>>>点击输入主题')
        self.d(resourceId="com.android.mms:id/subject",text='主题').set_text(text)


class message():
    def __init__(self,d):
        self.d=d

    def __sleep(func):
        def inner(self):
            time.sleep(1)
            return func(self)
        return inner


    @__sleep
    def start_message_instrument(self):
        print('>>>>>>>>>>>>>>>>>>>>开启短信工具')
        self.d.app_start(pkg_name='com.example.filleventtests')

    @__sleep
    def stop_message_instrument(self):
        print('>>>>>>>>>>>>>>>>>>>>关闭短信工具')
        self.d.app_stop(pkg_name='com.example.filleventtests')

    @__sleep
    def data_type(self):
        print('>>>>>>>>>>>>>>>>>>>>选择数据类型')
        self.d(resourceId="com.example.filleventtests:id/imageView1").click()

    @__sleep
    def click_MMS(self):
        print('>>>>>>>>>>>>>>>>>>>>点击彩信')
        self.d(resourceId="com.example.filleventtests:id/app_name").click()

    @__sleep
    def click_SMS(self):
        print('>>>>>>>>>>>>>>>>>>>>点击短信')
        self.d(resourceId="com.example.filleventtests:id/app_name", text=u"短信").click()

    @__sleep
    def click_linkman(self):
        print('>>>>>>>>>>>>>>>>>>>>点击联系人')
        self.d(resourceId="com.example.filleventtests:id/app_name", text=u"联系人").click()


    def input_number(self,num):
        print('>>>>>>>>>>>>>>>>>>>>输入新增的条数')
        self.d(resourceId="com.example.filleventtests:id/editText_Count").set_text(num)
        print('>>>>>>>>>>>>>>>>>>>>点击确定')
        self.d(resourceId="com.example.filleventtests:id/confirm").click()

    @__sleep
    def add_number(self):
        print('>>>>>>>>>>>>>>>>>>>>选择添加次数')
        self.d(resourceId="com.example.filleventtests:id/imageView2").click()

    @__sleep
    def operation_mode(self):
        print('>>>>>>>>>>>>>>>>>>>>选择操作方式')
        self.d(resourceId="com.example.filleventtests:id/imageView3").click()

    @__sleep
    def add_data(self):
        print('>>>>>>>>>>>>>>>>>>>>点击添加数据')
        self.d(resourceId="com.example.filleventtests:id/radioButton_Insert").click()
        print('>>>>>>>>>>>>>>>>>>>>点击确定')
        self.d(resourceId="com.example.filleventtests:id/confirm").click()

    @__sleep
    def examine_phone(self):
        print('>>>>>>>>>>>>>>>>>>>>选择查看手机')
        self.d(resourceId="com.example.filleventtests:id/imageView4").click()

    @__sleep
    def message_instrument_back(self):
        print('>>>>>>>>>>>>>>>>>>>>已进入手机数据界面，点击返回')
        self.d(resourceId="com.example.filleventtests:id/title_left_btn").click()

    @__sleep
    def start_add_message(self):
        print('>>>>>>>>>>>>>>>>>>>>开始生成数据')
        self.d(resourceId="com.example.filleventtests:id/imageView_Operation").click()
        schedule=self.d(resourceId="com.example.filleventtests:id/textView_Percent",text=100).wait(timeout=1000)
        if schedule==True:
            print('成功生成短信')
        pop_up = self.d(resourceId="android:id/alertTitle").wait(timeout=2)
        if pop_up == True:
            print('>>>>>>>>>>>>>>>>>>>>处理弹窗')
            self.d(resourceId="android:id/button1").click()
            self.d(resourceId="com.example.filleventtests:id/imageView_Operation").click()
            schedule = self.d(resourceId="com.example.filleventtests:id/textView_Percent", text=100).wait(timeout=1000)
            if schedule == True:
                print('成功生成数据')
        else:
            pass


    def Generate_SMS(self,num=500):
        '''
        生成短信
        :param num: 传入生成的数量
        :return:
        '''
        self.start_message_instrument()
        time.sleep(4)
        self.data_type()
        self.click_SMS()
        self.add_number()
        self.input_number(num)
        self.operation_mode()
        self.add_data()
        self.start_add_message()


    def Generate_MMS(self,num=500):
        '''
        生成彩信
        :param num: 传入生成的数量
        :return:
        '''
        self.start_message_instrument()
        time.sleep(4)
        self.data_type()
        self.click_MMS()
        self.add_number()
        self.input_number(num)
        self.operation_mode()
        self.add_data()
        self.start_add_message()


    def Generate_Linkman(self,num=1500):
        '''
        生成联系人
        :param num: 传入生成的数量
        :return:
        '''
        self.start_message_instrument()
        time.sleep(4)
        self.data_type()
        self.click_linkman()
        self.add_number()
        self.input_number(num)
        self.operation_mode()
        self.add_data()
        self.start_add_message()



if __name__=='__main__':
    d=u2.connect()
    a=Message1(d)
    path = "F:\\terminal_ts\\enter_resource\\"
    print(a.contrast_message(path))