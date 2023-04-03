from ._landsat import landsat_5_sr, landsat_7_sr, landsat_8_sr, landsat_9_sr
from ._sentinel_2 import s2_sr_harmonized
from pathlib import Path


__all__ = [
    "s2_sr_harmonized",
    "landsat_7_sr",
    "landsat_8_sr",
    "landsat_5_sr",
    "landsat_9_sr",
]

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
LOCAL_DATA_DIR = DATA_DIR / "local"
