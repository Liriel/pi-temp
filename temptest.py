#!/usr/bin/python
import Adafruit_DHT
import RPi.GPIO as GPIO
import sys
import signal
from repo import Repo
import time
import curses

# Example using a Raspberry Pi with DHT sensor
# connected to GPIO4
pin = 4

# define CTRL+C signal handler
def signal_handler(signal, frame):
    print("CTRL + C - terminating")
    GPIO.cleanup()
    sys.exit(0)

# register CTRL+C signal handler
signal.signal(signal.SIGINT, signal_handler)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# configure database
dbPath = "readings.db"
print ("Initializing database %s" % dbPath)
repo = Repo(dbPath)

# measure intervall in seconds
intervall = 20

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22

try:
    # setup ncurses
    screen = curses.initscr()
    # turn off key echo
    curses.noecho()
    # enable instant keycode scanning
    curses.cbreak()
    # enable color
    curses.start_color()
    # define our color pairs
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
    # make getch non-blocking
    screen.nodelay(1)

    time.sleep(1)

    # main application loop
    while(True):
        # get current window size
        (maxY, maxX) = screen.getmaxyx()

        screen.addstr(2, (maxX / 2) - 15, "PI Temperature/Humidity Sensor", curses.A_UNDERLINE | curses.A_BOLD)
        screen.clrtoeol()

        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        
        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if humidity is not None and temperature is not None:
            repo.AddReading(temperature, humidity)

            xOffset = 2 
            screen.addstr(7, xOffset, "Temperature: {0:0.1f}*C".format(temperature))
            screen.clrtoeol()

            xOffset = maxX / 2 
            screen.vline(7, xOffset, curses.ACS_VLINE ,maxY)
            xOffset += 2
            #screen.addstr(7, xOffset, "Humidity:")
            screen.addstr(7, xOffset, "Humidity: {0:0.1f}*C".format(humidity))

        else:
            print('Failed to get reading. Try again!')


        screen.border(0)
        screen.refresh()

        time.sleep(intervall)

finally:
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()

