#!/bin/bash
# Auxiliary script to execute bandecoWarnin.py on Ubuntu. Used also to configure the cron jobs.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

case $1 in
	--install|-i|--config|-c)
		addcronjob(){ ( crontab -l -u $USER 2>/dev/null | grep -v -F "$2" ; echo "$1 $2" ) | crontab  -u $USER -;}
		#addcronjob "0 11,17 * * 1-5" "bash '$DIR/bandecoWarning.sh'" # Lunch & dinner warning
		addcronjob "* * * * *" "bash '$DIR/bandecoWarning.sh'"
		#PATH=/home/anmol/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
		;;
	--uninstall|-u|--remove|-r)
		removecronjob(){ ( crontab -l -u $USER 2>/dev/null | grep -v -F "$1" ) | crontab  -u $USER -;}
		removecronjob "bash '$DIR/bandecoWarning.sh'"
		;;
	*)
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
