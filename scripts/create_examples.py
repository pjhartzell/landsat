import os

from pystac import CatalogType, Link

# from stactools.landsat.usgs_stac import create_collection_c2l1
from stactools.landsat.stac import create_stac_item

# Item: Multi Spectral Scanner (MSS), Collection 2 Level-1, Landsat 1-5
mtl_xml_href = "tests/data-files/usgs-stac/mss/LM01_L1GS_001010_19720908_20200909_02_T2_MTL.xml"
item = create_stac_item(mtl_xml_href, use_usgs_stac=False)
item.validate()
destination = "examples/items/mss"
item_path = os.path.join(destination, f"{item.id}.json")
item.set_self_href(item_path)
item.save_object(include_self_link=False)

# Item: Thematic Mapper (TM), Collection 2 Level-2, Landsat 4-5
mtl_xml_href = "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_MTL.xml"  # noqa
item = create_stac_item(mtl_xml_href, use_usgs_stac=False)
item.validate()
destination = "examples/items/tm"
item_path = os.path.join(destination, f"{item.id}.json")
item.set_self_href(item_path)
item.save_object(include_self_link=False)

# Item: Enhanced Thematic Mapper (ETM+), Collection 2 Level-2, Landsat 7
mtl_xml_href = "tests/data-files/usgs-stac/etm/LE07_L2SP_021030_20100109_20200911_02_T1_MTL.xml"  # noqa
item = create_stac_item(mtl_xml_href, use_usgs_stac=False)
item.validate()
destination = "examples/items/etm"
item_path = os.path.join(destination, f"{item.id}.json")
item.set_self_href(item_path)
item.save_object(include_self_link=False)

# Item: Operational Land Imager-Thermal InfraRed Sensor (OLI-TIRS)
# # Collection 2 Level-2, Landsat 8-9
mtl_xml_href = "tests/data-files/assets4/LC08_L2SP_017036_20130419_20200913_02_T2_MTL.xml"  # noqa
item = create_stac_item(mtl_xml_href, use_usgs_stac=False)
# This is a hack to get validation working, since v1.1.0 of the
# landsat schema lists "collection" as a required property.
item.collection_id = "landsat-8-c2-l2"
item.links.append(Link(rel="collection", target="http://example.com"))
item.validate()
destination = "examples/items/oli-tirs"
item_path = os.path.join(destination, f"{item.id}.json")
item.set_self_href(item_path)
item.save_object(include_self_link=False)




# # Collection: Collection 2 Level-1 data (MSS)
# mtl_xml_href = "tests/data-files/usgs-stac/mss/LM01_L1GS_001010_19720908_20200909_02_T2_MTL.xml"  # noqa
# collection = create_collection_c2l1(mtl_xml_href)
# destination = "examples/collections"
# collection_path = os.path.join(destination, f"{collection.id}.json")
# collection.set_self_href(collection_path)
# collection.save(catalog_type=CatalogType.SELF_CONTAINED)
