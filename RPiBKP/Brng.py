import pyproj

lat1 = -5.436902
long1 = 35.910058
lat2 = -5.516875
long2 = 36.037202


Geodesic = pyproj.Geod(ellps='WGS84')
fwd_azimuth, bck_azimuth, Distance = Geodesic.inv(lat1, long1, lat2, long2)

print fwd_azimuth
print Distance
