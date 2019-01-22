import time
class Coo_Clean:
    def __init__(self, d):
        self.d = d

    def start(self):
        print(">>>>>>>>>>>>>>>>> 启动APP：酷管家")
        self.d.app_start("com.cootf.kuoperation")

    def click_accelerate(self):
        print(">>>>>>>>>>>>>>>>> 酷管家，点击智能查杀")
        time.sleep(5)
        self.d(resourceId="com.cootf.kuoperation:id/cover").click()

        if self.d(text=u"成功清理").wait(timeout=20):
            return True
        else:
            return "酷管家，点击智能查杀，断言异常"

    def click_process_cleaning(self):
        print(">>>>>>>>>>>>>>>>> 酷管家，点击进程清理")
        self.d(resourceId="com.cootf.kuoperation:id/bt_process_manager").click()
        if self.d(resourceId="com.cootf.kuoperation:id/actionbar_title", text=u'进程清理').wait(timeout=10):
            return True
        else:
            return "酷管家，点击进程清理，断言异常"

    def click_pure_background(self):
        print(">>>>>>>>>>>>>>>>> 酷管家，点击纯净后台")
        self.d(resourceId="com.cootf.kuoperation:id/bt_auto_start_manager").click()
        if self.d(resourceId="com.cootf.kuoperation:id/actionbar_title", text=u'纯净后台').wait(timeout=2):
            return True
        else:
            return "酷管家，点击纯净后台，断言异常"


    def click_cache_cleaning(self):
        print(">>>>>>>>>>>>>>>>> 酷管家，点击缓存清理")
        self.d(resourceId="com.cootf.kuoperation:id/bt_cache_manager").click()
        if self.d(resourceId="com.cootf.kuoperation:id/actionbar_title", text=u'缓存清理').wait(timeout=10):
            return True
        else:
            return "酷管家，点击缓存清理，断言异常"


    def click_trash_cleaning(self):
        print(">>>>>>>>>>>>>>>>> 酷管家，点击垃圾清理")
        self.d(resourceId="com.cootf.kuoperation:id/bt_system_trash_manager").click()
        if self.d(resourceId="com.cootf.kuoperation:id/actionbar_title",text=u'垃圾清理').wait(timeout=2):
            return True
        else:
            return "酷管家，点击垃圾清理，断言异常"

    def click_remain_cleaning(self):
        print(">>>>>>>>>>>>>>>>> 酷管家，点击残留清理")
        self.d(resourceId="com.cootf.kuoperation:id/bt_app_remain_manager").click()
        if self.d(resourceId="com.cootf.kuoperation:id/actionbar_title",text=u'残留清理').wait(timeout=2):
            return True
        else:
            return "酷管家，点击残留清理，断言异常"

    def Case_menu_traversal(self):
        result_message=''
        self.start()
        accelerate=self.click_accelerate()
        if accelerate!=True:
            result_message=result_message+accelerate
        process_cleaning=self.click_process_cleaning()
        if process_cleaning!=True:
            result_message=result_message+process_cleaning
        self.d.press("back")
        pure_background=self.click_pure_background()
        if pure_background!=True:
            result_message=result_message+pure_background
        self.d.press("back")
        cache_cleaning=self.click_cache_cleaning()
        if cache_cleaning!=True:
            result_message=result_message+cache_cleaning
        self.d.press("back")
        trash_cleaning=self.click_trash_cleaning()
        if trash_cleaning!=True:
            result_message=result_message+trash_cleaning
        self.d.press("back")
        remain_cleaning=self.click_remain_cleaning()
        if remain_cleaning!=True:
            result_message=result_message+remain_cleaning
        self.d.press("back")
        self.stop()
        return result_message



    def stop(self):
        print(">>>>>>>>>>>>>>>>> 关闭APP：酷管家")
        self.d.app_stop("com.cootf.kuoperation")
        self.d.press("home")



# import uiautomator2 as u2
#
# d = u2.connect()
# c = Coo_Clean(d)
