from pathlib import Path

from loguru import logger

log_file_path = Path(__file__).absolute().parent.parent.parent / 'data/logs/log.out'

logger.add(log_file_path, format='[{time}] [{level}] [{file.name}:{line}]  {message}', level='DEBUG')
