# Python ONNX Runtime 图像分类部署 Demo

本项目是一个基于 **Python + ONNX Runtime** 的图像分类部署示例，用于完成从 PyTorch 模型导出、ONNX 模型检查、图像预处理、批量推理、TopK 后处理、结果保存到性能 benchmark 的完整部署流程。

当前项目目标不是只让代码跑通，而是形成一个可以写进 README、简历并用于面试讲解的视觉 AI 部署工程项目。

---

## 1. 项目功能

当前已实现功能：

- PyTorch ResNet18 模型导出为 ONNX
- ONNX 模型合法性检查
- ONNX 模型输入输出结构查看
- OpenCV 图像读取、resize、归一化、NCHW 转换
- ONNX Runtime 批量推理
- Softmax + TopK 分类后处理
- ImageNet 类别映射
- 推理结果保存为 CSV
- 预处理、推理、后处理、结果保存耗时统计
- 不同 batch_size 下的 benchmark 测试
- benchmark 明细与汇总结果保存
- 自动标记当前测试中吞吐量最高的 batch_size

---

## 2. 项目结构

```text
python-onnx-demo/
├── config/
│   └── config.yaml
├── input/
│   └── images/
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
│   └── benchmark_summary.csv
│   └── images_resize
├── src/
│   ├── main.py
│   ├── benchmark_test.py
│   ├── export_model.py
│   ├── check_onnx.py
│   ├── inspect_onnx.py
│   ├── image_process.py
│   ├── postprocess.py
│   ├── label_map.py
│   ├── save_result_csv.py
│   ├── benchmark.py
│   ├── timer.py
│   ├── generate_labens.py
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
```

可以根据当前环境生成依赖文件：

```bash
pip freeze > requirements.txt
```

安装依赖：

```bash
pip install -r requirements.txt
```

---

## 4. 配置文件

配置文件路径：

```text
config/config.yaml
```

配置文件中通常包含：

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

其中：

| 字段 | 含义 |
|---|---|
| base_path | 项目根目录 |
| extensions | 支持读取的图片后缀 |
| size | 模型输入图片尺寸 |
| batch_size | 主推理流程默认 batch_size |

> 当前代码中 `base_path` 仍依赖本地路径。后续可以优化为自动识别项目根目录，减少路径硬编码。

---

## 5. 主推理流程

主程序入口为：

```bash
python src/main.py \
  --input data/images \
  --output outputs \
  --models models \
  --config config \
  --log logs
```

如果你的脚本就在项目根目录，而不是 `src/` 目录下，则使用：

```bash
python main.py \
  --input data/images \
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
8. 对模型输出做 softmax 和 TopK 后处理
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
图片预处理
↓
ONNX Runtime 推理
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
| image_name | 图片文件名 |
| image_path | 图片路径 |
| top1_index | Top1 类别索引 |
| top1_label | Top1 类别名称 |
| top1_score | Top1 置信度 |
| top5_indices | Top5 类别索引 |
| top5_labels | Top5 类别名称 |
| top5_scores | Top5 置信度 |

该文件用于记录每张图片的分类结果，便于后续检查模型输出是否合理，也可以作为项目运行证据。

---

## 7. Benchmark：batch_size 对推理性能的影响

本项目提供 `benchmark_test.py`，用于测试不同 `batch_size` 对 ONNX Runtime 推理性能的影响。

测试脚本会对多个 batch_size 进行重复测试，并保存两类结果：

| 文件 | 作用 |
|---|---|
| `benchmark_results.csv` | 保存每一次 repeat 的明细结果 |
| `benchmark_summary.csv` | 保存每个 batch_size 的汇总统计结果 |

### 7.1 运行命令

如果脚本位于 `src/` 目录：

```bash
python src/benchmark_test.py \
  --input data/images \
  --output outputs \
  --models models \
  --config config \
  --log logs \
  --batch_size 1 4 8 12 16 32 \
  --repeat 3
```

如果脚本位于项目根目录：

```bash
python benchmark_test.py \
  --input data/images \
  --output outputs \
  --models models \
  --config config \
  --log logs \
  --batch_size 1 4 8 12 16 32 \
  --repeat 3
```

### 7.2 测试设置

| 项目 | 设置 |
|---|---|
| 模型 | ResNet18 ONNX |
| 推理框架 | ONNX Runtime |
| 输入尺寸 | 224 × 224 |
| 图片数量 | 244 |
| batch_size | 1 / 4 / 8 / 12 / 16 / 32 |
| repeat | 每个 batch_size 重复 3 次 |
| 主要指标 | 平均单图推理耗时、吞吐量 |

### 7.3 汇总结果

本次 benchmark 结果如下：

| batch_size | repeat_count | image_count | avg_infer_ms_mean | throughput_mean | best_by_throughput |
|---:|---:|---:|---:|---:|---|
| 1 | 3 | 244 | 5.095 | 196.288 | False |
| 4 | 3 | 244 | 4.633 | 215.846 | False |
| 8 | 3 | 244 | 4.591 | 217.907 | False |
| 12 | 3 | 244 | 4.513 | 221.571 | True |
| 16 | 3 | 244 | 4.522 | 221.151 | False |
| 32 | 3 | 244 | 4.519 | 221.295 | False |

### 7.4 结果分析

从测试结果看，`batch_size=1` 时平均吞吐量约为 `196.288 image/s`。当 batch_size 增大到 `4`、`8`、`12` 后，吞吐量逐步提升。

本次测试中，`batch_size=12` 的平均吞吐量最高，为 `221.571 image/s`，对应平均单图 ONNX 推理耗时为 `4.513 ms/image`。

但 `batch_size=12`、`16`、`32` 的吞吐量差距较小：

| batch_size | throughput_mean |
|---:|---:|
| 12 | 221.571 image/s |
| 16 | 221.151 image/s |
| 32 | 221.295 image/s |

因此，不能简单认为 `batch_size=12` 在所有环境下都绝对最优。更合理的结论是：在当前测试环境下，batch_size 增大到 `8～12` 后，吞吐量进入平台期。实际部署时应结合吞吐量、单次请求延迟、内存占用和业务需求选择合适的 batch_size。

---

## 8. 指标说明

### 8.1 avg_infer_ms

`avg_infer_ms` 表示平均每张图片的 ONNX 推理耗时，单位是 `ms/image`。

计算方式：

```text
avg_infer_ms = infer_time / image_count × 1000
```

其中：

| 变量 | 含义 |
|---|---|
| infer_time | 所有图片的 ONNX 推理总耗时，单位为秒 |
| image_count | 图片数量 |
| 1000 | 秒转换为毫秒 |

### 8.2 throughput

`throughput` 表示单位时间内可以处理多少张图片，单位是 `image/s`。

计算方式：

```text
throughput = image_count / infer_time
```

其中：

| 变量 | 含义 |
|---|---|
| image_count | 图片数量 |
| infer_time | 所有图片的 ONNX 推理总耗时，单位为秒 |

### 8.3 mean 与 std

benchmark 中对每个 batch_size 重复测试多次：

- `mean` 表示多次测试的平均性能
- `std` 表示多次测试之间的波动程度

这样可以避免只根据单次运行结果判断性能。

### 8.4 batch_size 的影响

较大的 batch_size 通常可以提升吞吐量，因为模型推理中的部分固定开销可以被多张图片分摊。

但 batch_size 不是越大越好。batch_size 增大后，可能带来更高的内存占用，也可能增加单批次等待时间。在实时推理场景中，除了吞吐量，还需要关注单张图片的响应延迟。

---

## 9. 日志输出

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
- 每个 batch 的推理状态
- 总耗时统计
- benchmark 每轮测试结果
- benchmark 汇总结果

日志用于定位运行问题，也可以作为项目运行证据。

---

## 10. 当前项目阶段总结

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
性能结果汇总
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

---

## 11. 后续计划

后续可继续扩展：

1. 增加 ONNX Runtime Provider 对比  
   例如 `CPUExecutionProvider` 和 `CUDAExecutionProvider`

2. 增加 warmup  
   减少首次推理、缓存和初始化带来的 benchmark 波动

3. 增加 benchmark 可视化  
   绘制 batch_size 与 throughput、avg_infer_ms 的关系曲线

4. 优化路径配置  
   减少 `base_path` 绝对路径依赖，提高项目可迁移性

5. 增加 C++ 版本推理链路  
   使用 C++、OpenCV、ONNX Runtime 实现同类部署流程

6. 进行真实设备部署验证  
   在 NVIDIA 小主机、Jetson、RK3588 或其他边缘设备上测试推理性能

---

## 12. 面试表达示例

可以这样介绍本项目：

> 我实现了一个 Python ONNX Runtime 图像分类部署 demo，包含模型导出、ONNX 检查、图像预处理、batch 推理、TopK 后处理、CSV 结果保存和推理耗时统计。  
>  
> 在性能测试部分，我实现了 batch_size benchmark，对多个 batch_size 进行重复测试，保存每次测试明细，并生成汇总统计文件。测试结果显示 batch_size 从 1 增大到 8～12 后吞吐量明显提升，之后进入平台期。  
>  
> 因此我没有简单把单次最高值当成绝对最优，而是结合平均吞吐量、波动情况和业务场景来判断较优 batch 区间。后续可以继续扩展 CPU/GPU Provider 对比和边缘设备部署验证。

---

## 13. 当前限制

当前项目仍有以下限制：

- 目前主要验证的是 ResNet18 分类模型
- 目前 benchmark 主要关注 ONNX 推理时间，尚未完整比较端到端总耗时
- 当前结果依赖本地硬件环境，不代表所有设备上的性能
- 还未加入 CPU / GPU Provider 对比
- 还未进行真实边缘设备部署验证

这些限制也是后续继续完善项目的方向。

