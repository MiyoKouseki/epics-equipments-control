#! /usr/bin/env python

## By K. Miyo and Y. Enomoto, 2019/3/20

import ezca
import sys
import time

from e8663d import VoltageControlledOscillator

ezca = ezca.Ezca()

### argument check ###
if len(sys.argv) != 5:
    print 'Wrong arguments. Usage: ARM start stop rate'
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

with VoltageControlledOscillator(IP,5025) as vco:
    if sys.argv[2] == 'current':
        start = float(vco.sweepfrequency)
    else:
        start = float(sys.argv[2])
    if sys.argv[3][0] == '+':
        relative = float(sys.argv[3][1:])
        stop = start + relative
    else:
        stop = float(sys.argv[3])
    rate = float(sys.argv[4])
    vco.sweep(start,stop,rate)
    timeout = time.time() + (stop-start)/rate *1.1
    while (float(vco.sweepfrequency)<stop) and (time.time()< timeout):
        ezca['ALS-'+arm+'_BEAT_LO_FREQ'] = float(vco.sweepfrequency) - freq_default
        if time.time() >= timeout:
            print 'sweep timeout'
    ezca['ALS-'+arm+'_BEAT_LO_FREQ'] = float(vco.sweepfrequency) - freq_default
