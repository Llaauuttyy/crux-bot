import sys
sys.path.append("ALTERNATIVE PATH")
import cruxbot.loggers


def call_logger():
    cruxbot.loggers.debug_logger.debug("Has been executed")
    cruxbot.loggers.debug_logger.debug("Has been executed")
    input("Pause")

    return call_logger()


def main():
    call_logger()


main()
