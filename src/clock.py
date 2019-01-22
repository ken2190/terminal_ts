import time,datetime
import uiautomator2 as u2


class Clock():

    def __init__(self,d):
        self.d=d



    '''
    开启关闭时钟
    '''

    def start_clock(self):
        print('---------->开启时钟')
        self.d.app_start('com.android.deskclock')


    def stop_clock(self):
        print('---------->关闭时钟')
        self.d.app_stop('com.android.deskclock')


    '''
    进入时钟界面的操作
    '''


    def clock_menu(self,operation):
        '''
        点击始终顶部的菜单
        :param operation:传入菜单名称
        :return:
        '''
        self.d(description=operation).click()



    '''
    闹钟界面的操作
    '''


    def add_alarm(self):
        print('---------->添加一个闹钟')
        self.d(resourceId="com.android.deskclock:id/fab").click()



    '''
    设置闹钟界面
    '''


    def acquire_now_hour(self):
        print('---------->获取当前的时间：小时')
        hour=self.d(resourceId="android:id/hours").get_text()
        return hour

    def acquire_now_minute(self):
        print('---------->获取当前的时间：分钟')
        minute=self.d(resourceId="android:id/minutes").get_text()
        return minute

    def select_time(self,hour ,minute):
        time_minute=self.acquare_clock_time_minute()
        if int(time_minute)>=54:
            hour=int(hour)+1
        print('---------->选择时间：小时')
        self.d(description=int(hour)).click()
        time.sleep(3)
        print('---------->选择时间：分钟')
        print(minute)
        if int(minute)==59 and int(minute)==0:
            self.d(description='5').click()
            return str(hour)+':05'
        elif int(minute)>=54 and int(minute)<=58:
            self.d(description='0').click()
            if int(hour)<10:
                return '0'+str(hour)+':00'
            else:
                return str(hour) + ':00'
        else:
            click_minute = (int(minute) + 6) - (int(minute) + 1) % 5
            self.d(description=str(click_minute)).click()
            if int(click_minute)<10:
                return str(hour)+':0'+str(click_minute)
            else:
                return str(hour) + ':' + str(click_minute)


    def click_confirm(self):
        print('---------->点击确定')
        self.d(resourceId="android:id/button1").click()

    def delete_clock(self):
        print('---------->删除闹钟')
        for i in range(0,2):
            delete=self.d(resourceId="com.android.deskclock:id/delete").wait(timeout=3)
            if delete==True:
                self.d(resourceId="com.android.deskclock:id/delete").click()
                break
            else:
                self.d.swipe(0.691,0.904,0.52,0.083)
                self.d.click(0.596, 0.634)
                self.d.swipe(0.691, 0.904, 0.52, 0.083)
        if delete != True:
            return False







    '''
    闹钟响起时的操作
    '''

    def wait_suspend(self):
        print('---------->等待闹钟响起时的暂停按钮')
        suspend=self.d(resourceId="android:id/action0").wait(timeout=400)
        return suspend

    def wait_cancel(self):
        print('---------->等待闹钟响起时的取消按钮')
        cancel=self.d(resourceId="android:id/action0", text=u"取消").wait(timeout=400)
        return cancel

    def click_suspend(self):
        print('---------->点击暂停按钮')
        self.d(resourceId="android:id/action0").click()

    def click_cancel(self):
        print('---------->点击取消按钮')
        self.d(resourceId="android:id/action0", text=u"取消").click()

    '''
    获取文本
    '''

    def acquare_phone_time(self):
        print('---------->获取当前手机的时间文本')
        time=self.d(resourceId="com.android.systemui:id/time_view").get_text()
        return time

    def acquare_clock_time_minute(self):
        print('获取设置闹钟时显示的时间：分钟')
        time_minute=self.d(resourceId="android:id/minutes").get_text()
        return time_minute

    def acquare_clock_time_hour(self):
        print('获取设置闹钟时显示的时间：小时')
        time_hour=self.d(resourceId="android:id/hours").get_text()
        return time_hour









if __name__=='__main__':
    d=u2.connect()
    a=Clock(d)
    print(d(resourceId="com.android.systemui:id/time_view").get_text())



