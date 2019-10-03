import os

import time

import ezca
ezca = ezca.Ezca()
while True:
    ezca['ALS-X_BEAT_LO_STEP_FWD'] = 1 
    ezca['ALS-X_BEAT_LO_STEP_REV'] = 1
    time.sleep(0.1)

