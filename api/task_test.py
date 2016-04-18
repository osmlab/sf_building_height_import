import unittest
import task
from io import BytesIO
from lxml import etree

class TestTask(unittest.TestCase):

  def test_preserves_bounds(self):
    building_db = {}
    empty_osm = """<?xml version="1.0" encoding="UTF-8"?>
      <osm version="0.6" generator="CGImap 0.4.0 (21276 thorn-02.openstreetmap.org)" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">
        <bounds minlat="37.7772261" minlon="-122.5167847" maxlat="37.7793970" maxlon="-122.5140381"/>
      </osm>
    """
    changeset = task.changeset(BytesIO(empty_osm),building_db)
    self.assertTrue(changeset[0].tag == 'bounds')

  def test_preserves_only_referenced(self):
    building_db = {'10':(5,0.9)}
    empty_osm = """<?xml version="1.0" encoding="UTF-8"?>
      <osm>
        <node id="1"/>
        <node id="2"/>
        <node id="3"/>
        <way id="10">
          <nd ref="2"/>
          <tag k="building" v="yes"/>
          <tag k="foo" v="bar"/>
        </way>
        <way id="11">
          <nd ref="3"/>
        </way>
      </osm>
    """
    changeset = task.changeset(BytesIO(empty_osm),building_db)
    node = changeset[0]
    self.assertEqual(node.tag,'node')
    self.assertEqual(node.get("id"),"2")
    way = changeset[1]
    self.assertEqual(way.get("id"),"10")

    # retains referenced nodes
    self.assertEqual(way[0].tag,"nd")
    self.assertEqual(way[0].get("ref"),"2")
    self.assertEqual(way[1].tag,"tag")

    # retains building tag
    self.assertEqual(way[1].get("k"),"building")
    self.assertEqual(way[1].get("v"),"yes")
    self.assertEqual(way[2].tag,"tag")

    # retains other tags
    self.assertEqual(way[2].get("k"),"foo")
    self.assertEqual(way[2].get("v"),"bar")

    #does not include unreferenced nodes or ways
    self.assertEqual(len(changeset),2)

  def test_adds_heights(self):
    building_db = {'1':(5,0.9),'2':(5,0.2)}
    empty_osm = """<?xml version="1.0" encoding="UTF-8"?>
      <osm>
        <way id="1">
          <tag k="building" v="yes"/>
        </way>
        <way id="2">
          <tag k="building" v="yes"/>
        </way>
        <way id="3">
          <tag k="building" v="yes"/>
        </way>
      </osm>
    """
    changeset = task.changeset(BytesIO(empty_osm),building_db)

    # adds heights with high confidence
    way = changeset[0]
    self.assertEqual(way.get("id"),"1")
    self.assertEqual(way[1].tag,"tag")
    self.assertEqual(way[1].get("k"),"height")
    self.assertEqual(way[1].get("v"),"5")

    # retains buildings, but does not add heights if not high confidence
    way = changeset[1]
    self.assertEqual(way.get("id"),"2")
    self.assertEqual(len(way),1)

    # does not retain buildings if not appearing in height db
    self.assertEqual(len(changeset), 2)

  def test_preserves_heights(self):
    building_db = {'1':(5,0.9)}
    empty_osm = """<?xml version="1.0" encoding="UTF-8"?>
      <osm>
        <way id="1">
          <tag k="building" v="yes"/>
          <tag k="height" v="20"/>
        </way>
      </osm>
    """
    changeset = task.changeset(BytesIO(empty_osm),building_db)

    # does not overwrite existing heights
    self.assertEqual(len(changeset), 0)

if __name__ == '__main__':
    unittest.main()
