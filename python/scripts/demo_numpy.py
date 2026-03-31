import numpy as np
from pathlib import Path

def create_num():
    data_array = np.zeros(shape=(3, 224, 224), dtype=np.float32)
    print(data_array.shape)
    print(data_array.dtype)

    array_normal = data_array / 255.0
    print(array_normal.shape)
    print(array_normal.dtype)

    array_latest = array_normal.reshape(1, 3, 224, 224)
    print(array_latest.shape)
    #arrat_latest = np.expand_dims(array_normal, dim=0)
    #np.transpose : x = np.random.rand(224, 224, 3)   y = np.transpose(x, (2, 0, 1))

    data_dir = Path("/home/daydreamer/Desktop/study/python/data")
    data_dir.mkdir(exist_ok=True)

    file_path = Path("preprocessed_data.npy")
    data_savepath = data_dir / file_path

    np.save(data_savepath, array_latest)
    print("save success")

    load_array = np.load(data_savepath)
    print("load succeff")
    print(load_array)
    print(load_array.shape)

if __name__ == "__main__":
    create_num()