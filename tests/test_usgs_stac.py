import os
import unittest
from stactools.landsat.usgs_stac import convert_usgs_stac


class UsgsStacTest(unittest.TestCase):

    def test_tm(self):
        mtl_xml_href = "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_MTL.xml"  # noqa

        item = convert_usgs_stac(mtl_xml_href)
        item.validate()

        destination = "examples/usgs-stac-convert/tm"
        item_path = os.path.join(destination, f"{item.id}.json")
        item.set_self_href(item_path)
        item.save_object()

    def test_mss(self):
        mtl_xml_href = "tests/data-files/usgs-stac/mss/LM01_L1GS_001010_19720908_20200909_02_T2_MTL.xml"  # noqa

        item = convert_usgs_stac(mtl_xml_href)
        item.validate()

        destination = "examples/usgs-stac-convert/mss"
        item_path = os.path.join(destination, f"{item.id}.json")
        item.set_self_href(item_path)
        item.save_object()

    def test_read_href_modifier(self):
        mtl_xml_href = "tests/data-files/usgs-stac/tm/LT04_L2SP_002026_19830110_20200918_02_T1_MTL.xml"  # noqa
        did_it = False

        def do_it(href: str) -> str:
            nonlocal did_it
            did_it = True
            return href

        convert_usgs_stac(mtl_xml_href, read_href_modifier=do_it)
        assert did_it
