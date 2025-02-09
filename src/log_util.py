# -*- coding: utf-8 -*-

import logging


def _get_escape_codes():
    """Generates following dictionary of ANSI escape codes."""

    colors = [
        'black',
        'red',
        'green',
        'yellow',
        'blue',
        'purple',
        'cyan',
        'white']

    prefixes = [
        ('3', ''),
        ('01;3', 'bold_'),
        ('04;3', 'underscore_')]

    def f(*x):
        return '\033[' + ';'.join(x) + 'm'

    escape_codes = {
        'normal': f('00'),
        'bold': f('01'),
        'underscore': f('04')}

    for pf_code, pf_name in prefixes:
        for clr_code, clr_name in enumerate(colors):
            k = pf_name + clr_name
            v = f(pf_code + str(clr_code))
            escape_codes[k] = v

    return escape_codes


DEFAULT_LOG_COLORS = {
    'DEBUG': 'green',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red'}

ESCAPE_CODES = {
    'black': '\x1b[30m',
    'blue': '\x1b[34m',
    'bold': '\x1b[01m',
    'bold_black': '\x1b[01;30m',
    'bold_blue': '\x1b[01;34m',
    'bold_cyan': '\x1b[01;36m',
    'bold_green': '\x1b[01;32m',
    'bold_purple': '\x1b[01;35m',
    'bold_red': '\x1b[01;31m',
    'bold_white': '\x1b[01;37m',
    'bold_yellow': '\x1b[01;33m',
    'cyan': '\x1b[36m',
    'green': '\x1b[32m',
    'normal': '\x1b[00m',
    'purple': '\x1b[35m',
    'red': '\x1b[31m',
    'underscore': '\x1b[04m',
    'underscore_black': '\x1b[04;30m',
    'underscore_blue': '\x1b[04;34m',
    'underscore_cyan': '\x1b[04;36m',
    'underscore_green': '\x1b[04;32m',
    'underscore_purple': '\x1b[04;35m',
    'underscore_red': '\x1b[04;31m',
    'underscore_white': '\x1b[04;37m',
    'underscore_yellow': '\x1b[04;33m',
    'white': '\x1b[37m',
    'yellow': '\x1b[33m'}


class ColoredRecord(object):
    """
    Wraps a LogRecord, adding named escape codes to the internal dict.
    The internal dict is used when formatting the message.

    It keeps a reference to the original record so ``__getattr__`` can
    access functions that are not in ``__dict__``.
    """

    def __init__(self, record):
        self.__dict__.update(ESCAPE_CODES)
        self.__dict__.update(record.__dict__)
        self.__record = record

    def __getattr__(self, name):
        return getattr(self.__record, name)


class ColoredFormatter(logging.Formatter):

    def __init__(
            self, fmt=None, datefmt=None, log_colors=None, time_color=None):
        logging.Formatter.__init__(self, fmt, datefmt)

        self.log_colors = log_colors or DEFAULT_LOG_COLORS
        self.time_color = time_color or 'normal'
        self.normal = True

    def format(self, record):
        record = ColoredRecord(record)
        clr = self.log_colors.get(record.levelname, 'normal')
        record.log_color = ESCAPE_CODES[clr]
        record.time_color = ESCAPE_CODES[self.time_color]

        message = logging.Formatter.format(self, record)

        if not message.endswith(ESCAPE_CODES['normal']):
            message += ESCAPE_CODES['normal']

        return message


def custom_logger(name=None):
    """Customised logger used by SCOTER."""

    formatter = ColoredFormatter(
        fmt='%(time_color)s%(asctime)s%(normal)s '
            '[%(log_color)s%(levelname)s%(normal)s] %(name)s: %(message)s',
        datefmt='%H:%M:%S')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    if not logger.handlers:
        # Prevent logging from propagating to the root logger.
        logger.propagate = False
        logger.addHandler(stream_handler)

    return logger


__all__ = """
    ColoredFormatter
    DEFAULT_LOG_COLORS
    ESCAPE_CODES
    custom_logger
""".split()
