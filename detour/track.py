"""
Classes and methods related to tracks. These are the core pieces that make
up all routes and roads.
"""
import geopy.distance
from math import log10, floor


class TrackPoint:
    def __init__(self, lat=0.0, lon=0.0, ele=0.0):
        self.lat = lat
        self.lon = lon
        self.ele = ele

    def __repr__(self):
        return "<TrackPoint lat=%d, lon=%d, ele=%d>" % (
            self.lat, self.lon, self.ele)

    def __eq__(self, other):
        if not isinstance(other, TrackPoint):
            return False
        else:
            eq_lat = self.lat == other.lat
            eq_lon = self.lon == other.lon
            eq_ele = self.ele == other.ele
            return eq_lat and eq_lon and eq_ele

    def _round_3_sig(self, x):
        if x == 0.0:
            return 0.0
        else:
            return round(x, 2-int(floor(log10(x))))

    def distance_from(self, other):
        coord1 = (self.lat, self.lon)
        coord2 = (other.lat, other.lon)
        distance = geopy.distance.distance(coord1, coord2).meters
        return self._round_3_sig(distance)


class Track:
    def __init__(self, trkpts=[]):
        self.points = trkpts

    def __getitem__(self, key):
        return self.points[key]

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        else:
            eq_pts = self.points == other.points
            return eq_pts

    def __len__(self):
        return len(self.points)

    def append(self, trkpt):
        self.points.append(trkpt)

    def intersection(self, other):
        intersect = []
        for pt1 in self.points:
            for pt2 in other.points:
                if pt1.distance_from(pt2) < 10.0:
                    intersect.append(pt1)
        return intersect
