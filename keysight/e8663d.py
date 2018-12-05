#
#
from visa import ResourceManager

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
        self.socket = self.open_resource(resrc_name,read_termination = '\n')
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
        self.options[item] = value
        print('Dont set ',value)

    def __enter__(self):        
        return self        
        
    def __exit__(self, *args):
        self.close()


class VoltageControlledOscillator(E8663D):
    def __init__(self,ipaddr,port):
        super(VoltageControlledOscillator,self).__init__(ipaddr,port)

    @property
    def fixedfrequency(self):        
        self._fixedfrequency = self[':frequency:fixed']
        return self._fixedfrequency

    @fixedfrequency.setter
    def fixedfrequency(self,value):
        self[':frequency:fixed'] = value

    @property
    def sweeptarget(self):        
        self._sweeptarget = self[':frequency:SYNThesis:SWEep:TARGet']
        return self._sweeptarget

    @sweeptarget.setter
    def sweeptarget(self,value):
        self[':frequency:SYNThesis:SWEep:TARGet'] = value        

    @property
    def sweeprate(self):        
        self._sweeprate = self[':frequency:SYNThesis:SWEep:Rate']
        return self._sweeprate

    @sweeprate.setter
    def sweeprate(self,value):
        self[':frequency:SYNThesis:SWEep:Rate'] = value        

    @property
    def sweepfrequency(self):        
        self._sweepfrequency = self[':frequency:SYNThesis:SWEep:Frequency']
        return self._sweepfrequency

    @sweepfrequency.setter
    def sweepfrequency(self,value):
        self[':frequency:SYNThesis:SWEep:Frequency'] = value        
        

        
if __name__ == '__main__':
    # # TEST E8663D
    # with E8663D('10.68.150.65',5025) as e8663d_x:
    #     print(e8663d_x[':frequency:fixed'])
    #     print(e8663d_x['*IDN'])
    
    with VoltageControlledOscillator('10.68.150.65',5025) as vco_x:
        vco_x.sweep(10,15,1)
