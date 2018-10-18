import pcaspico
import newfocus8742
import sys

try :
    prefix = sys.argv[1]
    driverIP = sys.argv[2]
except IndexError:
    sys.exit("need argv like this; python -m K1:PICO-MCI_IM_ 10.68.10.230")

picoserver = pcaspico.PcasServer(prefix,newfocus8742.driver(driverIP))

try:
    picoserver.run()

except KeyboardInterrupt:
    pass

