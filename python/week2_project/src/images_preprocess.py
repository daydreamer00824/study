import argparse
from pathlib import Path
import logging
import yaml
import cv2
import numpy as np

base_dir = Path(__file__).resolve().parent.parent

def useargparse():
    parse = argparse.ArgumentParser(description="图像预处理")
    parse.add_argument("--input", type=str, default="input", help="输入目录")
    parse.add_argument("--output", type=str, default="output", help="输出目录")
    parse.add_argument("--config", type=str, default="configs", help="配置文件路径")
    parse.add_argument("--logs", type=str, default="logs", help="日志目录")

    return parse.parse_args()

def setlogs(logs_dir : Path):
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_name = Path("run.log")
    logsfile = logs_dir / log_name
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(logsfile, encoding="utf-8"), logging.StreamHandler()]
    )

def get_config(config_dir : Path):
    config_name = Path("config.yaml")
    configs_dir = config_dir / config_name
    try:
        with open(configs_dir, mode="r", encoding="utf-8") as c:
            config = yaml.safe_load(c)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件不存在:{config_dir}")
    except yaml.YAMLError as e:
        raise ValueError(f"YAML 格式错误:{e}")
    
def save_report(out_dir : Path, file : list[Path]):
    out_dir.mkdir(parents=True, exist_ok=True)
    report_name = Path("report.txt")
    report_txt = out_dir / report_name
    lines = [
        f"路径:{file_name} | 文件名:{file_name.name} | 后缀: {file_name.suffix}" 
        for file_name in file]
    report_txt.write_text("\n".join(lines), encoding="utf-8")
    logging.info(f"报告生成：{report_txt}")
    return report_txt
    

def collect_data_and_preprocess(input_dir : Path, output_dir : Path, extensions, sizes):
    datalist = []
    imglist = []

    if not input_dir.exists() or not input_dir.is_dir():
        logging.error(f"输入目录不存在或不是目录:{input_dir}")
        return [], [] #下面return是返回两个值,所以这里应该返回两个空列表
    
    for file_name in input_dir.iterdir():
        if file_name.is_file() and file_name.suffix.lower() in extensions:
            img = cv2.imread(str(file_name))
            if img is None:
                logging.warning(f"图片读取失败: {file_name}")
                continue
            logging.info(f"{file_name.name} | 原始 shape={img.shape} | dtype={img.dtype}")
            img_resize = cv2.resize(img, dsize=sizes)
            save_path = output_dir / file_name.name
            cv2.imwrite(str(save_path), img_resize)
            logging.info(f"预览图已保存: {save_path}")
            img_rgb = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)
            img_nor = img_rgb.astype(np.float32) / 255.0
            img_c = np.transpose(img_nor, (2, 0, 1))
            img_b = np.expand_dims(img_c, axis=0)
            datalist.append(file_name)
            imglist.append(img_b)
            logging.info(f"{file_name.name} | 处理后 shape={img_b.shape} | dtype={img_b.dtype}")
        else:
            logging.warning(f"不是图片:{file_name}")

    return datalist, imglist

def main():
    arg = useargparse()
    input_dir = base_dir / Path(arg.input)
    output_dir = base_dir / Path(arg.output)
    logs_dir = base_dir / Path(arg.logs)
    config_dir = base_dir / Path(arg.config)

    setlogs(logs_dir)
    logging.info("start")
    logging.info(f"根目录:{base_dir}")
    logging.info(f"输入目录: {input_dir}")
    logging.info(f"输出目录: {output_dir}")
    logging.info(f"配置文件目录: {config_dir}")
    logging.info(f"logs目录: {logs_dir}")

    try:
        config = get_config(config_dir)
        logging.info("配置文件加载成功")
    except Exception as e:
        logging.error(f"配置文件加载失败: {e}")
        return
    
    extensions = set(ext.lower() for ext in config.get("extensions", []))
    sizes = tuple(config.get("target_size", [224, 224]))

    file, img = collect_data_and_preprocess(input_dir, output_dir, extensions, sizes)
    logging.info(f"共找到 {len(file)} 个符合条件的文件")
    logging.info(f"共修改 {len(img)} 个符合条件的图片")

    save_name = Path("data.npy")
    save_path = output_dir / save_name
    # preprocessedata = np.stack(img, axis=0)
    preprocessedata = np.concatenate(img, axis=0) #!!!!
    np.save(save_path, preprocessedata)
    logging.info(f"保存处理后的图像数据：{output_dir / save_name}")
    logging.info(
        f"{save_path.name} | type={type(preprocessedata)} | shape={preprocessedata.shape} | dtype={preprocessedata.dtype}"
        )

    report = save_report(output_dir, file)

    logging.info("over")

if __name__ == "__main__":
    main()