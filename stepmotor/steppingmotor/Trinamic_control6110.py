# -*- coding:utf-8 -*-
"""
Created on Mar 7, 2012

@author: Filip
"""

#import serial
import socket
import struct
import time
from numpy import log2, sqrt

class MotorError(Exception):
    pass


class Trinamic_control6110():
    class ReceiveData():
        def __init__(self, adr=0, status=0, cmd=0, value=0):
            self.status = status
            self.commandNumber = cmd
            self.value = value
            self.moduleAddress = adr
            
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
        
#    def connectRS485(self, port, baudrate=9600):
#        try:
#            self.port = serial.Serial(port, baudrate, timeout=self.timeout, writeTimeout=self.writeTimeout)
#            self.connected = 'RS485'
#            self.portName = port
#            self.baudrate = baudrate
#        except Exception, e:
#            print 'Could not connect to RS485', e
            
    
            
    def connectTCP(self, ipadr, port):
        self.port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.port.connect((ipadr, port))
            self.port.settimeout(self.timeout)
            self.connected = 'TCP'
            self.portName = [ipadr, port]
        except Exception, e:
            print 'Could not connect to TCP', e
            
    def close(self):
        if self.port != None:
            self.port.close()
        self.connected = None

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

    def receiveData(self):
        if self.connected == 'RS485':
            RxBuffer = self.port.read(9)
            if self.port.inWaiting() > 0:
                self.port.flushInput()
        elif self.connected == 'TCP':
            RxBuffer = self.port.recv(9)
        else: 
            RxBuffer = ''
        if RxBuffer.__len__() == 9:
            data = struct.unpack('>BBBBiB', RxBuffer)
            rData = self.ReceiveData(data[1], data[2], data[3], data[4])
        else:
            rData = self.ReceiveData(None, None, None, None)
            self.reconnect()
        return rData

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
    

    def reset(self):
        cmd = 'RST'       # Reset
        type = 0          # 
        value = 1234         # 1234 
        self.sendCommand(cmd, type, 0, value)
        data = self.receiveData()
#        print 'Status',data.status
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        return data.value  

    def setBaudrate(self, baudrate):
        cmd = 'SGP'       # Set global parameter
        type = 65          # baudrate
        if baudrate >= 0 or baudrate > 115200:
            # if it is a number less than 8 assume it is an index to a list of baudrates
            if baudrate < 8:
                value = int(baudrate)
            # Or else it is the actual baudrate
            else:
                value = int(baudrate / 9600)
                # Snap to index in list of baudrates
                if value < 2:
                    # Baudrate 9600 has index 0. We lose 14400, but don't care
                    value = 0
            self.sendCommand(cmd, type, 0, value)
            data = self.receiveData()
            if data.status != 100:
                if self.errorDict.has_key(data.status):
                    raise MotorError(self.errorDict[data.status])
                elif data.status == None:
                    raise MotorError('Incorrect controller response, trying to reconnect')
                else:
                    raise MotorError(''.join(('Unknown error, ', str(data.status))))
            self.reset()
            time.sleep(0.5)
            port = self.port.getPort()
            self.close()
            if value > 1:
                actualBaudrate = value * 9600
            else:
                actualBaudrate = (1 + 0.5 * value) * 9600
            print 'New baudrate:', actualBaudrate
            self.connectRS485(port, actualBaudrate)
        else:
            if baudrate < 0:
                raise MotorError('Baud rate negative')
            else:        
                raise MotorError('Baud rate too high (>115200)')
            pass
            
    def getBaudrate(self):
        cmd = 'GGP'       # Get global parameter
        type = 65          # baudrate
        value = 0         # Don't care 
        self.sendCommand(cmd, type, 0, value)
        data = self.receiveData()
#        print 'Status',data.status
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        if data.value > 1:
            baudrate = data.value * 9600
        else:
            baudrate = 9600 * (1 + 0.5 * data.value)
        return baudrate        
    
    def setTargetPosition(self, pos, motor=0):
        cmd = 'MVP'       # Move to position
        type = 0          # Absolute
        value = int(pos)
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
    
    def setMaxCurrent(self, current, motor=0):
        cmd = 'SAP'       # Get axis parameter
        type = 6          # Maximum current (peak)
        value = int(current / self.maxModuleCurrent * 255.0)         # Value in % to max module current 
                                           # (scaled to 255) 
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        cmd = 'SAP'       # Get axis parameter
        type = 7          # Standby current 
        value = int(current / self.maxModuleCurrent * 255.0 * 0.1)         # Value in % to max module current 
                                           # (scaled to 255)
                                           # Standby current set to 10% of the drive current 
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        return data.status

    def getMaxCurrent(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 6          # Maximum current (peak)
        value = 0         # Don't care 
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
#        print 'Status',data.status
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        current = data.value * self.maxModuleCurrent / 255.0
        return current        
    
    def setIdleCurrent(self, idleCurrent, motor=0):
        cmd = 'SAP'       # Get axis parameter
        type = 7          # Standby current 
        value = int(idleCurrent / self.maxModuleCurrent * 255.0)         # Value in % to max module current 
                                           # (scaled to 255)
                                           # Standby current set to idleCurrent 
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        return data.status
    
    def getPulseDivisor(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 154          # Pulse divisor
        value = 0         # Don't care 
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
    
    def setPulseDivisor(self, pd, motor=0):  
        """ Number of pulse division per step.
        Should be 0-13"""   
        cmd = 'SAP'       # Get axis parameter
        type = 154          # Microstep resolution
        value = int(pd)         # Microstep resolution 
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
    
    def getMicrostepResolution(self, motor=0):  
        cmd = 'GAP'       # Get axis parameter
        type = 140          # Microstep resolution
        value = 0         # Don't care 
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
#        print 'Status',data.status
#        print 'Value:',data.value
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))

        res = 2 ** data.value
        return res  
    
    def setMicrostepResolution(self, res, motor=0):
        """ Number of microsteps per full step.
        Should be 1,2,4,8,16,32 or 64"""   
        cmd = 'SAP'       # Get axis parameter
        type = 140          # Microstep resolution
        value = int(log2(res))         # Microstep resolution 
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        
        
    def getActualPosition(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 1          # Actual position
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
    
    def stop(self, motor=0):
        cmd = 'MST'       # Motor stop
        type = 0          # don't care
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
        
    def getTargetSpeed(self, motor=0):
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
    
    def setTargetSpeed(self, speed, motor=0):
        cmd = 'SAP'       # Get axis parameter
        type = 4          # Target speed (max pos speed)
        value = int(speed)         # Speed
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))

    def getActualSpeed(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 3          # Actual speed
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
    
    def getTargetPosition(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 0          # Target position
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
    
    def getTargetPositionReached(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 8          # Target position
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

    def setLimitSwitchPolarity(self, polarity):
        '''The TMCM6110 can set the limit switch polarity (normally open / normally closed)
        in sets of three motors. Motors 0-2 are controlled by bit 0 in GP 79, motors 3-5
        by bit 1. It would be confusing to divide half of the controller , so we set the 
        polarity of all six motors with this command. 
        '''
        cmd = 'SGP'        # Set global parameter 
        type = 79       # Limit polarity is controlled by global parameter 79, selected by parameter "type"
        motor = 0        # Bank 0
        if polarity == 0:
            value = 3    # Invert all outputs
        else:
            value = 0
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
    
    def getRightLimitSwitch(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 10          # Target position
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

    def getRightLimitSwitchEnabled(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 12          # Right limit switch enabled
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
        if data.value == 0:   # If return value = 0, the limit switch is enabled
            return True
        else:
            return False

    def setRightLimitSwitchEnable(self, enable, motor=0):
        cmd = 'SAP'       # Get axis parameter
        type = 12          # Right limit switch enabled
        if enable == True:
            value = 0         # If 0, switch is enabled
        else:
            value = 1
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
    
        
    def getLeftLimitSwitch(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 11          # Target position
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

    def getLeftLimitSwitchEnabled(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 13          # Left limit switch enabled
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
        if data.value == 0:
            return True
        else:
            return False
        
    def setLeftLimitSwitchEnable(self, enable, motor=0):
        cmd = 'SAP'       # Get axis parameter
        type = 13          # Right limit switch enabled
        if enable == True:
            value = 0         # If 0, switch is enabled
        else:
            value = 1
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
        

    
    def setupMotor(self, motor=0):
        self.setMaxCurrent(0.3, motor)
        self.setMicrostepResolution(1, motor)
        cmd = 'SAP'       # Set axis parameter
        type = 12          # Right limit switch disable
        value = 1         
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        if data.status == 100:
            cmd = 'SAP'       # Set axis parameter
            type = 13          # Left limit switch disable
            value = 1         
            self.sendCommand(cmd, type, motor, value)
            data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        if data.status == 100:
            cmd = 'SAP'       # Set axis parameter
            type = 149          # Soft stop flag (stop immediately at limit switch)
            value = 0         
            self.sendCommand(cmd, type, motor, value)
            data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        return data.status
    
    def definePosition(self, pos, motor=0):
        self.stop(motor)    # Needed to prevent the motor from moving when setting position
        cmd = 'SAP'       # Set axis parameter
        type = 1          # Set actual position
        value = pos         
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        cmd = 'SAP'       # Set axis parameter
        type = 0          # Set target position
        value = pos         
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))

    def setZeroPosition(self, motor=0):
        self.stop(motor)    # Needed to prevent the motor from moving when setting position
        cmd = 'SAP'       # Set axis parameter
        type = 1          # Set actual position
        value = 0         
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        print 'setZeroPosition, motor ', motor, ' return ', data.status
        status = data.status
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        if data.status == 100:
            status = self.setTargetPosition(0, motor)
        return status

    def getRampDivisor(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 153          # Ramp divisor
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

    def setRampDivisor(self, rampDivisor, motor=0):
        cmd = 'SAP'       # Get axis parameter
        type = 153          # Ramp divisor
        if rampDivisor < 0:
            raise MotorError('rampDivisor negative')
        elif rampDivisor > 13:
            raise MotorError('rampDivisor too high (>13)')
        value = int(rampDivisor)
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
    
    def getAcceleration(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 5          # Max acceleration
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

    def setAcceleration(self, acceleration, motor=0):
        cmd = 'SAP'       # Get axis parameter
        type = 5          # Max acceleration
        value = acceleration         # don't care
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
      
    def getFirmwareVersion(self):
        cmd = 'VER'       # Firmware version
        type = 0          # return string
        value = 0         # don't care
        motor = 0
        self.sendCommand(cmd, type, motor, value)
        RxBuffer = self.port.read(9)
        
        return RxBuffer[1:]
        
    
    def groupMotors(self, motorList, groupIndex):
        cmd = 'SAP'       # Set axis parameter
        type = 213          # Set actual position
        value = groupIndex         
        for motor in motorList:
            self.sendCommand(cmd, type, motor, value)
            data = self.receiveData()
            if data.status != 100:
                if self.errorDict.has_key(data.status):
                    raise MotorError(self.errorDict[data.status])
                elif data.status == None:
                    raise MotorError('Incorrect controller response, trying to reconnect')
                else:
                    raise MotorError(''.join(('Unknown error, ', str(data.status))))
    
    def getPMul(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 146          # Max acceleration
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

    def getPDiv(self, motor=0):
        cmd = 'GAP'       # Get axis parameter
        type = 137          # Max acceleration
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
    
    def startReferenceSearch(self, motor=0):
        # Make sure limit switch is enabled
        swEnabled = self.getLeftLimitSwitchEnabled(motor)  
        if swEnabled == False:
            self.setLeftLimitSwitchEnable(True, motor)
            
        # Setup ref search parameters
        cmd = 'SAP'       # Set axis parameter
        type = 193        # Ref search mode
        value = 1         # Search left limit switch only
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        speed = self.getTargetSpeed(motor) / 2
        cmd = 'SAP'       # Set axis parameter
        type = 194        # Ref search speed
        value = speed     # Use half speed as normal running
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        cmd = 'SAP'       # Set axis parameter
        type = 195        # Ref switch calibration speed
        value = speed / 2 # Use quarter speed as normal running
        self.sendCommand(cmd, type, motor, value)
        data = self.receiveData()
        if data.status != 100:
            if self.errorDict.has_key(data.status):
                raise MotorError(self.errorDict[data.status])
            elif data.status == None:
                raise MotorError('Incorrect controller response, trying to reconnect')
            else:
                raise MotorError(''.join(('Unknown error, ', str(data.status))))
        

        
        cmd = 'RFS'       # Reference search
        type = 0          # Start ref search
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

    def stopReferenceSearch(self, motor=0):        
        cmd = 'RFS'       # Reference search
        type = 1          # Stop ref search
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
            
    def getReferenceSearchStatus(self, motor=0):
        cmd = 'RFS'       # Reference search
        type = 2          # Ref search status
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
    
    def getActualMotorLoad(self, motor):
        cmd = 'GAP'       # Get axis parameter
        type = 206        # Actual load value
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
    
    def getDriverErrorFlags(self, motor):
        cmd = 'GAP'       # Get axis parameter
        type = 208        # TMC206 driver error flags
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
        
        
        
        
if __name__ == '__main__':
    tc = Trinamic_control6110()
#    tc.connectTCP('130.235.95.232', 4001)
