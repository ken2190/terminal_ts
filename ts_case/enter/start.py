import uiautomator2 as u2
from ts_case.enter.case_enter import Case_Enter
from ts_case.enter.case_sim_enter import Case_SIM_Enter
from src import writer_report
from ts_case.report_datas import *
from src.settings import Settings
from ts_case.enter.case_external_software import External_software
from ts_case.enter.update import Update

import datetime


class Setup():
    def __init__(self, d ):
        self.d = d

    def setup(self):
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取测试开始的时间
        print("---------->>初始化已完成<<----------\n开始执行测试时间：" + self.start_time + "\n")


    def setdown(self, all_cases):
        print("\n---------->>测试已完成<<----------\n")
        report_datas = Report_Datas(self.d)                     # 初始化 获取测试设备版本信息等数据
        report_datas.get_end_time()                             # 获取测试结束时间
        report_details = Report_Details()                       # 初始化 获取测试case数据方法
        report_datas.get_start_time(self.start_time)            # 获取测试开始时间
        report_details.add_case(all_cases)                      # 写入所有cases
        rep_details = report_details.get_report_details()       # 组合所有的case
        sum, success, failed = report_details.get_test_sum()    # 获取测试详情中的用例总数等信息
        path, rep_datas = report_datas.get_report_datas(sum, success, failed)       # 获取所有测试报告总概括数据
        path = os.path.abspath(os.path.join(os.getcwd(), "../..")) + "\\enter_resource\\report\\enter_report.xlsx"
        writer_report.write(rep_datas, rep_details, path)  # 写入报告


if __name__ == "__main__":
    d = u2.connect()
    set = Setup(d)
    set.setup()


    all_cases = []

    # 执行入口测试（无需插卡）
    cases1 = Case_Enter(d).run()
    all_cases.append(cases1)

    #执行入口测试（需要插卡）
    print("\n\n未插卡用例已测试完成，请插入sim卡进行继续的测试\n若已插入sim卡请输入：ok\n\n")
    while True:
        end = input("请输入：")
        if end == "ok":
            phone_number = Settings(d).get_sims_number()
            m_number = Settings(d).get_mcwill_number()
            print(m_number)
            print(phone_number )
            if phone_number != "未插入SIM卡":
                cases2 = Case_SIM_Enter(d,phone_number).run()
                all_cases.append(cases2)
                break
            else:
                print("检查没有正常读到sim卡信息，无法进行后续测试")
                break
        else :
            print("输入错误，请确定是否已插入sim卡并重新输入：")



    # 执行入口测试（点击所有第三方apk）
    case3=External_software(d).run()
    all_cases.append(case3)
    #
    #执行手机的本地升级和恢复出厂设置操作
    case4=Update(d).run()
    all_cases.append(case4)




    set.setdown(all_cases)



