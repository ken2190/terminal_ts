from src.settings import Settings
from src import writer_report
from ts_case.report_datas import *
from src import third_party
from src.factory_pattern import Factory_Pattern
import uiautomator2 as u2
class Setup:

    def __init__(self, d):
        self.d = d
        self.start_time = ""


    def setup(self):
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        # settings = Settings(self.d )
        # settings.display_setting()                                              # 设置休眠时间为最长时间
        # settings.auto_connect_wifi()                                            # 设置自动连接wifi
        # third_party.install_third_app()                                         # 安装所有resource\third_apk目录下的第三方apk
        # Factory_Pattern(self.d).start_log_run()                                 # 设置开启后台Log日志
        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 获取测试开始的时间
        print("---------->>初始化已完成<<----------\n开始执行测试时间："+self.start_time+"\n")


    def setdown(self,all_cases):
        print("\n---------->>测试已完成<<----------\n")
        report_datas = Report_Datas(self.d )                                   # 初始化 获取测试设备版本信息等数据
        report_datas.get_end_time()                                            # 获取测试结束时间
        report_details = Report_Details()                                      # 初始化 获取测试case数据方法
        report_datas.get_start_time(self.start_time)                           # 获取测试开始时间
        report_details.add_case(all_cases)                                     # 写入所有cases
        rep_details = report_details.get_report_details()                      # 组合所有的case
        sum, success, failed = report_details.get_test_sum()                   # 获取测试详情中的用例总数等信息
        path,rep_datas = report_datas.get_report_datas(sum, success, failed)   # 获取所有测试报告总概括数据
        writer_report.write(rep_datas, rep_details,  path)                     # 写入报告
