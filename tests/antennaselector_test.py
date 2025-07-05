import random
import math
from tests.nmeaparser_test import createNMEAGGA
from main.antennaselector import getCorrectAntenna, getTilt, getAzimuth

balloon_location = {"lat": 56.169200, "lon" : 10.202600, "alt": 39000.000000}
groundstation_location = {"lat": balloon_location["lat"], "lon" : balloon_location["lon"]-0.1, "alt": balloon_location["alt"]} # West of the balloon
groundstation_NMEA = createNMEAGGA(groundstation_location["lat"], groundstation_location["lon"], 0.000000)
print(groundstation_NMEA)
def getRandomBalloonNMEA():
    point1 = getRandomLocationOffset(balloon_location)
    point2 = getRandomLocationOffset(balloon_location)
    NMEA_point1 = createNMEAGGA(point1["lat"], point1["lon"], point1["alt"])
    NMEA_point2 = createNMEAGGA(point2["lat"], point2["lon"], point2["alt"])
    return NMEA_point1, NMEA_point2

def getRandomLocationOffset(location):
    lat_randomness = random.randint(1, 50)/100000
    lon_randomness = random.randint(1, 50)/100000
    alt_randomness = random.randint(1, 10)/100000
    offsetLocation = {"lat": location["lat"] - lat_randomness, "lon": location["lon"] - lon_randomness, "alt": location["alt"] - alt_randomness}
    return offsetLocation

def draw_groundstation_compass(angle):
    angle = angle % 360  
    compass_radius = 5 
    canvas_size = compass_radius * 2 + 1 
    compass_grid = [[" " for _ in range(canvas_size)] for _ in range(canvas_size)]
    
    center = compass_radius

    compass_grid[center][center] = "GS"  
    compass_grid[0][center] = "N"   
    compass_grid[center][canvas_size-1] = "E"  
    compass_grid[canvas_size-1][center] = "S"  
    compass_grid[center][0] = "W" 

    # Compute position of the pointer
    radian_angle = math.radians(-angle + 90)  # Convert to radians (90° offset to align with standard compass)
    pointer_x = round(center + compass_radius * math.cos(radian_angle))
    pointer_y = round(center - compass_radius * math.sin(radian_angle))  # Inverted Y-axis for terminal display
    
    compass_grid[pointer_y][pointer_x] = "*"

    compass_string = "\n".join("".join(row) for row in compass_grid)
    print(compass_string)
    print(f"Direction to groundstation: {int(angle)}°")

def draw_balloon_compass(angle, tilt):
    angle = angle % 360 
    compass_radius = 5 
    canvas_size = compass_radius * 2 + 1 
    compass_grid = [[" " for _ in range(canvas_size)] for _ in range(canvas_size)]
    
    center = compass_radius 
    compass_grid[center][center] = "B"  # Center name

    # Define cardinal directions and their positions relative to the compass direction
    directions = ["1", "2", "3", "4"]
    for i, direction in enumerate(directions):
        dir_angle = angle + (i * 90)  # Rotate N, E, S, W accordingly
        rad = math.radians(-dir_angle + 90)  # Convert to radians (90° offset)
        x = round(center + compass_radius * math.cos(rad))
        y = round(center - compass_radius * math.sin(rad))
        compass_grid[y][x] = direction  # Place rotated direction

    # Pointer always at the front of the balloon
    rad_pointer = math.radians(-angle + 90)
    pointer_x = round(center + compass_radius * math.cos(rad_pointer))
    pointer_y = round(center - compass_radius * math.sin(rad_pointer))
    
    if compass_grid[pointer_y][pointer_x] == " ":
        compass_grid[pointer_y][pointer_x] = "*"

    compass_string = "\n".join("".join(row) for row in compass_grid)
    print(compass_string)
    print(f"Ballon rotated by: {int(angle)}°")
    print(f"Ballon tilt is: {float(tilt)}°")

def testAntennaChoice():
    # The groundstation is east of the balloon, the correct antenna will be chosen based on the rotation of the balloon. 
    # Antenna: 1 (north/front), 2 (east/right), 3 (south/back) and 4 (west/left), 
    groundstation_direction = 90
    
    ballon_rotation = 0
    print(getCorrectAntenna(ballon_rotation, groundstation_direction))
    assert getCorrectAntenna(ballon_rotation, groundstation_direction) == 2
    
    ballon_rotation = 90
    assert getCorrectAntenna(ballon_rotation, groundstation_direction) == 1
    
    ballon_rotation = 180
    assert getCorrectAntenna(ballon_rotation, groundstation_direction) == 4
    
    ballon_rotation = 270
    assert getCorrectAntenna(ballon_rotation, groundstation_direction) == 3
    
    ballon_rotation = 360
    assert getCorrectAntenna(ballon_rotation, groundstation_direction) == 2
    
    ballon_rotation = 316
    assert getCorrectAntenna(ballon_rotation, groundstation_direction) == 2
    
    print("Passed tests for choosing correct antenna")

testAntennaChoice()
# Get random values and calculate correct antenna
point1_NMEA, point2_NMEA = getRandomBalloonNMEA()
balloon_rotation = random.randrange(0, 360)
balloon_tilt = getTilt(point1_NMEA, point2_NMEA)
groundstation_direction = getAzimuth(point1_NMEA, groundstation_NMEA)
correctAntenna = getCorrectAntenna(balloon_rotation, groundstation_direction)

draw_groundstation_compass(groundstation_direction) 
draw_balloon_compass(balloon_rotation, balloon_tilt) 
print(f"You should use antenna {correctAntenna}")