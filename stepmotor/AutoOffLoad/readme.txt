The script is written by A.Shoda June. 2018

**** CONCEPT ****

The script is to offload the DC control offset of the GAS filters and IPs using the stepping motors automatically.
This can be used either the stage is controlled or not.

If the absolute of the averaged control output is more than 2000 counts (during the control is on), or the difference between the target position and the current position is more than 200 counts (when the control is off), it actuate the stepping motor by 20000 steps.



**** USAGE ****

* Before use, please check if the stepping motor epics is availabel.
(It can be checked easily by activating 'K1:STEPPER-*stage*_*channel*_UPDATE')

If the stepping motor epics is not properly working,
- Turn on the driver power from the BO control.
- login k1script by ssh
- check whether the epics script is already running or not. if it is, kill it.
- step_start DRIVER_NAME
See KAGRA wiki page for more details: http://gwwiki.icrr.u-tokyo.ac.jp/JGWwiki/KAGRA/Subgroups/DGS/Projects/StepperMotor

* From the command line,
type
> python AutoOffload.py OPTIC_(GAS/IP)
ex.)
> python AutoOffload.py PR3_GAS

* From the medm,
sitemap -> STEPPING MOTOR -> AUTO OFFLOAD
(in preparation)

* the BO switch is turned off after the auto-offload is finished.
The EPICS script will not be killed. And it can be used after you turn on the BO switch again.

* You can see the log what this script have done via optic.log in (userapps)/cds/common/script/epics-motor-control/stepmotor/AutoOffLoad.
Also, important messages will apprear in the commish messages in each suspension.

* If you find any bugs, please let Shoda knows.
ayaka.shoda@nao.ac.jp
