#!/usr/bin/python
from math import *

class CoordinateConversion(object):
   
    def __init__(self):
        # Constant Values for calculation
        self.equatorialRadius = 6378137
        self.polarRadius = 6356752.314
        self.K0 = 0.9996 # Scale factor
        self.e = sqrt(1 - (self.polarRadius / self.equatorialRadius)**2) # eccentricity
        self.e1sq = self.e * self.e / (1 - self.e * self.e)
        self.A0 = 6367449.146
        self.B0 = 16038.42955
        self.C0 = 16.83261333
        self.D0 = 0.021984404
        self.E0 = 0.000312705

    def convertLatLonToUTM(self, latitude, longitude):
        # Validate Latitude and Longitude
        if (latitude < -90) or (latitude > 90) or (longitude < -180) or (longitude >= 180):
            raise ValueError("Acceptable values: latitude [-90,90], longitude [-180,180).")

        # Determine Latitude and Longitude Zones
        longZone = self._getLongZone(longitude)
	latZone = self._getLatZone(latitude)

        # Calculate values for easting and northing 
        radLatitude = radians(latitude)
        nu = self.equatorialRadius / sqrt(1 - (self.e**2 * sin(radLatitude)**2))
        p = radians((longitude - ((6*longZone) - 183)))
 
        # Calculate Easting and Northing
        easting = self._getEasting(radLatitude, nu, p)
        northing = self._getNorthing(radLatitude, nu, p)

        # Output Results
        longZone = str(longZone)
        longZone = '0'+longZone if len(longZone) == 1 else longZone
        return "%s %s %s %s" % (longZone, latZone, easting, northing)

    def _getLongZone(self, longitude):
        if longitude < 0:
            longZone = ((180 + longitude) / 6) + 1
        else:
            longZone = (longitude / 6) + 31

        return int(longZone)

    def _getLatZone(self, latitude):
        DEGREE_LETTERS = { -90:'A', -84:'C', -72:'D', -64:'E', -56:'F', -48:'G', -40:'H', -32:'J', -24:'K', -16:'L', -8:'M', 0:'N', 8:'P', 16:'Q', 24:'R', 32:'S', 40:'T', 48:'U', 56:'V', 64:'W', 72:'X', 84:'Z' }
        DEGREES = DEGREE_LETTERS.keys()
        DEGREES.sort()

        lat = int(latitude)
        for degree in DEGREES:
            if lat == degree:
                return DEGREE_LETTERS[degree]
            elif lat <= degree:
                return DEGREE_LETTERS[prevDegree]
            prevDegree = degree
        else:
            return DEGREE_LETTERS[prevDegree]

    def _getEasting(self, radLatitude, nu, p):
        K4 = nu * cos(radLatitude) * self.K0
        K5 = (self.K0 * nu * cos(radLatitude)**3 / 6) * (1 - tan(radLatitude)**2 + self.e1sq * cos(radLatitude)**2)

        return int(500000 + (K4 * p + K5 * p**3))

    def _getNorthing(self, radLatitude, nu, p):
        s = self.A0 * radLatitude - self.B0 * sin(2 * radLatitude) + self.C0 * sin(4 * radLatitude) - self.D0 * sin(6 * radLatitude) + self.E0 * sin(8 * radLatitude)
        K1 = s * self.K0
        K2 = self.K0 * nu * sin(2 * radLatitude) / 4
        K3 = (self.K0 * nu * sin(radLatitude) * cos(radLatitude)**3 / 24) * (5 - tan(radLatitude)**2 + 9 * self.e1sq * cos(radLatitude)**2 + 4 * self.e1sq**2 * cos(radLatitude)**4)

        northing = int(K1 + K2 * p * p + K3 * p**4)
	if degrees(radLatitude) < 0:
            northing = 10000000 + northing
        return northing


if __name__ == '__main__':
    cc = CoordinateConversion()
    print cc.convertLatLonToUTM(0.0000,0.0000) # "31 N 166021 0"
    print cc.convertLatLonToUTM(0.1300,-0.2324) # "30 N 808084 14385"
    print cc.convertLatLonToUTM(-45.6456,23.3545) # "34 G 683473 4942631"
    print cc.convertLatLonToUTM(-12.7650,-33.8765) # "25 L 404859 8588690"
    print cc.convertLatLonToUTM(-80.5434,-170.6540) # "02 C 506346 1057742"
    print cc.convertLatLonToUTM(90.0000,177.0000) # "60 Z 500000 9997964"
    print cc.convertLatLonToUTM(-90.0000,-177.0000) # "01 A 500000 2035"
    print cc.convertLatLonToUTM(90.0000,3.0000) # "31 Z 500000 9997964"
    print cc.convertLatLonToUTM(23.4578,-135.4545) # "08 Q 453580 2594272"
    print cc.convertLatLonToUTM(77.3450,156.9876) # "57 X 450793 8586116"
    print cc.convertLatLonToUTM(-89.3454,-48.9306) # "22 A 502639 75072"
