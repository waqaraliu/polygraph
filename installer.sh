#!/bin/sh
# installer.sh will install the necessary packages to get the gifcam up and running with 
# basic functions

echo "insatalling packages"
# Install packages for streaming dependencies
PACKAGES="libevent-dev libjpeg8-dev libbsd-dev"
DEBPACKAGES=" build-essential libevent-dev libjpeg-dev libbsd-dev"
sudo apt update -y
sudo apt upgrade -y
mkdir /home/pi/src && cd /home/pi/src
echo $PWD
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo apt install $PACKAGES -y
sudo apt install $DEBPACKAGES -y
#if this opencv version does not work on Rpi then use below one
pip install opencv-python==4.2.0.34
#pip install opencv-contrib-python==4.1.0.25
#now install app
mkdir /home/pi/tempdir
cd /home/pi/tempdir
echo $PWD
git clone --depth=1 https://github.com/pikvm/ustreamer
cd ustreamer
make
#now clone from my Repo, make files and src files
cd /home/pi
echo $PWD
git clone --depth=1 https://github.com/waqaraliu/polygraph
cd polygraph
make
mv /home/pi/polygraph /home/pi/polygraf
sudo rm -rf /home/pi/polygraf/src/polygraf
#remove temp files
sudo rm -rf /home/pi/tempdir
echo "Done Updating"
echo "Starting Config File Edit"

## change config file to have more power on USB ports
CONFIG="/boot/config.txt"
# If a line containing "disable_splash" exists
if grep -Fq "disable_splash" $CONFIG
then
	# Replace the line
	echo "Modifying disable_splash"
	sed -i "/disable_splash/c\disable_splash=1" $CONFIG
else
	# Create the definition
	echo "disable_splash not defined. Creating definition"
	echo "disable_splash=1" >> $CONFIG
fi

# If a line containing "arm_freq" exists
if grep -Fq "arm_freq" $CONFIG
then
	# Replace the line
	echo "Modifying arm_freq"
	sed -i "/arm_freq/c\arm_freq=2000" $CONFIG
else
	# Create the definition
	echo "arm_freq not defined. Creating definition"
	echo "arm_freq=2000" >> $CONFIG
fi

# If a line containing "core_freq" exists
if grep -Fq "core_freq" $CONFIG
then
	# Replace the line
	echo "Modifying core_freq"
	sed -i "/core_freq/c\core_freq=550" $CONFIG
else
	# Create the definition
	echo "core_freq not defined. Creating definition"
	echo "core_freq=550" >> $CONFIG
fi

# If a line containing "over_voltage" exists
if grep -Fq "over_voltage" $CONFIG
then
	# Replace the line
	echo "Modifying over_voltage"
	sed -i "/over_voltage/c\over_voltage=6" $CONFIG
else
	# Create the definition
	echo "over_voltage not defined. Creating definition"
	echo "over_voltage=6" >> $CONFIG
fi

# If a line containing "enable_tvout" exists
if grep -Fq "enable_tvout" $CONFIG
then
	# Replace the line
	echo "Modifying enable_tvout"
	sed -i "/enable_tvout/c\enable_tvout" $CONFIG
else
	# Create the definition
	echo "enable_tvout not defined. Creating definition"
	echo "enable_tvout" >> $CONFIG
fi


echo "Install complete, exiting."
exit
#reboot
