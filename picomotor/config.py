



def pvdb_dof(i):
    _REV = '{0}_REV'.format(i)
    _FWD = '{0}_FWD'.format(i)
    _POSITION = '{0}_POSITION'.format(i)
    _STEP = '{0}_STEP'.format(i)
    _SPEED = '{0}_SPEED'.format(i)
    pvdb = {
        _REV: {
            'prec': 4,
            'value': 0,
        },
        _FWD: {
            'prec': 4,
            'value': 0,
        },
        _POSITION: {
            'prec': 10,
            'value': 0,
        },
        _STEP: {
            'prec': 5,
            'value': 34,
        },    
        _SPEED: {
            'prec': 4,
            'value': 500,
        },
    }
    return pvdb

pvdb = pvdb_dof(1)
pvdb.update(pvdb_dof(2))
pvdb.update(pvdb_dof(3))
pvdb.update(pvdb_dof(4))
_ERROR = 'ERROR'
_ERRORMESSAGE = 'ERRORMESSAGE'
_STATUS = 'STATUS'
_COMMAND = 'COMMAND'    
dic = {\
       _ERROR: {
           'prec': 3,
           'value': 0,
       },
       _ERRORMESSAGE: {
           'type':'string',
       },    
       _STATUS: {
            'prec': 3,
           'value': 0,
       },
       _COMMAND: {
           'type':'string',
       },
   }
pvdb.update(dic)
if __name__ == '__main__':    
    print pvdb
