import ee


def _mask_clouds_snow(img):
    """Mask clouds and snow using the quality band of Landsat 9.
    See quality assesment band section here https://www.usgs.gov/land-resources/nli/landsat/
    """
    qa = img.select("QA_PIXEL")
    mask = qa.bitwiseAnd(1 << 3).eq(0).And(qa.bitwiseAnd(1 << 4).eq(0))
    return img.updateMask(mask)


def landsat_9_sr(aoi, start_date="2021-10-31", end_date=None, cloud_prob_thresh=100):
    """USGS Landsat 9 Level 2, Collection 2, Tier 1 surface reflectance"""
    return (
        ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lte("CLOUD_COVER", cloud_prob_thresh))
        .scaleAndOffset()
    ).map(_mask_clouds_snow)


def landsat_8_sr(aoi, start_date, end_date, cloud_prob_thresh=100):
    """USGS Landsat 8 Level 2, Collection 2, Tier 1 surface reflectance"""
    return (
        ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lte("CLOUD_COVER", cloud_prob_thresh))
        .scaleAndOffset()
    ).map(_mask_clouds_snow)


def landsat_7_sr(aoi, start_date, end_date, cloud_prob_thresh=100):
    """USGS Landsat 7 Level 2, Collection 2, Tier 1 surface reflectance"""
    return (
        ee.ImageCollection("LANDSAT/LE07/C02/T1_L2")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lte("CLOUD_COVER", cloud_prob_thresh))
        .scaleAndOffset()
    ).map(_mask_clouds_snow)


def landsat_5_sr(
    aoi, start_date="1984-03-16", end_date="2012-05-05", cloud_prob_thresh=100
):
    """USGS Landsat 5 Level 2, Collection 2, Tier 1 surface reflectance"""
    return (
        ee.ImageCollection("LANDSAT/LT05/C02/T1_L2")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lte("CLOUD_COVER", cloud_prob_thresh))
        .scaleAndOffset()
    ).map(_mask_clouds_snow)
