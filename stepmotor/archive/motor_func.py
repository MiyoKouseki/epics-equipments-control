from Trinamic_control6110 import *
#a                 ^ L
#a      _          |     <--
#a     /           |      mt_b
#a    v Y          |     
#a T               | 
#a <----|mt_c--------------
#a      v          |
#a                 |       -->
#a                 |       mt_a
#a

mt_a = 0
mt_b = 1
mt_c = 2

prt_a = -1
prt_b = -1
prt_c = +1

def move_T(a, value):
    a.sendCommand('GAP', 1, mt_a, 0)
    data = a.receiveData()

    if data.status != 100:
    	if self.errorDict.has_key(data.status):
   		raise MotorError(self.errorDict[data.status])
    	elif data.status == None:
     		raise MotorError('Incorrect controller response, trying to reconnect in motor a')
     	else:
 	       raise MotorError(''.join(('Unknown error, ', str(data.status))))
	
    a.sendCommand('GAP', 1, mt_b, 0)
    data = a.receiveData()
       #if data.status != 100:
       #	if self.errorDict.has_key(data.status):
        #      	raise MotorError(self.errorDict[data.status])
         #     elif data.status == None:
         #            raise MotorError('Incorrect controller response, trying to reconnect in motor a')
         #     else:
         #            raise MotorError(''.join(('Unknown error, ', str(data.status))))
		
    a.sendCommand('MVP',1,mt_a,-1*prt_a*value)
    data = a.receiveData()
    if data.status == 100:
        print 'status: OK, motor A position:', str(data.value)
    else:
        print 'Error'
    a.sendCommand('MVP',1,mt_b,prt_b*value)
    data = a.receiveData()
    if data.status == 100:
        print 'status: OK, motor B position:', str(data.value)
    else:
        print 'Error'


def move_L(a, value):
    a.sendCommand('GAP', 1, mt_a, 0)
    data = a.receiveData()

    if data.status != 100:
    	if self.errorDict.has_key(data.status):
   		raise MotorError(self.errorDict[data.status])
    	elif data.status == None:
     		raise MotorError('Incorrect controller response, trying to reconnect in motor a')
     	else:
 	       raise MotorError(''.join(('Unknown error, ', str(data.status))))
	
    a.sendCommand('GAP', 1, mt_b, 0)
    data = a.receiveData()
       #if data.status != 100:
       #	if self.errorDict.has_key(data.status):
        #      	raise MotorError(self.errorDict[data.status])
         #     elif data.status == None:
         #            raise MotorError('Incorrect controller response, trying to reconnect in motor a')
         #     else:
         #            raise MotorError(''.join(('Unknown error, ', str(data.status))))
		
    a.sendCommand('MVP',1,mt_c,-2*prt_c*value)
    data = a.receiveData()
    if data.status == 100:
        print 'status: OK, motor C position:', str(data.value)
    else:
        print 'Error'
    a.sendCommand('MVP',1,mt_b, prt_b*value)
    data = a.receiveData()
    if data.status == 100:
        print 'status: OK, motor B position:', str(data.value)
    else:
        print 'Error'
    a.sendCommand('MVP',1,mt_a, prt_a*value)
    data = a.receiveData()
    if data.status == 100:
        print 'status: OK, motor A position:', str(data.value)
    else:
        print 'Error'

def move_Y(a, value):
    a.sendCommand('GAP', 1, mt_a, 0)
    data = a.receiveData()

    if data.status != 100:
    	if self.errorDict.has_key(data.status):
   		raise MotorError(self.errorDict[data.status])
    	elif data.status == None:
     		raise MotorError('Incorrect controller response, trying to reconnect in motor a')
     	else:
 	       raise MotorError(''.join(('Unknown error, ', str(data.status))))
	
    a.sendCommand('GAP', 1, mt_b, 0)
    data = a.receiveData()
       #if data.status != 100:
       #	if self.errorDict.has_key(data.status):
        #      	raise MotorError(self.errorDict[data.status])
         #     elif data.status == None:
         #            raise MotorError('Incorrect controller response, trying to reconnect in motor a')
         #     else:
         #            raise MotorError(''.join(('Unknown error, ', str(data.status))))
		
    a.sendCommand('MVP',1,mt_c, prt_c*value)
    data = a.receiveData()
    if data.status == 100:
        print 'status: OK, motor C position:', str(data.value)
    else:
        print 'Error'
    a.sendCommand('MVP',1,mt_b, prt_b*value)
    data = a.receiveData()
    if data.status == 100:
        print 'status: OK, motor B position:', str(data.value)
    else:
        print 'Error'
    a.sendCommand('MVP',1,mt_a, prt_a*value)
    data = a.receiveData()
    if data.status == 100:
        print 'status: OK, motor A position:', str(data.value)
    else: 
        print 'Error'

