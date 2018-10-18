#!/usr/bin/env python

import os
import pcaspy
import conf
import logging
import funcIP
from datetime import datetime

##################################################
pvdb ={
    'L_STEP': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'T_STEP': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'Y_STEP': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'F0Y_STEP': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'ACC': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 500,
    },
    'VEL': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 500,
    },
    'STOP': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'A_POSITION': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'B_POSITION': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'C_POSITION': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'F0Y_POSITION': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'UPDATE': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    }
}
    
        


##################################################

#os.environ['EPICS_CAS_INTF_ADDR_LIST'] = 'localhost'
#os.environ['EPICS_CAS_SERVER_PORT'] = '58901'

# https://pcaspy.readthedocs.org/en/latest/tutorial.html

class PcasDriver(pcaspy.Driver):
    def __init__(self, driver, prefix):
        super(PcasDriver, self).__init__()
        self.driver = driver
        self.conf = conf
        self.prefix = prefix
	a, sus = prefix.split("-")
	self.part = sus[:-1]
        
        self.driver.setTargetSpeed(500, 0)
        self.driver.setAcceleration(500,0)
        self.driver.setTargetSpeed(500, 1)
        self.driver.setAcceleration(500,1)
        self.driver.setTargetSpeed(500, 2)
        self.driver.setAcceleration(500,2)
        self.driver.setTargetSpeed(500, 3)
        self.driver.setAcceleration(500,3)
        self.driver.setTargetSpeed(500, 4)
        self.driver.setAcceleration(500,4)
        self.driver.setTargetSpeed(500, 5)
        self.driver.setAcceleration(500,5)
        
	self.logfile = '/kagra/Dropbox/Subsystems/VIS/Scripts/StepMotor/LogFiles/'+self.prefix+'.log'

        self.updatePVs()

        
    def read(self, channel):
        value = self.getParam(channel)
        logging.info('%s == %s' % (channel, value))
        return value

    def write(self, channel, value):
        print('%s => %s' % (channel, value))
        self.setParam(channel, value)
        #driverAddr = self.conf.channel[self.prefix+channel[:3]]["driver"]
        motorAddrA  = self.conf.channel[self.part]["motorA"]
        motorAddrB  = self.conf.channel[self.part]["motorB"]
        motorAddrC  = self.conf.channel[self.part]["motorC"]
        motorAddrY  = self.conf.channel[self.part]["motorY"]
        
        #        with self.driver:
        if (channel == "UPDATE") and (value == 1.0):
            self.driver.reconnect()
            
            posA = self.driver.getActualPosition(motorAddrA)
            self.setParam("A_POSITION",posA)
            posB = self.driver.getActualPosition(motorAddrB)
            self.setParam("B_POSITION",posB)
            posC = self.driver.getActualPosition(motorAddrC)
            self.setParam("C_POSITION",posC)
            posY = self.driver.getActualPosition(motorAddrY)
            self.setParam("F0Y_POSITION",posY)
        
	    d = datetime.now()
	    with open(self.logfile,'a') as f:
	        f.write(d.strftime('%Y-%m-%d %H:%M:%S')+' position updated as motorA:'+str(posA)+' motorB:'+str(posB)+' motorC:'+str(posC)+' F0Y:'+str(posY)+'\n')

        if channel == "ACC":
            acc = self.getParam("ACC")
            self.driver.setAcceleration(acc, motorAddrA)
            self.driver.setAcceleration(acc, motorAddrB)
            self.driver.setAcceleration(acc, motorAddrC)
            self.driver.setAcceleration(acc, motorAddrY)
            
        if channel == "VEL":
            vel = self.getParam("VEL")
            self.driver.setTargetSpeed(vel, motorAddrA)
            self.driver.setTargetSpeed(vel, motorAddrB)
            self.driver.setTargetSpeed(vel, motorAddrC)
            self.driver.setTargetSpeed(vel, motorAddrY)
            
        if channel == "STOP":
            self.driver.stop(motorAddrA)
            self.driver.stop(motorAddrB)
            self.driver.stop(motorAddrC)
            self.driver.stop(motorAddrY)
        
        if channel == "L_STEP":
            funcIP.Move_L(self.part,self.driver,value)
            d = datetime.now()
	    with open(self.logfile,'a') as f:
		f.write(d.strftime('%Y-%m-%d %H:%M:%S')+' IP moved in L by '+str(value)+'\n')

        if channel == "T_STEP":
            funcIP.Move_T(self.part,self.driver,value)
            
            d = datetime.now()
	    with open(self.logfile,'a') as f:
		f.write(d.strftime('%Y-%m-%d %H:%M:%S')+' IP moved in T by '+str(value)+'\n')

        if channel == "Y_STEP":
            funcIP.Move_Y(self.part,self.driver,value)
            
            d = datetime.now()
	    with open(self.logfile,'a') as f:
		f.write(d.strftime('%Y-%m-%d %H:%M:%S')+' IP moved in Y by '+str(value)+'\n')

        if channel == "F0Y_STEP":
            signY = self.conf.channel[self.part]["signY"]
            pos = self.driver.getActualPosition(motorAddrY)
            self.driver.setTargetPosition(pos+signY*value, motorAddrY)
            
            d = datetime.now()
	    with open(self.logfile,'a') as f:
		f.write(d.strftime('%Y-%m-%d %H:%M:%S')+' F0Y moved by '+str(value)+'\n')

        self.updatePVs()
        
        return True

class PcasServer(pcaspy.SimpleServer):
    def __init__(self, prefix, driver):
        super(PcasServer, self).__init__()
        logging.info("initializing server...")
        self.server = pcaspy.SimpleServer()
        self.server.createPV(prefix, pvdb)
        driver = PcasDriver(driver,prefix)
        
    def run(self):
        logging.info("Starting server...")
        while True:
            self.server.process(0.1)
