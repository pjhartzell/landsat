from datetime import datetime, timezone

from pystac import Extent, SpatialExtent, TemporalExtent, Provider, ProviderRole, Link


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
