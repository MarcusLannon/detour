"""
Code for testing route objects
"""
import pytest

from detour.route import Route
from detour.track import TrackPoint, Track


class TestRoute:

    def test_create_route(self):
        _route = Route()

    def test_route_bounding_box(self):
        trackpoints = [
            TrackPoint(lat=0.0, lon=0.0),
            TrackPoint(lat=1.0, lon=1.0)
        ]
        expected = {
            "max_lat": 1.0,
            "min_lat": 0.0,
            "max_lon": 1.0,
            "min_lon": 0.0
        }
        track = Route(track=Track(trkpts=trackpoints))
        assert track.bbox == expected

    @pytest.mark.skip("Refactoring needed")
    def test_interset_fail(self):
        pass