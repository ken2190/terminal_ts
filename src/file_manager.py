import uiautomator2 as u2
import time
import os
from src.general import image_comparison
class File_Manager():

    def __init__(self,d):
        self.d=d
        self.path = image_comparison.get_path()

    def __sleep(func):
        def inner(self):
            time.sleep(1)
            return func(self)
        return inner


    def ScreenShot(self, name):
        '''
        :param name: 传入图片的名称
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>开始截图')
        path = self.path+'image\\file_manager_picture\\'+name+'.jpg'
        self.d.screenshot(path)

    '''
    打开文件管理器的操作
    '''


    @__sleep
    def On_File_Manager(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>打开文件管理器')
        self.d.app_start('com.cyanogenmod.filemanager',activity= '.activities.NavigationActivity')
        if self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").wait(timeout=2):
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()

    @__sleep
    def Off_File_Manager(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>关闭文件管理器')
        self.d.app_stop('com.cyanogenmod.filemanager')

    def Set(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>打开导航抽屉')
        self.set=self.d(description=u"打开导航抽屉").wait(timeout=2)
        print(self.set)
        if self.set==True:
            self.d(description=u"文件系统信息").left(description=u"打开导航抽屉").click()
        else:
            self.d.swipe(0.015, 0.395, 0.823, 0.424)
        self.d(description=u"打开导航抽屉")

    @__sleep
    def Gain_Path(self):
        self.Set()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>获取当前的路径')
        if self.d(resourceId="com.cyanogenmod.filemanager:id/drawer_bookmarks_tab",text=u'书签').wait(timeout=1):
            self.d(resourceId="com.cyanogenmod.filemanager:id/drawer_bookmarks_tab", text=u'书签').click()
        self.text=self.d(resourceId="com.cyanogenmod.filemanager:id/bookmarks_item_path").get_text()
        print(self.text)
        self.d.swipe(0.872, 0.522, 0.244, 0.524)
        return self.text

    @__sleep
    def All_Button(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>进入文件管理器，点击所有，查看所有文件')
        wait = self.d(resourceId="com.cyanogenmod.filemanager:id/navigation_view_item_name", text=u"所有",
                           className="android.widget.TextView").wait(timeout=2)  # 等待【所有】按钮出现
        if wait == True:
            self.d(resourceId="com.cyanogenmod.filemanager:id/navigation_view_item_name", text=u"所有",
              className="android.widget.TextView").click()


    '''
    对文件夹的操作
    '''

    def Long_Click(self,i,select='name'):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>长按文件夹')
        if select=="num":
            self.d(resourceId="com.cyanogenmod.filemanager:id/navigation_view_item_icon", className="android.widget.ImageView",
              instance=i).long_click(duration=1)
        elif select=='name':
            self.d(resourceId="com.cyanogenmod.filemanager:id/navigation_view_item_name",text=i).long_click(duration=1)


    def refresh_file_manager(self):
        '''
        刷新文件管理器
        :return:
        '''
        self.d(resourceId="com.cyanogenmod.filemanager:id/breadcrumb_item", text=0).click()

    def page_number(self,i=None):
        '''
        获取当前页面的文件夹数量
        :return: 返回数量
        '''
        if i==None:
            number=len(self.d(resourceId="com.cyanogenmod.filemanager:id/navigation_view_item_name",
                       className="android.widget.TextView"))  # 获取当前页面的文件夹或文件的数量
            return number
        else:
            wait_first_name=self.d(resourceId="com.cyanogenmod.filemanager:id/navigation_view_item_name",
                   className="android.widget.TextView")[i].wait(timeout=3)
            return wait_first_name


    def page_file_name(self,num):
        '''
        获取当前页面的指定的文件名称
        :param num: 根据页面的数量指定，num为页面第几个
        :return: 返回文件的名称
        '''
        file_name=self.d(resourceId="com.cyanogenmod.filemanager:id/navigation_view_item_name",
                   className="android.widget.TextView")[num].get_text()
        return file_name


    '''
    打开文件夹的菜单后的操作
    '''

    @__sleep
    def Click_Attribute(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>长按文件夹后，点击属性')
        self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu1_item_text", text=u"属性",
          className="android.widget.TextView").click()

    def Gain_File_Path(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>获取当前文件的路径')
        self.text=self.d(resourceId="com.cyanogenmod.filemanager:id/fso_properties_parent").get_text()
        print(self.text)
        return self.text

    @__sleep
    def Click_Select(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>长按文件夹后，点击选择')
        select=self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text", text=u"选择",
               className="android.widget.TextView").wait(timeout=3)
        if select==True:
            self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text", text=u"选择",
              className="android.widget.TextView").click()
        return select

    def Click_deselect(self,operation=None):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>长按文件夹后，点击取消选择')
        if operation==None:
            deselect = self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text",
                                   text='取消选择').wait(timeout=2)
            return deselect
        elif operation=='click':
            self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text",
                   text='取消选择').click()


    @__sleep
    def Click_Delete(self,pop='是'):
        yes=self.d(resourceId="com.cyanogenmod.filemanager:id/dialog_title_text").wait(timeout=2)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>长按文件夹后，点击删除')
        self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu1_item_text", text=u"删除",
          className="android.widget.TextView").click()
        if yes==True:
            if pop=='是':
                self.d(resourceId="android:id/button1",text='是').click()
            else:
                self.d(resourceId="android:id/button2",text='否').click()
        else:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有弹出确认删除框')
            self.ScreenShot('没有弹出确认框')

    @__sleep
    def Click_Ren(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>长按文件夹后，点击重命名')
        self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text", text=u"重命名",
          className="android.widget.TextView").click()

    @__sleep
    def Click_Transcript(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>长按文件夹后，点击创建副本')
        self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu1_item_text", text=u"创建副本",
          className="android.widget.TextView").click()

    @__sleep
    def Click_Bookmark(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>长按文件夹后，点击添加到书签')
        self.d( text=u"添加到书签",className="android.widget.TextView").click()

    @__sleep
    def Click_Shortcut(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>长按文件夹后，点击添加快捷方式')
        self.d(text=u"添加快捷方式",className="android.widget.TextView").click()

    @__sleep
    def Click_Homepage(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>长按文件夹后，点击设置为主页')
        homepage=self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text", text=u"设置为主页",
          className="android.widget.TextView").wait(timeout=2)
        if homepage==True:
            self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text", text=u"设置为主页",
                   className="android.widget.TextView").click()
        else:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>没有找到主页按钮，这可能不是一个文件夹')
            self.Click_Cancle()

    @__sleep
    def OpenMode(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>点击打开方式')
        self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text", text=u"打开方式").click()

    @__sleep
    def Send_File(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>发送文件')
        self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text", text=u"发送").click()

    def Calculate_Verify(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>点击计算校验和')
        self.d(text=u"计算校验和").click()
        File_Path=self.d(resourceId="com.cyanogenmod.filemanager:id/checksum_filename").get_text()
        return File_Path

    def homepage_top_file_name(self,j):
        '''
        获取主页顶部的文件名称
        :param j: 传入文件的名称
        :return: 返回获取到的文件名称
        '''
        home_top=self.d(resourceId="com.cyanogenmod.filemanager:id/breadcrumb_item",
               text=j).get_text()
        return home_top

    '''
    针对弹框的操作
    '''

    @__sleep
    def Click_Cancle(self):
        if self.d(resourceId="android:id/button2", text=u"取消", className="android.widget.Button").wait(timeout=2)==True:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>点击取消按钮')
            self.d(resourceId="android:id/button2", text=u"取消", className="android.widget.Button").click()

    def Click_ren_cancle(self):
        '''
        点击重命名中名称重复时的取消
        :return:
        '''
        self.d(resourceId="android:id/button2", text='取消').click()


    def Click_ren_confirm(self):
        '''
        点击重命名时的确定
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>点击确定')
        self.d(resourceId="android:id/button1", text='确定').click()

    def Click_Calculate_Verify_confirm(self):
        '''
        点击计算校验和时的确定
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>点击确定')
        self.d(resourceId="android:id/button3", text='确定').click()
    @__sleep
    def Back(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>点击返回按钮')
        self.d(description=u"向上导航",className='android.widget.ImageButton').click()

    def affirm(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>点击打开属性后的确认按钮')
        self.d(resourceId="android:id/button2", text=u"确定", className="android.widget.Button").click()


    '''
    文件夹在home界面打开方式的弹框操作
    '''

    def wait_home_page_file_open_mode(self):
        '''
        点击快捷方式后等待打开方式的弹框出现
        :return: 返回：True 或  False
        '''
        open_mode=self.d(resourceId="com.cyanogenmod.filemanager:id/dialog_title_text", text='打开方式').wait(timeout=3)
        return open_mode

    def wait_home_page_file_open_mode_compile(self,operation=None):
        '''
        在快捷方式点击打开后等待弹框出现
        :return: 返回：True 或  False
        '''
        if operation==None:
            compile=self.d(resourceId="com.cyanogenmod.filemanager:id/associations_item_icon").wait(timeout=3)
            return compile
        elif operation=='click':
            self.d(resourceId="com.cyanogenmod.filemanager:id/associations_item_icon").click()
            self.d(resourceId="android:id/button1", text='打开').click()


    def wait_home_page_file_open_mode_music(self):
        '''
        在快捷方式点击打开后等待音乐出现
        :return: 返回：True 或  False
        '''
        music=self.d(resourceId="com.cyanogenmod.filemanager:id/associations_item_icon").wait(timeout=3)
        return music

    def wait_file_name(self,j,operation='wait'):
        '''
        对文件夹的操作
        :param operation: 传入操作  wait:等待    click:长按   click():点击
        :param j: 传入文件夹的名称
        :return: 如果是等待文件夹，就返回文件夹的名称
        '''
        if operation=='wait':
            name=self.d(resourceId="com.cyanogenmod.filemanager:id/navigation_view_item_name",
                text=j).wait(timeout=3)
            return name
        elif operation=='click':
            self.d(resourceId="com.cyanogenmod.filemanager:id/navigation_view_item_name",
                   text=j).long_click(duration=1)
        elif operation=='click()':
            self.d(resourceId="com.cyanogenmod.filemanager:id/navigation_view_item_name",
                   text=j).click()


    def file_open_mode_wait_compile(self,operation='wait'):
        '''
        文件的打开方式等待编辑器的出现
        :param operation: 传入操作：wait:等待元素出现  click:点击元素
        :return: 如果是wait的话会返回  True 或  False
        '''
        if operation=='wait':
            redact = self.d(resourceId="com.cyanogenmod.filemanager:id/associations_item_text", text='编辑器').wait(
                timeout=2)
            return redact
        elif operation=='click':
            self.d(resourceId="com.cyanogenmod.filemanager:id/associations_item_text", text='编辑器').click()
            self.d(resourceId="android:id/button1", text='打开').click()


    def wait_bluetooth(self,operation='wait'):
        '''
        文件的发送等待蓝牙出现
        :param operation: wait：等待  click：点击
        :return: 如果是wait就返回： True 或  False
        '''
        if operation=='wait':
            bluetooth=self.d(resourceId="com.cyanogenmod.filemanager:id/associations_item_text",
                   text='蓝牙').wait(timeout=2)
            return bluetooth
        elif operation=='click':
            self.d(resourceId="com.cyanogenmod.filemanager:id/associations_item_text",
                   text='蓝牙').click()
            self.d(resourceId="android:id/button1", text='发送').click()



    '''
    等待元素消失
    '''
    def ren_spring_wait_vanish(self):
        '''
        等待重命名时的弹框的消失
        :return:返回：True 或  False
        '''
        spring=self.d(resourceId="com.cyanogenmod.filemanager:id/message_progress_dialog_label").wait_gone(
            timeout=20)
        return spring

    def transcript_pop_up_wait_vanish(self):
        '''
        等待创建副本时的弹窗消失
        :return: 返回：True 或  False
        '''
        pop_up=self.d(resourceId="com.cyanogenmod.filemanager:id/message_progress_dialog_label").wait_gone(timeout=10000.0)
        return pop_up






    '''
    home界面的操作
    '''

    def home_page(self,num=None):
        '''
        获取home页面快捷方式的名称
        :param num: 指定一个快捷方式。
                    如果num等于None就获取当前home页面的快捷方式的数量
        :return: 返回快捷方式的名称
        '''
        if num==None:
            shortcut_long=len(self.d(className='android.widget.TextView'))
            return shortcut_long
        else:
            name=self.d(className='android.widget.TextView')[num].get_text()
            return name


    '''
    等待元素的出现
    '''

    def wait_Attribute(self):
        '''
        判断属性菜单是否出现
        :return: 返回True 或 False
        '''
        attribute = self.d(text=u"属性",className="android.widget.TextView").wait(timeout=2)
        return attribute

    def wait_Select(self):
        '''
        判断选择菜单是否出现
        :return: 返回 True 或 False
        '''
        select=self.d(text=u"选择",className="android.widget.TextView").wait(timeout=2)
        return select

    def wait_homepage(self):
        '''
        判断设置主页是否出现
        :return: 返回 True 或 False
        '''
        homepage=self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text",
               text=u"设置为主页",
               className="android.widget.TextView").wait(timeout=1)
        return homepage

    def wait_sum(self):
        '''
        判断计算校验和是否出现
        :return: 返回 True 或 False
        '''
        sum=self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text",
               text=u"计算校验和",
               className="android.widget.TextView").wait(timeout=1)
        return sum

    def wait_send(self):
        '''
        判断发送是否出现
        :return: 返回 True 或 False
        '''
        send=self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text",
               text=u"发送",
               className="android.widget.TextView").wait(timeout=1)
        return send


    def wait_ren_element(self):
        '''
        等待重命名中的此名称已存在出现
        :return: 返回 True 或 False
        '''
        element=self.d(resourceId="com.cyanogenmod.filemanager:id/input_name_dialog_message",
            text='此名称已存在.').wait(timeout=3)
        return element



    '''
    对文件夹一个流程的操作
    '''

    def case_Attribute(self,gainpath,name):
        '''
        点击属性按钮，每次打开后截出每个文件的属性信息，判断文件的路径是否符合规定路径
        这个case是依赖内外层循环的
        :return:
        '''
        self.Click_Attribute()  # 点击属性
        time.sleep(2)
        self.ScreenShot('手工验证文件的属性信息：' + name)  # 打开文件夹或文件的属性后进行截图，截图路径保存到image下面的file_manager_picture
        message = self.d(resourceId="com.cyanogenmod.filemanager:id/fso_properties_dialog_tab_info",
                         text=u"信息", className="android.widget.TextView").wait(timeout=2)
        jurisdiction = self.d(
            resourceId="com.cyanogenmod.filemanager:id/fso_properties_dialog_tab_permissions", text=u"权限",
            className="android.widget.TextView").wait(timeout=2)
        gainfilepath = self.Gain_File_Path()

        if gainfilepath == gainpath and message==True and jurisdiction==True:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>当前的文件路径正确')
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>成功进入属性界面')
            self.affirm()
            return True
        elif gainfilepath!=gainpath:
            self.ScreenShot(name + '当前路径错误')
            time.sleep(2)
            return False

        elif message or jurisdiction==False:
            return 'error'


    def case_Add_Bookmark(self,name):
        '''
        添加到书签，添加后打印出它的toast弹框信息
        这个case是依赖内外层循环的
        :return:
        '''

        self.Click_Bookmark()
        toast=self.d.toast.get_message(5.0, 10.0)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是'+name+'添加书签的弹框信息：'+toast)
        if toast=='书签已成功加入.':
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>加入书签成功')
        elif toast=='书签已存在。':
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>书签已经存在，重复添加')
        else:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>书签添加失败')
            self.ScreenShot(name+'添加书签失败')
            result='Fail'
            return False


    def case_Shortcut(self,name):
        '''
        添加快捷方式，添加后打印它的toast弹框信息
        这个case是依赖内外层循环的
        它只是添加快捷方式，做完之后需要调用验证的case进行验证
        :return:
        '''

        self.Click_Shortcut()
        toast = self.d.toast.get_message(5.0, 10.0)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>这是' + name + '添加快捷方式的弹框信息：' + toast)
        if toast == '快捷方式创建成功.':
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>创建快捷方式成功')
        else:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>快捷方式创建失败')
            self.ScreenShot(name + '快捷方式失败')
            self.result = 'File'
            return False


    def case_Select(self,name):
        '''
        点击选择按钮，选中文件，然后检测是否选中，如果选中在取消选中
        这个case是依赖内外层循环的
        :return:
        '''
        self.deselect = self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text",
                               text='取消选择').wait(timeout=2)
        if self.deselect==False:
            self.Click_Select()
            self.Long_Click(name)
            self.deselect = self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text",
                                   text='取消选择').wait(timeout=2)
            if self.deselect == True:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>成功选中文件夹')
                time.sleep(1)
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>点击取消选择')
                self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text",
                       text='取消选择').click()
            else:
                return False
        else:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>文件夹已被选择')
            self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text",
                   text='取消选择').click()



    '''
    下面是移动文件的操作
    '''

    def open_operation(self):
        '''
        打开移动文件的操作界面
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>>>打开操作界面')
        self.d(resourceId="com.cyanogenmod.filemanager:id/ab_actions", description='操作').click()


    def file_paste(self):
        '''
        将选择的文件粘贴
        :return:
        '''
        print('>>>>>>>>>>>>>>>>>>>>>>>把选择的文件粘贴')
        self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu1_item_text", text=u"粘贴选择项").click()


    def cover_file(self):
        '''
        移动文件是否出现覆盖
        :return:
        '''
        cover=self.d(resourceId="com.cyanogenmod.filemanager:id/dialog_title_text", text='确认覆盖').wait(timeout=2)
        if cover == True:
            self.d(resourceId="android:id/button2", text='覆盖').click()


    def wait_copy_vanish(self):
        '''
        等待复制弹框消失
        :return: 返回 True 或 False
        '''
        copy_file = self.d(resourceId="com.cyanogenmod.filemanager:id/message_progress_dialog_progress").wait_gone(
            timeout=20000)
        return copy_file

    def wait_now_operation(self):
        '''
        等待正在操作的的弹框消失
        :return:
        '''
        operation=self.d(
            resourceId="com.cyanogenmod.filemanager:id/message_progress_dialog_label",
            text='正在执行操作...').wait_gone(timeout=20000)
        return operation

    def new_file(self,file_name):
        '''
        新建一个文件
        :return:
        '''
        self.open_operation()
        self.d(resourceId="com.cyanogenmod.filemanager:id/two_columns_menu2_item_text", text=u"新建文件").click()
        time.sleep(2)
        self.d.set_fastinput_ime(True)
        self.d.send_keys(file_name)
        self.d.set_fastinput_ime(False)
        time.sleep(2)
        self.Click_ren_confirm()


if __name__=='__main__':
    d=u2.connect('f750eaf4')
    a=File_Manager(d)
    a.new_file('aaa.txt')




