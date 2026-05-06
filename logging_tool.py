"""
@Date    : 2026/5/6 17:19
@Author  : Chiang
@Desc    : None
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

import colorlog

LOG_FMT = "%(asctime)s %(levelname)-7s [%(name)s] %(message)s"
FILE_LOG_PATH = 'logs/log'


def _console(level: int) -> None:
    """日志控制台"""
    root_logger = logging.getLogger()

    stream_handler = colorlog.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    formatter = colorlog.ColoredFormatter(
        fmt=f"%(log_color)s{LOG_FMT}%(reset)s",
        log_colors={
            "DEBUG": "thin,cyan",
            "INFO": "bold,blue",
            "WARNING": "bold,yellow",
            "ERROR": "bold,red",
            "CRITICAL": "bold,red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    stream_handler.setFormatter(formatter)

    root_logger.addHandler(stream_handler)


def _file(level: int, max_bytes: int = 10 * 1024 * 1024, backup_count: int = 5) -> None:
    """日志文件，按文件大小滚动切割"""
    root_logger = logging.getLogger()

    log_path = Path(FILE_LOG_PATH)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    formatter = logging.Formatter(
        fmt=LOG_FMT,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)


def init_log(level: int = logging.INFO) -> None:
    # 设置根日志等级
    logging.getLogger().setLevel(level)
    # 控制台多彩
    _console(level)
    # 日志文件
    _file(level)


init_log()
logger = logging.getLogger()
