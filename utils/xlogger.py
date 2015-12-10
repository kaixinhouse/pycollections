# -*- coding: utf-8 -*-

import sys
import os
import os.path
import logging
import logging.handlers


fmt_standard = logging.Formatter('%(asctime)s %(message)s')
fmt_compact = logging.Formatter("%(asctime)s [%(process)d][%(threadName)s] %(message)s")
fmt_full = logging.Formatter("%(asctime)s %(levelname)s [%(process)d][%(thread)d][%(threadName)s] %(message)s")


def setup_logger(log_file_path, error_log_file_path, debug_mode=False, debug_mode_level=0):
    logging.raiseExceptions = True

    logger = logging.getLogger()

    setup_standard_logger(logger)
    setup_info_logger(log_file_path, logger)
    setup_error_logger(error_log_file_path, logger)

    if debug_mode:
        setup_debug_logger(debug_mode_level, logger)


def setup_standard_logger(logger=None):
    """ standard output to the console """
    if logger is None:
        logger = logging.getLogger()

    if not logger.handlers:
        logger.setLevel(logging.NOTSET)

    standard = logging.StreamHandler(sys.stderr)
    standard.setLevel(logging.DEBUG)
    standard.setFormatter(fmt_standard)
    logger.addHandler(standard)

def setup_info_logger(log_file_path, logger=None, auto_stop_time=100, remove_old_handler=False):
    """ detail information output a file """
    if logger is None:
        logger = logging.getLogger()

    log_file_handler = logging.handlers.RotatingFileHandler(log_file_path, 'a', 1024*1024*20, 10)
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(fmt_full)
    logger.addHandler(log_file_handler)

def setup_info_logger_new(log_file_path, logger=None, auto_stop_time=100, remove_old_handler=False):
    """ detail information output a file """

    if auto_stop_time is None:
        auto_stop_time = int(os.environ['auto_stop_time'], 0)

    # auto_stop_time is 0 equals not set info logger
    if not auto_stop_time:
        return

    if logger is None:
        logger = logging.getLogger()

    if getattr(logger, '_old_handler', None) is not None:
        if remove_old_handler:
            old_handler = logger._old_handler
            logger._old_handler = None
            logger.removeHandler(old_handler)
        else:
            return auto_stop_time

    log_file_handler = logging.handlers.RotatingFileHandler(log_file_path, 'a', 1024*1024*20, 10)
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(fmt_full)
    logger.addHandler(log_file_handler)

    logger._old_handler = log_file_handler
    return start_logger_auto_stop_time(auto_stop_time, logger)


def start_logger_auto_stop_time(auto_stop_time, logger):
    """ delete one logger after auto_stop_time  """

    if auto_stop_time is None:
        auto_stop_time = int(os.environ['auto_stop_time'], 0)
    if not auto_stop_time:
        return auto_stop_time

    if logger is None:
        logger = logging.getLogger()

    handler = getattr(logger, '_old_handler', None)
    if handler is not None:
        def _remove_handler():
            log_file_handler = logger._old_handler
            logger._old_handler = None
            logger.removeHandler(log_file_handler)

        if auto_stop_time > 0:
            import threading
            t = threading.Timer(auto_stop_time, _remove_handler)
            t.setDaemon(True)
            t.start()

    return auto_stop_time


def setup_error_logger(error_log_file_path, logger=None):
    if logger is None:
        logger = logging.getLogger()
    error_handler = logging.handlers.RotatingFileHandler(error_log_file_path, 'a', 1024*1024*1, 3)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(fmt_full)
    logger.addHandler(error_handler)


def setup_debug_logger(debug_mode_level=0, logger=None):
    """ monitor the output information according to the debug_mode_level """

    if logger is None:
        logger = logging.getLogger()

    monitor = logging.StreamHandler(sys.stderr)
    monitor.setLevel(debug_mode_level)
    monitor.setFormatter(fmt_compact)
    logger.addHandler(monitor)


def main():

    setup_logger('./log_file.log', './error_log_file.log', False)
    logging.info('info')
    logging.debug('debug')
    logging.warn('warn')
    logging.error('error')
    logging.critical('critical')

if __name__ == '__main__':
    main()