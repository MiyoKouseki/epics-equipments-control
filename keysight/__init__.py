"""
this is for adl MIYOPICO_ver1.adl.
"""
import logging

def get_module_logger(modname):
    #logging.config.fileConfig('logging.conf')
    conf = '/opt/rtcds/userapps/release/cds/common/scripts/epics-motor-control/keysight/logging.conf'
    logging.config.fileConfig(conf)
    
    
    logger = logging.getLogger('logExample')
    return logger

