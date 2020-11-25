"""
Classes and methods related to tracks. These are the core pieces that make
up all routes and roads.
"""
import math
from math import log10, floor


class TrackPoint:
    def __init__(self, lat=0.0, lon=0.0, ele=0.0):
        self.lat = lat
        self.lon = lon
        self.ele = ele

    def __repr__(self):
        return "<TrackPoint lat=%.2f, lon=%.2f, ele=%.2f>" % (
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

    def _calc_distance(self, origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371  # km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) * math.sin(dlat / 2) +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
            math.sin(dlon / 2) * math.sin(dlon / 2)
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c

        return d*1000

    def distance_from(self, other):
        coord1 = (self.lat, self.lon)
        coord2 = (other.lat, other.lon)
        distance = self._calc_distance(coord1, coord2)
        return self._round_3_sig(distance)


class Track:
    def __init__(self, trkpts=None):
        if trkpts is None:
            trkpts = []
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

    def remove(self, trkpt):
        self.points.remove(trkpt)

    def intersection(self, other):
        # TODO: This is very slow, needs improvement
        intersect = []
        for pt1 in self.points:
            for pt2 in other.points:
                if pt1.distance_from(pt2) < 10.0:
                    intersect.append(pt1)
                if pt1.distance_from(pt2) > 5*1000.0 and len(intersect) == 0:
                    # If other track is over 5km from route point and
                    # there is no intersection then skip rest of route.
                    break
        return intersect
