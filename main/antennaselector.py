import pynmea2
from main.azimuth import calculateAzimuth
from main.tilt import calculateTilt

# Get azimuth based on two nmea points
def getAzimuth(point1_NMEA, point2_NMEA): 
    point1 = pynmea2.parse(point1_NMEA)   
    point2 = pynmea2.parse(point2_NMEA) 
    azimuth = calculateAzimuth(float(point1.lat), float(point1.lon), float(point2.lat), float(point2.lon))
    return azimuth

# Get tilt based on two nmea points
def getTilt(point1_NMEA, point2_NMEA):
    point1 = pynmea2.parse(point1_NMEA)   
    point2 = pynmea2.parse(point2_NMEA) 
    tilt = calculateTilt(float(point1.lat), float(point1.lon), float(point1.altitude), float(point2.lat), float(point2.lon), float(point2.altitude))
    return tilt

def getAntennaDirection(antenna_1_direction, antenna_number):
    return (antenna_1_direction + 90 * (antenna_number - 1)) % 360
    
# Finds correct antenna. Balloon rotation is the direction which patch antenna A1 points to. The locations of the other antennas are calculated based on that. 
def getCorrectAntenna(balloon_rotation, groundstation_direction):
    closest = 360
    antenna1 = {"number": 1, "degree": balloon_rotation}
    antenna2 = {"number": 2 , "degree": getAntennaDirection(balloon_rotation, 2)}
    antenna3 = {"number": 3, "degree": getAntennaDirection(balloon_rotation, 3)}
    antenna4 = {"number": 4, "degree": getAntennaDirection(balloon_rotation, 4)}
    antennas = [antenna1, antenna2, antenna3, antenna3, antenna4]
    correctAntenna = antenna1["number"]
    for antenna in antennas:
        if(abs(antenna["degree"] - groundstation_direction) <= closest): # = as, if same distance, choose new antenna
            correctAntenna = antenna["number"]
            closest = abs(antenna["degree"] - groundstation_direction)
    return correctAntenna
