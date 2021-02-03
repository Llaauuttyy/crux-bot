import logging


# DEBUG logger is created

debug_logger = logging.getLogger("debug")
debug_logger.setLevel(logging.DEBUG)

debug_formatter = logging.Formatter(
    "| %(asctime)s | Line %(lineno)d | %(levelname)s | (Module: %(module)s): (Function: %(funcName)s): %(message)s.",
    "%d/%m/%Y - %H:%M:%S"
)

debug_handler = logging.FileHandler("logs\\debug.log", "a")
debug_handler.setFormatter(debug_formatter)

debug_logger.addHandler(debug_handler)

debug_logger.debug("Debug message")
debug_logger.debug("Debug message")
debug_logger.debug("Debug message")


# CHAT logger is created

chat_logger = logging.getLogger("chat")
chat_logger.setLevel(logging.INFO)

chat_formatter = logging.Formatter(
    '''%(asctime)s, %(message)s.''',
    "%d/%m/%Y, %H:%M:%S"
)

chat_handler = logging.FileHandler("logs\\chat.log", "a")
chat_handler.setFormatter(chat_formatter)

chat_logger.addHandler(chat_handler)

chat_logger.info("Crux, Hiiiiiiiiiii")
chat_logger.info("Crux, Hiiiiiiiiiii")
chat_logger.info("Crux, Hiiiiiiiiiii")


# ERROR logger is created

error_logger = logging.getLogger("error")
error_logger.setLevel(logging.ERROR)

error_formatter = logging.Formatter(
    "| %(asctime)s | Line %(lineno)d | %(levelname)s | (Module: %(module)s): (Function: %(funcName)s): %(message)s.",
    "%d/%m/%Y - %H:%M:%S"
)

error_handler = logging.FileHandler("logs\\error.log", "a")
error_handler.setFormatter(error_formatter)

error_logger.addHandler(error_handler)


error_logger.error("Error message")
error_logger.error("Error message")
error_logger.error("Error message")
