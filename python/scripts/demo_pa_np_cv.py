import numpy as np
from pathlib import Path
import cv2

image_dir = Path("/home/daydreamer/Desktop/study/python/data")
file_dir = list(image_dir.glob("*.png"))
out_dir = Path(image_dir/"outputs")
out_dir.mkdir(exist_ok=True)

def myshell_image():
    for file_name in file_dir:
        img = cv2.imread(str(file_name))
        if img is None:
            print("failed to read:", file_name)
        else:
            img_resize = cv2.resize(img, (255, 255))
            img_nor = img_resize.astype(np.float32) / 255.0
            img_save = cv2.imwrite(out_dir / file_name.name, img_nor)
            # 如果你只是想保存“resize 后的可视化图片”，就直接保存 img_resize：

            # cv2.imwrite(str(out_dir / file_name.name), img_resize)

            # 如果你想保存归一化后的结果用于“看一眼”，那就要先乘回去再转 uint8：

            # img_to_save = (img_nor * 255).astype(np.uint8)
            # cv2.imwrite(str(out_dir / file_name.name), img_to_save)
            print("save:", img_save)

def myshell_np():
    img_list = []
    file_names = list(out_dir.glob("*.png"))
    if not file_names:
        print("empty")
        return
    
    # for file_path in file_names:
    #     # if file_names is None:
    #     # if not file_names:
    #     #     print("empty")
    #     #     return
    #     img = cv2.imread(str(file_path))
    #     img_c = np.transpose(img, (2, 0, 1))
    #     img_b = np.expand_dims(img_c, axis=0)
    #     # img_list += img_b
    #     img_list.append(img_b)

    for file_path in file_names:
        img = cv2.imread(str(file_path))  #cv2.imread() 就是把图片文件读进内存，并变成一个 NumPy 数组。
        if img is None:
            print("failed to read:", file_path)
            continue
        # img = img.astype(np.float32) / 255.0  上面已经做过了
        img_c = np.transpose(img, (2, 0, 1))   # HWC -> CHW
        img_list.append(img_c)
    print(type(img_list))
    print(type(img_list[0]))
    # preprocessed_data = np.array(img_list)
    preprocessed_data = np.stack(img_list, axis=0)   # NCHW
    print(type(preprocessed_data))
    print(preprocessed_data.dtype)
    print(preprocessed_data.shape)

if __name__ == "__main__":
    myshell_image()
    myshell_np()
            
#如果做可视化调试，再保存图片，如果直接模型输入，没必要


