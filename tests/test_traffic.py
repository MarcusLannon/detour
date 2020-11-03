import pytest

import json
import os
from detour import traffic
from detour.track import TrackPoint, Track


FILE_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def bbox_basic():
    return {"max_lat": 1.0, "min_lat": 0.0, "max_lon": 1.0, "min_lon": 0.0}


class TestTrafficAPI:
    def test_create_api_handler(self):
        _ = traffic.TrafficAPI()

    def test_api_config(self):
        api = traffic.TrafficAPI(test=True)
        url = "https://traffic.ls.hereapi.com/traffic/6.3/incidents.json"
        assert api.base_url == url
        assert api.key == "APIKEY"

    def test_read_api_key(self):
        api = traffic.TrafficAPI(test=False)
        assert api.key is None

    def test_set_params_key_only(self):
        api = traffic.TrafficAPI(test=True)
        api.set_params()
        assert api.params == {"apiKey": "APIKEY"}

    def test_set_params_bbox(self, bbox_basic):
        api = traffic.TrafficAPI(test=True)
        api.set_params(bbox=bbox_basic)
        assert api.params == {"bbox": "1.0,0.0;0.0,1.0", "apiKey": "APIKEY"}

    def test_api_ping(self, bbox_basic):
        api = traffic.TrafficAPI(test=True)
        api.set_params(bbox=bbox_basic)
        api.get()
        assert api.status_code == 401

    def test_parse_json(self):
        trkpts = [TrackPoint(lat=50, lon=0), TrackPoint(lat=51, lon=-1)]
        expected = [{
                "traffic_item_id": "1",
                "description": "ROAD_CLOSURE",
                "road_closed": True,
                "track": Track(trkpts)
        }]

        with open(f"{FILE_DIR}/data/dummy_traffic_data.json", "r") as f:
            data = json.load(f)
        api = traffic.TrafficAPI(test=True)
        api.json = data
        api.parse()
        assert api.traffic_items == expected
