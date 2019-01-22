class KHM_Cootv:
    def __init__(self,d):
        self.d = d

    def start(self):
        print(">>>>>>>>>>>>>>>>> 启动APP：cootv")
        self.d.app_start("com.tvata.tvaxw.mobile")
        for i in range(2):
            if self.d(resourceId="android:id/message",text=u"连接服务器失败！").wait(timeout=2):
                self.d(resourceId="android:id/button1").click()


    def click_cod(self):
        print(">>>>>>>>>>>>>>>>> cootv，点击推荐")
        self.d(resourceId="com.tvata.tvaxw.mobile:id/bt_good_movie").click()
        if self.d(resourceId="com.tvata.tvaxw.mobile:id/txt_title",text='推荐视频').wait(timeout=2):
            return True
        else:
            print("cootv，点击推荐，断言异常")
            return False

    def click_live(self):
        print(">>>>>>>>>>>>>>>>> cootv，点击直播")
        self.d(resourceId="com.tvata.tvaxw.mobile:id/bt_live").click()
        if self.d(resourceId="com.tvata.tvaxw.mobile:id/txt_title",text=u"看看直播").wait(timeout=2):
            return True
        else:
            print("cootv，点击直播，断言异常")
            return False

    def click_my(self):
        print(">>>>>>>>>>>>>>>>> cootv，点击个人")
        self.d(resourceId="com.tvata.tvaxw.mobile:id/bt_more").click()
        if self.d(resourceId="com.tvata.tvaxw.mobile:id/txt_title",text=u"私密").wait(timeout=2):
            return True
        else:
            print("cootv，点击个人，断言异常")
            return False


    '''
    以下为 我的 界面
    '''

    def my_favorite(self):
        print(">>>>>>>>>>>>>>>>> 个人界面，点击我的收藏")
        self.d(resourceId="myFavorite").click()

    def my_history(self):
        print(">>>>>>>>>>>>>>>>> 个人界面，点击观看历史")
        self.d(resourceId="myHistory").click()

    def my_userinfo(self):
        print(">>>>>>>>>>>>>>>>> 个人界面，点击资料设置")
        self.d(resourceId="setUserInfoId").click()

    def my_login(self):
        print(">>>>>>>>>>>>>>>>> 个人界面，点击登录")
        self.d(resourceId="isLoginId").click()

    def my_abot(self):
        print(">>>>>>>>>>>>>>>>> 个人界面，点击版本声明")
        self.d(description=u"版本声明").click()

    def click_back(self):
        self.d(resourceId="com.tvata.tvaxw.mobile:id/bt_left").click()

    def stop(self):
        print(">>>>>>>>>>>>>>>>> 关闭APP：cootv")
        self.d.app_stop("com.tvata.tvaxw.mobile")
        self.d.press("home")


    def Case_menu_traversal(self):
        self.start()
        try:
            self.click_live()
            self.click_cod()
            self.click_my()
            self.my_favorite()
            self.click_back()
            self.my_history()
            self.click_back()
            self.my_userinfo()
            self.click_back()
            self.my_login()
            self.click_back()
            self.my_abot()
            self.click_back()
        except BaseException as e:
            if self.d(resourceId="android:id/message",text='连接服务器失败！').wait(timeout=2)==True:
                self.d(resourceId="android:id/button1").click()
        self.stop()

class NCA_Cootv:
    def __init__(self, d):
        self.d = d

    def start(self):
        print(">>>>>>>>>>>>>>>>> 启动APP：cootv")
        self.d.app_start("com.xinwei.ni.cootv")

    def click_en_vivo(self):
        print(">>>>>>>>>>>>>>>>> cootv界面：点击en_vivo")
        self.d(resourceId="com.xinwei.ni.cootv:id/bt_live").click()
        if self.d(resourceId="com.xinwei.ni.cootv:id/txt_title",text=u"EN VIVO").wait(timeout=2):
            return True
        else:
            return False

    def click_yo(self):
        print(">>>>>>>>>>>>>>>>> cootv界面：点击YO")
        self.d(resourceId="com.xinwei.ni.cootv:id/bt_more").click()
        if self.d(resourceId="com.xinwei.ni.cootv:id/txt_title",text=u"YO").wait(timeout=2):
            return True
        else:
            return False

    def yo_favoritos(self):
        print(">>>>>>>>>>>>>>>>> YO界面：点击favoritos")
        self.d(resourceId="myFavorite").click()

    def yo_retroalimentacion(self):
        print(">>>>>>>>>>>>>>>>> YO界面：点击retroalimentacion")
        self.d(resourceId="feedbackId").click()

    def yo_iniciar_sesion(self):
        print(">>>>>>>>>>>>>>>>> YO界面：点击iniciar sesion")
        self.d(resourceId="doLoginId").click()

    def yo_acerca_de(self):
        print(">>>>>>>>>>>>>>>>> YO界面：点击acerca de")
        self.d(description=u"acerca de").click()

    def click_back(self):
        self.d(resourceId="com.xinwei.ni.cootv:id/bt_left").click()

    def stop(self):
        print(">>>>>>>>>>>>>>>>> 关闭APP：cootv")
        self.d.app_stop("com.xinwei.ni.cootv")
        self.d.press("home")

    def Case_menu_traversal(self):
        self.start()
        try:
            self.click_yo()
            self.click_en_vivo()
            self.click_yo()
            self.yo_favoritos()
            self.click_back()
            self.yo_retroalimentacion()
            self.click_back()
            self.yo_iniciar_sesion()
            self.click_back()
            self.yo_acerca_de()
            self.click_back()
        except BaseException as e:
            if self.d(resourceId="android:id/message",text='连接服务器失败！').wait(timeout=2)==True:
                self.d(resourceId="android:id/button1").click()
        self.stop()

#
# import uiautomator2 as u2
#
# d = u2.connect()
# c = NCA_Cootv(d)
