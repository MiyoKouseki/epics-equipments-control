# coding:utf-8
from visa import ResourceManager
'''



'''
__author__ = "Koseki.Miyo <miyo@icrr.u-tokyo.ac.jp>"
__status__ = "???"
__version__ = "0.0.1"
__date__    = "Dec 10 2018"


def is_correct_unit(func):
    def inner(*args,**kwargs):
        try:
            unit = kwargs['unit']
        except KeyError:
            print('[Error] Please give unit with either Hz or MHz.')            
            exit()
            
        if not unit in ['Hz','MHz']:
            raise ValueError('Invalid Unit')
        return func(*args,**kwargs)
    return inner


class E8663D(ResourceManager):        
    def __new__(cls,*args,**kwargs):
        '''

        Returns
        -------
        visa_socket : `pyvisa.resources.tcpip.TCPIPSocket`
        
        '''
        obj = super(E8663D, cls).__new__(cls,visa_library='@py')        
        return obj

    def __init__(self,ipaddr,port):
        '''
        '''
        resrc_name = 'TCPIP::{ipaddr}::{port}::SOCKET'.format(ipaddr=ipaddr,port=port)
        self.socket = self.open_resource(resrc_name,read_termination = '\n',write_termination='\n')
        #self.timeout = 5000
        self.options = {'fixed':None,
        }
        
    def __getitem__(self, cmd):
        '''
        '''
        self.options[cmd] = self.socket.query(cmd+'?')
        return self.options[cmd]
    
    def __setitem__(self, item,*value):
        '''
        '''
        cmd = item+' '+' '.join(value)
        print '"',cmd,'"'
        self.socket.write(cmd) # remove comment out when use. If not, do not remove!

    def __enter__(self):
        print('Socket open. Hello')
        return self        
        
    def __exit__(self, *args):        
        self.socket.close()
        print('Socket is now closed. Bye..!')


class VoltageControlledOscillator(E8663D):
    def __init__(self,ipaddr,port):
        super(VoltageControlledOscillator,self).__init__(ipaddr,port)

    # def __enter__(self):
    #     super(VoltageControlledOscillator,self).__enter__()

    # def __exit__(self,*args):
    #     super(VoltageControlledOscillator,self).__exit__(*args)        
        
        
    @property
    def fixedfrequency(self):        
        self._fixedfrequency = self[':frequency:fixed']
        return self._fixedfrequency

    @fixedfrequency.setter
    def fixedfrequency(self,value):
        self[':frequency:fixed'] = value

    @property
    def sweeptarget(self):        
        #self._sweeptarget = self[':frequency:SYNThesis:SWEep:TARGet']
        self._sweeptarget = self[':FREQuency:STOP']
        return self._sweeptarget

    @sweeptarget.setter
    def sweeptarget(self,value):
        #self[':frequency:SYNThesis:SWEep:TARGet'] = value        
        self[':FREQuency:STOP'] = value
    @property
    def sweeprate(self):        
        self._sweeprate = self[':SWEep[:FREQuency]:STEP:[LINear]']
        return self._sweeprate

    @sweeprate.setter
    def sweeprate(self,value):
        self[':SWEep[:FREQuency]:STEP:[LINear]'] = value        

    @property
    def sweepfrequency(self):
        #self._sweepfrequency = self[':frequency:SYNThesis:SWEep:Frequency']
        #return self._sweepfrequency
        #return self[':frequency:SYNThesis:SWEep:Frequency']
        return self[':frequency:fixed']
    @sweepfrequency.setter
    def sweepfrequency(self,value):
        self[':frequency:fixed'] = value        
        
    def step(self,value,unit='Hz'):
        if value>0:
            self.up(abs(value),unit=unit)
        elif value<0:
            self.down(abs(value),unit=unit)
        elif value==0:
            pass
        else:
            raise ValueError('Invalid Value')
        
    @is_correct_unit
    def up(self,value,unit='Hz'):
        print('Up..')
        self[':frequency:step'] = '{0}{1}'.format(value,unit)
        self[':frequency:fixed'] = 'up'

        
    @is_correct_unit
    def down(self,value,unit='Hz'):
        print('Down..')
        self[':frequency:step'] = '{0}{1}'.format(value,unit)
        self[':frequency:fixed'] = 'down'

        
    @is_correct_unit        
    #def fix(self,value,unit='MHz'):
    def fix(self,value,unit='Hz'):
        print('Fix..')
        
        #if unit is 'Hz':
        #    raise ValueError("Unit is Hz. Isn't this 'M'Hz ?")
            
        self[':frequency:fixed'] = '{0}{1}'.format(value,unit)

        
    def sweep(self,start,stop,rate):
        print('Sweep..')
        #self[':FREQuency:SYNThesis:SWEep:RATE'] = '{0}'.format(rate)
        #self[':FREQuency:SYNThesis:SWEep:target'] = '{0}'.format(stop)
        self[':frequency:fixed'] = '{0}'.format(start)        
        #self[':FREQuency:SYNThesis:SWEep:state'] = 'start'
        #self[':SWEep[:FREQuency]:STEP:[LINear]'] = '{0}'.format(rate)
        self[':FREQuency:STOP'] = '{0}'.format(stop)
        self[':FREQuency:STARt'] = '{0}'.format(start)

        
def test_e8663d():
    with E8663D('10.68.10.249',5025) as e8663d_x:
        print(e8663d_x[':frequency:fixed'])
        print(e8663d_x['*IDN'])
    #print(e8663d_x[':frequency:fixed']) # error due to a diconnect


def example():
    # ---------
    #  Example
    # ---------
    
    # Open scoket with given IP-address.    
    with VoltageControlledOscillator('10.68.10.249',5025) as vco_x:
        # 0. check current status
        print('fixedfrequency is ',vco_x.fixedfrequency)
        
        # 1. run some 'static' commands
        vco_x.fix(10,unit='MHz')
        vco_x.step(10,unit='Hz')
        vco_x.step(-10,unit='Hz')

        # 2. run sweep, and check status continuously
        vco_x.sweep(40.0272e6-10,40.0272e6+10,1)
    
    
if __name__ == '__main__':
    test_e8663d()
    #example()
    exit()
    import threading    
    def echo_swepfreq():
        _vco_x = VoltageControlledOscillator('10.68.150.65',5025)
        #print(_vco_x.sweepfrequency)
        print(_vco_x.fixedfreqency)
        _vco_x.close()
        
    print('wait 3 seconds')
    t = threading.Timer(3,echo_swepfreq)
    t.start()
