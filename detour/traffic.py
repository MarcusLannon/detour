import requests

from detour.config import HERE_URL, KEY
from detour.track import Track, TrackPoint
from detour import polyline


class TrafficAPI:
    def __init__(self, test=False):
        """If test is set to True then a dummy API key is used."""
        self.traffic_items = []
        self.test = test
        self.base_url = HERE_URL
        if not test:
            self.__key = KEY
        else:
            self.__key = "APIKEY"

    @property
    def key(self):
        if self.test:
            return self.__key
        else:
            return None

    def set_params(self, corridor=None, bbox=None):
        self.params = {"apiKey": self.__key}

        if corridor is not None:
            self.params["corridor"] = corridor
        if bbox is not None:
            max_lat = bbox["max_lat"]
            min_lat = bbox["min_lat"]
            max_lon = bbox["max_lon"]
            min_lon = bbox["min_lon"]
            bbox_str = f"{max_lat},{min_lon};{min_lat},{max_lon}"
            self.params["bbox"] = bbox_str

    def get(self):
        response = requests.get(self.base_url, params=self.params)
        self.status_code = response.status_code
        self.json = response.json()

    def _track_from_json(self, track_json):
        track = Track()
        for sec in track_json["routes"][0]["sections"]:
            pts = polyline.decode(sec["polyline"])
            for pt in pts:
                track.append(TrackPoint(pt[0], pt[1]))
        return track

    def _get_route_api(self, origin, end):
        params = {
            "origin": origin,
            "destination": end,
            "return": "polyline",
            "transportMode": "car",
            "departureTime": "0000-01-01T00:00:00",
            "apiKey": self.__key
        }
        url = "https://router.hereapi.com/v8/routes"
        r = requests.get(url, params=params)
        data = r.json()
        return data

    def _extract_track(self, item):
        """Turn the geo location data of an incident into a detour track
        The incident data only contains the origin and end point so the 
        routing api is used to complete the track."""
        geoloc = item["LOCATION"]["GEOLOC"]
        origin = geoloc["ORIGIN"]
        end = geoloc["TO"]

        origin_str = str(origin["LATITUDE"]) + "," + str(origin["LONGITUDE"])
        end_str = str(end[0]["LATITUDE"]) + "," + str(end[0]["LONGITUDE"])
        track_json = self._get_route_api(origin_str, end_str)
        track = self._track_from_json(track_json)

        return track

    def _extract_track_legacy(self, item):
        """Turn the geo location data of an incident into a detour track"""
        track = Track()
        shapes = item["LOCATION"]["GEOLOC"]["GEOMETRY"]["SHAPES"]["SHP"]
        for shape in shapes:
            points = shape["value"].split(" ")
            for point in points:
                lat, lon = point.split(",")  # Unpack the lat lon pairs
                lat = float(lat)
                lon = float(lon)
                track.append(TrackPoint(lat, lon))
        return track

    def parse(self):
        """ Method to parse all items out of the response json
        """
        if self.json.get("TRAFFIC_ITEMS"):
            traffic_items_json = self.json["TRAFFIC_ITEMS"]["TRAFFIC_ITEM"]
        else:
            traffic_items_json = []

        for item in traffic_items_json:
            ti = {}
            ti["track"] = self._extract_track(item)
            ti["traffic_item_id"] = item["TRAFFIC_ITEM_ID"]
            ti["description"] = item["TRAFFIC_ITEM_TYPE_DESC"]
            ti["road_closed"] = item["TRAFFIC_ITEM_DETAIL"]["ROAD_CLOSED"]
            self.traffic_items.append(ti)

    def get_incidents(self):
        self.get()
        self.parse()
        return self.traffic_items
