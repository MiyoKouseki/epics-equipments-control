#!/usr/bin/env python

import os
import pcaspy
import conf
import logging

##################################################
pvdb ={
    'PIT_STEP': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'PIT_SLOW': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'PIT_MIDDLE': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'PIT_QUICK': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'PIT_MOVE': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'PIT_REV': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'PIT_FWD': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'PIT_STOP': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'PIT_POSITION': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'YAW_STEP': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'YAW_SLOW': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'YAW_MIDDLE': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'YAW_QUICK': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'YAW_MOVE': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },    
    'YAW_STOP': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'YAW_REV': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'YAW_FWD': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },
    'YAW_POSITION': {
        'desc': "move pico motor forward",
        'prec': 4,
        'value': 0,
    },   
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
        
        self.setParam("PIT_MIDDLE", 300)
        self.driver.set_vel(1,1,300)
        self.setParam("YAW_MIDDLE", 300)
        self.driver.set_vel(1,1,300)

        
    def read(self, channel):
        value = self.getParam(channel)
        logging.info('%s == %s' % (channel, value))
        return value

    def write(self, channel, value):
        print('%s => %s' % (channel, value))
        self.setParam(channel, value)
        driverAddr = self.conf.channel[self.prefix+channel[:3]]["driver"]
        motorAddr  = self.conf.channel[self.prefix+channel[:3]]["motor"]
        dire = channel[:4]
        #        with self.driver:
        if channel[4:] == "STOP":
            self.driver.abort()
        if channel[4:] == "SLOW":   # speed:100
            self.driver.set_vel(driverAddr,motorAddr,value)
        if channel[4:] == "MIDDLE": # speed:300
            self.driver.set_vel(driverAddr,motorAddr,value)
        if channel[4:] == "QUICK":  # speed:500
            self.driver.set_vel(driverAddr,motorAddr,value)
        if channel[4:] == "REV":
            count = self.getParam(dire+"STEP")
            if self.getParam(dire+"SLOW")!=0:
                value = self.getParam(dire+"SLOW")
                vel = value
            elif self.getParam(dire+"MIDDLE")!=0:
                value = self.getParam(dire+"MIDDLE")
                vel = value
            elif self.getParam(dire+"QUICK")!=0:
                value = self.getParam(dire+"QUICK")
                vel = value
            self.driver.set_acc(driverAddr,motorAddr,1000)
            self.driver.set_vel(driverAddr,motorAddr,vel)
            self.driver.move_step(driverAddr,motorAddr,-1*count)
        if channel[4:] == "FWD":
            count = self.getParam(dire+"STEP")
            if self.getParam(dire+"SLOW")!=0:
                value = self.getParam(dire+"SLOW")
                vel = value
            elif self.getParam(dire+"MIDDLE")!=0:
                value = self.getParam(dire+"MIDDLE")
                vel = value
            elif self.getParam(dire+"QUICK")!=0:
                value = self.getParam(dire+"QUICK")
                vel = value
            self.driver.set_acc(driverAddr,motorAddr,1000)
            self.driver.set_vel(driverAddr,motorAddr,vel)
            self.driver.move_step(driverAddr,motorAddr,count)
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
