import pcaspico
import newfocus8742
import sys
import time
import logging
import logging.config
import os
#BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print BASE_DIR
#logging.config.fileConfig(os.path.join(BASE_DIR, 'utils', 'logger.conf')) 

from __init__ import get_module_logger
logger = get_module_logger(__name__)

try :
    prefix = sys.argv[1]
    driverIP = sys.argv[2]
    #import subprocess
    #pl = subprocess.Popen('ps alx | grep {0}'.format(prefix,driverIP),shell=True,stdout=subprocess.PIPE).communicate()[0]
    #print pl
    #exit()
except IndexError:
    sys.exit("python -m K1:PICO-MCI_IM_ 10.68.10.230.")
        
print prefix,driverIP
picoserver = pcaspico.PcasServer(prefix,newfocus8742.driver(driverIP))

try:
    logger.info("Start server!")
    picoserver.run()
except KeyboardInterrupt:
    mydriver.close()
    print e
    print 'Detect keyboard interrupt. Bye!'
    #logger.info("KeyboardInterrupt")
    #logger.info("Bye")
    exit()
    pass

'''
try:
    picoserver.run()
except KeyboardInterrupt as e:
    mydriver.close()
    print e
    print 'Detect keyboard interrupt. Bye!'
    exit()
'''
