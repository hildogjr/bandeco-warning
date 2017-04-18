#!/bin/bash
# Auxiliary script to execute bandecoWarnin.py on Ubuntu. Used also to configure the cron jobs.
# Written by Hildo Guillardi Júnior - FEEC - UNICAMP - 13/Apr/2017

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

case $1 in
	--install|-i|--config|-c)
		# Configure the crontab to execute the warning automatic.
		modifycronjob(){ ( crontab -l -u $USER 2>/dev/null | grep -v -F "$2" ; echo "$1 $2" ) | crontab  -u $USER -;}
		modifycronjob "0 11,17 * * 1-5" "bash '$DIR/bandecoWarning.sh'" # Lunch & dinner warning
		#PATH=/home/anmol/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
		;;
		
	--uninstall|-u|--remove|-r)
		# Remove tfrom the crontab.
		removecronjob(){ ( crontab -l -u $USER 2>/dev/null | grep -v -F "$1" ) | crontab  -u $USER -;}
		removecronjob "bash '$DIR/bandecoWarning'"
		;;
		
	--direct|-d)
		# Configure the crontab to execute the warning automatic, but calling the python script directly.
		modifycronjob(){ ( crontab -l -u $USER 2>/dev/null | grep -v -F "$2" ; echo "$1 $2" ) | crontab  -u $USER -;}
		modifycronjob "15 11,17 * * 1-5" 'eval "export $(egrep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ)";'" DISPLAY=:0; python '$DIR/bandecoWarning.py'" # Lunch & dinner warning
		;;
		
	*)
		# Just call the python function.
	#	DBUS_SESSION_BUS_ADDRESS=unix:abstract=/tmp/dbus-PwezoBTpF3
	#	export DBUS_SESSION_BUS_ADDRESS
	#	XAUTHORITY=/home/$USER/.Xauthority
	#	export XAUTHORITY
		eval "export $(egrep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ)"
		DISPLAY=:0
#		export DISPLAY
		python "$DIR/bandecoWarning.py"
esac

exit 0
