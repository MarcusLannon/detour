from detour.track import Track
from detour.traffic import TrafficAPI


class Route:
    def __init__(self, track=Track()):
        self.track = track
        self._get_bound_box()
        self._get_corridor()

    def _get_bound_box(self):
        """The bounding box is the latitude/longitude box that 
        contains the entire route. This is defined by the lat lon
        of the top-left and bottom-right corners:
        bbox = top,left;bottom,right
        bbox = max Latitude;min Longitude; min Latitude, max Longitude
        """
        if len(self.track) > 0:
            max_lat = max([pt.lat for pt in self.track.points])
            min_lat = min([pt.lat for pt in self.track.points])
            max_lon = max([pt.lon for pt in self.track.points])
            min_lon = min([pt.lon for pt in self.track.points])
            self.bbox = {
                "max_lat": max_lat,
                "min_lat": min_lat,
                "max_lon": max_lon,
                "min_lon": min_lon
            }
        else:
            self.bbox = None

    def _get_corridor(self):
        """The corridor is a route of latitude/longitude points and a width.
        The width is fixed at 10 meters to ensure full road coverage."""
        corridor = []
        for pt in self.track:
            corridor.append(f"{pt.lat},{pt.lon}")
        self.corridor = ";".join(corridor) + ";10"

    def reduce_points(self):
        """Reduce the number of points in the route by deduping pairwise any
        that are within 5 meters of eachother."""
        # TODO: Make this more effective by expanding beyond pairwise
        for i in range(len(self.track)):
            first = i
            second = i+1
            if second < len(self.track):
                pt1 = self.track[first]
                pt2 = self.track[second]
                if pt1.distance_from(pt2) < 5.0:
                    self.track.remove(pt2)

    def _get_incidents(self):
        api = TrafficAPI()
        api.set_params(bbox=self.bbox)
        self.incidents = api.get_incidents()

    def find_flags(self):
        self.flags = []
        for item in self.incidents:
            inter = self.track.intersection(item["track"])
            self.flags.append(Track(trkpts=inter))
