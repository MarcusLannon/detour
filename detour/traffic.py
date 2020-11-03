import requests

from detour.config import HERE_URL, KEY
from detour.track import Track, TrackPoint


class TrafficAPI:
    def __init__(self, test=False):
        """ If test is set to True then a dummy API key is used."""
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

    def set_params(self, bbox=None):
        self.params = {"apiKey": self.__key}

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

    def _extract_track(self, item):
        """Turn the geo location data of an incident into a detour track"""
        geoloc = item["LOCATION"]["GEOLOC"]

        origin = geoloc["ORIGIN"]
        origin_tp = TrackPoint(lat=origin["LATITUDE"], lon=origin["LONGITUDE"])
        track = Track(trkpts=[origin_tp])

        end = geoloc["TO"]
        for pt in end:
            track.append(TrackPoint(lat=pt["LATITUDE"], lon=pt["LONGITUDE"]))

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
