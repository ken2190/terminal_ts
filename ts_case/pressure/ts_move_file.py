import uiautomator2 as u2
from src.file_manager import *
from src.general.unlock import *
from src.loginfo import *
import time
from src.general import image_comparison


class Pre_Move_file():

    def __init__(self,d):
        self.d=d
        self.file_manager=File_Manager(self.d)
        self.Move_File_Manager_Report_Details=[]
        self.path = image_comparison.get_path()
        self.error_list = []

    def setup(self):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>停止所有运行的app')
        self.d.app_stop_all()
        self.file_manager.Off_File_Manager()
        self.file_manager.On_File_Manager()
        self.file_manager.refresh_file_manager()
        print(start_time)
        return start_time

    def Case_File_move(self,file_name,num=200,folder_name='video'):
        '''
        移动文件，这个case需要单独运行,需要在传输文件时接听电话
        :param file_name: 传入要移动的文件
        :param folder_name: 传入移动的文件夹，每次会自动创建
        :param num: 传入移动的次数
        :return:
        '''
        self.file_manager.All_Button()
        self.file_manager.refresh_file_manager()
        time.sleep(5)
        page_long = self.file_manager.page_number()
        result='Pass'
        count = 0
        for i in range(num):
            while True:
                print('##########  这是第%s次操作  ##########'%i)
                print('开始寻找要复制的文件：' + file_name)
                wait_file = self.file_manager.wait_file_name(file_name)
                if wait_file == True:
                    print('>>>>>>>>>>>>>>>>>>>>>>>找到了，长按这个文件：' + file_name)
                    self.file_manager.Long_Click(file_name)
                    self.file_manager.Click_Select()
                    self.file_manager.refresh_file_manager()
                    while True:
                        print('正在寻找目的地文件夹：'+folder_name )
                        move_file = self.file_manager.wait_file_name(folder_name)
                        if move_file == True:
                            print('>>>>>>>>>>>>>>>>>>>>>>>找到目的地文件夹，打开'+folder_name)
                            self.file_manager.wait_file_name(folder_name,operation='click()')
                            self.file_manager.open_operation()
                            self.file_manager.file_paste()
                            cover=self.file_manager.cover_file()
                            copy_file=self.file_manager.wait_copy_vanish()
                            while True:
                                if copy_file==False:
                                    print('寻找复制过来的文件，把它删掉：' + file_name)
                                wait_file1 = self.file_manager.wait_file_name(file_name)
                                if wait_file1 == True:
                                    print('长按复制过来的这个文件：' + file_name)
                                    self.file_manager.Long_Click(file_name)
                                    self.file_manager.Click_Delete()
                                    delete_file =self.file_manager.wait_now_operation()
                                    if delete_file==True:
                                        toast = self.d.toast.get_message(50.0, 1.0 )
                                        print('这是删除文件的toast：' + toast)
                                        self.file_manager.refresh_file_manager()
                                        print('##########  第%s次操作结束  ##########'%i)
                                        break
                                else:
                                    page_long1 = self.file_manager.page_number()
                                    start_text0 = self.file_manager.page_file_name(page_long1-2)
                                    self.d.swipe(0.683, 0.779, 0.808, 0.095)
                                    stop_text0 = self.file_manager.page_file_name(page_long1-2)
                                    if start_text0 == stop_text0:
                                        self.file_manager.refresh_file_manager()
                            if delete_file == True:
                                break
                        else:
                            page_long2 = self.file_manager.page_number()
                            start_text1 = self.file_manager.page_file_name(page_long2-2)
                            self.d.swipe(0.683, 0.779, 0.808, 0.095)
                            stop_text1 = self.file_manager.page_file_name(page_long2-2)
                            if start_text1 == stop_text1:
                                self.file_manager.refresh_file_manager()
                    if delete_file == True:
                        break
                else:
                    page_long3 = self.file_manager.page_number()
                    start_text2 = self.file_manager.page_file_name(page_long3 - 2)
                    self.d.swipe(0.683, 0.779, 0.808, 0.095)
                    print('page_long3 -2:', page_long3 -2)
                    page_long3 = self.file_manager.page_number()
                    stop_text2 = self.file_manager.page_file_name(page_long3 -2)
                    print(start_text2,stop_text2)
                    if start_text2 == stop_text2:
                        self.file_manager.refresh_file_manager()
                        count = count + 1
                        if count == 2:
                            self.file_manager.new_file(file_name)
                            count = 0
        return result

    def Teardown(self):
        self.d.app_stop("com.android.music")
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.file_manager.Off_File_Manager()
        writer_log(self.path+ 'log\\file.log.txt', self.error_list)
        print('错误日志：', self.error_list)
        return end_time

    def run(self,file_name='wlan.log'):
        start_time1 = self.setup()
        actul_reselt=''
        path=''
        try:
            result1=self.Case_File_move(file_name)
        except BaseException as e:
            result1 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：移动文件的测试" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "移动文件的测试" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time1 = self.Teardown()
        self.Move_File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器,在来电过程中移动文件的操作",
             "t_expected_result": "1.操作正常不会出现死机重启等异常现象",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})
        return self.Move_File_Manager_Report_Details



