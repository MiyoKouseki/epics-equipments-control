
import sys
import time
from ezca import Ezca
Ezca().export()
import conf
import subprocess as sb
import logging

 
### USAGE ###
# AutoOffload DRIVER_NAME(ex. PR2_GAS)
# It automatically offload the VIS filters using stepping motors. 
# Please use it after making the K1:STEPPER channes available.
# If the stage is controlled, it will actuate the stepping motor by +/-20000 counts via EPICS channel.
# 

#def DriverON(STEPPER):
    ## Check if the K1:STEPPER is available
    
#def DriverON(STEP_BIO,DRIVERNAME):
#    # Reset Driver
#    ezca[STEP_BIO] = 0
#    ezca[STEP_BIO] = 1
#    # Start STEP_START
#    cmd = 'step_start '+DRIVERNAME
#    proc_step = sb.Popen(cmd.split())
#    return proc_step

def Offload(CTRLflt, STEPPER, COM):
    # Check if the DAMP filter is ON or OFF.
    CheckState = 0b00100000000000000000000000100
    CTRLstate = int(ezca[CTRLflt+'_STATE_NOW'])
    CTRLgain = ezca[CTRLflt+'_GAIN']
    ezca[STEPPER+'_ACC'] = 100.0
    ezca[STEPPER+'_VEL'] = 100.0
    syscheck = 0
    if (CheckState == (CheckState & CTRLstate)) and (abs(CTRLgain) > 0):
        ## Damp control is on
        # Take output average for 3 sec
        ii = 0
        out = 0.0
        s_time = time.time()
        while time.time() - s_time <= 10.0:
            out += ezca[CTRLflt+'_OUTPUT']
            ii += 1
        out = out/float(ii)
        logging.info('initial output value is %f',out)
        
        while abs(out) >= 2000.0:
            ## If the averaged output is larger than 2000, actuate FRs
            if out >= 2000.0:
                ezca[STEPPER+'_STEP'] = -20000.0
                print 'Wait until the output settled (~60 sec)'
                logging.info('Actuating motors by -20000 counts, waiting 60 sec for settling')
                ezca[COM] = 'ACTUATING'+STEPPER
                time.sleep(60)
            elif out <= -2000.0:
                ezca[STEPPER+'_STEP'] = 20000.0
                print 'Wait until the output settled (~60 sec)'
                logging.info('Actuating motors by +20000 counts, waiting 60 sec for settling')
                ezca[COM] = 'ACTUATING'+STEPPER
                time.sleep(60)
            # Check if the output comes back in the range.
            ii = 0
            out_new = 0.0
            s_time = time.time()
            while time.time() - s_time <= 10.0:
                out_new += ezca[CTRLflt+'_OUTPUT']
                ii += 1
            out_new = out_new/float(ii)
            logging.info('new output value is %f',out_new)
            
            if abs(out_new - out) < 800.0:
                print '%s not seem to work well. Please check carefully.'%STEPPER
                ezca[COM] = 'PLS CHECK STEPPER MOTOR ACTUATION'
                logging.warning('%s does not seem to work well. Please check carefully.',STEPPER)
                syscheck = 1
                break

            out = out_new

    else:
        ## DAMP control is off
        # Take input average for 3 sec
        ii = 0
        out = 0.0
        s_time = time.time()
        while time.time() - s_time <= 10.0:
            out += ezca[CTRLflt+'_INMON']
            ii += 1
        out = out/float(ii) + ezca[CTRLflt+'_OFFSET']
        logging.info('initial input value (difference from the nominal) is %f',out)
   
        while abs(out) >= 200.0:
            if out >= 200:
                ezca[STEPPER+'_STEP'] = 20000.0
                logging.info('Actuating motors by +20000 counts, waiting 3 sec for settling')
                ezca[COM] = 'ACTUATING'+STEPPER
                time.sleep(3)
            elif out <= -200:
                ezca[STEPPER+'_STEP'] = -20000.0
                logging.info('Actuating motors by -20000 counts, waiting 3 sec for settling')
                ezca[COM] = 'ACTUATING'+STEPPER
                time.sleep(3)
            # Check if the output comes back in the range.
            ii = 0
            out_new = 0.0
            s_time = time.time()
            while time.time() - s_time <= 10.0:
                out_new += ezca[CTRLflt+'_INMON']
                ii += 1
            out_new = out_new/float(ii) + ezca[CTRLflt+'_OFFSET']
            logging.info('new input value (difference from the nominal) is %f', out_new)

            if abs(out_new - out) < 80.0:
                print 'Keystone does not seem to work well. Please check carefully.'
                ezca[COM] = 'PLS CHECK STEPPER MOTOR ACTUATION'
                logging.warning('Keystone does not seem to work well. Please check carefully.')
                syscheck = 1
                break

            out = out_new
    if syscheck == 0:
       ezca[COM] = 'Done'


def main():
    argc = len(sys.argv)
    if (argc != 2):
        print '! Check argv !'
        quit()
    driver = sys.argv[1]
    
    logging.basicConfig(filename='/opt/rtcds/userapps/release/cds/common/scripts/epics-motor-control/stepmotor/AutoOffLoad/'+driver+'.log', format='%(asctime)s %(message)s', level=logging.INFO)

    if optic in conf.driverGAS:
        StepDriver = 'STEPPER-'+conf.driverGAS[optic]['DRIVER']
        StepBio = 'VIS-'+conf.driverGAS[optic]['DRIVER'].split('_')[0]+'_BO_ENCODE_STEP_GAS_SW'
        ezca[StepBio] = 1
        #proc_step = DriverON(StepBio,conf.driverGAS[optic]['DRIVER'])
        CTRL = conf.driverGAS[optic]['CTRL']
        COM = 'VIS-%s_COMMISH_MESSAGE'%optic
        for stage in conf.driverGAS[optic]:
            if stage != 'CTRL' and stage != 'DRIVER':

                logging.info('Checking %s',stage)

                CTRLflt = 'VIS-'+optic+'_'+stage+'_'+CTRL+'_GAS' ## VIS-PR3_BF_DAMP_GAS
                DrivePort = conf.driverGAS[optic][stage]
                STEPchannel = StepDriver+'_'+DrivePort ## STEPPER-PR0_GAS_0
                Offload(CTRLflt, STEPchannel, COM)

                ezca[STEPchannel+'_UPDATE'] = 1
                ezca[STEPchannel+'_UPDATE'] = 0
                logging.info('finishing Offload %s',stage)

        ezca[StepBio] = 0

#    if optic in conf.driverIP:
#        StepDriver = 'STEPPER-'+optic+'_IP'
#        CTRL = conf.driverIP[optic]['CTRL']
#        for DOF in ['L','T','Y']:
#            CTRLflt = 'VIS-'+optic+'_IP_'+CTRL+'_'+DOF
#            STEPchannel = StepDriver+'_'+DOF
#            Offload(CTRLflt, STEPchannel)
#        ezca[StepDriver+'_UPDATE'] = 1
#        ezca[StepDriver+'_UPDATE'] = 0




    else:
        print '! Please check DRIVER_NAME %s' % argv[1]
        quit()

if __name__=="__main__":
    main()


