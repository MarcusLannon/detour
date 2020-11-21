import pytest

import json
import os
from detour import traffic
from detour.track import TrackPoint, Track


FILE_DIR = os.path.dirname(os.path.realpath(__file__))


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

    def test_set_params_corridor(self):
        expected = {"corridor": "0.0,0.0;1.0,1.0;10", "apiKey": "APIKEY"}
        test_corridor = "0.0,0.0;1.0,1.0;10"
        api = traffic.TrafficAPI(test=True)
        api.set_params(corridor=test_corridor)
        assert api.params == expected

    def test_api_ping(self):
        api = traffic.TrafficAPI(test=True)
        api.set_params()
        api.get()
        assert api.status_code == 401

    def test_track_from_shape(self):
        expected = Track(trkpts=[TrackPoint(0.0, 3.0), TrackPoint(1.0, 2.0)])
        data = {"LOCATION": {"GEOLOC": {"GEOMETRY": {"SHAPES": {"SHP": [
                {"value": "0.0,3.0 1.0,2.0"}
            ]}}}}}
        api = traffic.TrafficAPI(test=True)
        assert api._extract_track_legacy(data) == expected

    def test_extract_track(self):
        expected = Track(trkpts=[
                TrackPoint(51.29776, -0.11156),
                TrackPoint(51.29774, -0.11123)
            ])
        data = {"routes": [{"sections": [{"polyline": "BFgjj5Jn5VDiC"}]}]}
        api = traffic.TrafficAPI(test=True)
        assert api._track_from_json(data) == expected

    @pytest.mark.skip("Refactoring needed for this test")
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
