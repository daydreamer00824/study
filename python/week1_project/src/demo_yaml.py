import yaml
from pathlib import Path

yaml_path = Path("/home/daydreamer/Desktop/study/python/week1_project/configs/" \
"config_study1.yaml")
config = yaml.safe_load(yaml_path.read_text())

print(config["model"])
print(config["train"])