#!/usr/bin/python
import Adafruit_DHT
import RPi.GPIO as GPIO
import sys
import signal
import time
from optparse import OptionParser

from azure.storage.table import TableService, Entity

from repo import Repo
from config import Config
from tempui import TempUI

cfg = Config()

# define CTRL+C signal handler
def signal_handler(signal, frame):
    print("CTRL + C - terminating")
    GPIO.cleanup()
    sys.exit(0)

# register CTRL+C signal handler
signal.signal(signal.SIGINT, signal_handler)

GPIO.setmode(GPIO.BCM)
GPIO.setup(cfg.Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# configure database
print ("Initializing database %s" % cfg.DbPath)
repo = Repo(cfg.DbPath)

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22

# connect to azure storage
if(cfg.Azure):
    print ("Initializing conneciton to azure storage account: %s" % cfg.Account)
    table_service = TableService(account_name=cfg.Account, account_key=cfg.Key)
    table_service.create_table('Log')
    # generate a random partition name
    azure_part = time.strftime("%Y%m%d%H%M%S")
    azure_key = 0

# parse command line args
parser = OptionParser()
parser.add_option("-d", "--daemon", dest="noUI", help="run in deamon mode without UI", action="store_true")
(options, args) = parser.parse_args()

if(not options.noUI):
    ui = TempUI() 
else:
    ui = None
    print "running in deamon mode"

try:
    time.sleep(1)

    msg = "Loading complete"

    # main application loop
    while(True):

        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, cfg.Pin)
        
        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if humidity is not None and temperature is not None:
            readingId = repo.AddReading(temperature, humidity)

            if(cfg.Azure and readingId > 0):
                try:
                    reading = repo.GetReadingById(readingId)
                    if(reading):
                        # post values to azure table
                        keyStr = "%05d" % azure_key 
                        reading.PartitionKey = azure_part
                        reading.RowKey = keyStr
                        azure_key+=1
                        table_service.insert_entity('Log', reading.__dict__)
                except:
                    msg += "Azure upload failed\n"

        else:
            msg += "Failed to get reading.\n"

        # refresh ncurses UI
        if(ui):
            ui.RenderUI(temperature, humidity, msg)
        elif(len(msg) > 0):
            print msg

        # reset message
        if(len(msg) > 0):
            msg = ""

        time.sleep(cfg.Interval)

finally:
    if(ui):
        ui.End()

