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

def getClosestCardinal(degree):
    closest = 360
    correctCardinal = 0
    cardinals = [0, 90, 180, 270, 360]
    for cardinal in cardinals:
        if abs(cardinal - degree) < closest:
            closest = abs(cardinal - degree)
            correctCardinal = cardinal
    cardinalMap = {0: "N", 90: "E", 180: "S", 270: "W", 360: "N"}
    return cardinalMap.get(correctCardinal)

def mapCardinalToAntenna(cardinal):
    antennaMap = {"N": 1, "E": 2, "S": 3, "W": 4}
    return antennaMap.get(cardinal)
    
def getCorrectAntenna(balloon_rotation, groundstation_direction, draw=True):
    # We need to place the 4 patch antennas A1, A2, A3, A4 such that A1 corrosponds to north/(front), A2 to east/(right) and so on.
    corrected_direction = (groundstation_direction - balloon_rotation) % 360 # Correcting for the balloon rotation
    closestCardinal = getClosestCardinal(corrected_direction)
    correctAntenna = mapCardinalToAntenna(closestCardinal)
    return correctAntenna
