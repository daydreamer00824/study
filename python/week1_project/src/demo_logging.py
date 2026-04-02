import logging
from pathlib import Path

log_dir = Path("/home/daydreamer/Desktop/study/python/week1_project/logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "run.log"

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler(log_file, encoding='utf-8'), logging.StreamHandler()])

logging.info("initial success")

