import math

# Calculate distance (on a sphere) between two points
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    earthRadius = 6371 * 1000 
    return earthRadius * c

# Calculate distance, flat earth approach, can be assumed for small distances. 
def euclidean_distance(lat1, lon1, lat2, lon2):
    distance_sqaured = (lat2 - lat1) ** 2 + (lon2 - lon1) ** 2   
    distance = math.sqrt(distance_sqaured)
    return distance

def calculateTilt(lat1, lon1, alt1, lat2, lon2, alt2):
    horizontal_distance = euclidean_distance(lat1, lon1, lat2, lon2)
    delta_z = alt2 - alt1

    tilt_rad = math.atan2(delta_z, horizontal_distance)
    tilt_deg = math.degrees(tilt_rad)
    return tilt_deg

# Example usage
# lat1, lon1, alt1 = 37.7749, -122.4194, 99
# lat2, lon2, alt2 = 34.0522, -118.2437, 100
# lat1, lon1, alt1 = 56.16876, 10.20247, 38991.00001
# lat2, lon2, alt2 = 56.16876, 10.20247, 38991.0

# tilt_angle = calculateTilt(lat1, lon1, alt1, lat2, lon2, alt2)
# print(f"Tilt angle between the points: {tilt_angle} degrees")