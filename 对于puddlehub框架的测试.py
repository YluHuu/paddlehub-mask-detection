import matplotlib.pyplot as plt
import matplotlib.image as mping
import paddlehub as hub
import os
import cv2

# 加载模型
print('开始加载模型')
module = hub.Module(name="pyramidbox_lite_mobile_mask")
print('模型加载完毕')
# 待预测图片
#
test_img_path = ["./test_mask_detection.jpg"]
imgs = [cv2.imread(test_img_path[0])]

# 口罩检测预测
print('开始检测')
# visualization = True  预测结果可视化
# output_dir = 'detection_result'  预测结果图片保存在该文件夹下
results = module.face_detection(images=imgs, use_multi_scale=True, shrink=0.6,
                                visualization=True, output_dir='detection_result')
for result in results:
    print(result)

# 预测结果显示

path = os.path.join('detection_result', 'test_img.img')
img = mping.imread(path)
# 展示图片大小
plt.figure(figsize=(10, 10))
plt.imshow(img)
# 关闭轴
plt.axis('off')
plt.show()
print('检测完毕')

