import re
from datetime import datetime as dt
from xml.etree import ElementTree as ET

from detour.track import TrackPoint


class GPXError(Exception):
    pass


class GPXParser:
    def __init__(self, xml=None):
        if xml:
            self.raw = self._remove_namespace(xml)
            self.root = ET.fromstring(self.raw)
            self._extract_track_root()
            self._extract_track_meta()
        elif xml is not None and type(xml) != str:
            raise TypeError("Expected string or None")


    def _remove_namespace(self, xml):
        xml = re.sub(r"<gpx[^>]*>", "<gpx>", xml)
        return xml

    def _extract_track_root(self):
        self.track_root = self.root.find("trk")

    def _extract_track_meta(self):
        meta = self.root.find("metadata")
        if meta:
            self.track_name = meta.find("name").text
            self.track_link = meta.find("link").get("href")
            ctime = meta.find("time").text
            self.track_ctime = dt.strptime(ctime, "%Y-%m-%dT%X%z")
        else:
            self.track_name = ""
            self.track_link = ""
            self.track_ctime = ""

    def extract_trackpoints(self):
        seg = self.track_root.find("trkseg")
        pts = seg.findall("trkpt")
        trackpoints = []
        for pt in pts:
            lat = float(pt.get("lat"))
            lon = float(pt.get("lon"))
            ele = float(pt.find("ele").text)
            tp = TrackPoint(lat=lat, lon=lon, ele=ele)
            trackpoints.append(tp)
        return trackpoints
