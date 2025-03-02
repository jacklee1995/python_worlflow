import os
import logging
import logging.config
from typing import Dict, Any

from workflow_engine.core.config import get_config
from workflow_engine.core.output import Output
from workflow_engine.core.output_strategies import (
    ConsoleOutputStrategy, 
    FileOutputStrategy,
    EmailOutputStrategy
)


def setup_logging(config: Dict[str, Any] = None) -> logging.Logger:
    """
    设置日志配置并返回全局logger实例。

    Args:
        config (Dict[str, Any], optional): 日志配置字典。默认为None,使用默认配置。

    Returns:
        logging.Logger: 全局logger实例。
    """
    if not config:
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard'
                },
                'file': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'workflow.log',
                    'maxBytes': 1024 * 1024 * 10,  # 10MB
                    'backupCount': 10,
                    'formatter': 'standard',
                    'encoding': 'utf-8'
                }
            },
            'loggers': {
                '': {
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG',
                    'propagate': True
                }
            }
        }

    logging.config.dictConfig(config)
    return logging.getLogger()


def get_logger(name: str = None) -> logging.Logger:
    """
    获取logger实例。如果未指定name,则返回root logger。

    Args:
        name (str, optional): logger名称。默认为None,表示root logger。

    Returns:
        logging.Logger: logger实例。
    """
    return logging.getLogger(name)


def init_logger():
    """
    初始化全局logger。

    从配置文件读取日志配置,如果配置文件中未指定,则使用默认配置。
    根据配置创建logger实例和输出策略,并将它们关联起来。
    """
    config = get_config()
    log_config = config.get('logging', {})
    logger = setup_logging(log_config)

    output_config = log_config.get('output', {})
    output_strategies = []

    if output_config.get('console'):
        output_strategies.append(ConsoleOutputStrategy())

    if 'file' in output_config:
        file_config = output_config['file']
        output_strategies.append(FileOutputStrategy(**file_config))

    if 'email' in output_config:  
        email_config = output_config['email']
        output_strategies.append(EmailOutputStrategy(**email_config))

    log_output = Output(output_strategies)
    logger.addHandler(log_output)


# 在模块加载时初始化全局logger
init_logger() 