import time
from e8663d import VoltageControlledOscillator
import ezca
ezca = ezca.Ezca()

i = 0
freq_default = 40.e6

with VoltageControlledOscillator('10.68.150.65',5025) as vco_x:
    while True:
        try:
            freq = float(vco_x.sweepfrequency) - freq_default + i
            #freq = vco_x.sweepfrequency
            #ezca.write("ALS-X_BEAT_LO_FREQ",str(freq))
            ezca.write("ALS-X_BEAT_LO_FREQ",freq)
            i += 1
            time.sleep(0.01)
            print i,freq,type(freq)
        except KeyboardInterrupt:            
            exit()
