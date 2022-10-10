import sys
import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

window = tk.Tk()
window.title('mask-detection')
ttk.Label(window, text="选择合适的摄像头(默认为零)").grid(column=0, row=0)
def start():
    pass

def callbackClose():
    tkinter.messagebox.showwarning(title='警告', message = '点击了关闭按钮')
    sys.exit(0)

window.protocol("WM_DELETE_WINDOW", callbackClose())
action1 = ttk.Button(window, text='开始', command=start())
action1.grid(column=2, row=1)

# 创建一个下拉列表
number = tk.StringVar()
numberChosen = ttk.Combobox(window, width=12, textvariable=number)
numberChosen['value'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
numberChosen.grid(column=0, row=1)
numberChosen.current(0)  # 默认值
window.mainloop()