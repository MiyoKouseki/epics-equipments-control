#!/usr/bin/env python
#! coding:utf-8
"""
 modified in Oct 3 2017.
 K. miyo
"""

import sys,commands,os

driverDict = {
    "MCE"      :"10.68.150.2",
    "MCI"      :"10.68.150.3",
    "MCO"      :"10.68.150.4",
    "STM1"     :"10.68.150.5",
    "STM2"     :"10.68.150.6",
    "POM1"     :"10.68.150.7",
    "IMMT1"    :"10.68.150.14",
    "IMMT2"    :"10.68.150.13",
    "PR2_BF"   :"10.68.150.12",
    "PR2_IM"   :"10.68.150.15",
    "PR3_BF"   :"10.68.150.10",
    "PR3_IM"   :"10.68.150.11",
    "PRM_BF"   :"10.68.150.8",
    "PRM_IM"   :"10.68.150.9",
    "BS_IM"    :"10.68.150.16",
    "BS_BF"    :"10.68.150.17",
    "ETMX"      :"10.68.150.20",
    "ETMY"      :"10.68.150.21",
    "ITMX"      :"10.68.150.18",
    "ITMY"      :"10.68.150.19",
    "SR2_IM"   :"10.68.150.24",
    "SR2_BF"   :"10.68.150.25",
    "SR3_IM"   :"10.68.150.26",
    "SR3_BF"   :"10.68.150.27",
    "TEST"   :"10.68.150.22",    
    "POP_POM"   :"10.68.150.31",
    "PCAL_EX1"   :"10.68.150.35",
    "PCAL_EX2"   :"10.68.150.36",
    "PCAL_EY1"   :"10.68.150.37",
    "PCAL_EY2"   :"10.68.150.38",    
}

def print_driverList():
    print "| --- Driver List ---"
    for item in driverDict.items():
        print "| {0:10s} : {1:14s} |".format(item[0],item[1])
        
def main():
    agvs = sys.argv
    argc = len(agvs)
    if (argc != 2):
        print '! pico_start (DRIVER_NAME)'
        print_driverList()        
        quit()
    if agvs[1] not in driverDict:
        print '! please check DRIVER_NAME %s' % agvs[1]
        print_driverList()
        quit()

    #print "Exterminate !!!!!"
    #exit()
    #os.chdir('/opt/rtcds/userapps/release/cds/common/scripts/picomotor')
    os.chdir('/opt/rtcds/userapps/release/cds/common/scripts/picomotor_ver2')
    print 'python -m picomotor_ver2 K1:PICO-%s_ %s &' % (agvs[1],driverDict[agvs[1]])
    os.system('python -m picomotor_ver2 K1:PICO-%s_ %s &' % (agvs[1],driverDict[agvs[1]]) )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print e
        print 'Detect keyboard interrupt. Bye!'
        exit()    
