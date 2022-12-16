import fiona
import geopandas as gpd
import pandas as pd
import shapely


def _make_geom_2d(geom):
    """Converts a geometry from 3-D to 2-D"""
    return shapely.wkb.loads(shapely.wkb.dumps(geom, output_dimension=2))


def kml_to_geodataframe(filepath: str = None) -> gpd.GeoDataFrame:
    """Read a KML file and convert to a GeoPandas GeoDataFrame.
    Allows multiple folders/layers in KML
    """
    fiona.supported_drivers["KML"] = "rw"

    df = pd.DataFrame()
    for layer in fiona.listlayers(filepath):
        features = gpd.read_file(filepath, driver="KML", layer=layer)
        features["layer"] = layer
        df = pd.concat([df, features], ignore_index=True)

    # Convert geometry to 2-D
    df["geometry"] = df["geometry"].map(_make_geom_2d)
    return df
