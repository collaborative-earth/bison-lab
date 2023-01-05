import ee


def mask_exclude(img, mask):
    """Set mask on an image to exclude regions in `mask`.

    Args:
        img: An ee.Image
        mask: An ee.FeatureCollection of polygons

    Returns:
        An ee.Image
    """
    img = img.updateMask(ee.Image(1).toByte().paint(mask, 0))
    return img


def mask_include(img, mask):
    """Set mask on an image to include regions in `mask`.

    Args:
        img: An ee.Image
        mask: An ee.FeatureCollection of polygons

    Returns:
        An ee.Image
    """
    img = img.mask(ee.Image(0).toByte().paint(mask, 1))
    return img
