from tkinter import *
from src.handlers.default import *
import time
import threading
import functools


# 线程处理池，防止阻塞
def threading_pool(eve):
    th = threading.Thread(target=eve)
    th.start()
    th.join()


root = Tk()
root.title("自动推广")
root.geometry("400x300+700+200")

menu = Menu(root)
root.overrideredirect(False)
root.config(menu=menu)
# 多级菜单实例
file_menu_ = Menu(root)
file_menu_other = Menu(root)
file_menu_other.add_command(label="1")
file_menu_.add_command(label="配置文件")
file_menu_.add_command(label="日志文件")
file_menu_.add_cascade(label="其他", menu=file_menu_other)

file_menu_.add_separator()
file_menu_.add_command(label="退出", command=root.quit)

tools_menu_ = Menu(root)
start = functools.partial(threading_pool, excel_to_db)
tools_menu_.add_command(label="数据入库", command=start)

help_menu_ = Menu(root)
help_menu_.add_command(label="使用教程")
help_menu_.add_command(label="关于作者")
help_menu_.add_command(label="版本信息")

menu.add_cascade(label="文件", menu=file_menu_)
menu.add_cascade(label="工具", menu=tools_menu_)
menu.add_cascade(label="帮助", menu=help_menu_)

root.mainloop()
