#!/usr/bin/python 

import pygame
import time

pygame.init()
pygame.joystick.init()

print pygame.joystick.get_count()

_joystick = pygame.joystick.Joystick(0)
_joystick.init()

print _joystick.get_init()
print _joystick.get_id()
print _joystick.get_name()
print _joystick.get_numaxes()
print _joystick.get_numballs()
print _joystick.get_numbuttons()
print _joystick.get_numhats()

time.sleep(5)

while (True):
	pygame.event.pump()
	print "=========================="
	for i in range(_joystick.get_numaxes()):
		print "Axis %g: %4.2f"%(i,_joystick.get_axis(i))
	for i in range(_joystick.get_numbuttons()):
		print "Button %g: %g"%(i,_joystick.get_button(i))

	time.sleep(0.25)