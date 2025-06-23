import enum
from collections.abc import Mapping

from .trait import LogLevel


class BColors(enum.StrEnum):
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARN = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


LB: Mapping[LogLevel, str] = {
    LogLevel.NULL: "",
    LogLevel.FATAL: BColors.FAIL,
    LogLevel.ERROR: BColors.FAIL,
    LogLevel.WARN: BColors.WARN,
    LogLevel.BRIEF: BColors.OKCYAN,
    LogLevel.INFO: BColors.OKGREEN,
    LogLevel.DEBUG: BColors.OKBLUE,
}

RB: Mapping[LogLevel, str] = {
    LogLevel.NULL: "",
    LogLevel.FATAL: BColors.ENDC,
    LogLevel.ERROR: BColors.ENDC,
    LogLevel.WARN: BColors.ENDC,
    LogLevel.BRIEF: BColors.ENDC,
    LogLevel.INFO: BColors.ENDC,
    LogLevel.DEBUG: BColors.ENDC,
}
