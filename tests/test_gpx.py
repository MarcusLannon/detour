import datetime

from detour import gpx
from detour.track import TrackPoint


class TestGPXParser:
    def test_create_parser(self):
        _ = gpx.GPXParser()

    def test_read_raw_gpx(self):
        test_gpx = "<gpx></gpx>"
        parser = gpx.GPXParser(test_gpx)
        assert parser.raw == "<gpx></gpx>"

    def test_parse_gpx(self):
        test_gpx = "<gpx></gpx>"
        parser = gpx.GPXParser(test_gpx)
        assert parser.root.tag == "gpx"

    def test_get_track_meta(self):
        test_gpx = """
        <gpx>
            <metadata>
                <name>test route</name>
                <link href="dummy_url"></link>
                <time>2020-08-13T22:08:05Z</time>
            </metadata>
        </gpx>
        """
        parser = gpx.GPXParser(test_gpx)
        assert parser.track_name == "test route"
        assert parser.track_link == "dummy_url"

        ctime = datetime.datetime(
            2020, 8, 13, 22, 8, 5, 
            tzinfo=datetime.timezone.utc
        )
        assert parser.track_ctime == ctime

    def test_remove_namespace(self):
        test_gpx = """<gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxdata="http://www.cluetrust.com/XML/GPXDATA/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.cluetrust.com/XML/GPXDATA/1/0 http://www.cluetrust.com/Schemas/gpxdata10.xsd" version="1.1" creator="http://ridewithgps.com/"></gpx>"""
        parser = gpx.GPXParser(test_gpx)
        assert parser.raw == "<gpx></gpx>"


    def test_extract_one_trackpoint(self):
        test_gpx = """
        <gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gpxdata="http://www.cluetrust.com/XML/GPXDATA/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.cluetrust.com/XML/GPXDATA/1/0 http://www.cluetrust.com/Schemas/gpxdata10.xsd" version="1.1" creator="http://ridewithgps.com/">
            <trk>
                <trkseg>
                    <trkpt lat="0.0" lon="0.0">
                        <ele>0.0</ele>
                    </trkpt>
                </trkseg>
            </trk>
        </gpx>
        """
        expected = [TrackPoint(lat=0.0, lon=0.0, ele=0.0)]
        parser = gpx.GPXParser(test_gpx)
        trackpoints = parser.extract_trackpoints()
        assert trackpoints == expected


    def test_extract_multi_trackpoints(self):
        test_gpx = """
        <gpx>
            <trk>
                <trkseg>
                    <trkpt lat="0.0" lon="0.0">
                        <ele>0.0</ele>
                    </trkpt>
                    <trkpt lat="1.0" lon="1.0">
                        <ele>1.0</ele>
                    </trkpt>
                </trkseg>
            </trk>
        </gpx>
        """
        expected = [
            TrackPoint(lat=0.0, lon=0.0, ele=0.0),
            TrackPoint(lat=1.0, lon=1.0, ele=1.0)
        ]
        parser = gpx.GPXParser(test_gpx)
        trackpoints = parser.extract_trackpoints()
        assert trackpoints == expected