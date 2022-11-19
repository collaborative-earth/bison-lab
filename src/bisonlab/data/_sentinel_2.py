import ee


def _get_s2_sr_with_cloud_prob(aoi, start_date, end_date, cloud_filter=60):
    """Import, filter and join Sentinel-2 surface reflectance harmonized and Sentinel-2 cloud probability datasets.

    Returns:
        S2_SR_HARMONIZED collection where each image has a new 's2cloudless' property
        whose value is the corresponding s2cloudless image.
    """

    # Import and filter S2 SR Harmonized
    s2_sr_har = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", cloud_filter))
    )

    # Import and filter S2_CLOUD_PROBABILITY
    s2_cloud_prob = (
        ee.ImageCollection("COPERNICUS/S2_CLOUD_PROBABILITY")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
    )

    # Join S2 with S2 cloud probability with the 'system:index' property
    return ee.ImageCollection(
        ee.Join.saveFirst("s2cloudless").apply(
            **{
                "primary": s2_sr_har,
                "secondary": s2_cloud_prob,
                "condition": ee.Filter.equals(
                    **{"leftField": "system:index", "rightField": "system:index"}
                ),
            }
        )
    )


def _add_cloud_and_shadow_bands_and_scale(
    img, cloud_prob_thresh=60, nir_dark_thresh=0.15, cloud_proj_dist=1, buffer=50
):
    """Add dark pixels, cloud projection, and identified shadows as bands to an S2 SR image input.
    Note that the image input needs to be the result of the _get_s2_sr_with_cloud_prob.
    """
    # Get s2cloudless image, subset the probability band
    cld_prb = ee.Image(img.get("s2cloudless")).select("probability")

    # Condition s2cloudless by the probability threshold value.
    is_cloud = cld_prb.gt(cloud_prob_thresh).rename("clouds")

    # Add the cloud probability layer and cloud mask as image bands.
    img_cloud = img.addBands(ee.Image([cld_prb, is_cloud]))

    # Identify water pixels from the SCL band.
    not_water = img_cloud.select("SCL").neq(6)

    # Identify dark NIR pixels that are not water (potential cloud shadow pixels).
    SR_BAND_SCALE = 1e4
    dark_pixels = (
        img_cloud.select("B8")
        .lt(nir_dark_thresh * SR_BAND_SCALE)
        .multiply(not_water)
        .rename("dark_pixels")
    )

    # Determine the direction to project cloud shadow from clouds (assumes UTM projection).
    shadow_azimuth = ee.Number(90).subtract(
        ee.Number(img_cloud.get("MEAN_SOLAR_AZIMUTH_ANGLE"))
    )

    # Project shadows from clouds for the distance specified by the cloud_proj_dist input.
    cld_proj = (
        img_cloud.select("clouds")
        .directionalDistanceTransform(shadow_azimuth, cloud_proj_dist * 10)
        .reproject(**{"crs": img_cloud.select(0).projection(), "scale": 100})
        .select("distance")
        .mask()
        .rename("cloud_transform")
    )

    # Identify the intersection of dark pixels with cloud shadow projection.
    shadows = cld_proj.multiply(dark_pixels).rename("shadows")

    # Add dark pixels, cloud projection, and identified shadows as image bands.
    img_cloud_shadow = img_cloud.addBands(ee.Image([dark_pixels, cld_proj, shadows]))

    # Combine cloud and shadow mask, set cloud and shadow as value 1, else 0
    is_cld_shdw = (
        img_cloud_shadow.select("clouds").add(img_cloud_shadow.select("shadows")).gt(0)
    )

    # Remove small cloud-shadow patches and dilate remaining pixels by BUFFER input
    # 20 m scale is for speed, and assumes clouds don't require 10 m precision
    is_cld_shdw = (
        is_cld_shdw.focalMin(2)
        .focalMax(buffer * 2 / 20)
        .reproject(**{"crs": img.select([0]).projection(), "scale": 20})
        .rename("cloudmask")
    )

    img = img.addBands(is_cld_shdw)

    not_cloud_shadow = img.select("cloudmask").Not()

    # Subset reflectance bands and update their masks, return the result
    return img.select("B.*").updateMask(not_cloud_shadow).divide(10000)


def s2_sr_harmonized(
    aoi,
    start_date="2020-01-01",
    end_date="2020-12-31",
    cloud_filter=60,
    cloud_prob_thresh=50,
    nir_dark_thresh=0.15,
    cloud_proj_dist=1,
    buffer=50,
):
    """Load Sentinel 2 Surface Reflectance Harmonized for a given area of interest and date range"""

    s2 = _get_s2_sr_with_cloud_prob(
        aoi, start_date, end_date, cloud_filter=cloud_filter
    )

    def mapper(img):
        return _add_cloud_and_shadow_bands_and_scale(
            img,
            cloud_prob_thresh=cloud_prob_thresh,
            nir_dark_thresh=nir_dark_thresh,
            cloud_proj_dist=cloud_proj_dist,
            buffer=buffer,
        )

    return s2.map(lambda img: mapper(img))
