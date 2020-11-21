"""
Code for testing route objects
"""
import pytest

from detour.route import Route
from detour.track import TrackPoint, Track


class TestRoute:

    def test_create_route(self):
        _ = Route()

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
        test_route = Route(track=Track(trkpts=trackpoints))
        assert test_route.bbox == expected

    def test_route_corridor(self):
        trackpoints = [
            TrackPoint(lat=0.0, lon=0.0),
            TrackPoint(lat=1.0, lon=1.0)
        ]
        expected = "0.0,0.0;1.0,1.0;10"
        test_route = Route(track=Track(trkpts=trackpoints))
        assert test_route.corridor == expected
