HT_ON=1
HT_OFF=0
control=HT_OFF
for i in {1..17..2}
do 
	sudo echo $control > /sys/devices/system/cpu/cpu$i/online
done
for i in {16..23}
do 
        sudo echo $control > /sys/devices/system/cpu/cpu$i/online
done

