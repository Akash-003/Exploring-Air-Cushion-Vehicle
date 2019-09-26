#!/usr/bin/env python

from __future__ import division
import serial
import math
import os
import struct

with serial.Serial("/dev/ttyUSB0",
                    baudrate = 115200, 
                    parity=serial.PARITY_NONE,  
                    bytesize = serial.EIGHTBITS,
                    stopbits = serial.STOPBITS_ONE,
                    xonxoff = False,
                    rtscts = False,
                    dsrdtr = False) as sweep:

    print "Scanse Sweep open"
    sweep.write("ID\n")
    print "Query device information"
    resp = sweep.readline()
    print "Response: " + resp

    print "Starting scanning...",
    sweep.write("DS\n")
    resp = sweep.readline()
    assert (len(resp) == 6), "Bad data"

    status = resp[2:4]
    if  status == "00":
        print "OK"
    else:
        print "Failed %s" % status

        #-----------------------------------------------------------------------
        # Missing here is stopping the scanning - it will still be running next 
        # time code is initiated and it all gets very messy / confusong separating
        # binary data from ASCII command / response.  Really need to do a subset of
        # the finally: branch below.
        #-----------------------------------------------------------------------
        os.exit()

    log = open("sweep.csv", "wb")
    log.write("angle, distance, x, y\n")

    format = '=' + 'B' * 7

    try:
        while True:
            line = sweep.read(7)
            assert (len(line) == 7), "Bad data read: %d" % len(line)
            data = struct.unpack(format, line)
            assert (len(data) == 7), "Bad data type conversion: %d" % len(data)

            azimuth_lo = data[1]
            azimuth_hi = data[2]
            angle_int = (azimuth_hi << 8) + azimuth_lo
            degrees = (angle_int >> 4) + (angle_int & 15) / 16

            distance_lo = data[3]
            distance_hi = data[4]
            distance = ((distance_hi << 8) + distance_lo) / 100

            x = distance * math.cos(degrees * math.pi / 180)
            y = distance * math.sin(degrees * math.pi / 180)

            log.write("%f, %f, %f, %f\n" % (degrees, distance, x, y))

    #--------------------------------------------------------------------------
    # Catch Ctrl-C
    #--------------------------------------------------------------------------
    except KeyboardInterrupt as e:
        pass        

    #--------------------------------------------------------------------------
    # Catch incorrect assumption bugs
    #--------------------------------------------------------------------------
    except AssertionError as e:
        print e

    #--------------------------------------------------------------------------
    # Cleanup regardless otherwise the next run picks up data from this
    #--------------------------------------------------------------------------
    finally:
    	print "Stop scanning"
    	sweep.write("DX\n")
    	resp = sweep.read()
    	print "Response: %s" % resp
    	log.close()