from datetime import datetime, timezone
from enum import Enum

from pystac.extensions.eo import Band
from pystac import Extent, SpatialExtent, TemporalExtent, Provider, ProviderRole, Link, MediaType

class Sensor(Enum):
    MSS = "M"
    TM = "T"
    ETM = "E"
    OLI_TIRS = "C"

INSTRUMENT_KEYS = {
    "M": "MSS",
    "T": "TM_ETM",
    "E": "TM_ETM",
    "C": "OLI_TIRS"
}

INSTRUMENT_LIST = {
    "M": ["mss"],
    "T": ["tm"],
    "E": ["etm"],
    "C": ["oli", "tirs"]
}

LANDSAT_EXTENSION_SCHEMA = "https://landsat.usgs.gov/stac/landsat-extension/v1.1.1/schema.json"

COMMON_ASSETS = {
    "thumbnail": {
        "type": MediaType.JPEG,
        "title": "Thumbnail image",
        "roles": ["thumbnail"],
        "href_suffix": "thumb_small.jpeg"
    },
    "reduced_resolution_browse": {
        "type": MediaType.JPEG,
        "title": "Reduced resolution browse image",
        "roles": ["overview"],
        "href_suffix": "thumb_large.jpeg"
    },
    "MTL.json": {
        "type": MediaType.JSON,
        "title": "Product Metadata File (json)",
        "description": "Collection 2 Level-X Product Metadata File (json)",
        "roles": ["metadata"],
        "href_suffix": "MTL.json"
    },
    "MTL.txt": {
        "type": MediaType.TEXT,
        "title": "Product Metadata File",
        "description": "Collection 2 Level-X Product Metadata File (txt)",
        "roles": ["metadata"],
        "href_suffix": "MTL.txt"
    },
    "MTL.xml": {
        "type": MediaType.XML,
        "title": "Product Metadata File (xml)",
        "description": "Collection 2 Level-X Product Metadata File (xml)",
        "roles": ["metadata"],
        "href_suffix": "MTL.xml"
    },
    "ANG": {
        "type": MediaType.TEXT,
        "title": "Angle Coefficients File",
        "description": "Collection 2 Level-2 Angle Coefficients File (ANG)",
        "roles": ["metadata"],
        "href_suffix": "ANG.txt"
    },
    "QA_PIXEL": {
        "type": MediaType.COG,
        "title": "Pixel Quality Assessment Band",
        "description": "Collection 2 Level-1 Pixel Quality Assessment Band",
        "roles": ["data"],
        "href_suffix": "QA_PIXEL.TIF"
    },
    "QA_RADSAT": {
        "type": MediaType.COG,
        "title": "Radiometric Saturation Quality Assessment Band",
        "description": "Collection 2 Level-1 Radiometric Saturation Quality Assessment Band",
        "roles": ["data"],
        "href_suffix": "QA_RADSAT.TIF"
    },
}

INSTRUMENT_ASSETS = {
    "MSS": {
        "B4": {
            "title": "Green Band (B4)",
            "description": "Collection 2 Level-1 Green Band (B4) Top of Atmosphere Radiance",
            "gsd": 60,
            "roles": ["data"]
        },
        "B5": {
            "title": "Red Band (B5)",
            "description": "Collection 2 Level-1 Red Band (B5) Top of Atmosphere Radiance",
            "gsd": 60,
            "roles": ["data"]
        },
        "B6": {
            "title": "Near Infrared Band 0.7 (B6)",
            "description": "Collection 2 Level-1 Near Infrared Band 0.7 (B6) Top of Atmosphere Radiance",
            "gsd": 60,
            "roles": ["data"]
        },
        "B7": {
            "title": "Near Infrared Band 0.9 (B7)",
            "description": "Collection 2 Level-1 Near Infrared Band 0.9 (B7) Top of Atmosphere Radiance",
            "gsd": 60,
            "roles": ["data"]
        },
    },
    "TM_ETM": {
        "SR_B1": {
            "title": "Blue Band (B1)",
            "description": "Collection 2 Level-2 Blue Band (B1) Surface Reflectance",
            "gsd": 30,
            "roles": ["data"]
        },
        "SR_B2": {
            "title": "Green Band (B2)",
            "description": "Collection 2 Level-2 Green Band (B2) Surface Reflectance",
            "gsd": 30,
            "roles": ["data"]
        },
        "SR_B3": {
            "title": "Red Band (B3)",
            "description": "Collection 2 Level-2 Red Band (B3) Surface Reflectance",
            "gsd": 30,
            "roles": ["data"]
        },
        "SR_B4": {
            "title": "Near Infrared Band 0.8 (B4)",
            "description": "Collection 2 Level-2 Near Infrared Band 0.8 (B4) Surface Reflectance",
            "gsd": 30,
            "roles": ["data"]
        },
        "SR_B5": {
            "title": "Short-wave Infrared Band 1.6 (B5)",
            "description": "Collection 2 Level-2 Short-wave Infrared Band 1.6 (B6) Surface Reflectance",
            "gsd": 30,
            "roles": ["data"]
        },
        "SR_B7": {
            "title": "Short-wave Infrared Band 2.2 (B7)",
            "description": "Collection 2 Level-2 Short-wave Infrared Band 2.2 (B7) Surface Reflectance",
            "gsd": 30,
            "roles": ["data"]
        },
        "SR_ATMOS_OPACITY": {
            "title": "Atmospheric Opacity Band",
            "description": "Collection 2 Level-2 Atmospheric Opacity Band Surface Reflectance",
            "roles": ["data"]
        },
        "SR_CLOUD_QA": {
            "title": "Cloud Quality Analysis Band",
            "description": "Collection 2 Level-2 Cloud Quality Opacity Band Surface Reflectance",
            "roles": ["data"]
        },
        "ST_B6": {
            "title": "Surface Temperature Band (B6)",
            "description": "Landsat Collection 2 Level-2 Surface Temperature Band (B6) Surface Temperature Product",
            "gsd": 120,
            "roles": ["data"]
        },
        "ST_ATRAN": {
            "title": "Atmospheric Transmittance Band",
            "description": "Landsat Collection 2 Level-2 Atmospheric Transmittance Band Surface Temperature Product",
            "roles": ["data"]
        },
        "ST_CDIST": {
            "title": "Cloud Distance Band",
            "description": "Landsat Collection 2 Level-2 Cloud Distance Band Surface Temperature Product",
            "roles": ["data"]
        },
        "ST_DRAD": {
            "title": "Downwelled Radiance Band",
            "description": "Landsat Collection 2 Level-2 Downwelled Radiance Band Surface Temperature Product",
            "roles": ["data"]
        },
        "ST_URAD": {
            "title": "Upwelled Radiance Band",
            "description": "Landsat Collection 2 Level-2 Upwelled Radiance Band Surface Temperature Product",
            "roles": ["data"]
        },
        "ST_TRAD": {
            "title": "Thermal Radiance Band",
            "description": "Landsat Collection 2 Level-2 Thermal Radiance Band Surface Temperature Product",
            "roles": ["data"]
        },
        "ST_EMIS": {
            "title": "Emissivity Band",
            "description": "Landsat Collection 2 Level-2 Emissivity Band Surface Temperature Product",
            "roles": ["data"]
        },
        "ST_EMSD": {
            "title": "Emissivity Standard Deviation Band",
            "description": "Landsat Collection 2 Level-2 Emissivity Standard Deviation Band Surface Temperature Product",
            "roles": ["data"]
        },
        "ST_QA": {
            "title": "Surface Temperature Quality Assessment Band",
            "description": "Landsat Collection 2 Level-2 Surface Temperature Band Surface Temperature Product",
            "roles": ["data"]
        }
    },
}

INSTRUMENT_EO_BANDS = {
    "MSS": {
        "B4": {
            "name": "B4",
            "common_name": "green",
            "center_wavelength": 0.55
        },
        "B5": {
            "name": "B5",
            "common_name": "red",
            "center_wavelength": 0.65
        },
        "B6": {
            "name": "B6",
            "common_name": "nir08",
            "center_wavelength": 0.75
        },
        "B7": {
            "name": "B7",
            "common_name": "nir09",
            "center_wavelength": 0.95
        }
    },
    "TM_ETM": {
        "SR_B1": {
            "name": "B1",
            "common_name": "blue",
            "center_wavelength": 0.49
        },
        "SR_B2": {
            "name": "B2",
            "common_name": "green",
            "center_wavelength": 0.56
        },
        "SR_B3": {
            "name": "B3",
            "common_name": "red",
            "center_wavelength": 0.66
        },
        "SR_B4": {
            "name": "B4",
            "common_name": "nir08",
            "center_wavelength": 0.84
        },
        "SR_B5": {
            "name": "B5",
            "common_name": "swir16",
            "center_wavelength": 1.65
        },
        "SR_B7": {
            "name": "B7",
            "common_name": "swir22",
            "center_wavelength": 2.22
        },
        "ST_B6": {
            "name": "B6",
            "common_name": "lwir",
            "center_wavelength": 11.45
        }
    }
}

C2_L1_ID = "landsat-c2-l1"
C2_L1_TITLE = "Landsat Collection 2 Level-1"
C2_L1_DESCRIPTION = (
    "The Landsat program provides a comprehensive, continuous archive of the "
    "Earth's surface. Landsat Collection 2 Level-1 data products consist of "
    "quantized and calibrated scaled Digital Numbers (DN) representing the "
    "multispectral image data. This dataset represent the global archive of "
    "Level-1 data acquired by the Multispectral Scanner System onboard "
    "Landsat 1 through Landsat 5. MSS data is only available in Level-1 form.")
C2_L1_KEYWORDS = [
    "Landsat", "USGS", "NASA", "Satellite", "Global", "Imagery", "Reflectance"
]
C2_L1_EXTENTS = Extent(
    SpatialExtent([[-180., 90., 180., -90.]]),
    TemporalExtent([datetime(1972, 8, 1, tzinfo=timezone.utc),
                    None])  # ballpark only
)
C2_L1_PROVIDERS = [
    Provider("NASA",
             roles=[ProviderRole.PRODUCER, ProviderRole.LICENSOR],
             url="https://landsat.gsfc.nasa.gov/"),
    Provider("USGS",
             roles=[
                 ProviderRole.PRODUCER, ProviderRole.PROCESSOR,
                 ProviderRole.LICENSOR
             ],
             url=("https://www.usgs.gov/landsat-missions/landsat-collection-2-"
                  "level-1-data")),
    Provider("Microsoft",
             roles=[ProviderRole.HOST],
             url="https://planetarycomputer.microsoft.com")
]
C2_L1_LICENSE = "proprietary"
C2_L1_LICENSE_LINK = Link(
    rel="license",
    target="https://www.usgs.gov/core-science-systems/hdds/data-policy",
    title="Public Domain")

L8_PLATFORM = "landsat-8"
L8_INSTRUMENTS = ["oli", "tirs"]

OLD_L8_EXTENSION_SCHEMA = "https://landsat.usgs.gov/stac/landsat-extension/schema.json"
L8_EXTENSION_SCHEMA = "https://landsat.usgs.gov/stac/landsat-extension/v1.1.0/schema.json"
L8_ITEM_DESCRIPTION = "Landsat Collection 2 Level-2 Surface Reflectance Product"

L8_SR_BANDS = {
    "SR_B1":
    Band({
        "name": "SR_B1",
        "common_name": "coastal",
        "gsd": 30,
        "center_wavelength": 0.44,
        "full_width_half_max": 0.02
    }),
    "SR_B2":
    Band({
        "name": "SR_B2",
        "common_name": "blue",
        "gsd": 30,
        "center_wavelength": 0.48,
        "full_width_half_max": 0.06
    }),
    "SR_B3":
    Band({
        "name": "SR_B3",
        "common_name": "green",
        "gsd": 30,
        "center_wavelength": 0.56,
        "full_width_half_max": 0.06
    }),
    "SR_B4":
    Band({
        "name": "SR_B4",
        "common_name": "red",
        "gsd": 30,
        "center_wavelength": 0.65,
        "full_width_half_max": 0.04
    }),
    "SR_B5":
    Band({
        "name": "SR_B5",
        "common_name": "nir08",
        "gsd": 30,
        "center_wavelength": 0.86,
        "full_width_half_max": 0.03
    }),
    "SR_B6":
    Band({
        "name": "SR_B6",
        "common_name": "swir16",
        "gsd": 30,
        "center_wavelength": 1.6,
        "full_width_half_max": 0.08
    }),
    "SR_B7":
    Band({
        "name": "SR_B7",
        "common_name": "swir22",
        "gsd": 30,
        "center_wavelength": 2.2,
        "full_width_half_max": 0.2
    })
}

L8_SP_BANDS = {
    # L2SP only bands

    #  ST_B10 Note:
    # Changed common_name from UGSG STAC - should be lwir11 based on wavelength
    # Also, resolution at sensor is 100m, even though the raster is 30m pixel width/height.
    "ST_B10":
    Band({
        "name": "ST_B10",
        "common_name": "lwir11",
        "gsd": 100.0,
        "center_wavelength": 10.9,
        "full_width_half_max": 0.8
    }),
    "ST_ATRAN":
    Band({
        "name": "ST_ATRAN",
        "description": "atmospheric transmission",
        "gsd": 30
    }),
    "ST_CDIST":
    Band({
        "name": "ST_CDIST",
        "description": "distance to nearest cloud",
        "gsd": 30
    }),
    "ST_DRAD":
    Band({
        "name": "ST_DRAD",
        "description": "downwelled radiance",
        "gsd": 30
    }),
    "ST_URAD":
    Band({
        "name": "ST_URAD",
        "description": "upwelled radiance",
        "gsd": 30
    }),
    "ST_TRAD":
    Band({
        "name": "ST_TRAD",
        "description": "thermal radiance",
        "gsd": 30
    }),
    "ST_EMIS":
    Band({
        "name": "ST_EMIS",
        "description": "emissivity",
        "gsd": 30
    }),
    "ST_EMSD":
    Band({
        "name": "ST_EMSD",
        "description": "emissivity standard deviation",
        "gsd": 30
    })
}
