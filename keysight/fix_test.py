#! /usr/bin/env python

## By K. Miyo and Y. Enomoto, 2019/3/20

import ezca
import sys

from e8663d import VoltageControlledOscillator

ezca = ezca.Ezca()

### argument check ###
if len(sys.argv) != 4:
    print 'Wrong arguments. Usage: ARM freq unit'
    sys.exit()
arm = str(sys.argv[1]).upper()

## IP address and etc
if arm == 'X':
    IP = '10.68.150.65'
    freq_default = 40e6
elif arm == 'Y':
    IP = '10.68.150.66'
    freq_default = 45e6
else:
    print 'ARM is X or Y'
    sys.exit()

freq = float(sys.argv[2])
unit = str(sys.argv[3])
    
with VoltageControlledOscillator(IP,5025) as vco:
    vco.fix(freq,unit=unit)
    ezca['ALS-'+arm+'_BEAT_LO_FREQ'] = float(vco.sweepfrequency) - freq_default
