def getrmc():
 
    serial = wp.serialOpen("/dev/ttyAMA0",57600) # open serial port 
 
    wp.serialFlush(serial)
    print(serial)
    while True: # repeat until we get a RMC NMEA string
        gpsstring = ""
        while True: # repeat until we have a complete string
            if (wp.serialDataAvail(serial) > 0):
        letter = wp.serialGetchar(serial)
                if letter == 10:
                    break
            else:
                    gpsstring += str(chr(letter))
        if (gpsstring[3:6]=="RMC"):
           break
    wp.serialClose(serial)
    return(gpsstring)