
from dateutil import parser
from datetime import datetime, timezone

from pystac import Item

from stactools.landsat.ang_metadata import AngMetadata
# from pystac.extensions.view import ViewExtension

# item = Item
# v = ViewExtension.ext(item, add_if_missing=True)
# v.


class StacMetadata:
    """Structure to hold values from a USGS STAC Item json file."""

    def __init__(self, item: Item):
        self.id = item.id

        properties = item.properties

        self.view_sun_azimuth = properties.get("view:sun_azimuth") or properties.get("eo:sun_azimuth")
        self.view_sun_elevation = properties.get("view:sun_elevation") or properties.get("eo:sun_elevation")
        self.view_off_nadir = properties.get("view:off_nadir") or properties.get("eo:off_nadir")

        item_time = parser.parse(properties["datetime"]).astimezone(timezone.utc)
        self.datetime = item_time.isoformat().replace("+00:00", "Z")

        self.eo_cloud_cover = properties["eo:cloud_cover"]
        self.platform = item.properties["platform"].lower().replace("_", "-")
        self.instruments = [i.lower() for i in properties["instruments"]]

        self.landsat = {key: value for key, value in properties.items() if "landsat" in key}
        if self.landsat.get("landsat:correction") is None:
            self.landsat["landsat:correction"] = item.id[5:9]



use_usgs_stac = False
geometry = None
if use_usgs_stac:
    stac_metadata = StacMetadata(mtl_xml_href, read_href_modifier)
    geometry = StacMetadata.scene_geometry()

if geometry is None:
    ang_metadata = AngMetadata()
    geometry = ang_metadata.get_scene_geometry()

