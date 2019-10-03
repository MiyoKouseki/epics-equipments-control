import os

import time

import ezca
ezca = ezca.Ezca()
while True:
    ezca['ALS-Y_BEAT_LO_STEP_FWD'] = 1 
    ezca['ALS-Y_BEAT_LO_STEP_REV'] = 1
    time.sleep(0.1)

