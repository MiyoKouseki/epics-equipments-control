

'''
All epics channels for pico in single PCAserver are ;
(PREFIX)_(ODF)_FWD,
(PREFIX)_(ODF)_REV,
(PREFIX)_(ODF)_POSITION,
(PREFIX)_(ODF)_STEP,
(PREFIX)_(ODF)_SPEED,
(PREFIX)_ERRORMESSAGE,
(PREFIX)_COMMAND,
(PREFIX)_STATUS,
where PREFIX is "K1:PICO-BS_IM_" and DOF is 1,2,3,4.

'''


def pvdb_dof(dof):
    _REV = '{dof}_REV'.format(dof=dof)
    _FWD = '{dof}_FWD'.format(dof=dof)
    _POSITION = '{dof}_POSITION'.format(dof=dof)
    _STEP = '{dof}_STEP'.format(dof=dof)
    _SPEED = '{dof}_SPEED'.format(dof=dof)
    
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


pvdb = {}
for dof in ['1','2','3','4']:
    pvdb.update(pvdb_dof(dof))

    

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
    for items in pvdb.items():
        print items
