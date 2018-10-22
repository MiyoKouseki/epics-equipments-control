#
# -*- coding:utf-8 -*-


import socket
import time
import logging
import logging.config
from __init__ import get_module_logger
logger = get_module_logger(__name__)

class controller(object):
    def init(self,ipaddr):
        self.ipaddr        = ipaddr
        self.port          = 23
        self.BUFFER_SIZE = 4096
        self.reply_message = None
        self.connect()        
        self.maxModuleCurrent = 1.6
        
    def __init__(self):
        self.commandDict = {'ROR':1, 'ROL':2, 'MST':3, 'MVP':4, 'SAP':5, 'GAP':6,
             'STAP':7, 'RSAP':8, 'SGP':9, 'GGP':10, 'RFS':13, 'SIO':14, 'GIO':15, 'WAIT':27, 'STOP':28,
             'SCO':30, 'GCO':31, 'CCO':32, 'VER':136, 'RST':255}

        self.position = 0
        self.speed = 0.0
        self.timeout = 2.
        self.writeTimeout = 0.0
        self.connected = None
        self.port = None
        self.portName = None
        
        self.errorDict = {1:'Wrong checksum', 2:'Invalid command', 3:'Wrong type', 4:'Invalid value',
                        5:'Configuration EEPROM locked', 6:'Command not available'}
        
        self.maxModuleCurrent = 1.6
        
                
    def connect(self):
        logger.info('Connecting to {0}:{1}'.format(self.ipaddr,self.port))
        try:
            netAddr=(self.ipaddr, self.port)
            self.netsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.netsock.connect(netAddr)
            self.netsock.setblocking(1)
            self.netsock.settimeout(5.0)
        except socket.error as e:
            logger.info(e)
            print e
            print 'Could not connect to {0}:{1}. '\
                'Please check network configuration.'.format(self.ipaddr,self.port)
            print 'exit..'
            exit()            
        
    def __enter__(self):
        #self.connect()
        return self

    def sendCommand(self, cmd, type, motor, value):
        adr = 1
        try:
            command = self.commandDict[cmd]
        except KeyError:
            return 'Wrong command'
        tmp = struct.pack('BBBBi', adr, command, type, motor, value)
        checksum = sum(struct.unpack('BBBBBBBB', tmp)) % 256
        TxBuffer = struct.pack('>BBBBiB', adr, command, type, motor, value, checksum)
        if self.connected == 'RS485':
            if self.port.inWaiting() > 0:
                self.port.flushInput()
                self.port.flushOutput()
            self.port.write(TxBuffer)
        elif self.connected == 'TCP':
            self.port.send(TxBuffer)
        return TxBuffer
    
    def read(self):
        hoge = ''

    def reconnect(self):
        print 'Reconnecting...'
        if self.connected == 'RS485':
            self.close()
            self.connectRS485(self.portName, self.baudrate)
        elif self.connected == 'TCP':
            self.close()
            self.connectTCP(self.portName[0], self.portName[1])
        print 'Testing connection:'
        self.sendCommand('GAP', 1, 0, 0)
        if self.connected == 'RS485':
            RxBuffer = self.port.read(9)
        elif self.connected == 'TCP':
            RxBuffer = self.port.recv(9)
        else: 
            RxBuffer = ''
        if RxBuffer.__len__() != 9:
            status = 0
            self.close()
            raise MotorError('Reconnection failed.')
        else:
            status = 1
            print '...ok'
        return status        

    def connectTCP(self, ipadr, port):
        self.port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.port.connect((ipadr, port))
            self.port.settimeout(self.timeout)
            self.connected = 'TCP'
            self.portName = [ipadr, port]
        except Exception, e:
            print 'Could not connect to TCP', e
        
                
    def send(self, sendString):
        logger.info('Send "{1}" to {0}'.format(self.ipaddr,sendString))
        

    def close(self):
        logger.info('Closing controller {0}'.format(self.ipaddr))
        self.netsock.close()
        logger.info('OK. Bye {0}'.format(self.ipaddr))
        
    def __exit__(self,type, value, traceback):
        self.close()
        
class driver(controller):
    def __init__(self,ipaddr):
        super(driver,self).__init__(ipaddr)
        
    def __enter__(self):
        super(driver,self).__enter__()
        return self
    
    def ask_driver_error(self):
        self.send('TE?')

    def ask_position(self,driverAddr,motorAddr):
        self.send('%sTP?'%(motorAddr))

    def ask_speed(self,driverAddr,motorAddr):
        self.send('%sVA?'%(motorAddr))        
        
    def check_reply_message(self):
        self.read()
        logger.info('Reply message is "{0}"'.format(self.reply_message))
        return self.reply_message
    
    def check_error_message(self):
        self.read()
        return errorMessage[int(self.reply_message)]
    
    def set_vel(self,driverAddr,motorAddr,vel):
        """ Max velocity 
        standard motor : 2000[step/sec] maybe..
        tiny motor     : 1750[step/sec]
        """
        self.send('%s>%sVA%s'%(driverAddr,motorAddr,vel))
        
    def set_acc(self,driverAddr,motorAddr,acc):
        self.send('%s>%sAC%s'%(driverAddr,motorAddr,acc))
        
    def move_step(self,driverAddr,motorAddr,count):
        self.send('%s>%sPR%d'%(driverAddr,motorAddr,count))
        
    def stop_motor(self,driverAddr,motorAddr):
        self.send('%s>%sST'%(driverAddr,motorAddr))

    def abort(self):
        self.send('AB')
        
    def soft_stop(self):
        self.send('ST')

    def restart(self):
        self.send('RS')
        
    def __exit__(self,type, value, traceback):
        #self.stop_motor("1","1") # stop all motor
        super(driver,self).__exit__(type, value, traceback)
        
    def getTargetPosition(self):
        cmd = 'GAP'       # Get axis parameter
        type = 4          # Target speed... maybe use 4 (max pos speed)?
        value = 0         # don't care
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        return data.value
        
        
if __name__ == "__main__":    
    with driver("10.68.150.51",4001) as k1stepper:
        k1stepper.reconnect()
        print k1stepper.getTargetPosition(0)
        
