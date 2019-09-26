def cmd_read_GPS():
    reading=getrmc()
    # determine the position of the value separating commas
    commas = [0,1,2,3,4,5,6,7,8,9,10,11]
    comnum = 0
    for i in range (0,len(reading)):
        if reading[i] == ",":
            commas[comnum] = i # save the position of the comma
            comnum += 1
    # Extract latitude
    if (reading[commas[3] + 1:commas[4]]) == "N":
        sign = 1
    else:
        sign = -1
 
    degrees = float(reading[commas[2]+1:commas[2]+3])
    minutes = float(reading[commas[2] + 3:commas[3]])/60
    latitude = sign*(degrees + minutes)
    # Extract Longitude
    if (reading[commas[5] + 1:commas[6]]) == "E":
        sign = 1
    else:
        sign = -1
 
    degrees = float(reading[commas[4]+1:commas[4]+3])
    minutes = float(reading[commas[4] + 3:commas[5]])/60
    longitude = sign*(degrees + minutes)
     
 
    return(str(latitude),",",str(longitude))