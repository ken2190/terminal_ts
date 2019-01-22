import uiautomator2 as u2
import time

def unlock(unlockyard,d):         #:param unlockyard: 传入解锁方式 0：无解锁   1：滑动解锁   code 传入状态码
        d.screen_on()
        if unlockyard==0:
            pass
        elif unlockyard==1:
            d.unlock()

def detection1(assert1,d):#判断界面元素 传入判断的内容和手机的状态码
        '''
        :param assert1: 传入参数   brighten：判断亮屏后的界面   unlock1：判断进入解锁界面
        :return: 返回元素是否存在返回一个bool类型
        '''

        if assert1=='brighten':     #断言屏幕是否先要向上滑动才能打开图案解锁界面，如果是就执行向上滑动
            d.screen_on()
            time1 = d(resourceId="com.android.systemui:id/clock_view").wait(timeout=1.0)#定位的是屏幕上的时间
            if time1 == True:
                d.swipe(0.492, 0.805, 0.525, 0.247)
            else:
                pass
                print('没有该元素，没有在亮屏界面，可能改变了亮屏上面的元素，还有可能直接在解锁图案界面')
        elif assert1=='unlock1':        #断言是否进入解锁界面
            a=d(text="紧急呼救").wait(timeout=10.0)
            if a==False:
                print('没有进入输入图形密码界面，可能机器卡顿请在试一次')
            return a

def pattern(pattern1,d):      #传入解锁样式只支持：L  N  G  Z  和状态码
        if pattern1=='L':
            d.swipe_points([(0.206, 0.479), (0.216, 0.795), (0.778, 0.802)])#l
        elif pattern1=='N':
            d.swipe_points([(0.219, 0.481), (0.221, 0.796), (0.778, 0.484), (0.778, 0.795)])#n
        elif pattern1=='G':
            d.swipe_points([(0.206, 0.479), (0.216, 0.795), (0.778, 0.802), (0.783, 0.484), (0.502, 0.481), (0.5, 0.637)])#g
        elif pattern1=='Z':
            d.swipe_points([(0.206, 0.479), (0.785, 0.479), (0.221, 0.797), (0.788, 0.8)])#z
        else:
            print('暂不支持这个解锁方式')

def patternunlock(pattern2,d):     #输入解锁图案：L N Z G   传入手机的状态码
        detection1('brighten',d)           #调用上面的函数，处理亮屏后的界面
        if detection1('unlock1',d)==True:  #判断是否进入了解锁界面
            pattern(pattern2,d)
            error=d(text="图案错误").wait(timeout=10.0)
            if error==True:
                print('解锁图案输入错误，有可能图案传入错误，传入的图案不是手机正确解锁的图案，有可能手机型号发生变化，也可能系统反应异常，请在试一次')

def detection2(assert1,d):#判断界面元素 code 手机的状态码
    '''
    :param assert1: 传入参数   brighten：判断亮屏后的界面   unlock1：判断进入解锁界面
    :return: 返回元素是否存在返回一个bool类型
    '''
    if assert1=='brighten':     #断言屏幕是否先要向上滑动才能打开PIN解锁界面，如果是就执行向上滑动
        d.screen_on()
        time1 = d(resourceId="com.android.systemui:id/clock_view").wait(timeout=1.0)#定位的是屏幕上的时间
        if time1 == True:
            d.swipe(0.492, 0.805, 0.525, 0.247)
        else:
            pass
            print('没有该元素，没有在亮屏界面，可能改变了亮屏上面的元素，还有可能直接在PIN解锁界面')
    elif assert1=='unlock1':        #断言是否进入解锁界面
        a=d(text="紧急呼救").wait(timeout=10.0)
        if a == False:
            print('没有进入输入PIN码界面，可能机器卡顿请在试一次')
        return a

def PINyard(num,d):          #传入一个四位数的PIN code 传入手机的状态码
    num=str(num)
    detection2('brighten',d)
    if detection2('unlock1',d)==True:
        num = list(num)
        for i in num:
            d(resourceId="com.android.systemui:id/digit_text", text=i).click()
        error=d(text="PIN码有误").wait(timeout=1.0)
        if error==True:
            print('密码输入错误，可能是传入密码与设置密码不符，请再试一次')

def detection3(assert1,d):#判断界面元素  code传入手机的状态码
    '''
    :param assert1: 传入参数   brighten：判断亮屏后的界面   unlock1：判断进入解锁界面
    :return: 返回元素是否存在返回一个bool类型
    '''
    if assert1=='brighten':     #断言屏幕是否先要向上滑动才能打开密码解锁界面，如果是就执行向上滑动
        d.screen_on()
        time1 = d(resourceId="com.android.systemui:id/clock_view").wait(timeout=1.0)#定位的是屏幕上的时间
        if time1 == True:
            d.swipe(0.492, 0.805, 0.525, 0.247)
        else:
            pass
            print('没有该元素，没有在亮屏界面，可能改变了亮屏上面的元素，还有可能直接在密码解锁界面')
    elif assert1=='unlock1':        #断言是否进入解锁界面
         a=d(text="紧急呼救").wait(timeout=10.0)
         if a==False:
            print('没有进入输入密码界面，可能机器卡顿请在试一次')
         return a

def password(pw,d): #pw 传入手机密码  code 传入手机的状态码
    detection3('brighten',d)
    if detection3('unlock1',d)==True:
        d(resourceId="com.android.systemui:id/passwordEntry").send_keys(pw)
        d.click(0.89,0.896)
        error= d(text="密码错误").wait(timeout=10.0)
        if error==True:
            print('输入密码错误，可能是输入的密码和设置的密码没有对应，或者没有定位准确，请再试一次')


