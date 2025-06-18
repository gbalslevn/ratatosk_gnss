import pynmea2
import io
import serial
from datetime import datetime

# https://github.com/Knio/pynmea2

def parseNMEA(data):
    msg = pynmea2.parse(data)
    return msg

def readFile(path):
    file = open(path, "r")

    for line in file.readlines():
        try:
            msg = pynmea2.parse(line)
            print(repr(msg))
            if hasattr(msg, "latitude") and hasattr(msg, "longitude"):
                print(f"NMEA {msg.sentence_type} DATA")
                print(f'Lat: {msg.latitude}, Long: {msg.longitude}')
            if hasattr(msg, "altitude"):
                print(f'Alt: {msg.altitude}')
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
            continue

def readUART(serialPort, baud):
    ser = serial.Serial(serialPort, baud, timeout=5.0)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    while 1:
        try:
            line = sio.readline()
            msg = pynmea2.parse(line)
            print(repr(msg))
        except serial.SerialException as e:
            print('Device error: {}'.format(e))
            break
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
            continue

def createNMEAGGA(lat, lon, alt):   
    lat_dir = 'N' if lat >= 0 else 'S'
    lon_dir = 'E' if lon >= 0 else 'W'
    
    date_time = datetime.now().strftime("%H%M%S")
    
    # Create a GGA sentence
    # https://github.com/Knio/pynmea2/blob/master/pynmea2/types/talker.py
    # fields = (
    #     ('Timestamp', 'timestamp', timestamp),
    #     ('Latitude', 'lat'),
    #     ('Latitude Direction', 'lat_dir'),
    #     ('Longitude', 'lon'),
    #     ('Longitude Direction', 'lon_dir'),
    #     ('GPS Quality Indicator', 'gps_qual', int),
    #     ('Number of Satellites in use', 'num_sats'),
    #     ('Horizontal Dilution of Precision', 'horizontal_dil'),
    #     ('Antenna Alt above sea level (mean)', 'altitude', float),
    #     ('Units of altitude (meters)', 'altitude_units'),
    #     ('Geoidal Separation', 'geo_sep'),
    #     ('Units of Geoidal Separation (meters)', 'geo_sep_units'),
    #     ('Age of Differential GPS Data (secs)', 'age_gps_data'),
    #     ('Differential Reference Station ID', 'ref_station_id'),
    # )
    gga = pynmea2.GGA(
        'GP', 'GGA', (date_time , str(lat), lat_dir,  str(lon), lon_dir, "1", "10", "1.0", str(alt), "M", "", "M", "",  "")   
    )
    return str(gga)
    
# msg = createNMEAGGA(123, 123, 0)
# print(msg)
# msg = parseNMEA(msg)
# # print(repr(msg))
# assert msg.lat == "123"
# assert msg.lon == "123"
# readFile("NMEA_data/nmea.txt")
# readUART("dev/ttyUSB0", 115200)
