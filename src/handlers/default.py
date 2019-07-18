import xlrd
import requests
from wxpy import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from src.modules.db import *
import traceback
import re
import datetime
import time


# 去除小弹框
def get_excel_path():
    root = Tk()  # 创建一个Tkinter.Tk()实例
    root.withdraw()  # 将Tkinter.Tk()实例隐藏
    return askopenfilename()


# 登录
def login_weixin():
    bot = Bot(cache_path=True, qr_path="")  # 获取微信bot对象
    return bot


def check(price, coupon_denomination, coupon_begin_time, coupon_end_time):
    result = bool()

    # 判断优惠券是否可用
    if price >= int(re.findall('\d+', coupon_denomination)[0]):
        now_time_str = datetime.datetime.now().strftime('%Y-%m-%d')
        print(now_time_str)
        # 将时间转换为秒
        now_time = float(time.mktime(time.strptime(now_time_str, "%Y-%m-%d")))
        coupon_end_time = float(time.mktime(time.strptime(coupon_end_time, "%Y-%m-%d")))
        if now_time < coupon_end_time:
            result = True
        else:
            result = False
    else:
        result = False
    return result


# excel信息入库
def excel_to_db():
    try:
        excel_path = get_excel_path()
    except FileNotFoundError:
        print(traceback.format_exc())
        return
    data = xlrd.open_workbook(excel_path)
    table = data.sheets()[0]
    num = table.nrows
    for eve in range(1, num):
        all_message = table.row_values(eve)
        mes_1 = "{}\n".format(all_message[1])
        mes_2 = "【在售价】{}\n".format(all_message[5])
        mes_3 = "【券后价】{}\n-----------\n".format(111)
        mes_4 = "【立即领劵】复制{}\n打开手机淘宝领劵并下单".format(all_message[19])
        mes_5 = "【立即下单】复制{}打开手机淘宝立即下单".format(all_message[12])
        message = mes_1 + mes_2 + mes_3 + mes_4 + mes_5

        picture_link = all_message[2]
        picture_path = "files/images/" + str(picture_link).split("/")[-1]
        rq = requests.get(picture_link)

        if check(price=float(all_message[5]), coupon_denomination=all_message[15], coupon_begin_time=all_message[16],
                 coupon_end_time=all_message[17]):
            # 存储图片
            with open(picture_path, "wb") as f:
                f.write(rq.content)
                f.close()
            value = Promotion(commodity_id=all_message[0],
                              message_text=message,
                              picture_path=picture_path,
                              coupon_begin_time=all_message[16],
                              coupon_end_time=all_message[17])
            DB.add(value)
            DB.commit()
    Message(text="入库成功").pack()

# 自动聊天
# @bot.register()
# def print_others(msg):
#     print(str(msg).split(" "))
#     friend_name = str(msg).split(" ")[0]
#     if friend_name in ["焦久鑫"]:
#         message_ = str(msg).split(" ")[2]
#         rq = requests.get("http://api.qingyunke.com/api.php?key=free&appid=0&msg={}".format(message_))
#         result_message = dict(rq.json())["content"]
#         friend_ = bot.friends().search(friend_name)[0]
#         friend_.send(result_message)
