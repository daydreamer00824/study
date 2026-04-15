import torch
import torchvision.models as models
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent

save_dir_name = Path("models")
save_name = Path("model.onnx")
save_dir= base_dir / save_dir_name
save_dir.mkdir(parents=True, exist_ok=True)
save_path = save_dir / save_name


model = models.resnet18(weights = None)

model.eval()

dummy_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model,
    (dummy_input),
    save_path,
    input_names=["input"],
    output_names=["output"]
)

print(f"Export finished:{save_path}")