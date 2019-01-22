import os
import datetime

def __parameter():
    path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    path = path + "\\resource\\"
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return path, now_time

def get_path():
    path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    return path

def get_meminfo(d, filename='adb_meminfo.log'):
    '''
    查看指定apk的内存信息
    '''
    path, now_time = __parameter()
    apk = d.current_app()
    packageName = apk['package']
    logcmd =  "adb shell dumpsys meminfo "+packageName
    print(">>>>>>>>>>>>>>>>> 执行adb指令(查看指定apk的内存信息)：", logcmd)
    log_msg = ">>>>>>>>>>>>>>>>> 执行adb指令(查看指定apk的内存信息)："+packageName+"\n测试时间："+now_time+"\n"
    outcome = os.popen(logcmd).read()
    filepath = path +"adbLog\\"+ filename
    wirte_txt(filepath, log_msg, outcome)

def get_cpuinfo(d, filename='adb_cpuinfo.log'):
    '''
    查看指定apk的CPU信息
    '''
    path, now_time = __parameter()
    apk = d.current_app()
    packageName = apk['package']
    logcmd =  'adb shell dumpsys cpuinfo | find "' + packageName + '"'
    print(">>>>>>>>>>>>>>>>> 执行adb指令(查看指定apk的CPU信息)：", logcmd)
    log_msg = ">>>>>>>>>>>>>>>>> 执行adb指令(查看指定apk的CPU信息)："+packageName+"\n测试时间："+now_time+"\n"
    outcome = os.popen(logcmd).read()
    filepath = path +"adbLog\\"+ filename
    wirte_txt(filepath, log_msg, outcome)

def get_battery(d, filename='adb_battery.log'):
    '''
    查看指定apk的电量消耗信息
    '''
    path, now_time = __parameter()
    apk = d.current_app()
    packageName = apk['package']
    logcmd =  'adb shell dumpsys battery ' + packageName + ' | more'
    print(">>>>>>>>>>>>>>>>> 执行adb指令(查看指定apk的电量消耗信息)：", logcmd)
    log_msg = ">>>>>>>>>>>>>>>>> 执行adb指令(查看指定apk的电量消耗信息)："+packageName+"\n测试时间："+now_time+"\n"
    outcome = os.popen(logcmd).read()
    filepath = path +"adbLog\\"+ filename
    wirte_txt(filepath, log_msg, outcome)

def chmod_adb_logcat(directive,filename = "adb.log"):
    '''
    执行adb指令，并保存打印信息
    '''
    path, now_time = __parameter()
    print(">>>>>>>>>>>>>>>>> 执行adb指令：", directive)
    log_msg = ">>>>>>>>>>>>>>>>> 执行adb指令：" + directive + "\n测试时间：" + now_time + "\n"
    filepath = path + "adbLog\\" + filename
    outcome = os.popen(directive).read()
    wirte_txt(filepath, log_msg, outcome)

def chmod_adb(directive):
    '''
    执行任意adb指令
    '''
    print(">>>>>>>>>>>>>>>>> 执行adb_logcat指令：", directive)
    return os.system(directive)

def read_adb(directive):
    '''
    执行任意adb指令
    '''
    print(">>>>>>>>>>>>>>>>> 执行adb_logcat指令：", directive)
    return os.popen(directive).read()

def install_app(apk_name):
    '''
    安装 resource\third_apk 目录下的apk
    '''
    path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    apk_path = path + "\\resource\\third_apk\\" + apk_name
    adb = "adb install "+apk_path
    print(">>>>>>>>>>>>>>>>> 安装apk：", apk_name)
    return os.popen(adb).read()

def wirte_txt(filepath, log_msg, meminfo):
    f = open(filepath, 'a')                                 # 如果filename不存在会自动创建， 'a'表示写数据，文件指针将会放在文件的结尾，新的内容将会被写入到已有内容之后
    f.write(log_msg)
    f.write(meminfo)
    f.close()

def Install_Apk(path):
    for now_path,subdirectory,subfile in os.walk(path):
        for i in subfile:
            install_app='adb install '+path+"\\"+i
            os.system(install_app)

def acquire_versions():
    '''
    获取android手机版本
    :return:
    '''
    read_adb ="adb shell getprop ro.build.display.id >"+get_path()+"\\enter_resource\\log_message\\adb_instruct.txt"
    os.system(read_adb)

def acquire_battery_message(path):
    '''
    获取当前手机的电量信息
    :return:返回当前的电量信息
    '''
    #获取手机的电量信息
    battery=read_adb('adb shell dumpsys battery')
    #将信息写入文件
    with open(path+'log_message\\battery.txt','w') as f:
        f.write(battery)
    #将信息读取
    with open(path+'log_message\\battery.txt','r') as f:
        i=f.readlines()
        return int(i[16].strip('\n').replace("level:", ''))

def detection_terminal_connect():
    '''
    执行adb 指令获取设备是否连接
    :return: 返回：True为已连接 False:为未连接
    '''
    devices='adb shell getprop ro.build.version.release'
    connect_status = os.popen(devices).read()
    if len(connect_status) < 1:
        return False
    else:
        return True

def reboot_device():
    devices='adb reboot'
    connect_status = os.popen(devices).read()







