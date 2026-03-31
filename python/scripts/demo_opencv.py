import cv2
import numpy as np

#cv2.imread() 就是把图片文件读进内存，并变成一个 NumPy 数组。
img = cv2.imread("/home/daydreamer/Desktop/study/python/data/test.png")

print(type(img))
print(img.dtype)
print(img.shape)

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
print(img_rgb.shape)

img = cv2.resize(img_rgb, (255, 255))
print(img.shape)
img_save = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
ok1 = cv2.imwrite("/home/daydreamer/Desktop/study/python/data/testresize.png", img_save)
#因为你前面已经把图从 BGR 转成 RGB 了。如果你想继续用 OpenCV 保存、查看，通常转回 BGR 更稳妥一些。
#!!!OpenCV 读彩色图时，默认通道顺序通常是 BGR
print("save success: ", ok1)

img = np.transpose(img, (2,0,1))  #!!!can't save
print(img.shape)
# ok2 = cv2.imwrite("/home/daydreamer/Desktop/study/python/data/testtranspose.png", img)
# print("save success: ", ok2)

img_normal = img.astype("float32") / 255.0
print(img_normal.dtype)
print(img_normal.shape)

img_batch = np.expand_dims(img_normal, axis=0)  #!!!can't save
print(img_batch.dtype)
print(img_batch.shape)
# cv2.imwrite("/home/daydreamer/Desktop/study/python/data/testbatch.png", img_batch)
# print("save success")

#more channel: np.stack(..., axis = 0)

#!!!opencv不能保存张量，只能保存图片,np.transpose之后以及变成CHW张量了，所以不能保存，np.expand_dims同样道理
# 1. (H, W, 3) 是普通图片，可以保存。
# 2. (3, H, W) 和 (1, 3, H, W) 是模型张量，不能直接保存。
# 3. cv2.imwrite() 只适合保存普通图片，不适合直接保存 batch tensor.