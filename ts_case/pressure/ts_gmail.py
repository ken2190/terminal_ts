from src.gmail import Gmail
from datetime import datetime
from time import sleep
from src.general import image_comparison
from src.general import adb
import datetime
import os
from src import loginfo
from src.settings import Settings

class Ts_Gmail():
    def __init__(self, d):
        self.d = d
        self.gmail = Gmail(self.d)
        self.path = image_comparison.get_path()
        self.log_data = []
        self.settings = Settings(d)
        self.gmail_report_details = []

    def set_up(self, casename):
        print(casename)
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        self.gmail.stop()
        self.d.app_stop_all()
        self.settings.auto_connect_wifi()
        self.gmail.start()
        adb.get_meminfo(self.d)
        adb.get_battery(self.d)
        adb.get_cpuinfo(self.d)
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.d.screenshot(self.path + "image\\gmail\\" + casename + nowTime + ".jpg")
        self.d.screen_on()
        return time


    def case1(self, num= 151):
        '''
        连续发送带附件的邮件
        '''
        result = "fail"
        status = False
        if self.gmail.detection_got_it():
            status = True
        else:
            if self.gmail.add_oth_addresses():
                status = True
        if status:
            start_unread_number = self.gmail.get_unread()
            for i in range(num):
                self.d.screen_on()
                if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                    self.d.unlock()
                    self.gmail.start()
                self.gmail.write_gmail()
                self.gmail.gmail_click_pop()
                self.gmail.gmail_add_addressee()
                self.gmail.gmail_add_subject()
                self.gmail.gmail_add_details()
                self.gmail.gmail_attachment()
                self.gmail.gmail_add_attachment()
                self.gmail.attachment_open_file()
                self.gmail.gmail_click_pop()
                self.gmail.gmail_send()
                sleep(3)
            for i in range(5):
                if self.gmail.check_outbox():
                    end_unread_number = self.gmail.get_unread()
                    if end_unread_number == "99+":
                        result = "pass"
                        break
                    else:
                        if int(end_unread_number) - int(start_unread_number) == num:
                            result = "pass"
                            break
                else:
                    sleep(60)
        else:
            result = "fail"
            err_msg = "连接到服务异常，请手动尝试"
            img_name = self.path + "gmail\\" + err_msg + ".jpg"
            self.d.screenshot(img_name)
            print(err_msg)
            self.gmail.stop()
        return result



    def tear_down(self, casename):
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.d.screenshot(self.path + "image\\gmail\\"+casename + nowTime+".jpg")
        adb.get_meminfo(self.d )
        adb.get_battery(self.d )
        adb.get_cpuinfo(self.d )
        self.gmail.stop()
        print(casename)
        return time

    def run(self):
        count = 2

        actual_result = ""
        err_path = ""
        starttime1 = self.set_up("开始测试：不间断发送"+str(count)+"封带附件邮件")
        try:
            t_reference_result1 = self.case1(count)
        except BaseException as e:
            t_reference_result1 = "fail"
            print("except:", e)
            actual_result = str(e)[7:]
            print("=====>>>>>执行测试：不间断发送"+str(count)+"封带附件邮件；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            err_path = self.path + "image\\gmail\\不间断发送"+str(count)+"封带附件邮件；出现异常.jpg"
            self.d.screenshot(err_path)
            self.gmail.stop()
            self.d.app_stop_all()
        endtime1 = self.tear_down("结束测试：不间断发送"+str(count)+"封带附件邮件")
        self.gmail_report_details.append({"t_module": "邮件", "t_case": "压力测试", "t_steps": "不间断发送"+str(count)+"封带附件邮件 ", "t_expected_result": "邮件发送成功，收件人成功接收到所有发送的邮件",
         "t_actual_result": actual_result + "\n" + err_path, "t_start_time": starttime1, "t_end_time": endtime1, "t_reference_result": t_reference_result1, "t_result": ""})
        sleep(2)

        return self.gmail_report_details