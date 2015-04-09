#!/bin/bash
export PATH=/opt/TurboVNC/bin/:$PATH
/opt/TurboVNC/bin/vncserver -noauth -noxstartup 2>vnc.log
DISPLAY=`cat vnc.log | grep New | grep desktop | awk '{print $5}'`
HOST=${DISPLAY%:*}
echo $DISPLAY > vncid
export DISPLAY=$DISPLAY
gnome-wm &
#xclock 

vglclient -force &

sleep 1

#
#vglrun -d $DISPLAY /usr/local/bin/${PAS_JOB_TYPE}

# if [ ${PAS_JOB_TYPE} == "hw" ] 
# then 
# 	wish ./runtime/openHW
# fi

# if [ ${PAS_JOB_TYPE} == "hm" ] 
# then 
# 	wish ./runtime/openHM
# fi

rdesktop 192.168.40.159 -u pbsadmin -p 1qaz2wsx -f 









