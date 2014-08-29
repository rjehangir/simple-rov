#!/usr/bin/python 

import socket

UDP_IP = "127.0.0.1"
UDP_SEND_PORT = 5006
UDP_RECV_PORT = 5005

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_RECV_PORT))

import select

sock.setblocking(0)

import serial
import time

ser = serial.Serial('/dev/tty.usbmodemfd141',57600,timeout=0.05,writeTimeout=0)
time.sleep(1.0)
if ser.isOpen():
	print "Serial port opened."

import signal
import sys

def sigint_handler(*args):
	print "Closing serial port."
	ser.close()
	print "Quiting gracefully."
	time.sleep(0.25)
	sys.exit()

signal.signal(signal.SIGINT, sigint_handler)

from pprint import pprint

print "Bridging serial to UDP..."

while True:
	ready = select.select([sock], [], [], 0.5)
	data = []
	if ready[0]:
		data, addr = sock.recvfrom(1024)

	if data is not None:
		if len(data) > 0:
			#print "Send: ",
			#pprint(data)
			ser.write(data)

	data = ser.read(64)
	if data is not None:
		if len(data) > 0:
			#pprint(data)
			sock.sendto(data,(UDP_IP,UDP_SEND_PORT))