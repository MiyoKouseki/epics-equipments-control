#
#!coding:utf-8

import socket
#import select
import time
import logging
import logging.config
from __init__ import get_module_logger
logger = get_module_logger(__name__)

errorMessage = \
{
    -1 :"TIMEOUT",
    0  :"NO ERROR DETECTED",
    3  :"OVER TEMPERATURE SHUTDOWN",
    6  :"COMMAND DOES NOT EXIST",
    7  :"PARAMETER OUT OF RANGE",
    9  :"AXIS NUMBER OUT OF RANGE",
    10 :"EEPROM WRITE FAILED",
    11 :"EEPROM READ FAILED",
    37 :"AXIS NUMBER MISSING",
    38 :"COMMAND PARAMETER MISSING",
    46 :"RS-485 ETX FAULT DETECTED",
    47 :"RS-485 CRC FAULT DETECTED",
    48 :"CONTROLLER NUMBER OUT OF RANGE",
    49 :"SCAN IN PROGRESS",
    100:"MOTOR_1 TYPE NOT DEFINED",
    200:"MOTOR_2 TYPE NOT DEFINED",
    300:"MOTOR_3 TYPE NOT DEFINED",
    400:"MOTOR_4 TYPE NOT DEFINED",
    101:"MOTOR_1 PARAMETER OUT OF RANGE",
    102:"MOTOR_2 PARAMETER OUT OF RANGE",
    103:"MOTOR_3 PARAMETER OUT OF RANGE",
    104:"MOTOR_4 PARAMETER OUT OF RANGE",
    108:"MOTOR_1 NOT CONNECTED",
    208:"MOTOR_2 NOT CONNECTED",
    308:"MOTOR_3 NOT CONNECTED",
    408:"MOTOR_4 NOT CONNECTED",
    110:"MOTOR_1 MAXIMUM VELOCITY EXCEEDED",
    210:"MOTOR_2 MAXIMUM VELOCITY EXCEEDED",
    310:"MOTOR_3 MAXIMUM VELOCITY EXCEEDED",
    410:"MOTOR_4 MAXIMUM VELOCITY EXCEEDED",
    111:"MOTOR_1 MAXIMUM ACCELERATION EXCEEDED",
    211:"MOTOR_2 MAXIMUM ACCELERATION EXCEEDED",
    311:"MOTOR_3 MAXIMUM ACCELERATION EXCEEDED",
    411:"MOTOR_4 MAXIMUM ACCELERATION EXCEEDED",
    114:"MOTOR_1 MOTION IN PROGRESS",
    214:"MOTOR_2 MOTION IN PROGRESS",
    314:"MOTOR_3 MOTION IN PROGRESS",
    414:"MOTOR_4 MOTION IN PROGRESS",
}

class controller(object):
    def __init__(self,ipaddr):
        self.ipaddr        = ipaddr
        self.port          = 23
        self.BUFFER_SIZE = 4096
        self.reply_message = None
        self.connect()
        
    def connect(self):
        logger.info('Connecting to {0}:{1}'.format(self.ipaddr,self.port))
        try:
            netAddr=(self.ipaddr, self.port)
            self.netsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.netsock.connect(netAddr)
            self.netsock.setblocking(1)
            self.netsock.settimeout(1.0)
        except socket.error as e:
            logger.info(e)
            print e
            print 'Could not connect to {0}:{1}. '\
                'Please check network configuration.'.format(self.ipaddr,self.port)
            print 'exit..'
            exit()
        except Exception as e:
            logger.info(e)
            print e
            exit()
        
    def __enter__(self):
        #self.connect()
        return self
    
    def read(self):
        time.sleep(0.1)
        try:
            data =  self.netsock.recv(self.BUFFER_SIZE)
            data = data.replace('\xff\xfb\x01\xff\xfb\x03','')
            data = data.replace('\r\n','')
            text = ([chr(ord(i)) for i in data])
            data = int(''.join(text))
            self.reply_message = data
        except Exception as e:
            logger.warning(e)
            logger.warning('failed data reciving')
            self.reply_message = -1
            
    def send(self, sendString):
        logger.info('Send "{1}" to {0}'.format(self.ipaddr,sendString))
        try:
            self.netsock.send(sendString+'\n')
        except socket.error as e:
            logger.info(e)
            logger.info("Reconnecting..")
            self.connect()
        except Exception as e:
            logger.info(e)
            print type(e)
            print dir(e)
            logger.info("Exit. Bye")
            exit()

    def close(self):
        logger.info('Closing controller {0}'.format(self.ipaddr))
        self.netsock.close()
        logger.info('OK. Bye {0}'.format(self.ipaddr))
        
    def __exit__(self,type, value, traceback):
        self.close()
        
class driver(controller):
    def __init__(self,ipaddr):
        super(driver,self).__init__(ipaddr)
        self.ipaddr = ipaddr
        self.set_acc(1,1,500)
        self.set_vel(1,1,500)                
        
    def __enter__(self):
        super(driver,self).__enter__()
        return self    

    def reconnect(self):
        self.__init__(self.ipaddr)
    
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
        try:
            logger.info('Reply message is "{0}"'.format(errorMessage[int(self.reply_message)]))
            return errorMessage[int(self.reply_message)]
        except:
            pass
        return -34
    
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
        
if __name__ == "__main__":    
    with driver("10.68.150.22") as k1pico:
        k1pico.ask_position(1,1)
        k1pico.check_reply_message()
        k1pico.ask_driver_error()
        k1pico.check_reply_message()
        k1pico.ask_speed(1,1)
        k1pico.check_reply_message()
        
