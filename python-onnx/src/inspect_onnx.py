import onnxruntime as ort
from pathlib import Path

model_path = Path(__file__).resolve().parent.parent / "models/model.onnx"

session = ort.InferenceSession(model_path)

print(session.get_inputs()[0])


print("=== inputs ===")
for x in session.get_inputs():
    print(f"name:{x.name}")
    print(f"shape:{x.shape}")
    print(f"type:{x.type}")
    print("-" * 30)

for y in session.get_outputs():
    print(f"name:{y.name}")
    print(f"shape:{y.shape}")
    print(f"type:{y.type}")
    print("-" * 30)