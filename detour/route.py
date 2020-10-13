from detour.track import Track


class Route():
    def __init__(self, track=Track()):
        self.track = track
        self._get_bound_box()

    def _get_bound_box(self):
        if len(self.track) > 0:
            max_lat = max([pt.lat for pt in self.track.points])
            min_lat = min([pt.lat for pt in self.track.points])
            max_lon = max([pt.lon for pt in self.track.points])
            min_lon = min([pt.lon for pt in self.track.points])
            self.bounding_box = {
                "BL": (min_lat, min_lon),
                "BR": (min_lat, max_lon),
                "TL": (max_lat, min_lon),
                "TR": (max_lat, max_lon)
            }
        else:
            self.bounding_box = {}

    