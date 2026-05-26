import logging
import logging.handlers
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=10_000_00, backupCount=3)
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setFormatter(formatter)

logger = logging.getLogger("llm_library")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)

def get_logger():
    return logger
