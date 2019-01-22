from src.general import adb
import datetime
import os

class Report_Datas():
    def __init__(self,d):
        self.d = d
        self.report_data = {}
        self.report_data["build_number"] = adb.read_adb("adb shell getprop ro.build.display.id")
        self.report_data["model_number"] = adb.read_adb("adb shell getprop ro.product.model")
        self.report_data["android_version"] = adb.read_adb("adb shell getprop ro.build.version.release")

    def get_start_time(self,time):
        self. report_data["start_time"] = time


    def get_end_time(self):
        self. report_data["end_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def set_test_sum(self,sum, success, failed):
        self.report_data["case_sum"] = sum
        self.report_data["case_pass"] = success
        self.report_data["case_fail"] = failed
        pass_rate = int(int(success) / int(sum) * 100)
        self.report_data["pass_rate"] = str(pass_rate)+"%"
        print(self.report_data["pass_rate"])
        if pass_rate > 90:
            self.report_data["result"] = "PASS"
        else:
            self.report_data["result"] = "FAIL"




    def get_report_datas(self,sum, success, failed):
        self.set_test_sum(sum, success, failed)
        gpath = os.path.abspath(os.path.join(os.getcwd(), "../.."))
        path = gpath + "\\resource\\report\\report.xlsx"
        return path,self.report_data



class Report_Details():
    def __init__(self):
        self.report_details = {}
        self.cases = []

    def add_case(self,case):
        for i in case:
            for j in i:
                self.cases.append(j)

    def summarizing(self):
        test_success = 0
        test_failed = 0
        for i in self.cases:
            if i["t_reference_result"].upper() == 'PASS':
                test_success = test_success +1
            elif i["t_reference_result"].upper() == 'FAIL':
                test_failed = test_failed + 1
        self.report_details["info"] = self.cases
        self.report_details["test_sum"] = len(self.cases)
        self.report_details["test_success"] = test_success
        self.report_details["test_failed"] = test_failed


    def get_test_sum(self):
        return self.report_details["test_sum"], self.report_details["test_success"], self.report_details["test_failed"]


    def get_report_details(self):
        self.summarizing()
        return self.report_details