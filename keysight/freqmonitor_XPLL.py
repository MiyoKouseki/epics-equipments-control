import os
import datetime
import time
from e8663d import VoltageControlledOscillator
from pyvisa import errors
import ezca
ezca = ezca.Ezca()

## not to output to the terminal
# Define a context manager to suppress stdout and stderr.
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])
        os.close(self.save_fds[0])
        os.close(self.save_fds[1])

        
i = 0
freq_default = 40.e6

with VoltageControlledOscillator('10.68.150.65',5025) as vco_x:
    while True:
        try:
            freq = float(vco_x.sweepfrequency) - freq_default
            with suppress_stdout_stderr():
                try:
                    ezca.write("ALS-X_BEAT_LO_FREQ",str(freq))
                except Exception as e:
                    print e.message
            i += 1
            time.sleep(0.01)
        except KeyboardInterrupt:
            exit()
        except errors.VisaIOError as e:
            print e
            print datetime.datetime.now()
