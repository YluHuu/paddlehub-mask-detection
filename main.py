import json
import paddlehub as hub
import os
import cv2

import sys
import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

import wx
import wx.xrc


class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"gui", pos=wx.DefaultPosition, size=wx.Size(552, 121),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"开始", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button3.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOTEXT))
        self.m_button3.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        gSizer1.Add(self.m_button3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button4 = wx.Button(self, wx.ID_ANY, u"终止", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button4.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.m_button4.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        gSizer1.Add(self.m_button4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.SetSizer(gSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.MyFrame1OnClose)
        self.m_button3.Bind(wx.EVT_BUTTON, self.m_button3OnButtonClick)
        self.m_button4.Bind(wx.EVT_BUTTON, self.m_button4OnButtonClick)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def MyFrame1OnClose(self, event):
        event.Skip()
        sys.exit(0)

    def m_button3OnButtonClick(self, event):
        event.Skip()
        event.Skip()

        window = tk.Tk()
        window.title('mask-detection')
        ttk.Label(window, text="选择合适的摄像头(默认为零)").grid(column=0, row=0)

        def start_dete():
            action1.configure(text='已开启' + number.get() + '号摄像头检测')  # bottun显示的内容

            action1.configure(state='disabled')  # 设置按钮为灰色,不可使用状态
            num = number.get()

            module = hub.Module(name="pyramidbox_lite_mobile_mask")

            # 创建一个文件夹来保存视频
            path = './detection_result'
            if not os.path.exists(path):
                os.mkdir(path)

            name = './detection_result/1-mask_detection.avi'
            width = 1280
            height = 720
            fps = 30
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            writer = cv2.VideoWriter(name, fourcc, fps, (width, height))

            maskIndex = 0
            index = 0
            data = []

            capture = cv2.VideoCapture(int(num))
            while True:
                frameData = {}
                ret, frame = capture.read()
                # print(frame)
                if ret == False:
                    break
                # color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('frame',color)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
                frame_copy = frame.copy()
                input_dict = {"data": [frame]}
                results = module.face_detection(data=input_dict)

                print(results)
                print(len(results[0]['data']))

                # results的主要内容
                # [{'data': [{'label': 'NO MASK', 'confidence': 0.8980138897895813,
                # 'top': 4, 'bottom': 128, 'left': 258, 'right': 409}], 'path': 'ndarray_time=1665324028773899.0'}]

                maskFrameDatas = []
                try:
                    for result in results:
                        print(result)
                        label = result['data'][0]['label']
                        confidence = str(round(result['data'][0]['confidence'], 2))

                        # 开始记录口罩部分的坐标并且开始将其框起来
                        top, bottom, left, right = int(result['data'][0]['top']), int(result['data'][0]['bottom']), \
                                                   int(result['data'][0]['left']), int(result['data'][0]['right'])

                        # 将当前帧保存为图片
                        # img_mame = "NO.%d.png" % (maskIndex)
                        # path = "./detection_result/" + img_mame
                        # image = frame[top - 10:bottom + 10, left - 10:right + 10]
                        #
                        #
                        # try:
                        #     cv2.imwrite(path, image, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
                        # except cv2.error:
                        #     print('1')
                        #     label = 'NO BODY'
                        #     nobody(frame_copy, label)
                        #     whetherBody = 0

                        maskFrameData = {}
                        maskFrameData['top'] = top
                        maskFrameData['bottom'] = bottom
                        maskFrameData['left'] = left
                        maskFrameData['right'] = right
                        maskFrameData['confidence'] = confidence
                        maskFrameData['label'] = label
                        # maskFrameData['img'] = img_mame

                        maskFrameDatas.append(maskFrameData)

                        maskIndex += 1

                        color = (0, 255, 0)
                        label_cn = "有口罩"
                        if label == "NO MASK":
                            color = (0, 0, 255)
                            label_cn = "无口罩"

                        cv2.rectangle(frame_copy, (left, top), (right, bottom), color, 3)
                        if top == 0:
                            cv2.putText(frame_copy, label, (left + 20, top + 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                        else:
                            cv2.putText(frame_copy, label, (left, top - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                except IndexError:
                    pass
                finally:
                    # writer.write(frame_copy)
                    cv2.imshow('Mask Detection', frame_copy)

                    # 记录数据为json格式
                    frameData['frame'] = index
                    frameData['data'] = maskFrameDatas
                    data.append(frameData)
                    print(json.dumps(frameData))

                    index += 1
                    cv2.waitKey(1)
            # with open("./detection_result/2-mask_deteection.json", 'w') as f:
            #     json.dump(data, f)
            #
            # writer.release()
            cv2.destroyWindow()

        def callbackClose():
            tkinter.messagebox.showwarning(title='警告', message='点击了关闭按钮')
            sys.exit(0)

        # 按钮
        window.protocol("WM_DELETE_WINDOW", callbackClose)
        action1 = ttk.Button(window, text='开始', command=start_dete)
        action1.grid(column=2, row=1)

        # 创建一个下拉列表
        number = tk.StringVar()
        numberChosen = ttk.Combobox(window, width=12, textvariable=number)
        numberChosen['value'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        numberChosen.grid(column=0, row=1)
        numberChosen.current(0)  # 默认值
        window.mainloop()

    def m_button4OnButtonClick(self, event):
        event.Skip()
        sys.exit(0)


app = wx.App()
main_win = MyFrame1(None)
main_win.Show()

app.MainLoop()
