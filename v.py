
import os
import pygame
import sys
import time


pygame.init()
pygame.joystick.init()

print(pygame.joystick.get_count())

_joystick = pygame.joystick.Joystick(0)
_joystick.init()
print (_joystick.get_init())
print (_joystick.get_id())
print (_joystick.get_name())
print (_joystick.get_numaxes())
print (_joystick.get_numballs())
print (_joystick.get_numbuttons())
print (_joystick.get_numhats())
print (_joystick.get_axis(0))


def main():
    done = False
    numbuttonsCount = _joystick.get_numbuttons()
    print(numbuttonsCount)
    while 1:
        pygame.event.get()

        buttonstate = _joystick.get_button(1) or _joystick.get_button(0)





  #print (pygame.joystick.Joystick(0).get_button(0))
       #print (pygame.joystick.Joystick(0).get_button(1))


if __name__ == "__main__":
    main()
