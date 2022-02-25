from typing import Optional
import logging

from shapely.geometry import box, mapping
import pystac
from pystac.extensions.eo import EOExtension, Band
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.view import ViewExtension
from stactools.core.io import ReadHrefModifier

from stactools.landsat.assets import (ANG_ASSET_DEF, COMMON_ASSET_DEFS,
                                      SR_ASSET_DEFS, THERMAL_ASSET_DEFS)
from stactools.landsat.constants import (COMMON_ASSETS, INSTRUMENT_ASSETS,
                                         INSTRUMENT_EO_BANDS, INSTRUMENT,
                                         LANDSAT_EXTENSION_SCHEMA,
                                         L8_INSTRUMENTS, L8_ITEM_DESCRIPTION,
                                         L8_PLATFORM, L8_EXTENSION_SCHEMA,
                                         Sensor)
from stactools.landsat.mtl_metadata import MtlMetadata
from stactools.landsat.ang_metadata import AngMetadata

logger = logging.getLogger(__name__)


def create_item(
        mtl_xml_href: str,
        use_usgs_stac: bool,
        read_href_modifier: Optional[ReadHrefModifier] = None) -> pystac.Item:
    """Creates Landsat 1-5 Collection 2 Level-1 STAC Items and Landsat 4-5, 7-9
    Collection 2 Level-2 STAC Items.

    Uses the MTL XML HREF as the bases for other files; assumes that all
    files are co-located in a directory or blob prefix.
    """
    base_href = '_'.join(mtl_xml_href.split('_')[:-1])  # Remove the _MTL.txt

    mtl_metadata = MtlMetadata.from_file(mtl_xml_href, read_href_modifier)

    sensor = Sensor(mtl_metadata.item_id[1])
    satellite = int(mtl_metadata.item_id[2:4])
    level = int(mtl_metadata.item_id[6])

    # Don't change existing landsat 8 Item creation
    if satellite == 8:
        ang_href = ANG_ASSET_DEF.get_href(base_href)
        ang_metadata = AngMetadata.from_file(ang_href, read_href_modifier)
        scene_geometry = ang_metadata.get_scene_geometry(mtl_metadata.bbox)

        item = pystac.Item(id=mtl_metadata.item_id,
                        bbox=mtl_metadata.bbox,
                        geometry=scene_geometry,
                        datetime=mtl_metadata.scene_datetime,
                        properties={})

        item.common_metadata.platform = L8_PLATFORM
        item.common_metadata.instruments = L8_INSTRUMENTS
        item.common_metadata.description = L8_ITEM_DESCRIPTION

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        eo.cloud_cover = mtl_metadata.cloud_cover

        # view
        view = ViewExtension.ext(item, add_if_missing=True)
        view.off_nadir = mtl_metadata.off_nadir
        view.sun_elevation = mtl_metadata.sun_elevation
        view.sun_azimuth = mtl_metadata.sun_azimuth

        # projection
        projection = ProjectionExtension.ext(item, add_if_missing=True)
        projection.epsg = mtl_metadata.epsg
        projection.bbox = mtl_metadata.proj_bbox

        # landsat8
        item.stac_extensions.append(L8_EXTENSION_SCHEMA)
        item.properties.update(**mtl_metadata.landsat_metadata)

        # -- Add assets

        # Add common assets
        for asset_definition in COMMON_ASSET_DEFS:
            asset_definition.add_asset(item, mtl_metadata, base_href)

        # Add SR assets
        for asset_definition in SR_ASSET_DEFS:
            asset_definition.add_asset(item, mtl_metadata, base_href)

        # Add thermal assets, if this is a L2SP product
        if mtl_metadata.processing_level == 'L2SP':
            for asset_definition in THERMAL_ASSET_DEFS:
                asset_definition.add_asset(item, mtl_metadata, base_href)

    else:
        scene_geometry = None
        if use_usgs_stac:
            # get usgs stac metadata (geometry, asset hrefs keyed by new key names for alternate asset use)
            pass
        if scene_geometry is None and sensor is not Sensor.MSS:
            ang_href = ANG_ASSET_DEF.get_href(base_href)
            ang_metadata = AngMetadata.from_file(ang_href, read_href_modifier)
            scene_geometry = ang_metadata.get_scene_geometry(mtl_metadata.bbox)
        else:
            scene_geometry = mapping(box(*mtl_metadata.bbox))
            logger.warning(f"Using bbox for geometry for item generated from {mtl_xml_href}.")

        item = pystac.Item(id=mtl_metadata.item_id,
                        bbox=mtl_metadata.bbox,
                        geometry=scene_geometry,
                        datetime=mtl_metadata.scene_datetime,
                        properties={})

        item.common_metadata.platform = f"landsat-{satellite}"
        item.common_metadata.instruments = INSTRUMENT["lists"][sensor.value]
        item.common_metadata.description = f"Landsat Collection 2 Level-{level} Product"

        # -- EO
        eo = EOExtension.ext(item, add_if_missing=True)
        eo.cloud_cover = mtl_metadata.cloud_cover

        # -- View
        view = ViewExtension.ext(item, add_if_missing=True)
        view.off_nadir = mtl_metadata.off_nadir
        view.sun_elevation = mtl_metadata.sun_elevation
        view.sun_azimuth = mtl_metadata.sun_azimuth

        # -- Projection
        projection = ProjectionExtension.ext(item, add_if_missing=True)
        projection.epsg = mtl_metadata.epsg
        # TODO: Fix/Check This!
        #   - Assumes reflectance and thermal shapes always match (is there any
        #     case where they would not?)
        #   - Assumes reflectance will always exist (nighttime = only thermal?)
        #   - I have yet to see an instance of either
        projection.shape = mtl_metadata.sr_shape
        projection.transform = mtl_metadata.sr_transform

        # -- Landsat
        item.stac_extensions.append(LANDSAT_EXTENSION_SCHEMA)
        item.properties.update(**mtl_metadata.landsat_metadata)

        # -- Add common assets
        for key, asset_dict in COMMON_ASSETS.items():
            asset_dict["href"] = f"{base_href}_{asset_dict.pop('href_suffix')}"
            # MTL files are specific to the processing level
            if "MTL" in key:
                asset_dict["description"].replace("Level-X", f"Level-{level}")
            item.add_asset(key, pystac.Asset.from_dict(asset_dict))
        # MSS data does not have an angle file
        if key == "ANG" and sensor is Sensor.MSS:
            item.assets.pop("ANG", None)

        # -- Add optical assets
        instrument_key = INSTRUMENT["keys"][sensor.value]
        assets = INSTRUMENT_ASSETS[instrument_key]["SR"]
        bands = INSTRUMENT_EO_BANDS[instrument_key]["SR"]
        for key, asset_dict in assets.items():
            asset_dict["type"] = pystac.MediaType.COG
            asset_dict["href"] = f"{base_href}_{key}.TIF"
            item.add_asset(key, pystac.Asset.from_dict(asset_dict))
            band = bands.get(key, None)
            if band is not None:
                asset = item.assets[key]
                eo = EOExtension.ext(asset, add_if_missing=True)
                eo.bands = [Band.create(**band)]

        # -- Add thermal assets (can only exist if optical exists; no nighttime)
        if mtl_metadata.processing_level == 'L2SP':
            assets = INSTRUMENT_ASSETS[instrument_key]["ST"]
            bands = INSTRUMENT_EO_BANDS[instrument_key]["ST"]
            for key, asset_dict in assets.items():
                asset_dict["type"] = pystac.MediaType.COG
                asset_dict["href"] = f"{base_href}_{key}.TIF"
                item.add_asset(key, pystac.Asset.from_dict(asset_dict))
                band = bands.get(key, None)
                if band is not None:
                    asset = item.assets[key]
                    eo = EOExtension.ext(asset, add_if_missing=True)
                    eo.bands = [Band.create(**band)]

    # -- Add links
    instrument_dir = "-".join(i for i in INSTRUMENT["lists"][sensor.value])
    usgs_item_page = (
        f"https://landsatlook.usgs.gov/stac-browser/collection02/level-{level}"
        f"/standard/{instrument_dir}"
        f"/{mtl_metadata.scene_datetime.year}"
        f"/{mtl_metadata.wrs_path}/{mtl_metadata.wrs_row}"
        f"/{mtl_metadata.product_id}")

    item.add_link(
        pystac.Link(rel="alternate",
                    target=usgs_item_page,
                    title="USGS stac-browser page",
                    media_type="text/html"))

    return item
