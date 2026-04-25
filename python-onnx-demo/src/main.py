import argparse
from pathlib import Path
import yaml
from export_model import export_model
import logging
from set_log import set_logging
from inspect_onnx import inspect_onnx
from image_process import collect_image
import onnxruntime as ort
import numpy as np
from check_onnx import check_onnx
from save_result_csv import save_result
from postprocess import get_topk
from label_map import load_labels, index_to_label, indices_to_labels

def useparse():
    parse = argparse.ArgumentParser(description="Python ONNX Runtime 完整仓库")
    parse.add_argument("--input", type=str, required=True, help="图片输入目录")
    parse.add_argument("--output", type=str, required=True, help="输出目录")
    parse.add_argument("--models", type=str, required=True, help="模型导出目录")
    parse.add_argument("--config", type=str, default="/home/daydreamer/Desktop/study/python-onnx-demo/config", help="config目录")
    parse.add_argument("--log", type=str, default="/home/daydreamer/Desktop/study/python-onnx-demo/logs", help="日志目录")
    return parse.parse_args()

def load_conig(config_dir : Path):
    if not config_dir.exists():
        raise FileNotFoundError(f"配置目录不存在: {config_dir}")   #!
    try:
        config_name = Path("config.yaml")
        config_path = config_dir / config_name
        with open(config_path, "r", encoding="utf-8") as c:
            cfg = yaml.safe_load(c)
            if cfg is None:
                raise ValueError(f"配置文件为空: {config_path}")
            else:
                return cfg
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件不存在{config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"配置文件错误{e}")
        #!


def main():
    arg = useparse()
    set_logging(Path(arg.log))#!

    try:
        cfg = load_conig(Path(arg.config))#!
        logging.info(f"配置文件加载成功:{cfg}")
    except Exception as e:
        logging.error(f"配置文件加载失败:{e}")
        return
    
    try:
        label_path = Path(cfg["base_path"]) / Path("labels/imagenet_classes.txt")
        labels = load_labels(label_path)
    except Exception as e:
        logging.error(f"类别文件加载失败: {e}")
        return
    
    model_dir = Path(cfg["base_path"]) / Path(arg.models)
    model_path = model_dir / "model.onnx"
    try:
        if not model_path.exists():                                ####!!!!
            logging.info("未检测到 ONNX 模型，开始导出")
            model_path = export_model(model_dir)
            logging.info("模型导出成功")
        else:
            logging.info(f"检测到已有模型，直接使用: {model_path}")    ####!!!!
    except Exception as e:
        logging.error(f"模型导出失败: {e}")
        return

    try:
        check_onnx(model_path)
    except Exception as e:
        logging.error(f"onnx文件出错:{e}")
        return

    try:    
        inspect_onnx(model_path)
    except Exception as e:
        logging.error(f"ONNX 检查失败: {e}")
        return

    extensions = set(ext.lower() for ext in cfg.get("extensions", []))
    size = tuple(cfg.get("size", [224, 224]))

    input_path = Path(cfg["base_path"]) / Path(arg.input)
    output_path = Path(cfg["base_path"]) / Path(arg.output)
    try:
        image, image_path = collect_image(input_path, output_path, extensions, size)#!
        if not image:
            logging.error("没有收集到可用于推理的图片")
            return#!
    except Exception as e:
        logging.error(f"图片处理失败: {e}")
        return#!
    
    # img_batch = np.stack(image, axis=0).astype(np.float32)

    #infer
    try:
        batch_size = int(cfg.get("batch_size", 12))
        session = ort.InferenceSession(str(model_path))
        output_name = session.get_outputs()[0].name
        input_name = session.get_inputs()[0].name

        all_result = []

        for start in range(0, len(image), batch_size):
            end = start + batch_size
            image_batch = image[start : end]
            image_path_batch = image_path[start : end]
            input_batch = np.stack(image_batch, axis=0).astype(np.float32)
            result = session.run([output_name], {input_name : input_batch})[0]
            topk_indices, topk_scores = get_topk(result, k=5)
            # print("topk_indices shape:", topk_indices.shape)
            # print("topk_scores shape:", topk_scores.shape)
            pred = topk_indices[:, 0]
            autual_end = min(end, len(image))
            logging.info(f"当前批次: {start + 1} 到 {autual_end}")
            logging.info(f"推理成功, output shape: {result.shape}")
            for p, i, s in zip(image_path_batch, topk_indices, topk_scores):
                top1_index = int(i[0])
                top1_label = index_to_label(top1_index, labels)
                top1_score = float(s[0])
                top5_labels = indices_to_labels(i, labels)
                # print("top_indices shape:", i.shape)
                # print("top_scores shape:", s.shape)
                logging.info(f"{p.name} -> top1 index:{top1_index}, label:{top1_label}, score:{top1_score:.4f}")
                all_result.append({
                    "image_name" : p.name,
                    "image_path" : str(p),
                    "top1_index" : top1_index,
                    "top1_label" : top1_label,
                    "top1_score" : round(top1_score, 6),
                    "top5_indices" : ",".join(str(int(x)) for x in i),
                    "top5_labels" : ",".join(top5_labels),
                    "top5_scores" : ",".join(f"{float(y):.6f}" for y in s)
                })
        try:
            result_path = save_result(all_result, output_path)
            logging.info(f"结果文件路径: {result_path}")
        except Exception as e:
            logging.warning(f"result save fail:{e}")
        logging.info("*" * 50)
        # session = ort.InferenceSession(str(model_path))

        # result = session.run([session.get_outputs()[0].name], {session.get_inputs()[0].name : img_batch})
        # logging.info(f"推理成功, output shape: {result[0].shape}")
    except Exception as e:
        logging.error(f"推理失败: {e}")
        return
    
if __name__ == "__main__":
    main()



