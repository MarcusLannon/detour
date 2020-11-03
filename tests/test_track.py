import datetime
from xml.etree import ElementTree as ET

import pytest

from detour import gpx
from detour.track import TrackPoint, Track


class TestTrack:
    def test_create_trackpoint(self):
        tp = TrackPoint(lat=0.0, lon=1.0, ele=2.0)
        assert tp.lat == 0.0
        assert tp.lon == 1.0
        assert tp.ele == 2.0

    def test_create_track(self):
        _ = Track()

    def test_create_empty_track(self):
        track = Track()
        assert track.points == []

    def test_create_non_empty_track(self):
        track = Track(trkpts=[TrackPoint()])
        assert track.points == [TrackPoint()]

    def test_get_track_point(self):
        track = Track(trkpts=[TrackPoint()])
        assert track[0] == TrackPoint()

    def test_append_track_point(self):
        track = Track()
        track.append(TrackPoint())
        assert track.points == [TrackPoint()]

    def test_track_len(self):
        track = Track(trkpts=[TrackPoint()])
        assert len(track) == 1

    def test_track_iter(self):
        track = Track(trkpts=[TrackPoint()])
        x = 0
        for _ in track:
            x += 1
        assert x == 1

    def test_track_from_gpx(self):
        test_gpx = """
        <gpx>
            <trk>
                <trkseg>
                    <trkpt lat="0.0" lon="0.0">
                        <ele>0.0</ele>
                    </trkpt>
                </trkseg>
            </trk>
        </gpx>
        """
        expected = Track(trkpts=[TrackPoint(lat=0.0, lon=0.0, ele=0.0)])
        parser = gpx.GPXParser(test_gpx)
        trackpoints = parser.extract_trackpoints()
        track = Track(trkpts=trackpoints)
        assert track == expected

    def test_track_intersect_none(self):
        track1 = Track(trkpts=[TrackPoint(0.0, 0.0, 0.0)])
        track2 = Track(trkpts=[TrackPoint(1.0, 1.0, 1.0)])
        assert track1.intersection(track2) == []

    def test_track_intersect_one(self):
        track1 = Track(trkpts=[TrackPoint(0.0, 0.0, 0.0)])
        track2 = Track(trkpts=[TrackPoint(0.0, 0.0, 0.0)])
        assert track1.intersection(track2) == [TrackPoint(0.0, 0.0, 0.0)]

    def test_trackpoint_distance_from(self):
        tp1 = TrackPoint(0.0, 0.0, 0.0)
        tp2 = TrackPoint(1.0, 1.0, 0.0)
        assert tp1.distance_from(tp2) == 157000.0

    def test_track_intersect_close(self):
        track1 = Track(trkpts=[TrackPoint(0.0, 0.0, 0.0)])
        track2 = Track(trkpts=[TrackPoint(0.00001, 0.00001, 0.0)])
        assert track1.intersection(track2) == [TrackPoint(0.0, 0.0, 0.0)]
