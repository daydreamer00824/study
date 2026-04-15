import argparse
import onnxruntime as ort
from pathlib import Path
import cv2
import numpy as np

base_dir = Path(__file__).resolve().parent.parent

def useargparse():
    parse = argparse.ArgumentParser()
    parse.add_argument("--input", type=str, required=True)
    parse.add_argument("--output", type=str, required=True)
    parse.add_argument("--model", type=str, required=True)
    return parse.parse_args()


if __name__ == "__main__":
    arg = useargparse()
    input_dir = base_dir / Path(arg.input)
    out_dir = base_dir / Path(arg.output)
    model_path = base_dir / Path(arg.model)
    out_dir.mkdir(parents=True, exist_ok=True)

    session = ort.InferenceSession(str(model_path))

    print(session.get_inputs()[0])
    print(session.get_outputs()[0])

    input_name = Path("cat.png")
    input_path = input_dir / input_name

    img = cv2.imread(str(input_path))   ###string()
    if img is None:
        raise FileNotFoundError(f"failed to read image:{input_path}")
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_re = cv2.resize(img_rgb, (224,224))
    img_no = img_re.astype(np.float32) / 255.0
    img_c = np.transpose(img_no, (2, 0, 1))
    img_batch = np.expand_dims(img_c, axis=0)

    print(f"img shape:{img_batch.shape}")
    print(f"img dtype:{img_batch.dtype}")

    ###infer
    result = session.run([session.get_outputs()[0].name], {session.get_inputs()[0].name : img_batch})

    sorce = result[0]
    pred_id = int(np.argmax(sorce, axis=1)[0])
    pred_score = float(np.max(sorce, axis=1)[0])

    # print(sorce)
    print(type(sorce))
    print(sorce.shape)
    print(sorce.dtype)
    print(pred_id)
    print(pred_score)

    with open(out_dir / "result.txt", "w", encoding="utf-8") as f:
        f.write(f"pred_id: {pred_id}\n")
        f.write(f"pred_sorce: {pred_score}\n")
    print(f"result.txt success to save:{out_dir / 'result.txt'}")
