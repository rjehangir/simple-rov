BlueROV
=======

This project contains the embedded and topside code for the BlueROV. The BlueROV has the following hardware:

* APM2.6 Autopilot from 3D Robotics
* Raspberry Pi with RasPiCam
* BlueRobotics T100 thrusters

## Dependencies

This project currently requires:

* MPlayer
* PyGame

## Control Interface

```bash
python gcs.py
```

## Video Streaming from Raspberry Pi

Raspberry Pi:

```bash
raspivid -hf -w 640 -h 480 -t 999999999 -fps 20 -b 5000000 -o - | nc -l -p 4444
```

Client / Control Station:

```bash
nc 192.168.1.9 4444 | mplayer -fps 30 -demuxer h264es -
```

## ROS VM Setup for Compilation

```bash
sudo easy_install ino
sudo apt-get install arduino arduino-core

sudo apt-get install ros-indigo-rosserial-arduino
sudo apt-get install ros-indigo-rosserial

cd BlueROV/lib
rosrun rosserial_arduino make_libraries.py .
```

## Compilation on ROS VM

```bash
ino build
ino build
ino upload
```

## Firmware Flashing to APM

```bash
ino upload
```

OR

```bash
sudo avrdude -c stk500v2 -b 115200 -P /dev/ttyACM0 -p atmega2560 -U flash:w:.build/mega2560-XXXXXX/firmware.hex:i
```
