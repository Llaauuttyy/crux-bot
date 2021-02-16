import logging
import os

# ------------------------------------------------- #
# ------------ DEBUG LOGGER IS CREATED ------------ #
# ------------------------------------------------- #


def debug_logger_creation():

    debug_logger = logging.getLogger("debug")
    debug_logger.setLevel(logging.DEBUG)

    debug_formatter = logging.Formatter(
        "| %(asctime)s | Line %(lineno)d | %(levelname)s | (Module: %(module)s): (Function: %(funcName)s): %(message)s",
        "%d/%m/%Y - %H:%M:%S"
    )

    debug_handler = logging.FileHandler("logs\\debug.log", "a")
    debug_handler.setFormatter(debug_formatter)

    debug_logger.addHandler(debug_handler)

    return debug_logger


# ------------------------------------------------ #
# ------------ CHAT LOGGER IS CREATED ------------ #
# ------------------------------------------------ #


def chat_logger_creation():

    chat_logger = logging.getLogger("chat")
    chat_logger.setLevel(logging.INFO)

    chat_formatter = logging.Formatter(
        '''%(asctime)s, %(message)s.''',
        "%d/%m/%Y, %H:%M:%S"
    )

    chat_handler = logging.FileHandler("logs\\chat.log", "a")
    chat_handler.setFormatter(chat_formatter)

    chat_logger.addHandler(chat_handler)

    return chat_logger


# ------------------------------------------------- #
# ------------ ERROR LOGGER IS CREATED ------------ #
# ------------------------------------------------- #


def error_logger_creation():

    error_logger = logging.getLogger("error")
    error_logger.setLevel(logging.ERROR)

    error_formatter = logging.Formatter(
        "| %(asctime)s | Line %(lineno)d | %(levelname)s | (Module: %(module)s): (Function: %(funcName)s): %(message)s",
        "%d/%m/%Y - %H:%M:%S"
    )

    error_handler = logging.FileHandler("logs\\error.log", "a")
    error_handler.setFormatter(error_formatter)

    error_logger.addHandler(error_handler)

    return error_logger


os.makedirs("logs", exist_ok=True)

# Logger
debug_logger = debug_logger_creation()
chat_logger = chat_logger_creation()
error_logger = error_logger_creation()
