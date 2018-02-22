import pcaspico
import newfocus8742
import sys
import time

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
    picoserver.run()
except KeyboardInterrupt:
    pass

