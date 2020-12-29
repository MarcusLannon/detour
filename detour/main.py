"""Simple runner function that takes a gpx file and prints the
closed roads on route.
"""
from detour.route import Route
from detour.gpx import GPXParser
from detour.track import Track


# TODO: This needs to be productionised
def main(gpx_path):
    with open(gpx_path, "r") as f:
        data = f.read()
    gpx = GPXParser(data)
    track = Track(gpx.extract_trackpoints())
    route = Route(track)
    route.reduce_points()
    route._get_incidents()
    route.find_flags()
    route.display_inline()
    return route.flags
