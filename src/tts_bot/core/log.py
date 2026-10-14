import logging
from src import settings 
from discord.utils import setup_logging

def setting_logs():
    log_level = settings.LOG_LEVEL
    # 디스코드 기본 로그 셋업
    setup_logging(level= logging.getLevelNamesMapping().get(log_level.upper(), logging.INFO))
    

    # 출력 형식
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
        )

    
    # 파일 출력 핸들러 : warning이상 로그는 파일에 기록
    file_handler = logging.FileHandler(settings.LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    
    # root 로거에 설정 등록
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
    
def get_logger(module_name: str) -> logging.Logger:
    return logging.getLogger(f"tts_bot.{module_name}")