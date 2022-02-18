from datetime import datetime, timezone
import os
from enum import Enum
from typing import Dict, Optional, List
import copy

from pystac import Asset, Item, MediaType
from stactools.core.utils import href_exists
from stactools.core.io import ReadHrefModifier


class Instrument(Enum):
    MSS = "M"
    TM = "T"


class ItemFromFileError(Exception):
    """Unable to read Item from local or remote JSON file."""


def convert_usgs_stac(
        mtl_xml_href: str,
        read_href_modifier: Optional[ReadHrefModifier] = None) -> Item:

    # retrieve available stac items
    usgs_items = get_usgs_items(mtl_xml_href, read_href_modifier)

    # generate a formatted item with no assets
    item = format_usgs_item(copy.deepcopy(usgs_items[0]))

    # generate formatted assets, potentially from more than one JSON file
    assets = {}
    base_asset_href = os.path.dirname(mtl_xml_href)
    for usgs_item in usgs_items:
        formatted_assets = format_usgs_assets(usgs_item, base_asset_href)
        assets.update(formatted_assets)

    # add formatted assets to formatted item
    for key, value in assets.items():
        item.add_asset(key, value)

    return item


def get_usgs_items(
        mtl_xml_href: str,
        read_href_modifier: Optional[ReadHrefModifier] = None) -> List[Item]:

    def _read_item(href: str,
                   read_href_modifier: Optional[ReadHrefModifier]) -> Item:
        if read_href_modifier is not None:
            new_href = read_href_modifier(href)
        else:
            new_href = href
        if href_exists(new_href):
            item = Item.from_file(new_href)
            return item
        else:
            raise ItemFromFileError(f"Unable to read Item from {new_href}.")

    base_href, xml_filename = os.path.split(mtl_xml_href)
    base_filename = '_'.join(xml_filename.split('_')[:-1])
    base_file_href = os.path.join(base_href, base_filename)

    sensor = Instrument(base_filename[1])
    items = []
    if sensor is Instrument.TM:
        for product in ["SR", "ST"]:
            href = f"{base_file_href}_{product}_stac.json"
            item = _read_item(href, read_href_modifier)
            items.append(item)
    elif sensor is Instrument.MSS:
        href = f"{base_file_href}_stac.json"
        item = _read_item(href, read_href_modifier)
        items.append(item)

    return items


def format_usgs_item(stac_item: Item) -> Item:
    item = stac_item.to_dict(transform_hrefs=False)
    extensions = item["stac_extensions"]
    properties = item["properties"]
    links = item["links"]

    # remove unused extensions
    extensions = [e for e in extensions if "/file/" not in e]
    extensions = [e for e in extensions if "/storage/" not in e]
    item["stac_extensions"] = extensions

    # sensor specific
    id_parts = item["id"].split('_')
    instrument = Instrument(item["id"][1])
    if instrument is Instrument.TM:
        item["id"] = '_'.join(id_parts[:4] + id_parts[-3:-1])
        properties["description"] = "Landsat Collection 2 Level-2 Product"
    elif instrument is Instrument.MSS:
        item["id"] = '_'.join(id_parts[:4] + id_parts[-2:])
        properties["description"] = "Landsat Collection 2 Level-1 Product"

    properties.pop("proj:shape")
    properties.pop("proj:transform")
    properties["platform"] = properties["platform"].lower().replace("_", "-")
    properties["instruments"] = [i.lower() for i in properties["instruments"]]
    # properties["landsat:processing_level"] = properties.pop("landsat:correction")
    properties["created"] = datetime.now(tz=timezone.utc).isoformat().replace(
        "+00:00", "Z")
    item["properties"] = dict(sorted(properties.items()))

    # alternate usgs stac browser
    self_link_dict = next(lnk for lnk in links if lnk["rel"] == "self")
    self_href = self_link_dict["href"]
    browse_link, _ = os.path.split(self_href)
    browse_link = browse_link.replace("/data/", "/stac-browser/")
    alternate_link = {
        "rel": "alternate",
        "href": browse_link,
        "type": "text/html",
        "title": "USGS stac-browser page"
    }
    item["links"] = [alternate_link]

    item["assets"] = {}
    item.pop("collection")
    item.pop("description")

    item = Item.from_dict(item)

    return item


def format_usgs_assets(item: Item, base_asset_href: str) -> Dict[str, Asset]:
    assets = item.get_assets()
    formatted_assets = {}

    # remove unused assets
    assets.pop("index")

    # format the common assets
    common_asset_keys = [
        "thumbnail", "reduced_resolution_browse", "MTL.json", "MTL.txt",
        "MTL.xml", "ANG.txt"
    ]
    for asset_key in common_asset_keys:
        asset = assets.get(asset_key)
        if asset is None:
            continue
        else:
            asset = asset.to_dict()

        filename = os.path.basename(asset["href"])
        href = os.path.join(base_asset_href, filename)

        asset["alternate"] = {"usgs": asset["href"]}
        asset["href"] = href

        asset.pop("file:checksum")

        if asset_key == "ANG.txt":
            formatted_assets["ANG"] = Asset.from_dict(asset)
        else:
            formatted_assets[asset_key] = Asset.from_dict(asset)

        assets.pop(asset_key)

    # only the full-size spatial assets should remain now

    for asset_key in assets.keys():
        asset = assets.get(asset_key).to_dict()

        filename = os.path.basename(asset["href"])
        href = os.path.join(base_asset_href, filename)

        asset["alternate"] = {"usgs": asset["href"]}
        asset["href"] = href

        asset["type"] = MediaType.COG

        asset["proj:shape"] = item.properties["proj:shape"]
        asset["proj:transform"] = item.properties["proj:transform"]

        asset.pop("file:checksum")

        name, _ = os.path.splitext(filename)
        new_key = name[41:]
        formatted_assets[new_key] = Asset.from_dict(asset)

    return formatted_assets
