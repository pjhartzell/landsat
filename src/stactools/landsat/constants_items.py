from enum import Enum

from pystac import MediaType


class Sensor(Enum):
    MSS = "M"
    TM = "T"
    ETM = "E"
    OLI_TIRS = "C"

INSTRUMENT = {
    "keys": {
        "M": "MSS",
        "T": "TM_ETM",
        "E": "TM_ETM",
        "C": "OLI_TIRS"
    },
    "lists": {
        "M": ["mss"],
        "T": ["tm"],
        "E": ["etm"],
        "C": ["oli", "tirs"]
    }
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
        "title": "Product Metadata File (txt)",
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
    "QA_RADSAT": {
        "type": MediaType.COG,
        "title": "Radiometric Saturation Quality Assessment Band",
        "description": "Collection 2 Level-1 Radiometric Saturation Quality Assessment Band",
        "roles": ["saturation"],
        "href_suffix": "QA_RADSAT.TIF"
    },
}

INSTRUMENT_ASSETS = {
    "MSS": {
        "SR": {
            "QA_PIXEL": {
                "title": "Pixel Quality Assessment Band",
                "description": "Collection 2 Level-1 Pixel Quality Assessment Band",
                "roles": ["cloud"],
            },
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
            }
        },
        "ST": None
    },
    "TM_ETM": {
        "SR": {
            "QA_PIXEL": {
                "title": "Pixel Quality Assessment Band",
                "description": "Collection 2 Level-1 Pixel Quality Assessment Band",
                "roles": ["cloud"],
            },
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
            }
        },
        "ST": {
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
        }
    }
}

INSTRUMENT_EO_BANDS = {
    "MSS": {
        "SR": {
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
        "ST": None
    },
    "TM_ETM": {
        "SR": {
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
        },
        "ST": {
            "ST_B6": {
                "name": "B6",
                "common_name": "lwir",
                "center_wavelength": 11.45
            }
        }
    }
}

INSTRUMENT_RASTER_BANDS = {
    "MSS": {
        "SR": {
            "B4": {
                "data_type": "uint8"
            },
            "B5": {
                "data_type": "uint8"
            },
            "B6": {
                "data_type": "uint8"
            },
            "B7": {
                "data_type": "uint8"
            }
        },
        "ST": None
    },
    "TM_ETM": {
        "SR": {
            "SR_B1": {
                "data_type": "uint16"
            },
            "SR_B2": {
                "data_type": "uint16"
            },
            "SR_B3": {
                "data_type": "uint16"
            },
            "SR_B4": {
                "data_type": "uint16"
            },
            "SR_B5": {
                "data_type": "uint16"
            },
            "SR_B7": {
                "data_type": "uint16"
            },
        },
        "ST": {
            "ST_B6": {
                "data_type": "uint16"
            }
        }
    }
}