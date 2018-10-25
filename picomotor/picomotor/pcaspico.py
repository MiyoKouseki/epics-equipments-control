#
#! coding:utf-8
import os
import pcaspy
import logging
import time
import config
from datetime import datetime
from datetime import timedelta
#import pyttsx

pvdb = config.pvdb

ON = 1.0
#
#os.environ['EPICS_CAS_INTF_ADDR_LIST'] = '10.68.10.255'
#os.environ['EPICS_CAS_INTF_ADDR_LIST'] = 'localhost'
#os.environ['EPICS_CAS_SERVER_PORT'] = '58901'
# https://pcaspy.readthedocs.org/en/latest/tutorial.html

import logging
import logging.config

from __init__ import get_module_logger
logger = get_module_logger(__name__)


class PcasDriver(pcaspy.Driver):
    def __init__(self, driver, prefix):
        super(PcasDriver, self).__init__()
        self.driver = driver
        self.prefix = prefix
        
    def read(self, channel):
        value = self.getParam(channel)    
        return value    
    
    def write(self, channel, value):
        """ 
        
        This function is called every "CAPUT (EPICS-CHANNEL) (VALUE)" command.
        

        Parameters
        ----------
        channel : str
            Epics channel name that you want to change.
        value : int
            Value of the channel that you want to change. If switch epics channel,
            value is either 0 or 1.
        driverAddr : int, optional
            Driver number that you want to change. Default value is 1, which means
            master driver ethernet cable are connected. 
            
        Returns
        -------
        
        """        
        self.setParam(channel, value) # need ! why????
        
        driverAddr = 1
        
        if "REV" in channel and value == ON:
            MOTORNUMBER, OPTION = channel.split("_")
            step = self.getParam(MOTORNUMBER+"_STEP")
            self.driver.move_step(driverAddr,int(MOTORNUMBER),-1*step)
            
        if "FWD" in channel and value == ON:
            MOTORNUMBER, OPTION = channel.split("_")
            step = self.getParam(MOTORNUMBER+"_STEP")
            self.updatePVs()
            self.driver.move_step(driverAddr,int(MOTORNUMBER),step)
            
        if "COMMAND" in channel:
            command = value
            self.driver.send(command)
            
        if "STATUS" in channel and value == ON:
            MOTORNUMBER = str(1)
            self.driver.ask_position(driverAddr,MOTORNUMBER)
            posi = self.driver.check_reply_message()
            self.setParam(MOTORNUMBER+"_POSITION", posi)
            MOTORNUMBER = str(2)
            self.driver.ask_position(driverAddr,MOTORNUMBER)
            posi = self.driver.check_reply_message()
            self.setParam(MOTORNUMBER+"_POSITION", posi)            
            MOTORNUMBER = str(3)
            self.driver.ask_position(driverAddr,MOTORNUMBER)
            posi = self.driver.check_reply_message()
            self.setParam(MOTORNUMBER+"_POSITION", posi)            
            MOTORNUMBER = str(4)
            self.driver.ask_position(driverAddr,MOTORNUMBER)
            posi = self.driver.check_reply_message()
            self.setParam(MOTORNUMBER+"_POSITION", posi)            
            #
            self.driver.ask_driver_error()
            error = self.driver.check_reply_message()
            self.setParam("ERROR", error)
            errormessage = self.driver.check_error_message()
            self.setParam("ERRORMESSAGE", errormessage)
            
        self.updatePVs()
        return True
    
class PcasServer(pcaspy.SimpleServer):
    def __init__(self, prefix, driver):
        super(PcasServer, self).__init__()
        logger.info("Initialize PCAServer")
        self.server = pcaspy.SimpleServer()
        self.server.createPV(prefix, pvdb)
        self.driver = driver
        driver_ = PcasDriver(driver,prefix)
        
    def run(self):
        logger.info("Start server.")        
        i = 0
        start = datetime.now()
        dt = timedelta(seconds=3600)
        while True:
            self.server.process(0.1)
            now = datetime.now()
            diff = now- start
            #print diff,dt,diff>dt
            if diff>dt: # 12sec
                self.driver.close()
                print "=================================="
                print '60 minutes passed. Bye!'
                print "I'll be back.."
                print """
                　　　　　　　　　　　 /j^i
                　　　　　　　　　　 ./　 ;!
                　　　　　　　　　　/　 /_＿,,..
                　　　　　　　　　/　　`(_t＿,__〕
                　　　　　　　　 /　　　 '(_t＿,__〕
                　　　　　　　　/　　　　｛_i＿,__〕
                　　　　　　 ／　　　 ノ　 {_i＿_〉
                　　　　　／　　　　　　＿,..-'"
                　　　／　　　　　　／
                ～～～～～～～～～～～～～～～～
                """
                print "=================================="
                exit()
            else:
                i=i+1

if __name__ == '__main__':
    import pcaspico
    import newfocus8742
    import sys
    import time
    #
    prefix   = 'K1:PICO-BS_IM_'
    driver_ip = '10.68.150.16'
    driver_addr = 1 # means master
    mydriver   = newfocus8742.driver(driver_ip,driver_addr)
    picoserver = pcaspico.PcasServer(prefix, mydriver)
    try:
        picoserver.run()
    except KeyboardInterrupt as e:
        mydriver.close()
        print e
        print 'Detect keyboard interrupt. Bye!'
        exit()
