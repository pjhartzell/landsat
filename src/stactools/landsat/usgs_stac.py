from datetime import datetime, timezone
import os
from enum import Enum
from typing import Dict, Optional, List, Union
import copy

from pystac import Asset, Collection, Item, MediaType, Link, RelType
from pystac.extensions.item_assets import ItemAssetsExtension, AssetDefinition
from stactools.core.utils import href_exists
from stactools.core.io import ReadHrefModifier

from stactools.landsat import constants


class Instrument(Enum):
    MSS = "M"
    TM = "T"


def create_collection_c2l1(
        mss_mtl_xml_href: str,
        read_href_modifier: Optional[ReadHrefModifier] = None) -> Item:
    """Note that collection 2 level-1 is *currently* exclusively MSS data"""

    collection = Collection(id=constants.C2_L1_ID,
                            description=constants.C2_L1_DESCRIPTION,
                            extent=constants.C2_L1_EXTENTS,
                            title=constants.C2_L1_TITLE,
                            providers=constants.C2_L1_PROVIDERS,
                            keywords=constants.C2_L1_KEYWORDS)

    collection.license = constants.C2_L1_LICENSE
    collection.add_link(constants.C2_L1_LICENSE_LINK)

    collection.summaries.add("platform",
                             [f"landsat-{n}" for n in [1, 2, 3, 4, 5]])
    collection.summaries.add("instruments", "mss")
    collection.summaries.add("gsd", 60)

    item = create_item_from_usgs(mss_mtl_xml_href, read_href_modifier)
    assets = item.get_assets()
    mss_eo_bands = []
    for key in ["B4", "B5", "B6", "B7"]:
        asset = assets.get(key)
        mss_eo_bands.append(asset.extra_fields["eo:bands"][0])
    collection.summaries.add("eo:bands", mss_eo_bands)

    item_assets = {}
    for key, asset in assets.items():
        asset_dict = asset.to_dict()
        asset_dict.pop("href", None)
        asset_dict.pop("alternate", None)
        asset_dict.pop("proj:shape", None)
        asset_dict.pop("proj:transform", None)
        item_assets[key] = AssetDefinition(asset_dict)
    item_assets_ext = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets_ext.item_assets = item_assets

    return collection


def create_item_from_usgs(
        mtl_xml_href: str,
        read_href_modifier: Optional[ReadHrefModifier] = None) -> Item:

    # retrieve available stac items
    usgs_items = get_usgs_items(mtl_xml_href, read_href_modifier)

    # generate a formatted item with no assets
    item = format_usgs_item(copy.deepcopy(usgs_items[0]))

    # generate formatted assets, potentially from more than one item
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

    def _read_item(
            href: str, read_href_modifier: Optional[ReadHrefModifier]
    ) -> Union[Item, None]:
        if read_href_modifier is not None:
            new_href = read_href_modifier(href)
        else:
            new_href = href
        if href_exists(new_href):
            item = Item.from_file(new_href)
            return item
        else:
            return None

    base_href, xml_filename = os.path.split(mtl_xml_href)
    base_filename = '_'.join(xml_filename.split('_')[:-1])
    base_file_href = os.path.join(base_href, base_filename)

    sensor = Instrument(base_filename[1])
    items = []
    if sensor is Instrument.TM:
        for product in ["SR", "ST"]:
            href = f"{base_file_href}_{product}_stac.json"
            item = _read_item(href, read_href_modifier)
            if item is not None:
                items.append(item)
    elif sensor is Instrument.MSS:
        href = f"{base_file_href}_stac.json"
        item = _read_item(href, read_href_modifier)
        items.append(item)

    return items


def format_usgs_item(item: Item) -> Item:
    item.stac_extensions.remove(
        "https://stac-extensions.github.io/storage/v1.0.0/schema.json")
    item.stac_extensions.remove(
        "https://stac-extensions.github.io/file/v1.0.0/schema.json")

    id_parts = item.id.split('_')
    instrument = Instrument(item.id[1])
    if instrument is Instrument.TM:
        item.id = '_'.join(id_parts[:4] + id_parts[-3:-1])
        item.properties["description"] = "Landsat Collection 2 Level-2 Product"
    elif instrument is Instrument.MSS:
        item.id = '_'.join(id_parts[:4] + id_parts[-2:])
        item.properties["description"] = "Landsat Collection 2 Level-1 Product"

    item.properties.pop("proj:shape")
    item.properties.pop("proj:transform")
    item.properties["platform"] = item.properties["platform"].lower().replace(
        "_", "-")
    item.properties["instruments"] = [
        i.lower() for i in item.properties["instruments"]
    ]
    item.properties["created"] = datetime.now(
        tz=timezone.utc).isoformat().replace("+00:00", "Z")

    self_href = item.get_self_href()
    data_href, _ = os.path.split(self_href)
    usgs_stac_browse_href = data_href.replace("/data/", "/stac-browser/")
    usgs_stac_browse_link = Link(RelType.ALTERNATE,
                                 usgs_stac_browse_href,
                                 media_type="text/html",
                                 title="USGS stac-browser page")
    item.clear_links()
    item.add_link(usgs_stac_browse_link)

    item.assets = {}
    item.set_collection(None)
    item.extra_fields.pop("description")

    return item


def format_usgs_assets(item: Item, base_asset_href: str) -> Dict[str, Asset]:
    assets = item.get_assets()
    formatted_assets = {}

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

        asset.extra_fields["alternate"] = {"usgs": asset.href}
        filename = os.path.basename(asset.href)
        new_href = os.path.join(base_asset_href, filename)
        asset.href = new_href

        asset.extra_fields.pop("file:checksum")

        if asset_key == "ANG.txt":
            formatted_assets["ANG"] = asset
        else:
            formatted_assets[asset_key] = asset

        assets.pop(asset_key)

    # only the full-size spatial assets should remain now

    for asset_key in assets.keys():
        asset = assets.get(asset_key)

        asset.extra_fields["alternate"] = {"usgs": asset.href}
        filename = os.path.basename(asset.href)
        new_href = os.path.join(base_asset_href, filename)
        asset.href = new_href

        asset.media_type = MediaType.COG

        asset.extra_fields["proj:shape"] = item.properties["proj:shape"]
        asset.extra_fields["proj:transform"] = item.properties[
            "proj:transform"]

        asset.extra_fields.pop("file:checksum")

        name, _ = os.path.splitext(filename)
        new_key = name[41:]
        formatted_assets[new_key] = asset

    return formatted_assets
