# -*- coding: utf-8 -*-
import xlsxwriter
import os

def get_format(wd, option={}):
    return wd.add_format(option)

# 设置居中
def get_format_center(wd,num=1):
    return wd.add_format({'align': 'center','valign': 'vcenter','border':num})
def set_border_(wd, num=1):
    return wd.add_format({}).set_border(num)

# 写数据
def _write_center(worksheet, cl, data, wd):
    return worksheet.write(cl, data, get_format_center(wd))

def init(workbook, worksheet, report_data):

    # print(report_data)

    # 设置列的宽
    worksheet.set_column("A:A", 30)
    worksheet.set_column("B:B", 50)

    # 设置行的高
    worksheet.set_row(1, 30)
    worksheet.set_row(2, 40)
    worksheet.set_row(3, 40)
    worksheet.set_row(4, 40)
    worksheet.set_row(5, 40)
    worksheet.set_row(6, 40)
    worksheet.set_row(7, 40)
    worksheet.set_row(8, 40)
    worksheet.set_row(9, 40)
    worksheet.set_row(10, 40)
    worksheet.set_row(11, 40)

    define_format_H2 = get_format(workbook, {'bold': True, 'font_size': 18})
    define_format_H2.set_border(1)
    define_format_H2.set_align("center")
    define_format_H2.set_bg_color("blue")
    define_format_H2.set_color("#ffffff")
    # Create a new Chart object.

    worksheet.merge_range('A1:B1', '测试报告总概况', define_format_H2)

    _write_center(worksheet, "A2", '项目名称', workbook)
    _write_center(worksheet, "A3", 'Android版本', workbook)
    _write_center(worksheet, "A4", '版本号', workbook)
    _write_center(worksheet, "A5", '测试开始时间', workbook)
    _write_center(worksheet, "A6", '测试结束时间', workbook)
    _write_center(worksheet, "A7", '测试总数', workbook)
    _write_center(worksheet, "A8", '通过总数', workbook)
    _write_center(worksheet, "A9", '失败总数', workbook)
    _write_center(worksheet, "A10", '通过率', workbook)
    _write_center(worksheet, "A11", '测试结果', workbook)


    _write_center(worksheet, "B2", report_data['model_number'], workbook)
    _write_center(worksheet, "B3", report_data['android_version'], workbook)
    _write_center(worksheet, "B4", report_data['build_number'], workbook)
    _write_center(worksheet, "B5", report_data['start_time'], workbook)
    _write_center(worksheet, "B6", report_data['end_time'], workbook)
    _write_center(worksheet, "B7", report_data['case_sum'], workbook)
    _write_center(worksheet, "B8", report_data['case_pass'], workbook)
    _write_center(worksheet, "B9", report_data['case_fail'], workbook)
    _write_center(worksheet, "B10", report_data['pass_rate'], workbook)
    _write_center(worksheet, "B11", report_data['result'], workbook)




    # pie(workbook, worksheet)

#  # 生成饼形图
# def pie(workbook, worksheet):
#     chart1 = workbook.add_chart({'type': 'pie'})
#     chart1.add_series({
#     'name':       '接口测试统计',
#     'categories':'=测试总况!$D$4:$D$5',
#    'values':    '=测试总况!$E$4:$E$5',
#     })
#     chart1.set_title({'name': '接口测试统计'})
#     chart1.set_style(10)
#     worksheet.insert_chart('A9', chart1, {'x_offset': 25, 'y_offset': 10})


def te_detail(workbook, worksheet, rep_details):

    print(rep_details["info"])
    # 设置列行的宽高
    worksheet.set_column("A:A", 20)
    worksheet.set_column("B:B", 20)
    worksheet.set_column("C:C", 45)
    worksheet.set_column("D:D", 30)
    worksheet.set_column("E:E", 30)
    worksheet.set_column("F:F", 20)
    worksheet.set_column("G:G", 20)
    worksheet.set_column("H:H", 20)
    worksheet.set_column("I:I", 20)





    worksheet.merge_range('A1:I1', '测试详情', get_format(workbook, {'bold': True, 'font_size': 18 ,'align': 'center','valign': 'vcenter','bg_color': 'blue', 'font_color': '#ffffff'}))
    _write_center(worksheet, "A2", '模块', workbook)
    _write_center(worksheet, "B2", '测试点', workbook)
    _write_center(worksheet, "C2", '操作步骤', workbook)
    _write_center(worksheet, "D2", '预期结果', workbook)
    _write_center(worksheet, "E2", '实际结果', workbook)
    _write_center(worksheet, "F2", '测试开始时间', workbook)
    _write_center(worksheet, "G2", '测试结束时间', workbook)
    _write_center(worksheet, "H2", '参考测试结果', workbook)
    _write_center(worksheet, "I2", '实际测试结果', workbook)

    # report_details = {"info": [{"t_module": "音乐", "t_case": "压力测试", "t_steps": "数量较多的音乐文件填充T卡，再播放音乐","t_expected_result": "","t_actual_result":"", "t_start_time": "", "t_end_time": "", "t_reference_result": "pass","t_result":""},
    #                 {"t_module": "音乐", "t_case": "压力测试", "t_steps": "开启长时间背景播放音乐，背景放音乐","t_expected_result": "","t_actual_result":"", "t_start_time": "", "t_end_time": "", "t_reference_result": "pass","t_result":""}],
    #         "test_sum": 100,"test_success": 20, "test_failed": 80}

    for i in range(rep_details["test_sum"]+2):
        worksheet.set_row(i, 30)

    temp = 3
    for item in rep_details["info"]:
        _write_center(worksheet, "A"+str(temp), item["t_module"], workbook)
        _write_center(worksheet, "B"+str(temp), item["t_case"], workbook)
        _write_center(worksheet, "C"+str(temp), item["t_steps"], workbook)
        _write_center(worksheet, "D"+str(temp), item["t_expected_result"], workbook)
        _write_center(worksheet, "E"+str(temp), item["t_actual_result"], workbook)
        _write_center(worksheet, "F"+str(temp), item["t_start_time"], workbook)
        _write_center(worksheet, "G"+str(temp), item["t_end_time"], workbook)
        _write_center(worksheet, "H"+str(temp), item["t_reference_result"], workbook)
        _write_center(worksheet, "I"+str(temp), item["t_result"], workbook)
        temp = temp +1


gpath = os.path.dirname(os.getcwd())
def write(rep_datas, rep_details, path = gpath+"\\resource\\report\\report.xlsx"):

    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet("测试总况")
    worksheet2 = workbook.add_worksheet("测试详情")
    init(workbook, worksheet, rep_datas)
    te_detail(workbook, worksheet2 ,rep_details)

    workbook.close()
    print("#########    生成报告成功    #########")


