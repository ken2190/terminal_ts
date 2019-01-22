import os
import shutil
import time
from src.camtalk import *
from src.nictalk import *
from src.general import adb
from src.settings import *
class Init_Operation():

    def __init__(self):
        self.folder_list=['image','enter_resource']
        self.file_list=['adbLog','log','report']
        self.update_file_list = ['KHM_update', 'NCA_update']

    def get_path(self):
        '''
        指定到目录resource下面
        :return:返回完整目录
        '''
        path=os.path.abspath(os.path.dirname(os.getcwd()))
        return path


    def file_name(self,path1,x):
        '''
        获取指定目录下面的所有子目录或路径
        :param path1: 传入指定的路径
        :return: 返回指定路径下面的所有子目录
        '''
        path=self.get_path()+path1
        for root, dirs, files in os.walk(path):
            if x=='文件夹':
                return dirs
            elif x=='文件':
                return files
            # print(root)  # 当前目录路径
            # print(dirs)  # 当前路径下所有子目录
            # print(files)

    def adb_push(self):
        '''
        将指定目录下的视频和音乐push到手机上
        在执行case前需要保证手机上有视频和音乐
        :return:
        '''
        if adb.detection_terminal_connect()==True:
            print('---------->Push音乐与视频到手机')
            file_dir = self.get_path() + "\\resource\\resource\\video\\"
            for root, dirs, files in os.walk(file_dir):
                for i in files:
                    push='adb push '+ file_dir + i + ' /sdcard/video/'+ i+" >"+file_dir+"push.log"
                    print(push)
                    os.system(push)

    def init_equipment(self):
        '''
        初始化设备
        :return:
        '''
        print('\n\n---------->开始初始化设备')
        print('---------->提示：在init过程中手机会弹出一个提示框请手工点击确认')
        init = 'python -m uiautomator2 init'
        os.system(init)

    def init_equipment_operation(self):
        self.adb_push()
        self.init_equipment()
        time.sleep(2)
        adb.reboot_device()
        while True:
            if adb.detection_terminal_connect()==True:
                break
            else:
                time.sleep(60)

    def operation_folder(self):
        '''
        组合case先获取到当前目录下面的子目录将其删除
        然后在重现建目录
        :return:
        '''
        for folder_name in self.folder_list:
            # print(folder_name)
            if folder_name=='image':
                for j in self.file_name('\\resource\\'+folder_name,x='文件夹'):
                    shutil.rmtree(self.get_path() +'\\resource\\'+folder_name+'\\' +j)
                    os.mkdir(self.get_path() +'\\resource\\'+ folder_name+'\\' + j)
                continue
            elif folder_name=='enter_resource':
                for i in self.file_name('\\'+folder_name+'\\',x='文件夹'):
                    # print(i)
                    if i=='picture'or i=='package' or i == 'update_file':
                        continue
                    shutil.rmtree(self.get_path()+ '\\enter_resource\\' + '\\' + i)
                    os.mkdir(self.get_path() + '\\enter_resource\\' + '\\' + i)
                continue


    def operation_file(self):
        '''
        删除文件的操作
        :param path: 传入文件的父目录文件夹名称
        :return:
        '''

        for path in self.file_list:
            for j in self.file_name(path1='\\resource\\'+path,x='文件'):
                os.remove(self.get_path()+'\\resource\\'+path+'\\'+j)
        for path in self.update_file_list:
            for j in self.file_name(path1='\\enter_resource\\update_file\\'+path,x='文件'):
                os.remove(self.get_path()+'\\enter_resource\\update_file\\'+path+'\\'+j)



    def start_factory_pattern(self):
        pass

    def run(self):
        print('---------->开始执行初始化操作')
        print('---------->开始删除历史测试文件')
        self.operation_file()
        self.operation_folder()
        print('---------->删除历史测试文件完成')
        self.init_equipment_operation()




if __name__=='__main__':
    a=Init_Operation()
    a.run()









