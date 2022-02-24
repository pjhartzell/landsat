from datetime import datetime, timezone
from pystac.extensions.eo import Band
from pystac import Extent, SpatialExtent, TemporalExtent, Provider, ProviderRole, Link, MediaType


COMMON_ASSETS = {
    "thumbnail": {
        "href": "",
        "type": "image/jpeg",
        "title": "Thumbnail image",
        "alternate": {
            "usgs": {
                "title": "USGS asset location",
                "href": ""
            }
        },
        "roles": [
            "thumbnail"
        ]
    },
    "reduced_resolution_browse": {
        "href": "",
        "type": "image/jpeg",
        "title": "Reduced resolution browse image",
        "alternate": {
            "usgs": {
                "title": "USGS asset location",
                "href": ""
            }
        },
        "roles": [
            "overview"
        ]
    },
    "MTL.json": {
        "href": "",
        "type": "application/json",
        "title": "Product Metadata File (json)",
        "description": "Collection 2 Level-X Product Metadata File (json)",
        "alternate": {
            "usgs": {
                "title": "USGS asset location",
                "href": ""
            }
        },
        "roles": [
            "metadata"
        ]
    },
    "MTL.txt": {
        "href": "",
        "type": "text/plain",
        "title": "Product Metadata File",
        "description": "Collection 2 Level-X Product Metadata File (MTL)",
        "alternate": {
            "usgs": {
                "title": "USGS asset location",
                "href": ""
            }
        },
        "roles": [
            "metadata"
        ]
    },
    "MTL.xml": {
        "href": "",
        "type": "application/xml",
        "title": "Product Metadata File (xml)",
        "description": "Collection 2 Level-X Product Metadata File (xml)",
        "alternate": {
            "usgs": {
                "title": "USGS asset location",
                "href": ""
            }
        },
        "roles": [
            "metadata"
        ]
    },
    "QA_PIXEL": {
        "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_QA_PIXEL.TIF",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "title": "Pixel Quality Assessment Band",
        "description": "Collection 2 Level-2 Pixel Quality Assessment Band Surface Temperature",
        "alternate": {
            "usgs": {
                "title": "USGS asset location",
                "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_QA_PIXEL.TIF"
            }
        },
        "roles": [
            "cloud",
            "cloud-shadow",
            "snow-ice",
            "water-mask"
        ]
    },
    "QA_RADSAT": {
        "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_QA_RADSAT.TIF",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "title": "Radiometric Saturation Quality Assessment Band",
        "description": "Collection 2 Level-2 Radiometric Saturation Quality Assessment Band Surface Temperature",
        "alternate": {
            "usgs": {
                "title": "USGS asset location",
                "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_QA_RADSAT.TIF"
            }
        },
        "roles": [
            "saturation"
        ]
    },
}

INSTRUMENT_ASSETS = {
    "MSS": {
        "B4": {
            "href": "",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Green Band (B4)",
            "description": "Collection 2 Level-1 Green Band (B4) Top of Atmosphere Radiance",
            "eo:bands": [
                {
                    "name": "B4",
                    "common_name": "green",
                    "gsd": 60,
                    "center_wavelength": 0.55
                }
            ],
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": ""
                }
            },
            "roles": [
                "data"
            ]
        },
        "B5": {
            "href": "",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Red Band (B5)",
            "description": "Collection 2 Level-1 Red Band (B5) Top of Atmosphere Radiance",
            "eo:bands": [
                {
                    "name": "B5",
                    "common_name": "red",
                    "gsd": 60,
                    "center_wavelength": 0.65
                }
            ],
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": ""
                }
            },
            "roles": [
                "data"
            ]
        },
        "B6": {
            "href": "",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Near Infrared Band 0.7 (B6)",
            "description": "Collection 2 Level-1 Near Infrared Band 0.7 (B6) Top of Atmosphere Radiance",
            "eo:bands": [
                {
                    "name": "B6",
                    "common_name": "nir08",
                    "gsd": 60,
                    "center_wavelength": 0.75
                }
            ],
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": ""
                }
            },
            "roles": [
                "data"
            ]
        },
        "B7": {
            "href": "",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Near Infrared Band 0.9 (B7)",
            "description": "Collection 2 Level-1 Near Infrared Band 0.9 (B7) Top of Atmosphere Radiance",
            "eo:bands": [
                {
                    "name": "B7",
                    "common_name": "nir09",
                    "gsd": 60,
                    "center_wavelength": 0.95
                }
            ],
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": ""
                }
            },
            "roles": [
                "data"
            ]
        },
    },
    "TM": {
        "SR_B1": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B1.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Blue Band (B1)",
            "description": "Collection 2 Level-2 Blue Band (B1) Surface Reflectance",
            "eo:bands": [
                {
                    "name": "B1",
                    "common_name": "blue",
                    "gsd": 30,
                    "center_wavelength": 0.49
                }
            ],
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B1.TIF"
                }
            },
            "roles": [
                "data"
            ]
        },
        "SR_B2": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B2.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Green Band (B2)",
            "description": "Collection 2 Level-2 Green Band (B2) Surface Reflectance",
            "eo:bands": [
                {
                    "name": "B2",
                    "common_name": "green",
                    "gsd": 30,
                    "center_wavelength": 0.56
                }
            ],
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B2.TIF"
                }
            },
            "roles": [
                "data"
            ]
        },
        "SR_B3": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B3.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Red Band (B3)",
            "description": "Collection 2 Level-2 Red Band (B3) Surface Reflectance",
            "eo:bands": [
                {
                    "name": "B3",
                    "common_name": "red",
                    "gsd": 30,
                    "center_wavelength": 0.66
                }
            ],
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B3.TIF"
                }
            },
            "roles": [
                "data"
            ]
        },
        "SR_B4": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B4.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Near Infrared Band 0.8 (B4)",
            "description": "Collection 2 Level-2 Near Infrared Band 0.8 (B4) Surface Reflectance",
            "eo:bands": [
                {
                    "name": "B4",
                    "common_name": "nir08",
                    "gsd": 30,
                    "center_wavelength": 0.84
                }
            ],
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B4.TIF"
                }
            },
            "roles": [
                "data",
                "reflectance"
            ]
        },
        "SR_B5": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B5.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Short-wave Infrared Band 1.6 (B5)",
            "description": "Collection 2 Level-2 Short-wave Infrared Band 1.6 (B6) Surface Reflectance",
            "eo:bands": [
                {
                    "name": "B5",
                    "common_name": "swir16",
                    "gsd": 30,
                    "center_wavelength": 1.65
                }
            ],
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B5.TIF"
                }
            },
            "roles": [
                "data",
                "reflectance"
            ]
        },
        "SR_B7": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B7.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Short-wave Infrared Band 2.2 (B7)",
            "description": "Collection 2 Level-2 Short-wave Infrared Band 2.2 (B7) Surface Reflectance",
            "eo:bands": [
                {
                    "name": "B7",
                    "common_name": "swir22",
                    "gsd": 30,
                    "center_wavelength": 2.22
                }
            ],
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_SR_B7.TIF"
                }
            },
            "roles": [
                "data",
                "reflectance"
            ]
        },
        "SR_ATMOS_OPACITY": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_SR_ATMOS_OPACITY.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Atmospheric Opacity Band",
            "description": "Collection 2 Level-2 Atmospheric Opacity Band Surface Reflectance",
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_SR_ATMOS_OPACITY.TIF"
                }
            },
            "roles": [
                "data"
            ]
        },
        "SR_CLOUD_QA": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_SR_CLOUD_QA.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Cloud Quality Analysis Band",
            "description": "Collection 2 Level-2 Cloud Quality Opacity Band Surface Reflectance",
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_SR_CLOUD_QA.TIF"
                }
            },
            "roles": [
                "metadata",
                "cloud",
                "cloud-shadow",
                "snow-ice",
                "water-mask"
            ]
        },
        "ST_B6": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_ST_B6.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Surface Temperature Band (B6)",
            "description": "Landsat Collection 2 Level-2 Surface Temperature Band (B6) Surface Temperature Product",
            "eo:bands": [
                {
                    "name": "B6",
                    "common_name": "lwir",
                    "gsd": 120,
                    "center_wavelength": 11.45
                }
            ],
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_ST_B6.TIF"
                }
            },
            "roles": [
                "data",
                "temperature"
            ]
        },
        "ST_ATRAN": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_ST_ATRAN.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Atmospheric Transmittance Band",
            "description": "Landsat Collection 2 Level-2 Atmospheric Transmittance Band Surface Temperature Product",
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_ST_ATRAN.TIF"
                }
            },
            "roles": [
                "data"
            ]
        },
        "ST_CDIST": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_ST_CDIST.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Cloud Distance Band",
            "description": "Landsat Collection 2 Level-2 Cloud Distance Band Surface Temperature Product",
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_ST_CDIST.TIF"
                }
            },
            "roles": [
                "data"
            ]
        },
        "ST_DRAD": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_ST_DRAD.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Downwelled Radiance Band",
            "description": "Landsat Collection 2 Level-2 Downwelled Radiance Band Surface Temperature Product",
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_ST_DRAD.TIF"
                }
            },
            "roles": [
                "data"
            ]
        },
        "ST_URAD": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_ST_URAD.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Upwelled Radiance Band",
            "description": "Landsat Collection 2 Level-2 Upwelled Radiance Band Surface Temperature Product",
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_ST_URAD.TIF"
                }
            },
            "roles": [
                "data"
            ]
        },
        "ST_TRAD": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_ST_TRAD.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Thermal Radiance Band",
            "description": "Landsat Collection 2 Level-2 Thermal Radiance Band Surface Temperature Product",
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_ST_TRAD.TIF"
                }
            },
            "roles": [
                "data"
            ]
        },
        "ST_EMIS": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_ST_EMIS.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Emissivity Band",
            "description": "Landsat Collection 2 Level-2 Emissivity Band Surface Temperature Product",
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_ST_EMIS.TIF"
                }
            },
            "roles": [
                "data"
            ]
        },
        "ST_EMSD": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_ST_EMSD.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Emissivity Standard Deviation Band",
            "description": "Landsat Collection 2 Level-2 Emissivity Standard Deviation Band Surface Temperature Product",
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_ST_EMSD.TIF"
                }
            },
            "roles": [
                "data"
            ]
        },
        "ST_QA": {
            "href": "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_ST_QA.TIF",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "title": "Surface Temperature Quality Assessment Band",
            "description": "Landsat Collection 2 Level-2 Surface Temperature Band Surface Temperature Product",
            "alternate": {
                "usgs": {
                    "title": "USGS asset location",
                    "href": "https://landsatlook.usgs.gov/data/collection02/level-2/standard/tm/1983/002/026/LT04_L2SP_002026_19830110_20200918_02_T1/LT04_L2SP_002026_19830110_20200918_02_T1_ST_QA.TIF"
                }
            },
            "roles": [
                "data"
            ]
        }
    },
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
