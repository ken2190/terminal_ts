import re
import uiautomator2 as u2
import os
import time
from src.loginfo import writer_log
from src.general.unlock import unlock
from src.file_manager import *
from src.music import *
from src.general import image_comparison
from src.settings import Settings

class Pre_file_manager():

    def __init__(self,d):
        self.d=d
        self.settings=Settings(self.d)
        self.path = image_comparison.get_path()
        self.file_manager=File_Manager(self.d)
        self.File_Manager_Report_Details=[]
        self.music=Music(self.d)
        self.error_list = []


    def setup(self):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.d.screen_on()
        if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
            self.d.unlock()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>停止所有运行的app')
        self.d.app_stop_all()
        self.file_manager.Off_File_Manager()
        self.file_manager.On_File_Manager()
        self.file_manager.refresh_file_manager()
        print(start_time)
        return start_time

    def Case_execute_operation(self,select_operation):
        '''
        文件夹的操作
        :param select_operation: 传入：属性、添加到书签、添加快捷方式、选择
        :return: 返回测试的结果
        '''
        result='Pass'
        gainpath = self.file_manager.Gain_Path()
        self.file_manager.All_Button()
        j = 0
        while True:  # 外层循环控制页面的切换，
            page_long = self.file_manager.page_number()
            print('当前页面显示数量为：%s' % int(page_long-1))
            page_file_name = self.file_manager.page_file_name(page_long-1)
            print('当前页面的最后一条数据为：' + page_file_name)
            for i in range(page_long):
                file_name = self.file_manager.page_file_name(i)
                print('这是当前的文件名称：' + file_name)
                self.file_manager.Long_Click(file_name)
                attribute = self.file_manager.wait_Attribute()
                select = self.file_manager.wait_Select()
                if attribute or select == True:  # 断言是否进入了文件夹或文件的菜单框
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>成功打开文件夹的操作界面')
                else:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>第%s页的第%s次没有打开文件夹的操作界面' % (j,i))
                    self.file_manager.ScreenShot(file_name + '第%s页的第%s次没有打开文件夹的操作界面' % (j,i))
                    self.file_manager.Click_Cancle()  # 如果没有进入的话，将截图保存到error__picture目录下
                    result = 'Fail'
                    self.error_list.append(file_name + '第%s页的第%s次没有打开文件夹的操作界面' % (j,i) + '\n')
                    continue
                if select_operation == '属性':
                    attribute_request = self.file_manager.case_Attribute(gainpath, file_name)
                    print(attribute_request)
                    if attribute_request == 'error':
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>第%s次没有进入属性界面' % i)
                        self.file_manager.ScreenShot(file_name + '第%s次没有打开文件夹的属性界面' % i)
                        result = 'Fail'
                        self.error_list.append(file_name + '第%s次没有打开文件夹的属性界面' % i + '\n')
                    elif attribute_request == False:
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>第%s次路径显示错误' % i)
                        self.file_manager.ScreenShot(file_name + '第%s次路径显示错误' % i)
                        result = 'Fail'
                        self.error_list.append(file_name + '第%s次路径显示错误' % i + '\n')
                        self.file_manager.affirm()
                elif select_operation == '添加到书签':
                    bookmark_request = self.file_manager.case_Add_Bookmark(file_name)
                    if bookmark_request == False:
                        self.error_list.append(file_name + '第%s次添加书签错误' % i + '\n')
                elif select_operation == '添加快捷方式':
                    shortcut = self.file_manager.case_Shortcut(file_name)
                    if shortcut == False:
                        self.error_list.append(file_name + '快捷方式创建失败')
                else:
                    print('没有该选项')
            time.sleep(3)
            print('第%s页检查完毕，拖动到下一页' % j)
            self.d.swipe(0.729, 0.8, 0.808, 0.095)
            time.sleep(1)
            page_long1 =self.file_manager.page_number()
            page_file_name2 = self.file_manager.page_file_name(page_long1-1)
            print('拖动之后页面显示数量为：',page_long1-1)  # @获取到拖动之后的页面的最后一条数据，与拖动之前的数据进行对比，如果相同，说明已经到达了最后一页方法将结束
            print('拖动之后页面数据最后一条是：' + page_file_name2)
            if page_file_name == page_file_name2:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>已经达到最后一页')
                break
            j += 1
        return result

    def Case_execute_operation__select(self):
        '''
        文件夹的操作
        :return: 返回测试的结果
        '''
        result='Pass'
        gainpath = self.file_manager.Gain_Path()
        self.file_manager.All_Button()
        j = 0
        while True:  # 外层循环控制页面的切换，
            page_long = self.file_manager.page_number()
            print('当前页面显示数量为：%s' % int(page_long-1))
            page_file_name = self.file_manager.page_file_name(page_long-1)
            print('当前页面的最后一条数据为：' + page_file_name)
            for i in range(page_long-1):
                file_name = self.file_manager.page_file_name(i)
                print('这是当前的文件名称：' + file_name)
                self.file_manager.Long_Click(file_name)
                attribute = self.file_manager.wait_Attribute()
                select = self.file_manager.wait_Select()
                if attribute or select == True:  # 断言是否进入了文件夹或文件的菜单框
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>成功打开文件夹的操作界面')
                else:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>第%s页的第%s次没有打开文件夹的操作界面' % (j,i))
                    self.file_manager.ScreenShot(file_name + '第%s页的第%s次没有打开文件夹的操作界面' % (j,i))
                    self.file_manager.Click_Cancle()  # 如果没有进入的话，将截图保存到error__picture目录下
                    result = 'Fail'
                    self.error_list.append(file_name + '第%s页的第%s次没有打开文件夹的操作界面' % (j,i) + '\n')
                    continue
                select=self.file_manager.case_Select(file_name)
                if select==False:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有选中文件夹')
                    self.file_manager.ScreenShot(file_name + '滑动第%s页的第%s次没有选中文件夹' % (j, i))
                    result = 'Fail'
                    self.error_list.append(file_name + '滑动第%s页的第%s次没有选中文件夹' % (j, i) + '\n')
            time.sleep(3)
            print('第%s页检查完毕，拖动到下一页' % j)
            self.d.swipe(0.729, 0.8, 0.808, 0.095)
            time.sleep(1)
            page_long1 =self.file_manager.page_number()
            page_file_name2 = self.file_manager.page_file_name(page_long1-1)
            print('拖动之后页面显示数量为：',page_long1-1)  # @获取到拖动之后的页面的最后一条数据，与拖动之前的数据进行对比，如果相同，说明已经到达了最后一页方法将结束
            print('拖动之后页面数据最后一条是：' + page_file_name2)
            if page_file_name == page_file_name2:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>已经达到最后一页')
                break
            j += 1
        return result

    def Case_Delete(self):
        '''
        这是一个单独的case
        删除文件或文件夹，删除是删除所有
        默认删除是从第一个开始,可以改变i的值来选择从第几个开始
        删除可以设置开始值不能设置结束值
        只要开始就会从开始位置全部删除
        :return:
        '''
        i=0
        result = 'Pass'
        while True:
            wait_first_name=self.file_manager.page_number(i)
            if wait_first_name==True:
                delete_text = self.file_manager.page_file_name(i)
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>删除文件夹：' + delete_text)
                self.file_manager.Long_Click(i,'num')
                attribute = self.file_manager.wait_Attribute()
                if attribute==True:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>成功打开了文件夹的菜单框')
                else:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有打开文件夹的菜单框:'+delete_text)
                    result='Fail'
                    self.error_list.append('没有打开文件夹的菜单框:'+delete_text)
                self.file_manager.Click_Delete()
                self.file_manager.wait_error_vanish()
                toast = self.d.toast.get_message(5.0, 10.0)
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是删除文件夹：' + delete_text + '的弹窗信息：' + toast)
                if toast!='操作已成功的完成.':
                    i+=1
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有删除可能涉及权限问题，不能删除')
            else:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>获取不到文件信息，已经全部删除')
                break
        return result

    def Case_Verify_Shortcut(self):
        '''
        这是一个单独的case，但是运行添加快捷方式的case
        验证所添加快捷方式，需要先为每个文件添加快捷方式之后运行
        添加快捷方式一定要对所有文件或文件夹添加
        这个case主要是验证所添加的快捷方式，也是先获取全部的文件夹或文件的名称
        最后根据这个写名称去桌面验证
        :return:
        '''
        result = 'Pass'
        self.file_manager.All_Button()
        sum = 0
        file = []
        while True:  # 外层循环控制页面的切换，
            long = self.file_manager.page_number()
            print('当前页面显示数量为：%s' % int(long))
            page_end_file_name = self.file_manager.page_file_name(long-2)
            print('当前页面的最后一条数据为：' +page_end_file_name )
            for i in range(long):
                page_all_file_name=self.file_manager.page_file_name(i)
                print('>>>>>>>>>>>>>>>>>>>>>将文件夹名称加到列表中' + page_all_file_name)
                file.append(page_all_file_name)
            print('第%s页检查完毕，拖动到下一页' % sum)
            self.d.swipe(0.729, 0.8, 0.808, 0.095)
            long1 = self.file_manager.page_number()
            page_end_file_name1=self.file_manager.page_file_name(long-2)
            print('拖动之后页面显示数量为：%s' % long1)  # @获取到拖动之后的页面的最后一条数据，与拖动之前的数据进行对比，如果相同，说明已经到达了最后一页方法将结束
            print('拖动之后页面数据最后一条是：' + page_end_file_name1)
            if page_end_file_name == page_end_file_name1:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>已经达到最后一页')
                break
            sum += 1
        list1 = (set(file))
        time.sleep(1)
        self.d.press("home")
        time.sleep(1)
        self.d.press("home")
        file1 = []
        time.sleep(2)
        while True:
            shortcut_first_name =self.file_manager.home_page(0)
            page_namber =self.file_manager.home_page()
            for j in range(page_namber - 1):
                home_page_all_shortcut_first_name = self.file_manager.home_page(j)
                file1.append(home_page_all_shortcut_first_name)
            print(file1)
            for i in file1:
                if i in list1:
                    time.sleep(1)
                    list1.remove(i)
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>成功检索到添加的快捷方式' + i)
                    self.d(text=i).click()
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>打开：'+i)
                    open_mode=self.file_manager.wait_home_page_file_open_mode()
                    if open_mode==True:
                        compile=self.file_manager.wait_home_page_file_open_mode_compile()
                        if compile==True:
                            self.file_manager.wait_home_page_file_open_mode_compile(operation='click')
                        else:
                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有打开此文件的应用')
                    else:
                        toast=self.d.toast.get_message(5.0, 10.0)
                        if toast=='没有任何与此类型文件关联的应用':
                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'+toast)
                    self.file_manager.ScreenShot('手工验证打开的快捷方式：'+i)
                    time.sleep(2)
                    self.d.press("home")
                    continue
            self.d.swipe(0.849, 0.502, 0.153, 0.5)
            shortcut_first_name1 = self.file_manager.home_page(0)
            if shortcut_first_name == shortcut_first_name1:
                if len(list1) != 0:
                    for i in list1:
                        self.error_list.append('文件夹没有全部添加快捷方式，没有添加快捷方式的文件夹为：' + i)
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>快捷方式没有全部添加，还剩余：', list1)
                    result = 'Fail'
                break
        return result

    def Case_Circulation_Set_Homepage(self):
        '''
        对所有文件夹或文件设置主页
        这是一个单独case，可直接运行
        首先获取全部的文件名称，然后根据文件名称寻找该文件
        找到之后对文件设置主页，设置完成后退出在进入验证；
        :return:
        '''
        result = 'Pass'
        self.gainpath = self.file_manager.Gain_Path()
        self.file_manager.All_Button()
        num = 0
        self.folder = []
        while True:  # 外层循环控制页面的切换，
            page_long = self.file_manager.page_number()
            print('当前页面显示数量为：%s' % page_long)
            page_end_file_name = self.file_manager.page_file_name(page_long-1)
            print('当前页面的最后一条数据为：' + page_end_file_name)
            for i in range(page_long):  # 内层循环控制当前页面所有文件文件夹的点击查看属性操作
                print('这是第%s个文件夹' % i)
                homepage_page_all_file_name = self.file_manager.page_file_name(i)
                print('这是当前的文件名称：' + homepage_page_all_file_name)
                self.file_manager.Long_Click(homepage_page_all_file_name)  # 长按文件或文件夹，打开他的菜单框
                homepapg =self.file_manager.wait_homepage()
                sum = self.file_manager.wait_sum()
                send =self.file_manager.wait_send()
                if homepapg == True:  # 断言是否进入了文件夹或文件的菜单框
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是一个文件夹')
                    self.folder.append(homepage_page_all_file_name)
                    self.file_manager.Click_Cancle()
                elif sum or send == True:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是一个文件')
                    self.file_manager.Click_Cancle()
                else:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有进入文件夹的菜单界面')
                    result = 'File'
                    self.error_list.append('没有进入文件夹的菜单界面' + homepage_page_all_file_name)
            print('第%s页检查完毕，拖动到下一页' % num)
            self.d.swipe(0.729, 0.8, 0.808, 0.095)
            page_long1=self.file_manager.page_number()
            page_all_file_name1=self.file_manager.page_file_name(int(page_long1-1))
            print('拖动之后页面显示数量为：%s' % int(page_long1-1))  # @获取到拖动之后的页面的最后一条数据，与拖动之前的数据进行对比，
            print('拖动之后页面数据最后一条是：' + page_all_file_name1)  # 如果相同，说明已经到达了最后一页方法将结束
            if homepage_page_all_file_name==page_all_file_name1:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>已经达到最后一页')
                break
            num += 1
        time.sleep(2)
        self.file_manager.refresh_file_manager()
        time.sleep(5)
        folder_name=list(set(self.folder))

        # 从这里开始遍历列表，获取所有文件夹的名称，根据文件夹的名称，进行点击设置主页
        while True:
            for j in folder_name:
                for n in range(num + 1):
                    print('正在寻找文件夹：' + j)
                    file_name = self.file_manager.wait_file_name(j=j)
                    if file_name == True:
                        self.file_manager.wait_file_name(j=j,operation='click')
                        self.file_manager.Click_Homepage()
                        toast = self.d.toast.get_message(5.0, 10.0)
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是' + j + '设置主页的弹框信息：' +toast)
                        self.file_manager.Off_File_Manager()
                        self.file_manager.On_File_Manager()
                        time.sleep(2)
                        self.file_manager.All_Button()
                        homepapg_top_file_name = self.file_manager.homepage_top_file_name(j)
                        print('进入文件后，主页顶部显示的主页文件夹：' + homepapg_top_file_name)
                        if homepapg_top_file_name == j:
                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>设置主页成功：' + j)
                            self.file_manager.refresh_file_manager()
                            folder_name.remove(j)
                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>当前列表还剩余：', folder_name)
                            break
                        else:
                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>设置主页失败：' + j)
                            self.file_manager.refresh_file_manager()
                    else:
                        start_file_name =self.file_manager.page_file_name(page_long-2)
                        self.d.swipe(0.729, 0.8, 0.808, 0.095)
                        end_file_name =self.file_manager.page_file_name(page_long-2)
                        if start_file_name==end_file_name:
                            self.file_manager.refresh_file_manager()
                if file_name == False:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>设置主页没有找到这个文件夹' + j)
                    folder_name.remove(j)
                    result = 'File'
                    self.error_list.append('设置主页没有找到这个文件夹' + j + '\n')
            if len(folder_name) == 0:
                print(self.error_list)
                break
        return result

    def Case_Ren(self, new_name='B'):
        '''
        这是一个单独的case
        对文件夹的重命名
        先遍历出所有的文件夹，然后对每个文件夹重命名，重命名之后在改变回来
        :return:
        '''
        self.file_manager.All_Button()
        result='Pass'
        sum = 0
        ren_File = []
        while True:  # 外层循环控制页面的切换，
            ren_start_long = self.file_manager.page_number()
            print('当前页面显示数量为：%s' % int(ren_start_long))
            last_end_name = self.file_manager.page_file_name(ren_start_long-1)
            print('当前页面的最后一条数据为：' + last_end_name)
            for end_num in range(ren_start_long):
                ren_name =self.file_manager.page_file_name(end_num)
                print('>>>>>>>>>>>>>>>>>>>>将文件夹名称加到列表中' + ren_name)
                ren_File.append(ren_name)
            print('第%s页检查完毕，拖动到下一页' % sum)
            self.d.swipe(0.729, 0.8, 0.808, 0.095)
            end_long = self.file_manager.page_number()
            next_end_name = self.file_manager.page_file_name(end_long-1)
            print('拖动之后页面显示数量为：%s' % end_long)  # @获取到拖动之后的页面的最后一条数据，与拖动之前的数据进行对比，如果相同，说明已经到达了最后一页方法将结束
            print('拖动之后页面数据最后一条是：' + next_end_name)
            if last_end_name == next_end_name:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>已经达到最后一页')
                break
            sum += 1
        ren_file = (list(set(ren_File)))
        self.file_manager.refresh_file_manager()
        time.sleep(5)
        print(ren_file)
        while True:
            for ren_folder in ren_file:
                print('正在寻找文件夹：' + ren_folder)
                self.file_name = self.file_manager.page_number()
                for n in range(sum + 1):
                    print('正在寻找文件夹：' + ren_folder)
                    wait_ren_file_name = self.file_manager.wait_file_name(ren_folder)
                    if wait_ren_file_name == True:
                        self.file_manager.wait_file_name(ren_folder,operation='click')
                        self.file_manager.Click_Ren()
                        self.file_manager.wait_error_vanish()
                        self.d.set_fastinput_ime(True)
                        self.d.send_keys(ren_folder + new_name)
                        self.d.set_fastinput_ime(False)
                        repetition_name = self.file_manager.wait_ren_element()
                        if repetition_name == True:
                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>取消重命名，名称与现有文件重复，点击取消')
                            self.file_manager.ScreenShot('重命名' + ren_folder + new_name + '时名称重复')
                            self.file_manager.Click_ren_cancle()
                            self.file_manager.Click_Cancle()
                            time.sleep(2)
                            ren_file.remove(ren_folder)  ################
                            print(ren_file)
                            break
                        else:
                            self.file_manager.Click_ren_confirm()
                            spring = self.file_manager.ren_spring_wait_vanish()
                            if spring == True:
                                toast = self.d.toast.get_message(10.0, 30.0)
                                print('>>>>>>>>>>>>>>>这是重命名' + ren_folder + '的toast：' + toast)
                                ren_file.remove(ren_folder)    #############
                                print(ren_file)
                                for new_folder_name in range(sum + 1):
                                    print('正在寻找改过名字后的文件夹：' + ren_folder + new_name)
                                    file_new_name = self.file_manager.wait_file_name(ren_folder+new_name)
                                    if file_new_name == True:
                                        self.file_manager.Long_Click(ren_folder + new_name)
                                        self.file_manager.Click_Ren()
                                        self.d.set_fastinput_ime(True)
                                        self.d.send_keys(ren_folder)
                                        self.d.set_fastinput_ime(False)
                                        time.sleep(3)
                                        repetition_name = self.file_manager.wait_ren_element()
                                        if repetition_name == True:
                                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>取消重命名，名称与现有文件重复，点击取消')
                                            self.file_manager.ScreenShot('重命名' + ren_folder + new_name + '时名称重复')
                                            self.file_manager.Click_ren_cancle()
                                            self.file_manager.Click_Cancle()
                                            time.sleep(2)
                                            break
                                        else:
                                            self.file_manager.Click_ren_confirm()
                                            toast = self.d.toast.get_message(10.0, 30.0)
                                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>修改回重命名' + ren_folder + new_name + '的toast：' + toast)
                                        break
                                    else:
                                        start_name =self.file_manager.page_file_name(ren_start_long-1)
                                        self.d.swipe(0.729, 0.8, 0.808, 0.095)
                                        end_name =self.file_manager.page_file_name(ren_start_long-1)
                                        if start_name==end_name:
                                            self.file_manager.refresh_file_manager()
                                if file_new_name == False:
                                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>重命名没有找到这个文件夹' + ren_folder)
                                    result = 'Fail'
                                    self.error_list.append('重命名没有找到这个文件夹' + ren_folder + '\n')
                                break
                    else:
                        start_name1 = self.file_manager.page_file_name(ren_start_long-1)
                        self.d.swipe(0.729, 0.8, 0.808, 0.095)
                        end_name1 = self.file_manager.page_file_name(ren_start_long-1)
                        if start_name1==end_name1:
                            self.file_manager.refresh_file_manager()
                if wait_ren_file_name == False:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>设置主页没有找到这个文件夹' + ren_folder)
                    ren_file.remove(ren_folder)
                    result = 'Fail'
                    self.error_list.append('重命名没有找到这个文件夹' + ren_folder + '\n')
            if len(ren_file) == 0:
                print('>>>>>  重命名结束  <<<<<')
                print(self.error_list)
                break
        return result

    def Case_Transcript(self):
        '''
        这是一个单独的case
        创建副本，获取每一个文件夹，然后根据名称，去点击创建副本
        :return:
        '''
        self.file_manager.All_Button()
        result='Pass'
        sum = 0
        transcript_File = []
        while True:  # 外层循环控制页面的切换，
            transcript_start_long = self.file_manager.page_number()
            print('当前页面显示数量为：%s' % int(transcript_start_long))
            last_end_name =self.file_manager.page_file_name(transcript_start_long-1)
            print('当前页面的最后一条数据为：' + last_end_name)
            for end_num in range(transcript_start_long):
                ren_name = self.file_manager.page_file_name(end_num)
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>将文件夹名称加到列表中' + ren_name)
                transcript_File.append(ren_name)
            print('第%s页检查完毕，拖动到下一页' % sum)
            self.d.swipe(0.729, 0.8, 0.808, 0.095)
            end_long = self.file_manager.page_number()
            next_end_name = self.file_manager.page_file_name(end_long-1)
            print('拖动之后页面显示数量为：%s' % end_long)  # @获取到拖动之后的页面的最后一条数据，与拖动之前的数据进行对比，如果相同，说明已经到达了最后一页方法将结束
            print('拖动之后页面数据最后一条是：' + next_end_name)
            if last_end_name == next_end_name:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>已经达到最后一页')
                break
            sum += 1
        transcript_file = (list(set(transcript_File)))
        self.file_manager.refresh_file_manager()
        time.sleep(5)
        print(transcript_file)
        while True:
            for transcript_folder in transcript_file:
                while True:
                    print('正在寻找文件夹：' + transcript_folder)
                    transcript_file_name = self.file_manager.wait_file_name(transcript_folder)
                    if transcript_file_name == True:
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>长按文件夹')
                        self.file_manager.wait_file_name(transcript_folder,operation='click')
                        self.file_manager.Click_Transcript()
                        toast1 = self.d.toast.get_message(400.0, 1.0)
                        pop_up=self.file_manager.transcript_pop_up_wait_vanish()
                        if pop_up==True:
                            toast=self.d.toast.get_message(400.0, 1.0)
                            print('这是创建副本的toast：'+toast)
                            if toast or toast1=='操作已成功的完成.':
                                print('创建副本成功:'+transcript_folder)
                                time.sleep(2)
                                transcript_file.remove(transcript_folder)
                                print(transcript_file)
                                break
                            else:
                                print('创建副本失败:'+transcript_folder)
                                result='Fail'
                                self.error_list.append('创建副本失败:'+transcript_folder)
                                transcript_file.remove(transcript_folder)
                                print(transcript_file)
                                break
                    else:
                        start_text =self.file_manager.page_file_name(transcript_start_long-1)
                        self.d.swipe(0.729, 0.8, 0.808, 0.095)
                        stop_text = self.file_manager.page_file_name(transcript_start_long-1)
                        if start_text == stop_text:
                            self.file_manager.refresh_file_manager()
                            break

                if transcript_file_name == False:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>创建副本没有找到这个文件夹' + transcript_folder)
                    result = 'Fail'
                    self.error_list.append('创建副本没有找到这个文件夹' + transcript_folder + '\n')
                    self.file_manager.refresh_file_manager()
                    break

            if len(transcript_file) == 0:
                print('>>>>>  创建副本结束  <<<<<')
                print(self.error_list)
                break
        return result

    def Case_delete_transcript(self):
        result='Pass'
        print('>>>>>开始删除副本<<<<<')
        self.file_manager.All_Button()
        transcript_list=[]
        sum = 0
        original_file=[]
        delete_transcript = []
        while True:  # 外层循环控制页面的切换，
            start_long = self.file_manager.page_number()
            print('当前页面显示数量为：%s' % int(start_long))
            last_end_name = self.file_manager.page_file_name(start_long-1)  # 获取当前页面的最后的一个文件或文件的名称
            print('当前页面的最后一条数据为：' + last_end_name)
            for end_num in range(start_long):
                ren_name = self.file_manager.page_file_name(end_num)
                print('>>>>>>>>>>>>>>>>>>>>>>将文件夹名称加到列表中' + ren_name)
                delete_transcript.append(ren_name)
            print('第%s页检查完毕，拖动到下一页' % sum)
            self.d.swipe(0.729, 0.8, 0.808, 0.095)
            end_long = self.file_manager.page_number()
            next_end_name = self.file_manager.page_file_name(end_long-1)
            print('拖动之后页面显示数量为：%s' % end_long)  # @获取到拖动之后的页面的最后一条数据，与拖动之前的数据进行对比，如果相同，说明已经到达了最后一页方法将结束
            print('拖动之后页面数据最后一条是：' + next_end_name)
            if last_end_name == next_end_name:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>已经达到最后一页')
                break
            sum += 1
        delete_transcript = (list(set(delete_transcript)))
        self.file_manager.refresh_file_manager()
        time.sleep(5)
        later_long=len(delete_transcript)
        print(delete_transcript)
        while True:
            for del_file_name in delete_transcript:
                if '- 副本' in del_file_name:
                    transcript_list.append(del_file_name)
                    print('这是一个副本，正在寻找：'+del_file_name)
                    delete_transcript_file_name = self.file_manager.wait_file_name(del_file_name)
                    for x in range(sum + 1):
                        print('正在寻找：' + del_file_name)
                        delete_transcript_file_name = self.file_manager.wait_file_name(del_file_name)
                        if delete_transcript_file_name == True:
                            self.file_manager.Long_Click(del_file_name)
                            self.file_manager.Click_Delete()
                            delete_transcript.remove(del_file_name)
                            break
                        else:
                            start_text = self.file_manager.page_file_name(start_long-1)
                            self.d.swipe(0.729, 0.8, 0.808, 0.095)
                            stop_text = self.file_manager.page_file_name(start_long-1)
                            if start_text == stop_text:
                                self.file_manager.refresh_file_manager()

                    if delete_transcript_file_name == False:
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>创建副本没有找到这个文件夹' + del_file_name)
                        result = 'Fail'
                        self.error_list.append('创建副本没有找到这个文件夹' + del_file_name + '\n')
                        self.file_manager.refresh_file_manager()
                        break
                else:
                    original_file.append(del_file_name)
                    delete_transcript.remove(del_file_name)
            if len(delete_transcript) == 0:
                print('源文件夹数量：%s' % len(original_file))
                print('添加的副本数量为：%s' % len(transcript_list))
                if original_file==transcript_list:
                    print('##########   删除副本成功，所有文件都已经成功创建副本。  ##########')
                print('##########  删除创建的副本结束  ##########')
                print(self.error_list)
                break
        return result

    def Case_Open_Mode(self):
        '''
        文件的打开方式测试，只测试用编辑器打开的
        打开之后截图
        音频文件和其他没有测试
        :return:
        '''
        self.file_manager.All_Button()
        result='Pass'
        sum = 0
        file_open_mode = []
        while True:  # 外层循环控制页面的切换，
            openmode_long = self.file_manager.page_number()
            print('当前页面显示数量为：%s' % openmode_long)
            end_file_openmode_name = self.file_manager.page_file_name(openmode_long-2)
            print('当前页面的最后一条数据为：' + end_file_openmode_name)
            for i in range(openmode_long):  # 内层循环控制当前页面所有文件文件夹的点击查看属性操作
                print('这是第%s个文件夹' % i)
                file_openmode_name = self.file_manager.page_file_name(i)
                print('这是当前的文件名称：' + file_openmode_name)
                self.file_manager.Long_Click(file_openmode_name)  # 长按文件或文件夹，打开他的菜单框
                homepapg = self.file_manager.wait_homepage()
                count_sum = self.file_manager.wait_sum()
                send = self.file_manager.wait_send()
                if homepapg == True:  # 断言是否进入了文件夹或文件的菜单框
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是一个文件夹')
                    self.file_manager.Click_Cancle()
                elif count_sum or send == True:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是一个文件')
                    file_open_mode.append(file_openmode_name)
                    self.file_manager.Click_Cancle()
                else:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有进入文件夹的菜单界面')
                    result = 'Fail'
                    self.error_list.append('没有进入文件夹的菜单界面' +file_openmode_name)
            print('第%s页检查完毕，拖动到下一页' % sum)
            self.d.swipe(0.729, 0.8, 0.808, 0.095)
            openmode_long1 = self.file_manager.page_number()
            end_file_openmode_name1= self.file_manager.page_file_name(openmode_long1-2)
            print('拖动之后页面显示数量为：%s' % openmode_long1)  # @获取到拖动之后的页面的最后一条数据，与拖动之前的数据进行对比，
            print('拖动之后页面数据最后一条是：' + end_file_openmode_name1)  # 如果相同，说明已经到达了最后一页方法将结束
            if end_file_openmode_name==end_file_openmode_name1:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>已经达到最后一页')
                self.file_manager.refresh_file_manager()
                sum += 1
                break

        time.sleep(5)
        distinct=set(file_open_mode)
        print(distinct)
        while True:
            for file_open_mode_name in list(distinct):
                print('正在寻找：'+file_open_mode_name)
                wait_file=self.file_manager.wait_file_name(file_open_mode_name)
                while True:
                    wait_file = self.file_manager.wait_file_name(file_open_mode_name)
                    if wait_file==True:
                        print('长按这个文件：'+file_open_mode_name)
                        self.file_manager.Long_Click(file_open_mode_name)
                        self.file_manager.OpenMode()
                        toast = self.d.toast.get_message(5.0, 0.1)
                        if toast=='没有任何与此类型文件关联的应用。':
                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这个文件不能打开'+file_open_mode_name)
                            distinct.remove(file_open_mode_name)
                            print(distinct)
                            break
                        else:
                            redact=self.file_manager.file_open_mode_wait_compile()
                            if redact==True:
                                self.file_manager.file_open_mode_wait_compile(operation='click')
                                time.sleep(5)
                                self.file_manager.ScreenShot('打开的文件，手动查看文件内容：'+file_open_mode_name)
                                self.file_manager.Back()
                                time.sleep(5)
                                self.file_manager.refresh_file_manager()
                                distinct.remove(file_open_mode_name)
                                print(distinct)
                                break
                            elif redact==False:
                                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有编辑器不能打开'+file_open_mode_name)
                                self.file_manager.Click_ren_cancle()
                                distinct.remove(file_open_mode_name)
                                print(distinct)
                                break
                    elif wait_file==False:
                        start_text = self.file_manager.page_file_name(openmode_long-2)
                        self.d.swipe(0.729, 0.8, 0.808, 0.095)
                        stop_text = self.file_manager.page_file_name(openmode_long-2)
                        if start_text == stop_text:
                            self.file_manager.refresh_file_manager()
            if len(distinct)==0:
                break
        return result

    def Case_Send_file(self):
        '''
        文件的发送操作，获取到所有文件名称，然后根据文件名称点击
        然后点击发送，只测试蓝牙发送，进入蓝牙界面截图，手工查看
        :return:
        '''
        self.file_manager.All_Button()
        result = 'Pass'
        sum = 0
        send_file_list = []
        while True:  # 外层循环控制页面的切换，
            send_file_page_long = self.file_manager.page_number()
            print('当前页面显示数量为：%s' % send_file_page_long)
            send_file_page_end_name = self.file_manager.page_file_name(send_file_page_long-1)  # 获取当前页面的最后的一个文件或文件的名称
            print('当前页面的最后一条数据为：' + send_file_page_end_name)
            for i in range(send_file_page_long):  # 内层循环控制当前页面所有文件文件夹的点击查看属性操作
                print('这是第%s个文件夹' % i)
                send_file_page_name = self.file_manager.page_file_name(i)
                print('这是当前的文件名称：' + send_file_page_name)
                self.file_manager.Long_Click(send_file_page_name)  # 长按文件或文件夹，打开他的菜单框
                homepapg = self.file_manager.wait_homepage()
                count_sum = self.file_manager.wait_sum()
                send = self.file_manager.wait_send()
                if homepapg == True:  # 断言是否进入了文件夹或文件的菜单框
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是一个文件夹')
                    self.file_manager.Click_Cancle()
                elif count_sum or send == True:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是一个文件')
                    send_file_list.append(send_file_page_name)
                    self.file_manager.Click_Cancle()
                else:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有进入文件夹的菜单界面')
                    result = 'Fail'
                    self.error_list.append('没有进入文件夹的菜单界面' + send_file_page_name)
            print('第%s页检查完毕，拖动到下一页' % sum)
            self.d.swipe(0.729, 0.8, 0.808, 0.095)
            send_file_page_long1 = self.file_manager.page_number()
            send_file_page_end_name1 = self.file_manager.page_file_name(send_file_page_long1 - 1)
            print('拖动之后页面显示数量为：%s' %  send_file_page_long1)  # @获取到拖动之后的页面的最后一条数据，与拖动之前的数据进行对比，
            print('拖动之后页面数据最后一条是：' + send_file_page_end_name1)  # 如果相同，说明已经到达了最后一页方法将结束
            if send_file_page_end_name == send_file_page_end_name1:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>已经达到最后一页')
                break
            sum += 1
        self.file_manager.refresh_file_manager()
        time.sleep(5)
        distinct = set(send_file_list)
        print(distinct)
        while True:
            for file_send_name in list(distinct):
                print('正在寻找：' + file_send_name)
                wait_send_file_name = self.file_manager.wait_file_name(file_send_name)
                while True:
                    wait_send_file_name = self.file_manager.wait_file_name(file_send_name)
                    if wait_send_file_name == True:
                        print('长按这个文件：' + file_send_name)
                        self.file_manager.Long_Click(file_send_name)
                        self.file_manager.Send_File()
                        toast = self.d.toast.get_message(10.0, 1)
                        if toast == '没有任何与此类型文件关联的应用。':
                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这个文件不能发送' + file_send_name)
                            distinct.remove(file_send_name)
                            print(distinct)
                            break
                        if self.file_manager.wait_bluetooth() == True:
                            self.file_manager.wait_bluetooth(operation='click')
                            self.file_manager.wait_bluetooth_send_pop_up()
                            time.sleep(5)
                            self.file_manager.ScreenShot('点击蓝牙发送，手动查看蓝牙界面：' + file_send_name)
                            self.d.press("back")
                            self.file_manager.refresh_file_manager()
                            distinct.remove(file_send_name)
                            print(distinct)
                            break
                        elif self.file_manager.wait_bluetooth() == False:
                            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有蓝牙不能发送' + file_send_name)
                            self.file_manager.Click_ren_cancle()
                            self.file_manager.refresh_file_manager()
                            distinct.remove(file_send_name)
                            print(distinct)
                            break
                    elif wait_send_file_name == False:
                        start_text = self.file_manager.page_file_name(send_file_page_long-2)
                        self.d.swipe(0.729, 0.8, 0.808, 0.095)
                        stop_text = self.file_manager.page_file_name(send_file_page_long-2)
                        if start_text == stop_text:
                            self.file_manager.refresh_file_manager()
            if len(distinct) == 0:
                break
        return result

    def Case_Calculate_Verify(self):
        '''
        文件的计算校验和的操作
        :return:
        '''
        original_path=self.file_manager.Gain_Path()
        self.file_manager.All_Button()
        result = 'Pass'
        sum = 0
        calculate_verify_file_list = []
        while True:  # 外层循环控制页面的切换，
            calculate_verify_long = self.file_manager.page_number()
            print('当前页面显示数量为：%s' % calculate_verify_long)
            calculate_verify_long_end_name= self.file_manager.page_file_name(calculate_verify_long-1)
            print('当前页面的最后一条数据为：' + calculate_verify_long_end_name)
            for i in range(calculate_verify_long):  # 内层循环控制当前页面所有文件文件夹的点击查看属性操作
                print('这是第%s个文件夹' % i)
                calculate_verify_long_name = self.file_manager.page_file_name(i)
                print('这是当前的文件名称：' + calculate_verify_long_name)
                self.file_manager.Long_Click(calculate_verify_long_name)  # 长按文件或文件夹，打开他的菜单框
                homepapg = self.file_manager.wait_homepage()
                count_sum = self.file_manager.wait_sum()
                send = self.file_manager.wait_send()
                if homepapg == True:  # 断言是否进入了文件夹或文件的菜单框
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是一个文件夹')
                    self.file_manager.Click_Cancle()
                elif count_sum or send == True:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是一个文件')
                    calculate_verify_file_list.append(calculate_verify_long_name)
                    self.file_manager.Click_Cancle()
                else:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有进入文件夹的菜单界面')
                    result = 'Fail'
                    self.error_list.append('没有进入文件夹的菜单界面' + calculate_verify_long_name)
            print('第%s页检查完毕，拖动到下一页' % sum)
            self.d.swipe(0.729, 0.8, 0.808, 0.095)

            calculate_verify_long1 = self.file_manager.page_number()
            calculate_verify_long_end_name1 = self.file_manager.page_file_name(calculate_verify_long1-1)
            print('拖动之后页面显示数量为：%s' % calculate_verify_long1)  # @获取到拖动之后的页面的最后一条数据，与拖动之前的数据进行对比，
            print('拖动之后页面数据最后一条是：' + calculate_verify_long_end_name1)  # 如果相同，说明已经到达了最后一页方法将结束
            if calculate_verify_long_end_name == calculate_verify_long_end_name1:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>已经达到最后一页')
                break
            sum += 1
        self.file_manager.refresh_file_manager()
        time.sleep(5)
        calculate_verify = set(calculate_verify_file_list)
        print(calculate_verify)
        # while True:
        for original_verify_file_name in list(calculate_verify):
            print('正在寻找：' + original_verify_file_name)
            wait_file = self.file_manager.wait_file_name(original_verify_file_name)
            while True:
                print('正在寻找：' + original_verify_file_name)
                wait_file = self.file_manager.wait_file_name(original_verify_file_name)
                if wait_file == True:
                    print('长按这个文件：' + original_verify_file_name)
                    self.file_manager.Long_Click(original_verify_file_name)
                    file_path=self.file_manager.Calculate_Verify()
                    self.file_manager.ScreenShot('手工验证计算校验和的截图'+original_verify_file_name)
                    if original_path+'/'+original_verify_file_name==file_path:
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>文件路径验证成功，请手工验证其他')
                        self.file_manager.Click_Calculate_Verify_confirm()
                        calculate_verify.remove(original_verify_file_name)
                        print(calculate_verify)
                        break
                    else:
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>文件路径显示错误:'+original_verify_file_name)
                        result='Fail'
                        self.error_list.append('文件路径显示错误:'+original_verify_file_name)
                        self.file_manager.Click_Calculate_Verify_confirm()
                        calculate_verify_file_list.remove(original_verify_file_name)
                        print(calculate_verify_file_list)
                        break
                elif wait_file == False:
                    start_text = self.file_manager.page_file_name(calculate_verify_long-2)
                    self.d.swipe(0.729, 0.8, 0.808, 0.095)
                    stop_text = self.file_manager.page_file_name(calculate_verify_long-2)
                    if start_text == stop_text:
                       self.file_manager.refresh_file_manager()
            if len(calculate_verify_file_list) == 0:
                break
        return result

    def Teardown(self):
        self.d.app_stop("com.android.music")
        end_time= time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        self.file_manager.Off_File_Manager()
        writer_log(self.path+'log\\'+'file.log.txt',self.error_list)
        print('错误日志：',self.error_list)
        return end_time

    def run(self):
        start_time1=self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>初始化完成，开始执行属性操作')
        try:
            result1=self.Case_execute_operation('属性')
        except BaseException as e:
            result1 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：执行属性操作" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\'+ "执行属性操作" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.On_File_Manager()
            self.d.app_stop_all()
        end_time1=self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有文件夹或文件进行点击属性操作",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.属性信息显示正确 \n 4.请手工验证文件的属性信息，已截图",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time1, "t_end_time": end_time1,
             "t_reference_result": result1, "t_result": ""})
        time.sleep(5)


        start_time2 = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>初始化完成，属性操作执行完毕，开始执行选择操作')
        try:
            result2=self.Case_execute_operation__select()
        except BaseException as e:
            result2 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：执行选择操作" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "执行选择操作" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time2 = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有文件夹或文件进行点击选择操作",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.文件可以正常被选中取消",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time2, "t_end_time": end_time2,
             "t_reference_result": result2, "t_result": ""})
        time.sleep(5)


        start_time3 = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>初始化完成，选择操作执行完毕，开始执行添加到书签操作')
        try:
            result3=self.Case_execute_operation('添加到书签')
        except BaseException as e:
            result3 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：执行添加到书签操作" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "执行添加到书签操作" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time3 = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有文件夹或文件进行添加书签操作",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.文件或文件夹可以整成添加到书签",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time3, "t_end_time": end_time3,
             "t_reference_result": result3, "t_result": ""})
        time.sleep(5)


        start_time4 = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>初始化完成，添加到书签操作执行完毕，开始执行添加快捷方式操作')
        try:
            result4=self.Case_execute_operation('添加快捷方式')
        except BaseException as e:
            result4 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：执行添加快捷方式操作" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "执行添加快捷方式操作" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time4 = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有文件夹或文件进行添加快捷方式操作",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.文件或文件夹可以正常的添加快捷方式",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time4, "t_end_time": end_time4,
             "t_reference_result": result4, "t_result": ""})
        time.sleep(5)


        start_time5 = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>初始化完成，开始验证添加快捷方式')
        try:
            result5=self.Case_Verify_Shortcut()
        except BaseException as e:
            result5 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：验证添加快捷方式" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "验证添加快捷方式" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time5 = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有文件夹或文件进行验证添加的快捷方式的操作",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.验证问价或文件夹成功添加了快捷方式 \n 4.请手工验证添加的快捷方式打开后的截图",
             "t_actual_result": actul_reselt+'\n'+path, "t_start_time": start_time5, "t_end_time": end_time5,
             "t_reference_result": result5, "t_result": ""})
        time.sleep(5)


        start_time6 = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>快捷方式操作完成，开始设置主页')
        try:
            result6=self.Case_Circulation_Set_Homepage()
        except BaseException as e:
            result6 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：设置主页" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "设置主页" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time6 = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有文件夹或文件进行设置主页操作",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.文件夹可以正常设置为主页",
             "t_actual_result":  actul_reselt+'\n'+path, "t_start_time": start_time6, "t_end_time": end_time6,
             "t_reference_result": result6, "t_result": ""})

        start_time7 = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>设置主页完成，开始进行重命名的操作')
        try:
            result7 = self.Case_Ren()
        except BaseException as e:
            result7 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：进行重命名的操作" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "进行重命名的操作" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time7 = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有文件夹或文件进行重命名操作",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.文件夹可以正常重命名",
             "t_actual_result":  actul_reselt+'\n'+path, "t_start_time": start_time7, "t_end_time": end_time7,
             "t_reference_result": result7, "t_result": ""})


        start_time8 = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>重命名操作完成，开始进行添加副本的操作')
        try:
            result8 = self.Case_Transcript()
        except BaseException as e:
            result8 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：添加副本的操作" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "添加副本的操作" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time8 = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有文件夹或文件进行添加副本的操作",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.文件夹或文件可以正常添加副本",
             "t_actual_result":  actul_reselt+'\n'+path, "t_start_time": start_time8, "t_end_time": end_time8,
             "t_reference_result": result8, "t_result": ""})


        start_time8a = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>添加副本操作完成开始删除添加的副本')
        try:
            result8a = self.Case_delete_transcript()
        except BaseException as e:
            result8a = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：开始删除添加的副本" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\'+ "开始删除添加的副本" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time8a = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对添加的副本删除，并验证添加的副本",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.成功删除所有添加的副本，验证副本添加的数量正确",
             "t_actual_result":  actul_reselt+'\n'+path, "t_start_time": start_time8a, "t_end_time": end_time8a,
             "t_reference_result": result8a, "t_result": ""})


        start_time9 = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>添加副本操作完成开始文件打开方式的测试')
        try:
            result9 = self.Case_Open_Mode()
        except BaseException as e:
            result9 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：开始文件打开方式的测试" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "开始文件打开方式的测试" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time9 = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有文本文件和txt文件进行打开方式的测试",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.txt文件或 文本文件可以正常打开 \n 4.请手工验证文件打开后的界面，已截图",
             "t_actual_result":  actul_reselt+'\n'+path, "t_start_time": start_time9, "t_end_time": end_time9,
             "t_reference_result": result9, "t_result": ""})



        start_time10 = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>打开方式操作完成开始文件的删除操作')
        try:
            result10 = self.Case_Delete()
        except BaseException as e:
            result10 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：文件的删除操作" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "文件的删除操作" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time10 = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有的文件或文件夹做删除操作",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.文件或文件夹可以正常删除",
             "t_actual_result":  actul_reselt+'\n'+path, "t_start_time": start_time10, "t_end_time": end_time10,
             "t_reference_result": result10, "t_result": ""})


        start_time11 = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>文件的删除操作完成开始文件发送的测试')
        try:
            result11 = self.Case_Send_file()
        except BaseException as e:
            result11 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：文件发送的测试" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\'+ "文件发送的测试" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time11 = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有文本文件和txt文件进行蓝牙发送的测试",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.txt文件或 文本文件可以正常点击蓝牙发送 \n 4.请手工验证文件点击发送进入蓝牙后的界面，已截图",
             "t_actual_result":  actul_reselt+'\n'+path, "t_start_time": start_time11, "t_end_time": end_time11,
             "t_reference_result": result11, "t_result": ""})


        start_time12 = self.setup()
        actul_reselt=''
        path=''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>文件发送操作完成开始文件计算校验和的测试')
        try:
            result12 = self.Case_Calculate_Verify()
        except BaseException as e:
            result12 = 'Fail'
            print("except:", e)
            actul_reselt=str(e)[7:]
            print("=====>>>>>执行测试：文件计算校验和的测试" + "；出现异常<<<<<=====")
            self.d.screen_on()
            # 判断是否锁屏状态
            if self.d(resourceId="com.android.systemui:id/emergency_call_button"):
                self.d.unlock()
            path=self.path+'image\\error_picture\\' + "文件计算校验和的测试" + "；出现异常.jpg"
            self.d.screenshot(path)
            self.file_manager.Off_File_Manager()
            self.d.app_stop_all()
        end_time12 = self.Teardown()
        self.File_Manager_Report_Details.append(
            {"t_module": "文件管理器", "t_case": "压力测试", "t_steps": "打开文件管理器，对所有文本文件和txt文件进行计算校验和的测试",
             "t_expected_result": "1.可执行的功能仍可正常响应 \n 2.不可执行的功能给出正确提示信息 \n 3.txt文件或 文本文件可以正常打开计算校验和文件路径显示正确 \n 4.请手工验证进入文件的计算校验和的界面，已截图",
             "t_actual_result":  actul_reselt+'\n'+path, "t_start_time": start_time12, "t_end_time": end_time12,
             "t_reference_result": result12, "t_result": ""})
        return self.File_Manager_Report_Details
















