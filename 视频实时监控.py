import json
import paddlehub as hub
import os
import cv2
from PIL import Image, ImageDraw, ImageFont

# 模型加载
print('开始加载模型')
module = hub.Module(name="pyramidbox_lite_mobile_mask")
print('加载完毕')


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

capture = cv2.VideoCapture(0)
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
                cv2.putText(frame_copy, label, (left+20, top+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            else:
                cv2.putText(frame_copy, label, (left, top-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    except IndexError:
        pass
    finally:
        writer.write(frame_copy)
        cv2.imshow('Mask Detection', frame_copy)

        # 记录数据为json格式
        frameData['frame'] = index
        frameData['data'] = maskFrameDatas
        data.append(frameData)
        print(json.dumps(frameData))

        index += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

with open("./detection_result/2-mask_deteection.json", 'w') as f:
    json.dump(data, f)

writer.release()
cv2.destroyWindow()
