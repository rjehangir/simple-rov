#!/usr/bin/python 

import pygame
import time
import os
import sys

pygame.init()
pygame.joystick.init()

print pygame.joystick.get_count()

isJoystick = True
try:
	_joystick = pygame.joystick.Joystick(0)
except:
	isJoystick = False
	print("No joysticks attached.")

if isJoystick:
	_joystick.init()

	print _joystick.get_init()
	print _joystick.get_id()
	print _joystick.get_name()
	print _joystick.get_numaxes()
	print _joystick.get_numballs()
	print _joystick.get_numbuttons()
	print _joystick.get_numhats()

time.sleep(0)

import socket
import select

UDP_IP = "127.0.0.1"
UDP_SEND_PORT = 5005
UDP_RECV_PORT = 5006

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_RECV_PORT))
sock.setblocking(0)

import Queue

q = Queue.Queue(4096)

import signal

def sigint_handler(*args):
	print "Quiting gracefully."
	time.sleep(0.25)
	sys.exit()

signal.signal(signal.SIGINT, sigint_handler)

from transfer import decodeTransfer, encodeTransfer

incomingFormatString = 'hhhhhhhh'
outgoingFormatString = 'hhhhhh'

commandTimer = time.time()

while (True):
	if isJoystick:
		pygame.event.pump()
		# print "=========================="
		# for i in range(_joystick.get_numaxes()):
		# 	print "Axis %g: %4.2f"%(i,_joystick.get_axis(i))
		# for i in range(_joystick.get_numbuttons()):
		# 	print "Button %g: %g"%(i,_joystick.get_button(i))

		# Process joystick axes
		pilotRoll          = 0;
		pilotPitch         = _joystick.get_axis(3)*-1*200;
		pilotYaw           = _joystick.get_axis(2)*200;
		pilotForward       = _joystick.get_axis(1)*-1*300;
		pilotStrafe        = _joystick.get_axis(0)*200;
		pilotVertical      = (_joystick.get_axis(5)+1)/2*300-(_joystick.get_axis(4)+1)/2*300;
	else:
		pilotRoll          = 0;
		pilotPitch         = 0;
		pilotYaw           = 0;
		pilotForward       = 0;
		pilotStrafe        = 0;
		pilotVertical      = 0;

	ready = select.select([sock], [], [], 0.025)
	data = []
	if ready[0]:
		data, addr = sock.recvfrom(1024)
		from pprint import pprint
		pprint(data)
		for i in range(len(data)):
			q.put(data[i])

	values = decodeTransfer(q,incomingFormatString)

	if values is not None:
		os.system('clear')
		for i in range(6):
			print "Thruster %g: %g"%(i,values[i])
		print "Volts: ",values[6]/1000.0
		print "Amps: ",values[7]/1000.0

	toSend = encodeTransfer(outgoingFormatString,(pilotRoll,pilotPitch,pilotYaw,pilotForward,pilotStrafe,pilotVertical))


	if (time.time()-commandTimer > 0.1):
		commandTimer = time.time()
		sock.sendto(toSend,(UDP_IP,UDP_SEND_PORT))


