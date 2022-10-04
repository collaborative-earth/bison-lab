import ee
import folium


class Map(folium.Map):
    def add_ee_layer(self, ee_object, name):
        if isinstance(ee_object, ee.geometry.Geometry):
            folium.GeoJson(
                data=ee_object.getInfo(), name=name, overlay=True, control=True
            ).add_to(self)
        else:
            raise NotImplementedError(f"EE object is not supported for layer {name}")
