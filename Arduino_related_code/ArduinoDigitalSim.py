import datetime
import time

def openComPort(portname):
    ct = datetime.datetime.now().strftime("%M:%S.%f")
    print(f'COM port {portname} created.')

def DigitalHigh(pin):
    ct = datetime.datetime.now().strftime("%M:%S.%f")
    print(f"Arduino Digital channel {pin}, set to High. Time Stamp= {ct}")

def DigitalLow(pin):
    ct = datetime.datetime.now().strftime("%M:%S.%f")
    print(f"Arduino Digital channel {pin}, set to High. Time Stamp= {ct}")

def DigitalHighPulse(pin, width):
    ct = datetime.datetime.now().strftime("%M:%S.%f")
    #print(f"Arduino Digital channel {pin} set to high pulse. Width {width}, Time Stamp= {ct}")

def DigitalLowPulse(pin, width):
    ct = datetime.datetime.now().strftime("%M:%S.%f")
    print(f"Arduino Digital channel {pin} set to low pulse. Width {width}, Time Stamp= {ct}")
