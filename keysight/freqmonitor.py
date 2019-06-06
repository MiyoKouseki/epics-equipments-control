import time
from e8663d import VoltageControlledOscillator
import ezca
ezca = ezca.Ezca()

i = 0 
with VoltageControlledOscillator('10.68.150.65',5025) as vco_x:
    while True:
        try:
            freq = vco_x.sweepfrequency
            ezca.write("ALS-X_BEAT_LO_FREQ",freq)
            i += 1
            time.sleep(0.1)
            if i==int(10*3600*24):
                exit()            
        except KeyboardInterrupt:
                exit()
