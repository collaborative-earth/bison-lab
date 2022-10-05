import ee
import folium


class GeometryProxy:
    def __init__(self, geometry: ee.Geometry):
        self.geometry = geometry

    def add_to(self, map: folium.Map, **kwargs):
        folium.GeoJson(data=self.geometry.getInfo(), **kwargs).add_to(map)

    def get_centroid_coordinates(self) -> list[float]:
        return self.geometry.centroid().coordinates().getInfo()[::-1]

    def __getattr__(self, name):
        return getattr(self.geometry, name)
