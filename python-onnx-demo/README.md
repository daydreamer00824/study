# ONNX Runtime 图像分类部署与性能测试

本项目是一个基于 **PyTorch ResNet18 + ONNX Runtime** 的图像分类部署示例，覆盖模型导出、ONNX 模型检查、PyTorch / ONNX Runtime 输出一致性验证、批量推理、CPU / GPU 性能测试与结果可视化。

项目重点不在模型训练，而在部署流程验证：将 PyTorch 视觉模型导出为 ONNX，检查模型结构，验证导出前后输出一致性，并在不同 ONNX Runtime Execution Provider 下进行推理性能 benchmark。

## 项目亮点

- 使用 `torchvision.models.resnet18` 导出 ONNX 模型，并支持动态 batch
- 检查 ONNX 模型合法性，查看输入 / 输出名称、shape 和数据类型
- 基于同一张输入图像验证 PyTorch 与 ONNX Runtime 输出一致性
- 使用 OpenCV 完成图像预处理：resize、BGR 转 RGB、ImageNet 归一化、HWC 转 CHW、NCHW batch 构造
- 支持 ONNX Runtime 批量推理，并可通过参数切换 Execution Provider
- 支持 Softmax + TopK 后处理，并将分类结果保存为 CSV
- 支持不同 batch size 下的 warmup、repeat 和 benchmark 测试
- 在同一 benchmark 脚本下对比 `CPUExecutionProvider` 与 `CUDAExecutionProvider`
- 保存 benchmark 明细结果与汇总统计结果
- 支持绘制吞吐量曲线和平均推理耗时曲线

## 当前进度

| 模块 | 状态 |
|---|---|
| PyTorch 到 ONNX 导出 | 已完成 |
| ONNX 模型检查与输入输出信息查看 | 已完成 |
| PyTorch / ONNX Runtime 一致性验证 | 已完成 |
| ONNX Runtime Python 批量推理 | 已完成 |
| ONNX Runtime CPU benchmark | 已完成 |
| ONNX Runtime GPU benchmark | 已完成 |
| C++ ONNX Runtime 推理 | 独立 C++ 模块中维护 |
| TensorRT engine 构建 | 计划中 |
| TensorRT FP16 推理 | 计划中 |

## 项目结构

```text
python-onnx-demo/
├── config/
│   └── config.yaml
├── input/
│   └── *.jpg / *.png
├── labels/
│   └── imagenet_classes.txt
├── logs/
├── model/
│   └── model.onnx
├── output/
│   ├── prediction_results.csv
│   ├── benchmark_results.csv
│   ├── benchmark_summary.csv
│   ├── verify_pytorch_onnx_cpu.json
│   ├── verify_pytorch_onnx_cuda.json
│   ├── benchmark_throughput.png
│   └── benchmark_avg_infer_ms.png
├── src/
│   ├── export_model.py
│   ├── check_onnx.py
│   ├── inspect_onnx.py
│   ├── verify_pytorch_onnx.py
│   ├── main.py
│   ├── benchmark_test.py
│   ├── plot_benchmark.py
│   ├── image_process.py
│   ├── postprocess.py
│   ├── label_map.py
│   ├── save_result_csv.py
│   ├── benchmark.py
│   ├── timer.py
│   ├── generate_labels.py
│   └── set_log.py
├── requirements.txt
└── README.md
```

> 实际目录名称可以按本地项目调整，但运行命令中的路径需要与本地目录保持一致。

## 测试环境

| 项目 | 版本 / 硬件 |
|---|---|
| 系统 | WSL2 Ubuntu |
| GPU | NVIDIA GeForce RTX 3060 12GB |
| NVIDIA Driver | 566.14 |
| CUDA Driver API | 12.7 |
| Python | 3.10 |
| ONNX Runtime | 1.23.2 |
| 可用 ORT Providers | `TensorrtExecutionProvider`, `CUDAExecutionProvider`, `CPUExecutionProvider` |

## 环境安装

创建 conda 环境：

```bash
conda create -n python-onnx python=3.10 -y
conda activate python-onnx
```

安装支持 CUDA 的 PyTorch。当前测试环境中，CUDA 12.6 wheel 可正常运行：

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

安装项目依赖：

```bash
pip install -r requirements.txt
```

检查 PyTorch CUDA：

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
```

检查 ONNX Runtime Provider：

```bash
python -c "import onnxruntime as ort; print(ort.__version__); print(ort.get_available_providers())"
```

期望输出中至少包含：

```text
CUDAExecutionProvider
CPUExecutionProvider
```

## 配置文件

配置文件路径：

```text
config/config.yaml
```

示例配置：

```yaml
base_path: .
extensions:
  - .jpg
  - .jpeg
  - .png
size:
  - 224
  - 224
batch_size: 12
```

`base_path: .` 表示项目根目录。建议在仓库根目录下运行所有命令，避免路径错误。

## 整体流程

```text
PyTorch ResNet18
    ↓ 导出
ONNX 模型
    ↓ 检查 / 查看输入输出信息
ONNX Runtime 模型验证
    ↓ 同一张图片 + 同一套预处理
PyTorch / ONNX Runtime 一致性验证
    ↓
ONNX Runtime 批量推理
    ↓
TopK 后处理与 CSV 保存
    ↓
CPU / GPU benchmark
    ↓
性能分析与可视化
```

## 模型导出

导出 PyTorch ResNet18 为 ONNX：

```bash
python src/export_model.py
```

导出的 ONNX 模型支持动态 batch：

```text
input : ['batch', 3, 224, 224]
output: ['batch', 1000]
```

## ONNX 模型检查与输入输出查看

检查 ONNX 模型是否合法：

```bash
python -c "from pathlib import Path; from src.check_onnx import check_onnx; check_onnx(Path('model/model.onnx'))"
```

查看 ONNX 输入输出信息：

```bash
python -c "from pathlib import Path; from src.inspect_onnx import inspect_onnx; inspect_onnx(Path('model/model.onnx'))"
```

期望信息：

```text
input name : input
input shape: ['batch', 3, 224, 224]
output name : output
output shape: ['batch', 1000]
```

## PyTorch / ONNX Runtime 一致性验证

该步骤用于验证导出的 ONNX 模型是否与原始 PyTorch 模型输出一致。验证方式为：使用同一张输入图片，经过同一套 OpenCV 预处理后，分别输入 PyTorch 原模型和 ONNX Runtime，并比较 logits 误差以及 TopK 结果。

CPU 验证：

```bash
python src/verify_pytorch_onnx.py \
  --onnx model/model.onnx \
  --image input/0013035.jpg \
  --output output/verify_pytorch_onnx_cpu.json \
  --device cpu \
  --provider CPUExecutionProvider
```

GPU 验证：

```bash
python src/verify_pytorch_onnx.py \
  --onnx model/model.onnx \
  --image input/0013035.jpg \
  --output output/verify_pytorch_onnx_cuda.json \
  --device cuda \
  --provider CUDAExecutionProvider
```

CPU 验证结果：

| 指标 | 结果 |
|---|---:|
| max_abs_error | 0.00001152 |
| mean_abs_error | 0.00000216 |
| PyTorch Top5 | `[310, 309, 308, 316, 321]` |
| ONNX Runtime Top5 | `[310, 309, 308, 316, 321]` |
| Top1 same | True |
| Top5 same | True |
| Result | PASS |

GPU 验证结果：

| 指标 | 结果 |
|---|---:|
| max_abs_error | 0.00744581 |
| mean_abs_error | 0.00118966 |
| PyTorch Top5 | `[310, 309, 308, 316, 321]` |
| ONNX Runtime Top5 | `[310, 309, 308, 316, 321]` |
| Top1 same | True |
| Top5 same | True |

GPU 验证中，logits 层面的数值误差大于 CPU 验证，但 Top1 和 Top5 结果保持一致。该现象通常与 PyTorch CUDA 和 ONNX Runtime CUDA 后端使用的 GPU kernel、精度策略等差异有关。本项目将其记录为 GPU 后端输出存在小幅数值差异，但分类结果一致。

## 批量推理

运行 ONNX Runtime 批量推理：

```bash
python src/main.py \
  --input input \
  --output output \
  --models model \
  --config config \
  --log logs
```

预测结果保存到：

```text
output/prediction_results.csv
```

主要字段：

| 字段 | 含义 |
|---|---|
| image_name | 输入图片文件名 |
| image_path | 输入图片路径 |
| top1_index | Top1 类别索引 |
| top1_label | Top1 类别名称 |
| top1_score | Top1 置信度 |
| top5_indices | Top5 类别索引 |
| top5_labels | Top5 类别名称 |
| top5_scores | Top5 置信度 |

## Benchmark

`benchmark_test.py` 支持不同 batch size、warmup、repeat 以及可配置的 ONNX Runtime Execution Provider。

CPU benchmark：

```bash
python src/benchmark_test.py \
  --input input \
  --output output_cpu \
  --models model \
  --config config \
  --log logs \
  --provider CPUExecutionProvider \
  --batch_size 1 4 8 12 16 32 \
  --warmup 5 \
  --repeat 10
```

GPU benchmark：

```bash
python src/benchmark_test.py \
  --input input \
  --output output_gpu \
  --models model \
  --config config \
  --log logs \
  --provider CUDAExecutionProvider \
  --batch_size 1 4 8 12 16 32 \
  --warmup 5 \
  --repeat 10
```

输出文件：

| 文件 | 含义 |
|---|---|
| `benchmark_results.csv` | 每次 repeat 的 benchmark 明细结果 |
| `benchmark_summary.csv` | 每个 batch size 的 mean / std 汇总结果 |

Benchmark 指标：

| 指标 | 含义 |
|---|---|
| `avg_infer_ms_mean` | 平均单图推理耗时，单位 ms/image |
| `avg_infer_ms_std` | 平均单图推理耗时标准差 |
| `throughput_mean` | 平均吞吐量，单位 image/s |
| `throughput_std` | 吞吐量标准差 |
| `best_by_throughput` | 当前 batch size 是否为吞吐量最优 |

> 当前 benchmark 统计的是预处理后的 tensor 输入 ONNX Runtime 后的模型推理耗时，不包含图片读取、预处理和完整端到端耗时。

## Benchmark 结果

测试设置：

| 项目 | 设置 |
|---|---|
| 模型 | ResNet18 ONNX |
| 输入尺寸 | 224 × 224 |
| 图片数量 | 244 |
| Batch size | 1 / 4 / 8 / 12 / 16 / 32 |
| Warmup | 5 |
| Repeat | 10 |
| 统计指标 | 平均推理耗时与吞吐量 |

### CPUExecutionProvider

| Batch Size | 平均推理耗时 ms/image | 吞吐量 image/s | 是否最优 |
|---:|---:|---:|---|
| 1 | 5.507 | 182.018 | 是 |
| 4 | 5.717 | 175.689 | 否 |
| 8 | 5.599 | 178.771 | 否 |
| 12 | 5.640 | 177.414 | 否 |
| 16 | 5.573 | 179.679 | 否 |
| 32 | 5.985 | 167.664 | 否 |

### CUDAExecutionProvider

| Batch Size | 平均推理耗时 ms/image | 吞吐量 image/s | 是否最优 |
|---:|---:|---:|---|
| 1 | 1.437 | 695.959 | 否 |
| 4 | 0.859 | 1163.777 | 否 |
| 8 | 0.826 | 1210.189 | 否 |
| 12 | 0.829 | 1206.619 | 否 |
| 16 | 0.771 | 1297.303 | 否 |
| 32 | 0.692 | 1445.357 | 是 |

### CPU / GPU 对比

| Backend | 最优 Batch Size | 平均推理耗时 ms/image | 吞吐量 image/s |
|---|---:|---:|---:|
| ONNX Runtime CPU | 1 | 5.507 | 182.018 |
| ONNX Runtime GPU | 32 | 0.692 | 1445.357 |

在同一 benchmark 脚本与同一图片集下，GPU 最优吞吐约为：

```text
1445.357 / 182.018 ≈ 7.94×
```

该结果表明，在 RTX 3060 上，`CUDAExecutionProvider` 在批量 ResNet18 推理任务中相比 `CPUExecutionProvider` 具有明显吞吐优势。

## 可视化

生成 benchmark 曲线：

```bash
python src/plot_benchmark.py \
  --summary output_gpu/benchmark_summary.csv \
  --output output_gpu
```

预期输出：

| 文件 | 含义 |
|---|---|
| `benchmark_throughput.png` | batch size 与吞吐量关系曲线 |
| `benchmark_avg_infer_ms.png` | batch size 与平均推理耗时关系曲线 |

## Batch Size 说明

CPU benchmark 中，增大 batch size 没有提升吞吐量，最优吞吐出现在 batch size = 1。

GPU benchmark 中，随着 batch size 增大，吞吐量整体提升，最优吞吐出现在 batch size = 32。这说明在当前模型和输入尺寸下，较大的 batch size 能更充分利用 GPU 并行计算能力。

最优 batch size 与硬件、模型结构、输入尺寸、Provider 和部署场景有关，不能直接假设，需要在目标环境下实际测试。

## 当前限制

- 当前模型为 ResNet18 图像分类模型，暂未覆盖检测、分割等模型。
- 当前 benchmark 主要统计预处理后的模型推理耗时，不是完整端到端耗时。
- GPU 验证中 Top1 / Top5 一致，但 PyTorch CUDA 与 ONNX Runtime CUDA 的 logits 数值并非逐元素严格一致。
- TensorRT FP32 / FP16 engine 构建和 TensorRT 推理 benchmark 尚未纳入当前 README。
- C++ ONNX Runtime 推理目前作为独立模块维护，后续如合并到本仓库，需要单独补充文档。

## Roadmap

- [x] PyTorch ResNet18 导出 ONNX
- [x] ONNX 模型检查与输入输出信息查看
- [x] PyTorch / ONNX Runtime 一致性验证
- [x] ONNX Runtime Python 批量推理
- [x] CPUExecutionProvider benchmark
- [x] CUDAExecutionProvider benchmark
- [x] CPU / GPU benchmark 对比
- [ ] TensorRT FP32 engine 构建
- [ ] TensorRT FP16 engine 构建
- [ ] TensorRT 推理 benchmark
- [ ] ONNX Runtime 与 TensorRT 性能对比
- [ ] 增加包含预处理的端到端延迟统计
- [ ] 整合 C++ ONNX Runtime 文档

