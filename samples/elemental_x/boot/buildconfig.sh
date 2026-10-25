#!/sbin/sh

#Build config file
CONFIGFILE="/tmp/init.elementalx.rc"
BACKUP="/sdcard/.elementalx.backup"

if [ -d /tmp/ramdisk/boot ]; then

	echo "on boot" >> $CONFIGFILE
	echo "" >> $CONFIGFILE

	#fsync
	FSYNC=`grep "item.0.1" /tmp/aroma/mods.prop | cut -d '=' -f2`
	if [ $FSYNC = 1 ]; then
	  echo "write /sys/module/sync/parameters/fsync_enabled 0" >> $CONFIGFILE
	  echo "" >> $CONFIGFILE
	fi

	#backlight dimmer
	BLDIM=`grep "item.0.2" /tmp/aroma/mods.prop | cut -d '=' -f2`
	if [ $BLDIM = 1 ]; then
	  echo "write /sys/module/mdss_fb/parameters/backlight_dimmer 1" >> $CONFIGFILE
	else
	  echo "write /sys/module/mdss_fb/parameters/backlight_dimmer 0" >> $CONFIGFILE
	fi
	echo "" >> $CONFIGFILE

	#S2W
	SR=`grep "item.1.1" /tmp/aroma/gest.prop | cut -d '=' -f2`
	SL=`grep "item.1.2" /tmp/aroma/gest.prop | cut -d '=' -f2`
	SU=`grep "item.1.3" /tmp/aroma/gest.prop | cut -d '=' -f2`
	SD=`grep "item.1.4" /tmp/aroma/gest.prop | cut -d '=' -f2`

	if [ $SL = 1 ]; then
	  SL=2
	fi
	if [ $SU == 1 ]; then
	  SU=4
	fi
	if [ $SD == 1 ]; then
	  SD=8
	fi  

	S2W=$(( SL + SR + SU + SD ))
	echo "write /sys/android_touch/sweep2wake " $S2W >> $CONFIGFILE

	#DT2W
	DT2W=`grep "item.1.5" /tmp/aroma/gest.prop | cut -d '=' -f2`
	echo "write /sys/android_touch/doubletap2wake " $DT2W >> $CONFIGFILE

	#S2S
	S2S=`grep selected.0 /tmp/aroma/s2s.prop | cut -d '=' -f2`
	if [ $S2S = 2 ]; then
	  echo "write /sys/android_touch/sweep2sleep 1" >> $CONFIGFILE
	elif [ $S2S = 3 ]; then
	  echo "write /sys/android_touch/sweep2sleep 2" >> $CONFIGFILE
	elif [ $S2S = 4 ]; then
	  echo "write /sys/android_touch/sweep2sleep 3" >> $CONFIGFILE
	else
	  echo "write /sys/android_touch/sweep2sleep 0" >> $CONFIGFILE
	fi

	#WG vibration strength
	VIBSTRENGTH=`grep "item.2.1" /tmp/aroma/gest.prop | cut -d '=' -f2`
	if [ $VIBSTRENGTH = 0 ]; then
	  echo "write /sys/android_touch/vib_strength 0" >> $CONFIGFILE
	fi
	echo "" >> $CONFIGFILE

	echo "on property:sys.boot_completed=1" >> $CONFIGFILE
	echo "" >> $CONFIGFILE

	#i/o scheduler
	SCHED=`grep selected.1 /tmp/aroma/disk.prop | cut -d '=' -f2`
	if [ $SCHED = 1 ]; then
	  echo "write /sys/block/sda/queue/scheduler cfq"  >> $CONFIGFILE
	elif [ $SCHED = 2 ]; then
	  echo "write /sys/block/sda/queue/scheduler deadline"  >> $CONFIGFILE
	elif [ $SCHED = 3 ]; then
	  echo "write /sys/block/sda/queue/scheduler fiops"  >> $CONFIGFILE
	elif [ $SCHED = 4 ]; then
	  echo "write /sys/block/sda/queue/scheduler sio"  >> $CONFIGFILE
	elif [ $SCHED = 5 ]; then
	  echo "write /sys/block/sda/queue/scheduler bfq"  >> $CONFIGFILE
	elif [ $SCHED = 6 ]; then
	  echo "write /sys/block/sda/queue/scheduler noop"  >> $CONFIGFILE
	elif [ $SCHED = 7 ]; then
	  echo "write /sys/block/sda/queue/scheduler zen"  >> $CONFIGFILE
	fi

	#Readahead buffer size
	READAHEAD=`grep selected.2 /tmp/aroma/disk.prop | cut -d '=' -f2`
	if [ $READAHEAD = 1 ]; then
	  echo "write /sys/block/sda/queue/read_ahead_kb 128" >> $CONFIGFILE
	elif [ $READAHEAD = 2 ]; then
	  echo "write /sys/block/sda/queue/read_ahead_kb 256" >> $CONFIGFILE
	elif [ $READAHEAD = 3 ]; then
	  echo "write /sys/block/sda/queue/read_ahead_kb 512" >> $CONFIGFILE
	elif [ $READAHEAD = 4 ]; then
	  echo "write /sys/block/sda/queue/read_ahead_kb 1024" >> $CONFIGFILE
	fi
	echo "" >> $CONFIGFILE

fi

#reinstall options
echo -e "##### Reinstall Options #####" > $BACKUP
echo -e "# These settings are only applied if you run the express installer" >> $BACKUP

#Maximum CPU freqs
CPU0=$(cat /tmp/aroma/cpu0.prop | cut -d '=' -f2)

echo -e "\n\n##### Max Little Cluster Frequency #####" >> $BACKUP
echo -e "# 1=1593MHz 2=1516MHz" >> $BACKUP
echo -e "# 3=1440MHz 4=1363MHz" >> $BACKUP
echo -e "# 5=1286MHz\n" >> $BACKUP

echo "CPU0=$CPU0" >> $BACKUP;

CPU4=$(cat /tmp/aroma/cpu2.prop | cut -d '=' -f2)

echo -e "\n\n##### Max Big Cluster Frequency #####" >> $BACKUP
echo -e "# 1=2342MHz 2=2246MHz" >> $BACKUP
echo -e "# 3=2150MHz 4=2054MHz" >> $BACKUP
echo -e "# 5=1900MHz 6=1747MHz" >> $BACKUP
echo -e "# 7=1593MHz" >> $BACKUP

echo "CPU2=$CPU4" >> $BACKUP;

AUDIO=`grep "item.0.3" /tmp/aroma/mods.prop | cut -d '=' -f2`
echo -e "\n\n##### Disable audio codec power gating #####" >> $BACKUP
echo -e "# 1=disable 0=enable (default)" >> $BACKUP
echo "AUDIO_MOD=$AUDIO" >> $BACKUP;

COMPANDER=`grep "item.0.4" /tmp/aroma/mods.prop | cut -d '=' -f2`
echo -e "\n\n##### Compander enable (for analog headphone gain control) #####" >> $BACKUP
if [ $COMPANDER = 1 ]; then
  echo "COMPANDER=0" >> $BACKUP
else
  echo "COMPANDER=1" >> $BACKUP
fi

