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