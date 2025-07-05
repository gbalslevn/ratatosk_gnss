import pynmea2
import io
import serial
from .antennaselector import getCorrectAntenna
from .azimuth import calculateAzimuth

# Maybe rewrite to class instead, avoid weird global variable inside method
# tracker = BalloonTracker(groundstation_lat=56.1692, groundstation_lon=10.1026)
# tracker.readUART('/dev/ttyUSB0', 115200)

GROUNDSTATION_LAT = 56.1692
GROUNDSTATION_LON = 10.1026
balloon_lat = 0
balloon_lon = 0
balloon_rotation = 0
balloon_tilt = 0
groundstation_direction = 0
correctAntenna = 1

# https://pyserial.readthedocs.io/en/latest/pyserial_api.html
# Constantly reads from serial
def readUART(serialPort, baud):
    global balloon_lat, balloon_lon, balloon_rotation, groundstation_direction, correctAntenna 
    ser = serial.Serial(serialPort, baud, timeout=1) # Read from serial every second
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    while 1:
        try:
            line = sio.readline()
            with open("nmea_log.txt", "a") as log:
                log.write(line)
            msg = pynmea2.parse(line)
            # print(repr(msg))
            if msg.sentence_type == "HDT" and msg.heading is not None:
                balloon_rotation = msg.heading
            if hasattr(msg, "latitude") and hasattr(msg, "longitude"):
                balloon_lat = msg.latitude
                balloon_lon = msg.longitude
            if hasattr(msg, "altitude"):
                altitude = msg.altitude
                
            groundstation_direction = calculateAzimuth(float(balloon_lat), float(balloon_lon), float(GROUNDSTATION_LAT), float(GROUNDSTATION_LON))
            correctAntenna = getCorrectAntenna(balloon_rotation, groundstation_direction)
            selectAntenna_test(correctAntenna)
        except serial.SerialException as e:
            print('Device error: {}'.format(e))
            ser.reset_input_buffer()
            ser.close()
            break
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
            continue

def selectAntenna(antenna):
    # Implement choosing the antenna
    return antenna

# Placeholder before implementation
def selectAntenna_test(antenna):
    print(f"Groundstation direction: {groundstation_direction}")
    print(f"Balloon rotation: {balloon_rotation}") 
    print(f"Balloon location: {balloon_lat} : {balloon_lon}")
    print(f"You should use antenna {antenna}")
readUART("/dev/ttyACM0", 115200)
