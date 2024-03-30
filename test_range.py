import haversine as hs

def convertCoordinate(loc_string):
    lat_str, lon_str = loc_string.split(',')
    lat = float(lat_str.strip())
    lon = float(lon_str.strip())

    return (lat, lon)

loc1_str1 = "-6.894797, 107.610590"
loc2_str2 = "-6.893859, 107.614370"

loc1 = convertCoordinate(loc1_str1)
loc2 = convertCoordinate(loc2_str2)

print(hs.haversine(loc1,loc2))
print(bool('True'))