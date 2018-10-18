# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 12:37:17 2018

@author: ayaka.shoda

Functions to actuate IP in each DOFs using stepping motors.
Tyere are three types of alignment of the stepping motors of IP in KAGRA, SR, BS, and TM.
The motor number assignment was defined in conf.py.
For more details, please refer KAGRA wiki (DGS/MotorControl/StepperMotor).
"""

import numpy as np
import conf


########## Actuation Functions ###########
def Move_L(prefix,driver,value):
    Type = conf.channel[prefix]["config"]
    motorA = conf.channel[prefix]["motorA"]
    motorB = conf.channel[prefix]["motorB"]
    motorC = conf.channel[prefix]["motorC"]
    signA = conf.channel[prefix]["signA"]
    signB = conf.channel[prefix]["signB"]
    signC = conf.channel[prefix]["signC"]
    
    posA = driver.getActualPosition(motorA)
    posB = driver.getActualPosition(motorB)
    posC = driver.getActualPosition(motorC)
    
    if Type == 'SR':
        driver.setTargetPosition(posA+int(np.sqrt(3)/2*signA*value),motorA)
        driver.setTargetPosition(posB-int(np.sqrt(3)/2*signB*value),motorB)
        
    if Type == 'BS':
        driver.setTargetPosition(posA+int(np.sqrt(3)/2*signA*value),motorA)
        driver.setTargetPosition(posB-int(np.sqrt(3)/2*signB*value),motorB)
        
    elif Type == 'TM':
        driver.setTargetPosition(posA+int(signA*value),motorA)
        driver.setTargetPosition(posB-int(1/2*signB*value),motorB)
        driver.setTargetPosition(posC-int(1/2*signC*value),motorC)


def Move_T(prefix,driver,value):
    Type = conf.channel[prefix]["config"]
    motorA = conf.channel[prefix]["motorA"]
    motorB = conf.channel[prefix]["motorB"]
    motorC = conf.channel[prefix]["motorC"]
    signA = conf.channel[prefix]["signA"]
    signB = conf.channel[prefix]["signB"]
    signC = conf.channel[prefix]["signC"]
    
    posA = driver.getActualPosition(motorA)
    posB = driver.getActualPosition(motorB)
    posC = driver.getActualPosition(motorC)
    
    if Type == 'SR':
        driver.setTargetPosition(posC-int(signC*value),motorC)
        driver.setTargetPosition(posB+int(1/2*signB*value),motorB)
        driver.setTargetPosition(posA+int(1/2*signA*value),motorA)
        
    if Type == 'BS':
        driver.setTargetPosition(posB+int(signB*value),motorB)
        driver.setTargetPosition(posC-int(1/2*signC*value),motorC)
        driver.setTargetPosition(posA-int(1/2*signA*value),motorA)
        
    elif Type == 'TM':
        driver.setTargetPosition(posB-int(np.sqrt(3)/2*signB*value),motorB)
        driver.setTargetPosition(posC+int(np.sqrt(3)/2*signC*value),motorC)
        
def Move_Y(prefix,driver,value):
    motorA = conf.channel[prefix]["motorA"]
    motorB = conf.channel[prefix]["motorB"]
    motorC = conf.channel[prefix]["motorC"]
    signA = conf.channel[prefix]["signA"]
    signB = conf.channel[prefix]["signB"]
    signC = conf.channel[prefix]["signC"]
    
    posA = driver.getActualPosition(motorA)
    posB = driver.getActualPosition(motorB)
    posC = driver.getActualPosition(motorC)
    
    driver.setTargetPosition(posA+int(signA*value),motorA)
    driver.setTargetPosition(posB+int(signB*value),motorB)
    driver.setTargetPosition(posC+int(signC*value),motorC)
    
    
