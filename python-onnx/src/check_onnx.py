import onnx
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
model_dir = Path("models/model.onnx")

model_path = base_dir / model_dir

onnx_model = onnx.load(model_path)
onnx.checker.check_model(onnx_model)

print("ONNX model check passed")