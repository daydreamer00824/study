# Python ONNX Runtime 图像分类部署 Demo

本项目是一个基于 **Python + ONNX Runtime** 的图像分类部署示例，用于完成从 PyTorch 模型导出、ONNX 模型检查、图像预处理、批量推理、TopK 后处理、结果保存、性能 benchmark 到结果可视化的完整部署流程。

项目目标不是只让代码跑通，而是形成一个可复现、可分析、可展示的视觉 AI 部署工程小项目。项目覆盖模型导出、ONNX Runtime 推理、结果保存、性能测试与可视化分析，可作为后续 C++ 推理链路和边缘设备部署验证的基础。

---

## 1. 项目功能

当前已实现：

- PyTorch ResNet18 模型导出为 ONNX
- ONNX 模型合法性检查
- ONNX 模型输入输出结构查看
- OpenCV 图像读取、resize、BGR 转 RGB
- ImageNet 标准归一化
- NCHW 输入格式转换
- ONNX Runtime 批量推理
- Softmax + TopK 分类后处理
- ImageNet 类别映射
- 推理结果保存为 CSV
- 预处理、推理、后处理、结果保存耗时统计
- 不同 batch_size 下的 benchmark 测试
- benchmark warmup 预热
- repeat 多次重复测试
- mean / std 汇总统计
- ONNX Runtime Execution Provider 参数化
- benchmark 明细与汇总结果保存
- 自动标记当前测试中吞吐量最高的 batch_size
- benchmark 性能曲线可视化

---

## 2. 项目结构

```text
python-onnx-demo/
├── config/
│   └── config.yaml
├── input/
├── labels/
│   └── imagenet_classes.txt
├── logs/
│   ├── run.log
│   └── run_test.log
├── models/
│   └── model.onnx
├── outputs/
│   ├── prediction_results.csv
│   ├── benchmark_results.csv
│   ├── benchmark_summary.csv
│   ├── benchmark_throughput.png
│   ├── benchmark_avg_infer_ms.png
│   └── images_resize/
├── src/
│   ├── main.py
│   ├── benchmark_test.py
│   ├── plot_benchmark.py
│   ├── export_model.py
│   ├── check_onnx.py
│   ├── inspect_onnx.py
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

> 注：实际目录结构以本地项目为准。如果脚本不在 `src/` 目录下，请根据实际位置调整运行命令。

---

## 3. 环境依赖

主要依赖：

```text
python
torch
torchvision
onnx
onnxruntime
opencv-python
numpy
pyyaml
pandas
matplotlib
```

安装依赖：

```bash
pip install -r requirements.txt
```

如果只进行 CPU 推理，安装 `onnxruntime` 即可。  
如果后续需要 CUDA 推理，应根据 CUDA / cuDNN 版本安装匹配的 `onnxruntime-gpu`。

---

## 4. 配置文件

配置文件路径：

```text
config/config.yaml
```

配置文件示例：

```yaml
base_path: /path/to/python-onnx-demo
extensions:
  - .jpg
  - .jpeg
  - .png
size:
  - 224
  - 224
batch_size: 12
```

字段说明：

| 字段 | 含义 |
|---|---|
| `base_path` | 项目根目录 |
| `extensions` | 支持读取的图片后缀 |
| `size` | 模型输入图片尺寸 |
| `batch_size` | 主推理流程默认 batch_size |

> 当前版本仍使用 `base_path` 指定项目根目录，后续可优化为自动识别项目路径，提高可迁移性。

---

## 5. 主推理流程

主程序入口为：

```bash
python src/main.py \
  --input input \
  --output outputs \
  --models models \
  --config config \
  --log logs
```

如果脚本位于项目根目录，则使用：

```bash
python main.py \
  --input input \
  --output outputs \
  --models models \
  --config config \
  --log logs
```

主流程包括：

1. 读取配置文件
2. 加载 ImageNet 类别文件
3. 检查 ONNX 模型是否存在，不存在则自动导出
4. 检查 ONNX 文件合法性
5. 查看 ONNX 输入输出信息
6. 收集并预处理输入图片
7. 使用 ONNX Runtime 按 batch 推理
8. 对模型输出做 Softmax + TopK 后处理
9. 保存预测结果到 CSV
10. 统计预处理、推理、后处理和结果保存耗时

完整链路：

```text
配置加载
↓
类别加载
↓
模型导出 / 复用
↓
ONNX 检查
↓
输入输出结构查看
↓
图片预处理
↓
ONNX Runtime batch 推理
↓
TopK 后处理
↓
CSV 结果保存
↓
耗时统计
```

---

## 6. 推理结果保存

推理结果保存到：

```text
outputs/prediction_results.csv
```

主要字段：

| 字段 | 含义 |
|---|---|
| `image_name` | 图片文件名 |
| `image_path` | 图片路径 |
| `top1_index` | Top1 类别索引 |
| `top1_label` | Top1 类别名称 |
| `top1_score` | Top1 置信度 |
| `top5_indices` | Top5 类别索引 |
| `top5_labels` | Top5 类别名称 |
| `top5_scores` | Top5 置信度 |

该文件用于记录每张图片的分类结果，便于检查模型输出是否合理，也可以作为项目运行证据。

---

## 7. Benchmark：batch_size 对推理性能的影响

本项目提供 `benchmark_test.py`，用于测试不同 `batch_size` 对 ONNX Runtime 推理性能的影响。

当前 benchmark 支持：

- 指定 batch_size 列表
- 指定 repeat 重复测试次数
- 指定 warmup 预热次数
- 指定 ONNX Runtime Execution Provider
- 保存每次测试明细
- 保存按 batch_size 汇总后的 mean / std 结果
- 自动标记吞吐量最高的 batch_size

### 7.1 运行命令

如果脚本位于 `src/` 目录：

```bash
python src/benchmark_test.py \
  --input input \
  --output outputs \
  --models models \
  --config config \
  --log logs \
  --batch_size 1 4 8 12 16 32 \
  --repeat 10 \
  --warmup 3 \
  --provider CPUExecutionProvider
```

如果脚本位于项目根目录：

```bash
python benchmark_test.py \
  --input input \
  --output outputs \
  --models models \
  --config config \
  --log logs \
  --batch_size 1 4 8 12 16 32 \
  --repeat 10 \
  --warmup 3 \
  --provider CPUExecutionProvider
```

### 7.2 参数说明

| 参数 | 含义 |
|---|---|
| `--batch_size` | 要测试的 batch_size 列表 |
| `--repeat` | 每个 batch_size 重复测试次数 |
| `--warmup` | 正式计时前的预热轮数 |
| `--provider` | ONNX Runtime Execution Provider |

当前测试环境可用 Provider：

```text
AzureExecutionProvider
CPUExecutionProvider
```

当前环境暂未检测到 `CUDAExecutionProvider`，因此本阶段只进行 `CPUExecutionProvider` benchmark。

---

## 8. Benchmark 输出文件

Benchmark 会生成两个 CSV 文件：

| 文件 | 作用 |
|---|---|
| `outputs/benchmark_results.csv` | 保存每一次 repeat 的明细结果 |
| `outputs/benchmark_summary.csv` | 保存每个 batch_size 的汇总统计结果 |

`benchmark_results.csv` 主要字段：

| 字段 | 含义 |
|---|---|
| `provider` | ONNX Runtime Execution Provider |
| `batch_size` | 当前测试的 batch_size |
| `repeat_id` | 当前第几次重复测试 |
| `image_count` | 图片数量 |
| `preprocess_time` | 预处理耗时 |
| `infer_time` | ONNX 推理总耗时 |
| `postprocess_time` | 后处理耗时 |
| `save_result_time` | 结果保存耗时 |
| `avg_infer_ms` | 平均单图推理耗时 |
| `throughput` | 吞吐量 |

`benchmark_summary.csv` 主要字段：

| 字段 | 含义 |
|---|---|
| `provider` | ONNX Runtime Execution Provider |
| `batch_size` | 当前测试的 batch_size |
| `repeat_count` | 有效重复测试次数 |
| `image_count` | 图片数量 |
| `avg_infer_ms_mean` | 平均单图推理耗时均值 |
| `avg_infer_ms_std` | 平均单图推理耗时标准差 |
| `throughput_mean` | 吞吐量均值 |
| `throughput_std` | 吞吐量标准差 |
| `best_by_throughput` | 是否为当前测试中吞吐量最高的 batch_size |

---

## 9. Benchmark 可视化

`plot_benchmark.py` 用于读取 `benchmark_summary.csv`，并绘制性能曲线图。

运行命令：

```bash
python src/plot_benchmark.py \
  --summary outputs/benchmark_summary.csv \
  --output outputs
```

如果脚本位于项目根目录：

```bash
python plot_benchmark.py \
  --summary outputs/benchmark_summary.csv \
  --output outputs
```

输出图片：

| 文件 | 含义 |
|---|---|
| `outputs/benchmark_throughput.png` | batch_size 与吞吐量关系图 |
| `outputs/benchmark_avg_infer_ms.png` | batch_size 与平均单图推理耗时关系图 |

图中误差线表示多次 repeat 的标准差，用于观察性能波动情况。

### Throughput 曲线

![Batch Size vs Throughput](outputs/benchmark_throughput.png)

### Average Inference Time 曲线

![Batch Size vs Avg Inference Time](outputs/benchmark_avg_infer_ms.png)

---

## 10. 最新 Benchmark 结果

测试设置：

| 项目 | 设置 |
|---|---|
| 模型 | ResNet18 ONNX |
| 推理框架 | ONNX Runtime |
| Provider | CPUExecutionProvider |
| 输入尺寸 | 224 × 224 |
| 图片数量 | 244 |
| batch_size | 1 / 4 / 8 / 12 / 16 / 32 |
| repeat | 10 |
| warmup | 3 |

> 精确数值以 `outputs/benchmark_summary.csv` 为准。当前 README 的结果分析基于 repeat=10 后生成的可视化图和汇总结果。

---

## 11. 指标说明

### 11.1 avg_infer_ms

`avg_infer_ms` 表示平均每张图片的 ONNX 推理耗时，单位是 `ms/image`。

计算方式：

```text
avg_infer_ms = infer_time / image_count × 1000
```

其中：

| 变量 | 含义 |
|---|---|
| `infer_time` | 所有图片的 ONNX 推理总耗时，单位为秒 |
| `image_count` | 图片数量 |
| `1000` | 秒转换为毫秒 |

### 11.2 throughput

`throughput` 表示单位时间内可以处理多少张图片，单位是 `image/s`。

计算方式：

```text
throughput = image_count / infer_time
```

其中：

| 变量 | 含义 |
|---|---|
| `image_count` | 图片数量 |
| `infer_time` | 所有图片的 ONNX 推理总耗时，单位为秒 |

### 11.3 mean 与 std

benchmark 中对每个 batch_size 重复测试多次：

- `mean` 表示多次测试的平均性能
- `std` 表示多次测试之间的波动程度

这样可以避免只根据单次运行结果判断性能。

### 11.4 warmup

`warmup` 表示正式计时前先运行若干轮推理，但不把这些推理耗时计入最终 benchmark。

加入 warmup 的目的是减少 ONNX Runtime 初始化、内存分配、缓存状态等因素对正式计时的影响，使 benchmark 更稳定。

### 11.5 Provider

ONNX Runtime 通过 Execution Provider 指定模型运行后端，例如：

- `CPUExecutionProvider`：CPU 推理
- `CUDAExecutionProvider`：NVIDIA GPU 推理

当前项目在创建 Session 前会检查当前环境可用 Provider，并记录实际使用的 Provider，避免不清楚模型到底运行在哪个后端。

---

## 12. 结果分析

从当前 `CPUExecutionProvider` 测试结果看，batch_size 增大并没有稳定带来吞吐量提升。

在当前环境下，`batch_size=1` 的吞吐量表现较好，平均单图推理耗时也较低。`batch_size=4` 和 `batch_size=12` 表现相对接近，而较大的 batch_size，如 `16` 和 `32`，吞吐量下降且波动更明显。

这说明在当前 CPU 推理环境中，增大 batch_size 不一定能提升性能。相比 GPU，CPU 对大 batch 的并行收益可能有限，同时还可能受到缓存、内存带宽、线程调度和虚拟机环境波动等因素影响。

因此，本项目没有简单认为 batch_size 越大越好，而是通过 warmup、repeat、mean、std 和可视化曲线综合判断性能表现。实际部署时应根据具体硬件、Provider、输入规模和业务延迟要求重新测试。

---

## 13. 日志输出

主推理日志默认保存到：

```text
logs/run.log
```

benchmark 日志默认保存到：

```text
logs/run_test.log
```

日志内容包括：

- 配置文件是否加载成功
- ONNX 模型是否存在或是否重新导出
- ONNX 检查是否通过
- 模型输入输出 shape
- 图片数量
- 当前环境可用 Provider
- Session 实际使用 Provider
- warmup 执行情况
- 每个 batch_size 的 repeat 测试结果
- benchmark 汇总结果

日志用于定位运行问题，也可以作为项目运行证据。

---

## 14. 当前项目阶段总结

当前项目已经完成 Python ONNX Runtime 图像分类部署基础闭环：

```text
模型导出
↓
ONNX 检查
↓
图片预处理
↓
ONNX Runtime 推理
↓
TopK 后处理
↓
结果保存
↓
耗时统计
↓
batch_size benchmark
↓
warmup + repeat
↓
Provider 参数化
↓
性能结果汇总
↓
benchmark 可视化
```

当前项目可以用于展示以下能力：

- 基础视觉部署链路搭建
- ONNX 模型导出与检查
- 图像预处理与模型输入格式转换
- ONNX Runtime 批量推理
- 分类结果后处理
- CSV 结果保存
- 推理性能统计
- batch_size 性能测试与工程分析
- warmup、repeat、mean、std 的 benchmark 方法
- ONNX Runtime Provider 指定与记录
- benchmark 可视化与结果分析

---

## 15. 当前限制

当前项目仍有以下限制：

- 当前主要验证的是 ResNet18 图像分类模型
- 当前测试环境只检测到 `CPUExecutionProvider`，暂未进行 `CUDAExecutionProvider` 对比
- 当前运行环境存在虚拟机因素，benchmark 结果不代表所有物理机或边缘设备
- 当前 benchmark 主要关注 ONNX 推理时间，端到端耗时分析还可以进一步增强
- 当前路径配置仍依赖 `base_path`，项目可迁移性还有优化空间
- 当前尚未完成 C++ 推理链路和真实边缘设备部署验证

这些限制也是后续继续完善项目的方向。

---

## 16. 后续计划

后续可继续扩展：

1. 优化路径配置，减少本地绝对路径依赖
2. 增加主推理流程的 Provider 参数
3. 在真实 NVIDIA 小主机或边缘设备上测试 `CUDAExecutionProvider`
4. 增加 C++ OpenCV + ONNX Runtime 推理链路
5. 扩展到检测或分割模型部署
6. 完善端到端耗时统计与部署分析
