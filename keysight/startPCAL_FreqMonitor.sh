#!/bin/bash
#******************************************#
#     File Name: startPCAS_FreqMonitor.sh
#        Author: Masayuki Nakano
# Last Modified: 2019/08/01 17:18:01
#******************************************#


ARM=$1
DEMON=$2
pythonpath=/opt/apps/linux-x86_64/camera/lib::/kagra/apps//pyepics/lib/python/:/kagra/apps//cdsutils/lib/python2.7/site-packages/:/kagra/apps//pcaspy/lib/python2.7/site-packages/:/kagra/apps/guardian/lib/python2.7/site-packages:/kagra/apps/cdsutils/lib/python2.7/site-packages/ezca/:/kagra/apps/pyepics/lib/python/pyepics-3.2.4-py2.7.egg/:/kagra/apps/camera/lib:/usr/lib/x86_64-linux-gnu/root5.34/python/genreflex/

export SSH_ASKPASS=/usr/lib/seahorse/seahorse-ssh-askpass
if [ "${DEMON}" != "PCAS" ]; then
    setsid ssh -o NumberOfPasswordPrompts=1 k1script "source /kagra/apps/etc/client-user-env.sh && python /opt/rtcds/userapps/release/cds/common/scripts/epics-motor-control/keysight/freqmonitor_${ARM^}PLL.py" || zenity --error --text "login error"

else
    setsid ssh -o NumberOfPasswordPrompts=1  k1script "source /kagra/apps/etc/client-user-env.sh && /opt/rtcds/userapps/release/cds/common/scripts/epics-motor-control/keysight/pcas_${ARM,}pll.py" || zenity --error --text "login error"
fi

