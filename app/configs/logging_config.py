"""Настройка цветного логирования"""

import logging
import logging.config

import colorlog
import yaml


def setup_logging():
    with open("app/configs/logging_config.yaml") as file:
        config = yaml.safe_load(file)
        logging.config.dictConfig(config)

        logger = logging.getLogger()
        console_handler = next(
            h for h in logger.handlers if isinstance(h, logging.StreamHandler)
        )

        # Создание цветного форматтера
        colored_formatter = colorlog.ColoredFormatter(
            "\x1b[34m%(asctime)s\x1b[0m [%(log_color)s%(levelname)s] %(name)s: %(message)s",
            reset=True,  # Сбрасывает цвет после каждого поля
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )

        # Замена старого форматтера на цветной
        console_handler.setFormatter(colored_formatter)
