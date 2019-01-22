import uiautomator2 as u2
import time
class Record():
    def __init__(self,d):
        self.d=d

    def Start_Record(self):
        print('>>>>>>>>>>>>>>>>>>>>打开录音')
        self.d.app_start('com.android.soundrecorder',activity='.SoundRecorder')

    def Stop_Record(self):
        print('>>>>>>>>>>>>>>>>>>>>关闭录音')
        self.d.app_stop('com.android.soundrecorder')

    def Pop_up(self):
        while True:
            pop_up=self.d(resourceId="com.android.packageinstaller:id/permission_message",text='要允许录音机录制音频吗？').wait(timeout=2)
            if pop_up==True:
                print('>>>>>>>>>>>>>>>>>>>>处理弹窗')
                self.d(resourceId="com.android.packageinstaller:id/permission_allow_button",text='允许').click()
            if pop_up==False:
                break

    def Click_start_record(self):
        print('>>>>>>>>>>>>>>>>>>>>点击开始录音')
        self.d(resourceId="com.android.soundrecorder:id/recordButton").click()


    def Click_stop_record(self):
        print('>>>>>>>>>>>>>>>>>>>>点击停止录音')
        self.d(resourceId="com.android.soundrecorder:id/stopButton").click()


    def stop_record_select_yes(self):
        print('>>>>>>>>>>>>>>>>>>>>点击完成')
        self.d(resourceId="com.android.soundrecorder:id/acceptButton", text='完成').click()
        click_stop_pop_up = self.d(resourceId="com.android.packageinstaller:id/permission_message").wait(timeout=2)
        if click_stop_pop_up == True:
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button", text='允许').click()
            time.sleep(2)
            self.d(resourceId="android:id/button1", text='确定').click()
        else:
            self.d(resourceId="android:id/button1", text='确定').click()

    def stop_record_select_no(self):
        print('>>>>>>>>>>>>>>>>>>>>点击放弃')
        self.d(resourceId="com.android.soundrecorder:id/discardButton", text='放弃').click()
        time.sleep(2)
        self.d(resourceId="android:id/button1", text='确定').click()

    def Packaging_one(self,times):
        '''
        第一套录音操作
        打开录音、开始录音、录制一半暂停、再次开始录音、停止录音、点击放弃录音、关闭录音
        :param times: 传入录音时间
        :return:
        '''
        self.Start_Record()
        self.Click_start_record()
        self.Pop_up()
        time.sleep(times//2)
        self.Click_start_record()
        time.sleep(5)
        self.Click_start_record()
        time.sleep(times//2)
        self.Click_stop_record()
        self.Click_playback()
        time.sleep(times + 6)
        self.stop_record_select_no()
        self.Stop_Record()

    def Packaging_two(self,times):
        '''
        第二套录音操作
        打开录音、开始录音、录制一半暂停、再次开始录音、停止录音、点击完成保存录音、关闭录音
        :param times: 传入录音时间
        :return:
        '''
        self.Start_Record()
        self.Click_start_record()
        self.Pop_up()
        time.sleep(times//2)
        self.Click_start_record()
        time.sleep(5)
        self.Click_start_record()
        time.sleep(times// 2)
        self.Click_stop_record()
        self.Click_playback()
        time.sleep(times + 6)
        self.stop_record_select_yes()
        self.Stop_Record()

    def Packaging_three(self,times):
        '''
        第三套录音操作
        打开录音、开始录音、停止录音、不点击保存和放弃再次点击开始录音、停止录音、点击完成保存录音、关闭录音
        :param times: 传入录音的时间
        :return:
        '''
        self.Start_Record()
        self.Click_start_record()
        time.sleep(times)
        self.Click_stop_record()
        self.Click_start_record()
        time.sleep(times)
        self.Click_stop_record()
        self.stop_record_select_yes()
        self.Stop_Record()





    def Click_playback(self):
        print('>>>>>>>>>>>>>>>>>>>>点击回放')
        self.d(resourceId="com.android.soundrecorder:id/playButton").click()







if __name__=='__main__':
    d=u2.connect('f750eaf4')
    a=Record(d)
    a.Packaging_two(times=20)
    a.Packaging_one(times=20)


