"""
this is for adl MIYOPICO_ver1.adl.
"""
import logging
def get_module_logger(modname):
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('logExample')
    return logger

