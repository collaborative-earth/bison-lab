import fiona
import geopandas as gpd
import pandas as pd
import shapely
from zipfile import ZipFile
from pathlib import Path

def _make_geom_2d(geom):
    """Converts a geometry from 3-D to 2-D"""
    return shapely.wkb.loads(shapely.wkb.dumps(geom, output_dimension=2))


def kml_to_geodataframe(filepath: Path = None) -> gpd.GeoDataFrame:
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


def kmz_to_geodataframe(filepath: Path = None) -> gpd.GeoDataFrame:
    """Read a KMZ file and convert to a GeoPandas GeoDataFrame.
    Allows multiple folders/layers in KML
    """
    # Extract KML file from KMZ
    kmz = ZipFile(filepath, 'r')
    kml_filepath = filepath.with_suffix('.kml')
    kmz.extract("doc.kml", kml_filepath)
    
    # Open KML file with geopandas/fiona
    fiona.supported_drivers["KML"] = "rw"
    df = gpd.read_file(kml_filepath / "doc.kml", driver="KML")

    # Convert geometry to 2-D
    df["geometry"] = df["geometry"].map(_make_geom_2d)
    return df