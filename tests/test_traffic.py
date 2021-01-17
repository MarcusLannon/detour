import pytest
from unittest.mock import patch, MagicMock

import json
import os
from detour import traffic
from detour.track import TrackPoint, Track
from detour.config import HERE_URL


FILE_DIR = os.path.dirname(os.path.realpath(__file__))


class MockResponse:
    """Mock object for testing responses to get requests without calling
    requests.get itself.
    """
    def __init__(self, json, status_code):
        self.status_code = status_code
        self.json_obj = json

    def json(self):
        """The json method must be called as a function to match actual
        response object
        """
        return self.json_obj


class TestTrafficAPI:
    def test_create_api_handler(self):
        api = traffic.TrafficAPI()
        assert api.base_url == HERE_URL

    def test_set_params_key_only(self):
        api = traffic.TrafficAPI()
        api._TrafficAPI__key = "APIKEY"
        api.set_params()
        assert api.params == {"apiKey": "APIKEY"}

    def test_set_params_corridor(self):
        expected = {"corridor": "0.0,0.0;1.0,1.0;10", "apiKey": "APIKEY"}
        test_corridor = "0.0,0.0;1.0,1.0;10"
        api = traffic.TrafficAPI()
        api._TrafficAPI__key = "APIKEY"
        api.set_params(corridor=test_corridor)
        assert api.params == expected

    def test_set_params_bbox(self):
        expected = {"bbox": "1.0,0.0;0.0,1.0", "apiKey": "APIKEY"}
        test_bbox = dict(max_lat="1.0", max_lon="1.0",
                         min_lat="0.0", min_lon="0.0")
        api = traffic.TrafficAPI()
        api._TrafficAPI__key = "APIKEY"
        api.set_params(bbox=test_bbox)
        assert api.params == expected

    @patch("detour.traffic.requests.get")
    def test_api_get(self, mock_get):
        mock_get.return_value = MockResponse(json=["ok"], status_code=200)
        api = traffic.TrafficAPI()
        api.params = None
        data = api.get()
        assert api.status_code == 200
        assert data == ["ok"]

    def test_extract_track_from_json(self):
        expected = Track(trkpts=[
                TrackPoint(51.29776, -0.11156),
                TrackPoint(51.29774, -0.11123)
            ])
        data = {"routes": [{"sections": [{"polyline": "BFgjj5Jn5VDiC"}]}]}
        api = traffic.TrafficAPI()
        assert api._track_from_json(data) == expected

    @patch("detour.traffic.requests.get")
    def test_get_full_route(self, mock_get):
        mock_get.return_value = MockResponse(json=["ok"], status_code=200)
        expected_params = {
            "origin": "1.0,1.0",
            "destination": "0.0,0.0",
            "return": "polyline",
            "transportMode": "car",
            "departureTime": "0000-01-01T00:00:00",
            "apiKey": "APIKEY"
        }
        expected_url = "https://router.hereapi.com/v8/routes"
        api = traffic.TrafficAPI()
        api._TrafficAPI__key = "APIKEY"
        data = api._get_full_route("1.0,1.0", "0.0,0.0")
        mock_get.assert_called_with(expected_url, params=expected_params)
        assert data == ["ok"]

    def test_extract_track(self):
        """Note the lat/lon values in the test_item don't match the expected
        values. This is intentional and done for simplicity in testing since
        values are mocked in."""
        test_item = {"LOCATION": {"GEOLOC": {
                "ORIGIN": {"LATITUDE": 1.0, "LONGITUDE": 1.0},
                "TO": [{"LATITUDE": 0.0, "LONGITUDE": 0.0}]
        }}}
        expected = Track(trkpts=[
                TrackPoint(51.29776, -0.11156),
                TrackPoint(51.29774, -0.11123)
            ])
        test_json = {"routes": [{"sections": [{"polyline": "BFgjj5Jn5VDiC"}]}]}

        api = traffic.TrafficAPI()
        api._get_full_route = MagicMock(return_value=test_json)
        track = api._extract_track(test_item)
        api._get_full_route.assert_called_with("1.0,1.0", "0.0,0.0")
        assert track == expected

    def test_extract_details(self):
        expected = "test description"
        data = {"TRAFFIC_ITEM_DESCRIPTION": [{
                    "value": "test description",
                    "TYPE": "desc"
                }]}
        api = traffic.TrafficAPI()
        details = api._extract_details(data)
        assert details == expected

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
