import sys
sys.path.append("path-project")

import cruxbot.loggers as log


def call_logger():
    log.debug_logger.debug("TEST")
    log.debug_logger.debug("TEST")

    log.chat_logger.info("TEST")
    log.chat_logger.info("TEST")

    log.error_logger.error("TEST")
    log.error_logger.error("TEST")

    input("Pause to check time passing by")

    return call_logger()


def main():
    call_logger()


main()
