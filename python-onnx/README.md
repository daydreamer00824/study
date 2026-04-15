# Python ONNX 最小部署示例

## 1. 项目简介

本项目是一个基于 Python 的 ONNX 最小部署示例，用于学习和演示以下基本流程：

1. 将 PyTorch 模型导出为 ONNX 模型
2. 检查 ONNX 模型是否合法
3. 查看模型输入输出信息
4. 使用 ONNX Runtime 完成单张图片推理
5. 保存推理结果

本项目的目标是学习 ONNX / ONNX Runtime 的基础部署流程，而不是追求分类精度。

## 2. 项目结构

```text
python-onnx/
├── src/
│   ├── export_onnx.py
│   ├── check_onnx.py
│   ├── inspect_onnx.py
│   └── infer_one_image.py
├── models/
│   └── model.onnx
├── image/
│   └── cat.png
├── output/
│   └── result.txt
├── requirements.txt
└── README.md
3. 环境依赖
Python 3.10
torch
torchvision
onnx
onnxruntime
numpy
opencv-python

安装依赖：

pip install -r requirements.txt
4. 脚本说明
export_onnx.py

将 PyTorch 分类模型导出为 ONNX 格式。

check_onnx.py

检查导出的 ONNX 模型是否合法。

inspect_onnx.py

查看模型输入输出信息，包括：

输入名称
输入形状
输入类型
输出名称
输出形状
输出类型
infer_one_image.py

使用 ONNX Runtime 对单张图片进行推理，并将结果保存到 outputs/result.txt。

5. 运行方式
第一步：导出 ONNX 模型
python src/export_onnx.py
第二步：检查 ONNX 模型
python src/check_onnx.py
第三步：查看模型输入输出信息
python src/inspect_onnx.py
第四步：进行单张图片推理
python src/infer_one_image.py --input images --output output --model models/model.onnx
6. 输出结果

推理完成后，结果会保存在：

output/result.txt

示例结果：

pred_id: 123
pred_score: 0.56
7. 注意事项
当前脚本只适用于分类模型。
当前 export_onnx.py 中使用的是 weights=None，因此模型权重是随机初始化的。
当前推理结果仅用于验证部署流程是否跑通，不代表真实分类能力。
如果后续使用预训练权重，需要同步调整前处理方式，使其与模型训练时保持一致。
8. 学习目标

本项目重点学习以下内容：

PyTorch 模型导出
ONNX 模型检查
ONNX Runtime 模型加载
输入前处理
输出结果解析
9. 后续可扩展方向
使用预训练权重
增加批量推理
比较 PyTorch 与 ONNX Runtime 的输出一致性
扩展到检测或分割模型
增加日志与更规范的工程结构
从单图到批量推理。
从分类到检测和分割。
从固定 shape 到动态 shape。PyTorch 文档里也明确写了，如果需要动态 shape，要在导出时设置 dynamic_shapes。
从“能跑”到“和 PyTorch 输出做一致性验证”。PyTorch 导出接口里也提供了 verify 选项。

学习总结：
本周完成了 ONNX / ONNX Runtime 最小部署闭环的初步搭建。主要学习并实践了 PyTorch 模型导出为 ONNX、ONNX 模型检查、模型输入输出接口查看、单张图片推理与分类结果解析等内容。已完成 export_onnx.py 和单图推理脚本的基础编写，能够实现模型加载、图像前处理、推理执行与结果保存。当前代码已具备第 5 周最小可运行框架，（路径最好变换成字符串，mkdir只生成目录不能生成文件）
