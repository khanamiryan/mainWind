import RPi.GPIO as GPIO
import time
import threading

class Led(object):

    LED_OFF = 0
    LED_ON = 1
    LED_FLASHING = 2

    # the short time sleep to use when the led is on or off to ensure the led responds quickly to changes to blinking
    FAST_CYCLE = 0.05

    def __init__(self, led_pin):
        # create the semaphore used to make thread exit
        self.pin_stop = threading.Event()
        # the pin for the LED
        self.__led_pin = led_pin
        # initialise the pin and turn the led off
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__led_pin, GPIO.OUT)
        # the mode for the led - off/on/flashing
        self.__ledmode = Led.LED_OFF
        # make sure the LED is off (this also initialises the times for the thread)
        self.off()
        # create the thread, keep a reference to it for when we need to exit
        self.__thread = threading.Thread(name='ledblink',target=self.__led_pin) 
        # start the thread
        self.__thread.start()

    def blink(self, time_on=0.050, time_off=1):
        # blinking will start at the next first period
        # because turning the led on now might look funny because we don't know
        # when the next first period will start - the blink routine does all the
        # timing so that will 'just work'
        self.__ledmode = Led.LED_FLASHING
        self.__time_on = time_on
        self.__time_off = time_off

    def off(self):
        self.__ledmode = self.LED_OFF
        # set the cycle times short so changes to ledmode are picked up quickly
        self.__time_on = Led.FAST_CYCLE
        self.__time_off = Led.FAST_CYCLE
        # could turn the LED off immediately, might make for a short flicker on if was blinking

    def on(self):
        self.__ledmode = self.LED_ON
        # set the cycle times short so changes to ledmode are picked up quickly
        self.__time_on = Led.FAST_CYCLE
        self.__time_off = Led.FAST_CYCLE
        # could turn the LED on immediately, might make for a short flicker off if was blinking

    def reset(self):
        # set the semaphore so the thread will exit after sleep has completed
        self.pin_stop.set()
        # wait for the thread to exit
        self.__thread.join()
        # now clean up the GPIO
        GPIO.cleanup()