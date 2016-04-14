import unittest
import task
from io import BytesIO
from lxml import etree

class TestTask(unittest.TestCase):

  def test_preserves_bounds(self):
    empty_osm = """<?xml version="1.0" encoding="UTF-8"?>
      <osm version="0.6" generator="CGImap 0.4.0 (21276 thorn-02.openstreetmap.org)" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">
        <bounds minlat="37.7772261" minlon="-122.5167847" maxlat="37.7793970" maxlon="-122.5140381"/>
      </osm>
    """
    changeset = task.changeset(BytesIO(empty_osm))
    self.assertTrue(changeset[0].tag == 'bounds')

  def test_preserves_referenced_nodes(self):
    empty_osm = """<?xml version="1.0" encoding="UTF-8"?>
      <osm>
        <bounds/>
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
    changeset = task.changeset(BytesIO(empty_osm))
    node = changeset[1]
    self.assertEqual(node.tag,'node')
    self.assertEqual(node.get("id"),"2")
    way = changeset[2]
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
    self.assertEqual(len(changeset),3)

if __name__ == '__main__':
    unittest.main()
