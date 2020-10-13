from detour.track import Track


class Route():
    def __init__(self, track=Track()):
        self.track = track
        self._get_bound_box()

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
            self.bounding_box = {}

    