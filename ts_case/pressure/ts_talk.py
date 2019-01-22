import datetime
import uiautomator2 as u2
import time
from src.general import image_comparison
from src.nictalk import NicTalk
from src.camtalk import CamTalk
from src.general import adb
from src.general.unlock import *

class Ts_Talk:
    def __init__(self, d):
        self.d = d
        self.talk = None
        self.path = image_comparison.get_path()
        self.log_data = []
        self.Linkman_Report_Details=[]

    def set_up(self, casename):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print(casename)
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()

        nictalk = NicTalk(self.d)
        camtalk = CamTalk(self.d)

        nictalk.stop()
        camtalk.stop()
        nictalk.start()
        current = self.d.current_app()
        if current['package'] == "com.nictalk.start":
            self.talk = nictalk
        else:
            camtalk.start()
            current = self.d.current_app()
            if current['package'] == "com.nictalk.start":
                self.talk = nictalk
            elif current['package'] == "com.camtalk.start":
                self.talk = camtalk

        return start_time


    def add_linkman(self,num=1500):
        '''
        添加联系人
        :param num: 传入添加数量
        :return: 返回测试结果
        '''
        result='Pass'
        name='三'
        surnames = ['阿','巴','陈','度','娥','方','刚','胡','艾','杰','肯','兰','觅','籹','王']
        surname='张'
        number=10000
        phone=135000
        phone1=158000
        self.talk.click_calls()
        self.talk.click_contacts()
        for surname in surnames:
            for linkman_value in range(int(num/15)) :
                self.talk.contacts_right_drawable()
                self.talk.right_drawable_add_contact()
                self.d.set_fastinput_ime(True)
                self.talk.add_contact_name(name+str(linkman_value))
                self.talk.add_contact_surname(surname)
                self.talk.add_contact_phone_add()
                self.talk.add_contact_phone(str(phone)+str(number))
                self.talk.add_contact_phone(str(phone1) +str(number),1)
                self.talk.add_contact_email()
                self.talk.add_contact_address()
                self.talk.add_contact_accomplish()
                self.talk.add_contact_back()
                self.talk.contacts_search(surname+name+str(linkman_value))
                names=self.talk.linkman_text()
                print(names)
                if names==surname+name+str(linkman_value):
                    print('>>>>>>>>>>>>>>>>>>>>添加联系人成功')
                else:
                    print('>>>>>>>>>>>>>>>>>>>>添加联系人失败')
                    result='Fail'
                number+=1
        return result


    def delete_linkman(self,num=100):
        '''
        删除联系人挨个删除
        :param num: 传入删除的数量
        :return:
        '''
        result='Pass'
        self.talk.click_contacts()
        for delete_num in range(num,-1,-1):
            x = self.talk.contacts_search('get')
            self.d.set_fastinput_ime(True)
            st1 = str(x)[(str(x).index("索") + 1):str(x).index("位")]
            delete_name=self.talk.linkman_text()
            print('正在删除:'+delete_name)
            self.talk.select_linkman()
            toast = self.d.toast.get_message(5.0, 10.0, )
            print('这是删除联系人的toast-->' + toast)
            if toast=='删除好友成功':
                print('删除好友成功')
            else:
                print('删除好友失败')
                result='fail'
            x = self.talk.contacts_search('get')
            st2 = str(x)[(str(x).index("索") + 1):str(x).index("位")]
            if int(st1)-1==int(st2):
                print('>>>>>>>>>>>>>>>>>>>>删除联系人数量正确')
            else:
                print('>>>>>>>>>>>>>>>>>>>>删除联系人数量错误')
                result='Fail'
        return result

    def delete_all_linkman(self):
        '''
        删除所有联系人
        :return:
        '''
        result='Pass'
        self.talk.click_contacts()
        x=self.talk.contacts_search('get')
        self.d.set_fastinput_ime(True)
        st1 = str(x)[(str(x).index("索") + 1):str(x).index("位")]
        self.talk.long_click_linkman()
        select=self.talk.select_all_text()
        if select=='全不选':
            delete_pop_up=self.talk.delete_linkman()
            if delete_pop_up==True:
                self.talk.add_contact_back()
                x = self.talk.contacts_search('get')
                st2 = str(x)[(str(x).index("索") + 1):str(x).index("位")]
                if st2==0:
                    print('全部删除删除成功')
                else:
                    print('全部删除删除失败')
                    result='Fail'
        elif select=='全选':
            self.talk.all_select()
            delete_pop_up = self.talk.delete_linkman()
            if delete_pop_up == True:
                self.talk.add_contact_back()
                x = self.talk.contacts_search('get')
                st2 = str(x)[(str(x).index("索") + 1):str(x).index("位")]
                if int(st2) == 0:
                    print('全部删除删除成功')
                else:
                    print('全部删除删除失败')
                    result = 'Fail'
        return result

    def tear_down(self, casename):
        downTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.d.screenshot(self.path + "image\\talk\\" + casename + downTime + ".jpg")
        adb.get_meminfo(self.d)
        adb.get_battery(self.d)
        adb.get_cpuinfo(self.d)
        self.talk.stop()
        print(casename)
        return time



    def run(self):
        actul_reselt=''
        path=''
        start_time1=self.set_up('添加联系人开始')

        try:
            result1=self.add_linkman(num=300)
        except BaseException as e:
            result1 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：添加联系人的测试" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path + "image\\talk\\" + "添加联系人的测试" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.talk.stop()
            self.d.app_stop_all()
        end_time1=self.tear_down('添加联系人结束')
        self.Linkman_Report_Details.append(
            {"t_module":"手机联系人测试", "t_case": "压力测试", "t_steps": "1. 终端存有1500个联系人 \n 2. 联系人信息至少包含1个姓名、2个号码、1个email、1个地址",
             "t_expected_result": "1.联系人信息可以正常显示",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})
        time.sleep(5)

        start_time2=self.set_up('单独删除联系人开始')
        actul_reselt=''
        path=''
        try:
            result2=self.delete_linkman(num=100)
        except BaseException as e:
            result2 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：单独删除联系人" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path + "image\\talk\\" + "单独删除联系人" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.talk.stop()
            self.d.app_stop_all()
        end_time2=self.tear_down('单独删除联系人结束')
        self.Linkman_Report_Details.append(
            {"t_module": "手机联系人测试", "t_case": "压力测试", "t_steps": "1. 连续删除100联系人",
             "t_expected_result": "1. 要删除的联系人被删除",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time2, "t_end_time": end_time2,
             "t_reference_result": result2, "t_result": ""})
        time.sleep(5)


        start_time3=self.set_up('全部删除联系人开始')
        actul_reselt=''
        path=''

        try:
            result3=self.delete_all_linkman()
        except BaseException as e:
            result3 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：全部删除联系人" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path + "image\\talk\\" + "全部删除联系人" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.talk.stop()
            self.d.app_stop_all()
        end_time3=self.tear_down('全部删除联系人结束')
        self.Linkman_Report_Details.append(
            {"t_module":"手机联系人测试", "t_case": "压力测试", "t_steps": "1. 删除全部联系人",
             "t_expected_result": "1. 所有的联系人被删除",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time3, "t_end_time": end_time3,
             "t_reference_result": result3, "t_result": ""})
        time.sleep(5)





        return self.Linkman_Report_Details

