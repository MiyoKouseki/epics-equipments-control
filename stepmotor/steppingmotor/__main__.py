import pcasstep
import pcasip
from Trinamic_control6110 import *
import sys

try :
    prefix = sys.argv[1]
    driverIP = sys.argv[2]
except IndexError:
    sys.exit("need argv like this; python -m K1:STEPPER-PR2_GAS_ 10.68.150.40")

reload(pcasstep)
reload(pcasip)
driver = Trinamic_control6110()
driver.connectTCP(driverIP, 4001)
driver.reconnect()

sus,part,a=prefix.split('_')
if part == 'GAS':
    stepserver = pcasstep.PcasServer(prefix,driver)
    print 'GAS server started'
elif part == 'IP':
    stepserver = pcasip.PcasServer(prefix,driver)
    print 'IP server started'

try:
    stepserver.run()

except KeyboardInterrupt:
    pass

