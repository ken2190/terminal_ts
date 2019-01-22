import uiautomator2 as u2
import time
import datetime
from src.factory_pattern import *
from src.general.unlock import *
from src.general import image_comparison



class Ts_Factory_Pattern():

    def __init__(self, d):
        self.d=d
        self.factory=Factory_Pattern(self.d)
        self.path = image_comparison.get_path()
        self.log_data = []
        self.factory_report_details = []
        txtName = self.path+"mcWill.txt"
        self.f = open(txtName, "w")

    def set_up(self,casename):
        if self.factory.wait_facrory_pattern():
            pass
        else:
            self.factory.start()
        startTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        self.d.screenshot(self.path + "image\\music\\" + casename + startTime + ".jpg")

    def case1(self,count,sleeptime):
        for i in range(count):
            des = "第"+str(i)+"次复位"
            print(des)
            self.f.write(des)
            if self.factory.mcwill_restoration():
                time.sleep(sleeptime)
                end, msg = self.factory.mcwill_msg()
                print(msg)
                self.f.write(msg)
        self.f.close()


    def tear_down(self,casename):
        downTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.d.screenshot(self.path + "image\\music\\" + casename + downTime + ".jpg")
        print(casename)
        return time


if __name__ == "__main__":
    d = u2.connect()
    fp = Ts_Factory_Pattern(d)
    fp.set_up("测试McWill复位开始")
    fp.case1(100,20)
    fp.tear_down("测试McWill复位结束")
