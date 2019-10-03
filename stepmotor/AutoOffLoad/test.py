
import sys
import time
from ezca import Ezca
Ezca().export()

DAMPflt = 'VIS-PR2_BF_DAMP_GAS'
STEPPER = 'STEPPER-PR2_GAS_0'

ii = 0
out = 0.0
s_time = time.time()
while time.time() - s_time <= 3.0:
    out += ezca[DAMPflt+'_OUTPUT']
    ii += 1
out = out/float(ii)

print out
