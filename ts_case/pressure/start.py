import uiautomator2 as u2
from src.general import adb
import datetime
from ts_case.pressure.setup import Setup

from ts_case.pressure.ts_music import Ts_Music
from ts_case.pressure.ts_setting_wifi import Ts_Setting_Wifi
from ts_case.pressure.ts_setting_bluetooth import Ts_Setting_Bluetooth
from ts_case.pressure.ts_camera import *
from ts_case.pressure.ts_gmail import Ts_Gmail
from ts_case.pressure.ts_move_file import *
from ts_case.pressure.ts_camera_resolution_ratio import *
from ts_case.pressure.ts_file_manager import *
from ts_case.pressure.ts_chrome import Ts_Chrome
from ts_case.pressure.ts_terminal_load import *
from ts_case.pressure.ts_video import Ts_Video
from ts_case.pressure.ts_talk import Ts_Talk
from ts_case.pressure.ts_message import *


if __name__ == "__main__":

    d = u2.connect()
    all_cases = []
    setup = Setup(d)

    # 执行初始化的一些操作
    setup.setup()

    # '''
    # 以下开始执行测试
    # # '''
    # talk = Ts_Talk(d)
    # talk_report_details = talk.run()
    # all_cases.append(talk_report_details)                                   # 添加联系人的case
    #
    # message = Pre_Message(d)
    # message_report_details = message.run()
    # all_cases.append(message_report_details)                                # 添加短信的case详情
    #
    # c8_chrome = Ts_Chrome(d)
    # chrome_report_details = c8_chrome.run()
    # all_cases.append(chrome_report_details)                                 # 添加Chrome的case详情
    #
    # c8_music = Ts_Music(d)
    # music_report_details = c8_music.run()
    # all_cases.append(music_report_details)                                  # 添加音乐的case详情
    #
    # c8_video = Ts_Video(d)
    # video_report_details = c8_video.run()
    # all_cases.append(video_report_details)                                  # 添加视频的case详情
    #
    # camera = PressureCamera(d)
    # camera_report_details=camera.run(i=20)
    # all_cases.append(camera_report_details)                                 # 添加相机的case详情
    #
    # combination = Pre_camera_resolution_ratio(d)
    # camera_resolution_ratio_report_details = combination.run()
    # all_cases.append(camera_resolution_ratio_report_details)                # 相机的分辨率和质量测试还有组合测试case详情
    #
    # c8_gmail = Ts_Gmail(d)
    # gmail_report_details = c8_gmail.run()
    # all_cases.append(gmail_report_details)                                  # 添加gmail的case详情
    #
    #
    # c8_wifi = Ts_Setting_Wifi(d)
    # wifi_report_details = c8_wifi.run()
    # all_cases.append(wifi_report_details)                                   # 添加WIFI的case详情
    #
    # c8_bluetooth = Ts_Setting_Bluetooth(d)
    # bluetooth_report_details = c8_bluetooth.run()
    # all_cases.append(bluetooth_report_details)                              # 添加蓝牙的case详情
    #
    # file_manager=Pre_file_manager(d)
    # file_report_details=file_manager.run()
    # all_cases.append(file_report_details)                                   # 添加文件的case详情
    #
    # # 移动文件的操作
    # move_file = Pre_Move_file(d)
    # move_file_report = move_file.run(file_name='wlan.log')
    # all_cases.append(move_file_report)                                      # 添加移动文件的case详情

    # 满负载测试（待修改）
    terminal_load=Terminal_load(d)
    terminal_load_report_details=terminal_load.run()
    all_cases.append(terminal_load_report_details)                          # 满负载测试

    # 执行报告生成的一些操作
    setup.setdown(all_cases)
