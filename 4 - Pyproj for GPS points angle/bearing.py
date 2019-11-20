import pyproj
lat1 = -5.436902
long1 = 35.910058
lat2 = -5.516875
long2 = 36.037202
geodesic = pyproj.Geod(ellps='WGS84')
fwd_azimuth,back_azimuth,distance = geodesic.inv(lat1, long1, lat2, long2)
print fwd_azimuth
print distance