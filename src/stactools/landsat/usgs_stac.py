from datetime import datetime, timezone
import os
from enum import Enum
from typing import Any, Dict, Optional, List, Union
import copy

from pystac import Asset, Collection, Item, MediaType, Link, RelType
from pystac.extensions.item_assets import ItemAssetsExtension, AssetDefinition
from pystac.extensions.eo import EOExtension, Band
from stactools.core.utils import href_exists
from stactools.core.io import ReadHrefModifier

from stactools.landsat import constants
from stactools.landsat.constants import INSTRUMENT_EO_BANDS, COMMON_ASSETS, INSTRUMENT_ASSETS, INSTRUMENT_KEYS


class Sensor(Enum):
    MSS = "M"
    TM = "T"
    ETM = "E"

class InstrumentKey(Enum):
    M = "MSS"
    T = "TM_ETM"
    E = "TM_ETM"

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

    # generate a new item with no assets
    item = format_usgs_item(copy.deepcopy(usgs_items[0]))

    # add common assets to the new item
    base_asset_href = os.path.dirname(mtl_xml_href)
    usgs_common_keys = add_common_assets(item, usgs_items[0], base_asset_href)

    # for each usgs item, add the non-common assets to the new item
    for usgs_item in usgs_items:
        add_remaining_assets(item, usgs_item, usgs_common_keys, base_asset_href)

    # # generate formatted assets, potentially from more than one item
    # assets = {}
    # base_asset_href = os.path.dirname(mtl_xml_href)
    # for usgs_item in usgs_items:
    #     item = format_usgs_assets(item, usgs_item, base_asset_href)
    #     # assets.update(formatted_assets)

    # add formatted assets to formatted item
    # for key, value in assets.items():
    #     item.add_asset(key, value)

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

    sensor = Sensor(base_filename[1])
    items = []
    if sensor is Sensor.TM or sensor is Sensor.ETM:
        for product in ["SR", "ST"]:
            href = f"{base_file_href}_{product}_stac.json"
            item = _read_item(href, read_href_modifier)
            if item is not None:
                items.append(item)
    elif sensor is Sensor.MSS:
        href = f"{base_file_href}_stac.json"
        item = _read_item(href, read_href_modifier)
        items.append(item)

    return items


def format_usgs_item(item: Item) -> Item:
    # item.stac_extensions.clear()
    # item.stac_extensions.extend(
    #     [
    #         "https://landsat.usgs.gov/stac/landsat-extension/v1.1.1/schema.json",
    #         "https://stac-extensions.github.io/view/v1.0.0/schema.json",
    #         "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
    #         "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
    #         "https://stac-extensions.github.io/alternate-assets/v1.1.0/schema.json"
    #     ]
    # )
    item.stac_extensions.remove(
        "https://stac-extensions.github.io/storage/v1.0.0/schema.json")
    item.stac_extensions.remove(
        "https://stac-extensions.github.io/file/v1.0.0/schema.json")

    id_parts = item.id.split('_')
    sensor = Sensor(item.id[1])
    if sensor is Sensor.TM or sensor is Sensor.ETM:
        item.id = '_'.join(id_parts[:4] + id_parts[-3:-1])
        item.properties["description"] = "Landsat Collection 2 Level-2 Product"
    elif sensor is Sensor.MSS:
        item.id = '_'.join(id_parts[:4] + id_parts[-2:])
        item.properties["description"] = "Landsat Collection 2 Level-1 Product"


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


def add_common_assets(new_item: Item, usgs_item: Item, new_base_href: str) -> List[str]:
    usgs_assets = usgs_item.get_assets()
    sensor = Sensor(usgs_item.id[1])
    level = usgs_item.id[6]

    common_usgs_keys = []
    for new_key in COMMON_ASSETS.keys():
        if new_key == "ANG":
            usgs_key = "ANG.txt"
        elif "QA" in new_key:
            if sensor is Sensor.MSS or sensor is Sensor.TM:
                usgs_key = new_key.lower()
            elif sensor is Sensor.ETM:
                usgs_key = f"{new_key}.TIF"
        else:
            usgs_key = new_key

        usgs_asset = usgs_assets.get(usgs_key)
        if usgs_asset is not None:
            new_asset_dict = constants.COMMON_ASSETS[new_key]
            new_asset_dict = add_asset_hrefs(new_asset_dict, usgs_asset.href, new_base_href)
            if "MTL" in new_key:
                new_asset_dict["description"] = new_asset_dict["description"].replace("Level-X", f"Level-{level}")

            new_item.add_asset(new_key, Asset.from_dict(new_asset_dict))
            common_usgs_keys.append(usgs_key)

    return common_usgs_keys


def add_remaining_assets(new_item: Item, usgs_item: Item, usgs_common_keys:str, new_base_href: str) -> None:
    usgs_assets = usgs_item.get_assets()
    [usgs_assets.pop(key) for key in usgs_common_keys]
    usgs_assets.pop("index")

    instrument_key = INSTRUMENT_KEYS[usgs_item.id[1]]
    new_assets = INSTRUMENT_ASSETS[instrument_key]
    new_bands = INSTRUMENT_EO_BANDS[instrument_key]

    for usgs_asset_key in usgs_assets.keys():
        usgs_asset = usgs_assets.get(usgs_asset_key)

        new_asset_key = os.path.splitext(os.path.basename(usgs_asset.href))[0][41:]

        new_asset_dict = new_assets[new_asset_key]
        new_asset_dict = add_asset_hrefs(new_asset_dict, usgs_asset.href, new_base_href)
        new_asset_dict["type"] = MediaType.COG

        new_item.add_asset(new_asset_key, Asset.from_dict(new_asset_dict))

        band = new_bands.get(new_asset_key, None)
        if band is not None:
            new_asset = new_item.assets[new_asset_key]
            eo = EOExtension.ext(new_asset, add_if_missing=True)
            eo.bands = [Band.create(**band)]


def add_asset_hrefs(new_dict: Dict[str, Any], usgs_href: str, new_base_href: str) -> Dict[str, Any]:
    new_dict["alternate"] = {
        "usgs": {
            "title": "USGS asset location",
            "href": usgs_href
        }
    }
    filename = os.path.basename(usgs_href)
    new_dict["href"] = os.path.join(new_base_href, filename)
    return new_dict
