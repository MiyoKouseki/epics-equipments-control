# import socket
# HOST = "10.68.150.65"    # The remote host
# PORT = 5023             # The same port as used by the server

# s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))

# exit()
import visa
rm = visa.ResourceManager('@py')
visa.log_to_screen
ins = rm.open_resource('TCPIP::10.68.150.65::5025::SOCKET',read_termination = '\n')
cmd = '*IDN?'
cmd = ':SYSTem:COMMunicate:LAN:IP?'
cmd = ':FREQuency:OFFSet?'
cmd = ':FREQuency:CENTer?'
cmd = ':FREQuency:REFerence?'
cmd = ':FREQuency:STARt?'
cmd = ':DISPlay:ANNotation:AMPLitude:UNIT?'
cmd = ':MARKer:AMPLitude:VALue?'
print(ins.query(cmd))

### YE's play area ### 

cmd = ':FREQuency:FIXed 40.0272MHZ' # set the fixed frequency of sweep
ins.write(cmd)
cmd = ':FREQuency:SYNThesis:SWEep:TARGet 40052200' # set sweep target freq in Hz
ins.write(cmd)
cmd = ':FREQuency:SYNThesis:SWEep:RATE 100' # sweep speed in Hz/s
ins.write(cmd)

cmd = ':FREQuency:SYNThesis:SWEep:STATe STARt' # start sweep
ins.write(cmd)

cmd = ':FREQuency:SYNThesis:SWEep:FREQuency?' # calls current frequency even during a sweep
print(ins.query(cmd))

#cmd = ':FREQuency:STEP 100HZ'
#ins.write(cmd)
#cmd = ':FREQuency:FIXed DOWN'
#ins.write(cmd)

cmd = ':FREQuency:FIXed?'
print(ins.query(cmd))

### End of YE's play area ###

ins.close()
