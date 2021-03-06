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

    def test_route_intersect(self):
        trackpoints = [
            TrackPoint(lat=0.0, lon=0.0),
            TrackPoint(lat=1.0, lon=1.0)
        ]
        test_track = Track(trkpts=trackpoints)
        test_incidents = [{
            "track": test_track,
            "traffic_item_id": 1,
            "description": "ROAD_CLOSURE",
            "road_closed": True,
            "route_intersection": test_track
        }]
        test_route = Route(track=test_track)
        test_route.incidents = test_incidents
        test_route.find_flags()
        assert test_route.flags == test_incidents

    def test_reduce_points(self):
        expected = Track([
            TrackPoint(51.26686, -0.27281),
            TrackPoint(51.27106, -0.27334),
            TrackPoint(51.27206, -0.27331)
        ])
        trackpoints = [
            TrackPoint(51.26686, -0.27281),
            TrackPoint(51.27106, -0.27334),
            TrackPoint(51.27107, -0.27334),
            TrackPoint(51.27206, -0.27331)
        ]
        test_route = Route(track=Track(trackpoints))
        test_route.reduce_points()
        assert test_route.track == expected
