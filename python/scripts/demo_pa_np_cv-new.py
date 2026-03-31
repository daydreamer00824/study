import numpy as np
from pathlib import Path
import cv2

data_dir = Path("/home/daydreamer/Desktop/study/python/data")
file_dir = list(data_dir.glob("*.png"))
save_dir = Path("/home/daydreamer/Desktop/study/python/outputs")
save_dir.mkdir(exist_ok=True)

def build_batch():
    img_list = []

    if not file_dir:
        print("empty img")
        return
    
    for file_path in file_dir:
        img = cv2.imread(str(file_path))

        if img is None:
            print("failed to read:", file_path)
            continue

        #OpenCV 读图默认通常是 BGR。如果你后面模型希望输入是 RGB，那你这里应该加上：
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resize = cv2.resize(img_rgb, (255,255))
        img_normal = img_resize.astype(np.float32) / 255.0
        img_channel = np.transpose(img_normal, (2, 0, 1))
        # img_batch = np.expand_dims(img_channel, axis=0)
        # img_list.append(img_batch)
        img_list.append(img_channel)

    if not img_list:
        print("no vaild images")
        return

    batch_save = np.stack(img_list, axis=0)
    print(type(batch_save))
    print(batch_save.dtype)
    print(batch_save.shape)

    np.save(save_dir / "data.npy", batch_save)

    print("save success")

if __name__ == "__main__":
    build_batch()
    img_load = np.load(save_dir / "data.npy")
    print("load success")
    # print(img_load)
    print(type(img_load))
    print(img_load.dtype)
    print(img_load.shape)
    print(img_load.min(), img_load.max())

# 1. 图片也是数组，但不是所有数组都是图片。
# 2. cv2.imwrite() 适合保存图片，不适合保存任意张量。
# 3. .npy 适合保存 NumPy 数组，尤其适合保存模型输入和中间张量。
# 4. (H, W, 3) 更像图片，(N, 3, H, W) 更像模型输入。
# 5. 给人看的东西优先考虑图片格式，给模型用的东西优先考虑 .npy。
