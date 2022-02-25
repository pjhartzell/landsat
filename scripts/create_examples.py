import os

from pystac import CatalogType

# from stactools.landsat.usgs_stac import create_collection_c2l1
from stactools.landsat.stac import create_item

# Item: Multi Spectral Scanner (MSS), Collection 2 Level-1, Landsat 1-5
mtl_xml_href = "/Users/pjh/data/landsat-c2/level-1/standard/mss/1972/001/010/LM01_L1GS_001010_19720908_20200909_02_T2/LM01_L1GS_001010_19720908_20200909_02_T2_MTL.xml"  # noqa
item = create_item(mtl_xml_href, use_usgs_stac=False)
import json
print(json.dumps(item.to_dict(), indent=4))
item.validate()
destination = "examples/items/usgs-stac-convert/mss_new"
item_path = os.path.join(destination, f"{item.id}.json")
item.set_self_href(item_path)
item.save_object(include_self_link=False)

# # Item: OLI-TIRS (OLI-TIRS), Collection 2 Level-2, Landsat 8-9
# mtl_xml_href = "tests/data-files/assets4/LC08_L2SP_017036_20130419_20200913_02_T2_MTL.xml"  # noqa
# item = create_item(mtl_xml_href, use_usgs_stac=False)
# item.validate()
# destination = "examples/items/usgs-stac-convert/tm"
# item_path = os.path.join(destination, f"{item.id}.json")
# item.set_self_href(item_path)
# item.save_object(include_self_link=False)

# # Item: Enhanced Thematic Mapper (ETM+), Collection 2 Level-2, Landsat 7
# mtl_xml_href = "tests/data-files/usgs-stac/etm/LE07_L2SP_021030_20100109_20200911_02_T1_MTL.xml"  # noqa
# item = create_item_from_usgs(mtl_xml_href)
# item.validate()
# destination = "examples/items/usgs-stac-convert/etm"
# item_path = os.path.join(destination, f"{item.id}.json")
# item.set_self_href(item_path)
# item.save_object(include_self_link=False)


# # Collection: Collection 2 Level-1 data (MSS)
# mtl_xml_href = "tests/data-files/usgs-stac/mss/LM01_L1GS_001010_19720908_20200909_02_T2_MTL.xml"  # noqa
# collection = create_collection_c2l1(mtl_xml_href)
# destination = "examples/collections"
# collection_path = os.path.join(destination, f"{collection.id}.json")
# collection.set_self_href(collection_path)
# collection.save(catalog_type=CatalogType.SELF_CONTAINED)