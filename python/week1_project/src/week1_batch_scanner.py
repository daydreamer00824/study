import argparse
from pathlib import Path
import yaml
import logging

base_path = Path("/home/daydreamer/Desktop/study/python/week1_project")

def useargparse():
    parse = argparse.ArgumentParser(description="第一周批量扫描脚本")
    parse.add_argument("--input", type=str, required=True, help="数据输入目录")
    parse.add_argument("--output", type=str, required=True, help="数据输出目录")
    parse.add_argument("--config", type=str, help="配置文件目录")
    parse.add_argument("--logs", type=str, help="log文件目录")
    return parse.parse_args()

def get_config(config_path : Path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件不存在:{config_path}")
    except yaml.YAMLError as e:
        logging.error("配置文件格式错了")
        raise ValueError(f"yaml格式错误:{e}")

def logsystem(log_path : Path):
    log_path.mkdir(parents=True, exist_ok=True)
    log_file = log_path / "run.log"

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        handlers=[logging.FileHandler(log_file, encoding="utf-8"),
                                  logging.StreamHandler()])
    
def collect_data(input_dir : Path, extensions):
    data_list = []
    if not input_dir.exists() or not input_dir.is_dir():
        logging.error("目录不存在")
        return []
    for file_name in input_dir.iterdir():
        if file_name.is_file() and file_name.suffix.lower() in extensions:
            data_list.append(file_name)
    return data_list

def create_report(output_dir : Path, file: list[Path]):
    output_dir.mkdir(parents=True, exist_ok=True)
    output_name = output_dir / "report.txt"
    # lines = [str(file_name) for file_name in file]
    # lines2 = [f"{file_name.name} | {file_name.suffix}" for file_name in file]
    # all_lines = lines + lines2
    lines = [f"路径:{file_name} | 文件名:{file_name.name} | 后缀: {file_name.suffix}" for file_name in file]
    output_name.write_text("\n".join(lines), encoding="utf-8")
    return output_name

def main():
    arg = useargparse()

    log_dir = base_path / Path(arg.logs)
    logsystem(log_dir)
    output_dir = base_path / Path(arg.output)
    logging.info("start")

    input_dir = base_path / Path(arg.input)
    config_dir = base_path / Path(arg.config) / Path("config.yaml")
    
    logging.info(f"输入目录: {input_dir}")
    logging.info(f"输出目录: {output_dir}")
    logging.info(f"配置文件: {config_dir}")

    
    try:
        config = get_config(config_dir)
        logging.info("配置文件加载成功")
    except Exception as e:
        logging.error(f"加载配置失败: {e}")
        return
    
    # extensions = config["extensions"]
    extensions = set(ext.lower() for ext in config.get("extensions", [])) 
    #从字典 config 里取出键 "extensions" 对应的值。如果有，就拿出来。如果没有，就返回默认值 []，也就是空列表。
    #1.从配置里拿 extensions
    #2.如果没有，就用空列表
    #3.把里面每个后缀转成小写
    #4.再放进集合里

    files = collect_data(input_dir, extensions)
    logging.info(f"共找到 {len(files)} 个符合条件的文件")

    report = create_report(output_dir, files)
    logging.info(f"报告已保存到: {report}")

    logging.info("over")

if __name__ == "__main__":
    main()