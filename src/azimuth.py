import math

# Get azimuth in degrees from north (0=north, 90=east, 180=south, 270=east)
def calculateAzimuth(lat1, lon1, lat2, lon2):    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    delta_lon = lon2 - lon1
    
    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    
    azimuth = math.atan2(x, y)
    azimuth = math.degrees(azimuth)
    
    return (azimuth + 360) % 360  # Ensure azimuth is not negative, convert to 0-360 degrees

# Coordinates lat1, lon1 is the current location and lat2, lon2 is the location pointed to
# lat1, lon1 = 56.160052, 10.204373 
# lat2, lon2 = 56.159995, 10.204405 
# azimuth = get_azimuth(lat1, lon1, lat2, lon2)
# print(f"Azimuth is: {azimuth:.2f} degrees")