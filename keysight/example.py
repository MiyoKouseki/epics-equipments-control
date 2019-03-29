
from e8663d import VoltageControlledOscillator

with VoltageControlledOscillator('10.68.150.65',5025) as vco_x:
    # 0. check current status
    print('fixedfrequency is ',vco_x.fixedfrequency)
    
    # 1. run some 'static' commands
    vco_x.fix(40,unit='MHz')
    vco_x.step(10,unit='Hz')
    vco_x.step(-10,unit='Hz')
    
    # 2. run sweep, and check status continuously
    start = 40e6 - 50 
    stop =  40e6 + 50
    rate = 1
    vco_x.sweep(start,stop,rate)
