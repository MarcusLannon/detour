import requests

from detour.config import HERE_URL, KEY
from detour.track import Track, TrackPoint
from detour import polyline


class TrafficAPI:
    def __init__(self):
        self.base_url = HERE_URL
        self.__key = KEY

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
        return response.json()

    def _track_from_json(self, track_json):
        track = Track()
        for sec in track_json["routes"][0]["sections"]:
            pts = polyline.decode(sec["polyline"])
            for pt in pts:
                track.append(TrackPoint(pt[0], pt[1]))
        return track

    def _get_full_route(self, origin, end):
        """Call the HERE routing API with the start and end points
        of the closed road to produce the full polyline. Time is
        set to year 0 so no diversions are suggested."""
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
        track_json = self._get_full_route(origin_str, end_str)
        track = self._track_from_json(track_json)

        return track

    def _extract_details(self, item):
        td = item["TRAFFIC_ITEM_DESCRIPTION"]
        details = [det["value"] for det in td if det["TYPE"] == "desc"][0]
        return details

    def parse(self, data):
        """Method to parse all items out of the response json."""
        if data.get("TRAFFIC_ITEMS"):
            traffic_items_json = data["TRAFFIC_ITEMS"]["TRAFFIC_ITEM"]
        else:
            traffic_items_json = []
        traffic_items = []
        for item in traffic_items_json:
            ti = {}
            ti["track"] = self._extract_track(item)
            ti["traffic_item_id"] = item["TRAFFIC_ITEM_ID"]
            ti["description"] = item["TRAFFIC_ITEM_TYPE_DESC"]
            ti["road_closed"] = item["TRAFFIC_ITEM_DETAIL"]["ROAD_CLOSED"]
            ti["details"] = item["TRAFFIC_ITEM_DESCRIPTION"][0]["value"]
            traffic_items.append(ti)
        return traffic_items

    def get_incidents(self):
        data = self.get()
        traffic_items = self.parse(data)
        return traffic_items
