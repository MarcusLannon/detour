"""
Classes and methods related to tracks. These are the core pieces that make
up all routes and roads.
"""

class TrackPoint:
    def __init__(self, lat=0.0, lon=0.0, ele=0.0):
        self.lat = lat
        self.lon = lon
        self.ele = ele

    def __eq__(self, other):
        if not isinstance(other, TrackPoint):
            return False
        else:
            eq_lat = self.lat == other.lat
            eq_lon = self.lon == other.lon
            eq_ele = self.ele == other.ele
            return eq_lat and eq_lon and eq_ele


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

