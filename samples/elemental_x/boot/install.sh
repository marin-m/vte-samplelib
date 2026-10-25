#!/sbin/sh

/tmp/busybox fstrim /data

SLOT=$(for i in `cat /proc/cmdline`; do echo $i | grep slot | dd bs=1 skip=24 2>/dev/null; done)
BOOTPATH="/dev/block/bootdevice/by-name/boot$SLOT"

/tmp/busybox dd if=$BOOTPATH of=/tmp/boot.img
/tmp/unpackbootimg -i /tmp/boot.img -o /tmp/

CPU0=$(cat /tmp/aroma/cpu0.prop | cut -d '=' -f2)
case $CPU0 in
	1)
	  cpu_max_c1="cpu_max_c1=1593600"
	  ;;
	2)
	  cpu_max_c1="cpu_max_c1=1516800"
	  ;;
	3)
	  cpu_max_c1="cpu_max_c1=1440000"
	  ;;
	4)
	  cpu_max_c1="cpu_max_c1=1363200"
	  ;;
	5)
	  cpu_max_c1="cpu_max_c1=1286400"
	  ;;
esac

CPU2=$(cat /tmp/aroma/cpu2.prop | cut -d '=' -f2)
case $CPU2 in
	1)
	  cpu_max_c2="cpu_max_c2=2342400"
	  ;;
	2)
	  cpu_max_c2="cpu_max_c2=2246400"
	  ;;
	3)
	  cpu_max_c2="cpu_max_c2=2150400"
	  ;;
	4)
	  cpu_max_c2="cpu_max_c2=2054400"
	  ;;
	5)
	  cpu_max_c2="cpu_max_c2=1900800"
	  ;;
  	6)
	  cpu_max_c2="cpu_max_c2=1747200"
	  ;;
  	7)
	  cpu_max_c2="cpu_max_c2=1593600"
	  ;;
esac
COMPANDER=`grep "item.0.4" /tmp/aroma/mods.prop | cut -d '=' -f2`
  case $COMPANDER in
	0)
	  compander="compander=1"
	  ;;
	1)
	  compander="compander=0"
	  ;;	
  esac

if  grep cpu_max_c1 /tmp/boot.img-cmdline; then
	sed -i "s/cpu_max_c1.*/$cpu_max_c1 $cpu_max_c2 $compander/" /tmp/boot.img-cmdline
else
	echo -n $cpu_max_c1 $cpu_max_c2 $compander >> /tmp/boot.img-cmdline
fi

AUDIO=`grep "item.0.3" /tmp/aroma/mods.prop | cut -d '=' -f2`
if [ $AUDIO = 1 ]; then
	if  ! grep "snd-soc-wcd9335.dig_core_collapse_enable=0" /tmp/boot.img-cmdline; then
		echo -n " snd-soc-wcd9335.dig_core_collapse_enable=0 " >> /tmp/boot.img-cmdline
	fi
else
	if  grep "snd-soc-wcd9335.dig_core_collapse_enable=0" /tmp/boot.img-cmdline; then
		sed -i "s/snd-soc-wcd9335.dig_core_collapse_enable=0//" /tmp/boot.img-cmdline
	fi
fi

mkdir /tmp/ramdisk
cp /tmp/boot.img-ramdisk.gz /tmp/ramdisk/
cd /tmp/ramdisk/
/tmp/busybox gunzip -c /tmp/ramdisk/boot.img-ramdisk.gz | /tmp/busybox cpio -i
rm /tmp/ramdisk/boot.img-ramdisk.gz
#rm /tmp/boot.img-ramdisk.gz

#Create config
/tmp/buildconfig.sh

if [ -d /tmp/ramdisk/.subackup -o -d /tmp/ramdisk/.backup ]; then

	#Override skip_initramfs
	if ! grep -q skip_override /tmp/boot.img-cmdline; then
		echo -n " skip_override" >> /tmp/boot.img-cmdline
	fi

	#Start elementalx script
#	if [ $(grep -c "import /init.elementalx.rc" /tmp/ramdisk/boot/init.rc) == 0 ]; then
#	   sed -i "/import \/init\.environ\.rc/aimport /init.elementalx.rc" /tmp/ramdisk/boot/init.rc
#	fi

	#Copy elementalx scripts
#	cp /tmp/init.elementalx.rc /tmp/ramdisk/boot/init.elementalx.rc
#	chmod 0750 /tmp/ramdisk/boot/init.elementalx.rc

else
	#remove skip_override
	if grep -q skip_override /tmp/boot.img-cmdline; then
		sed -i "s/skip_override//" /tmp/boot.img-cmdline
	fi

fi

#/tmp/busybox find . | /tmp/busybox cpio -o -H newc | /tmp/busybox gzip > /tmp/boot.img-ramdisk.gz
#rm -r /tmp/ramdisk

echo \#!/sbin/sh > /tmp/createnewboot.sh
echo /tmp/mkbootimg --kernel /tmp/elex.Image --ramdisk /tmp/boot.img-ramdisk.gz --cmdline \"$(cat /tmp/boot.img-cmdline)\" --base 0x80000000 --kernel_offset 0x00008000 --pagesize 4096 --ramdisk_offset 0x01000000 --tags_offset 0x00000100 --output /tmp/newboot.img >> /tmp/createnewboot.sh
chmod 777 /tmp/createnewboot.sh
/tmp/createnewboot.sh

/tmp/busybox dd if=/tmp/newboot.img of=$BOOTPATH

