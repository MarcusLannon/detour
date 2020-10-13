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
            "BL": (0.0, 0.0),
            "BR": (0.0, 1.0),
            "TL": (1.0, 0.0),
            "TR": (1.0, 1.0)
        }
        track = Route(track=Track(trkpts=trackpoints))
        assert track.bounding_box == expected

    @pytest.mark.skip("Refactoring needed")
    def test_interset_fail(self):
        pass