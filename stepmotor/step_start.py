#!/usr/bin/env python
#! coding:utf-8
"""
 modified in Feb 3 2018.
 A. Shoda
"""

import sys,commands,os

driverDict = {
    "PR2_GAS"   :"10.68.150.40",
    "PR0_GAS"   :"10.68.150.41",
    "ITMX_GAS"  :"10.68.150.43",
    "ITMX_IP"   :"10.68.150.44",
    "ETMX_GAS"  :"10.68.150.45",
    "ETMX_IP"   :"10.68.150.46",
    "ITMY_GAS"  :"10.68.150.47",
    "ITMY_IP"   :"10.68.150.48",
    "ETMY_GAS"  :"10.68.150.49",
    "ETMY_IP"   :"10.68.150.50",
    "BS_GAS"    :"10.68.150.51",
    "BS_IP"     :"10.68.150.52",
    "SR2_GAS"   :"10.68.150.53",
    "SR2_IP"    :"10.68.150.54",
    "SR3_GAS"   :"10.68.150.55",
    "SR3_IP"    :"10.68.150.56",
    "SRM_GAS"   :"10.68.150.57",
    "SRM_IP"    :"10.68.150.58"
}

def print_driverList():
    print "| --- Driver List ---"
    for item in driverDict.items():
        print "| {0:10s} : {1:14s} |".format(item[0],item[1])
        
def main():
    agvs = sys.argv
    argc = len(agvs)
    if (argc != 2):
        print '! step_start (DRIVER_NAME)'
        print_driverList()        
        quit()
    if agvs[1] not in driverDict:
        print '! please check DRIVER_NAME %s' % agvs[1]
        print_driverList()
        quit()

    #print "Exterminate !!!!!"
    #exit()
    os.chdir('/opt/rtcds/userapps/release/cds/common/scripts/epics-motor-control/stepmotor')
    print 'python -m steppingmotor K1:STEPPER-%s_ %s &' % (agvs[1],driverDict[agvs[1]])
    os.system('python -m steppingmotor K1:STEPPER-%s_ %s &' % (agvs[1],driverDict[agvs[1]]) )

if __name__ == "__main__":
    main()    
