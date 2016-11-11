from lxml import etree
import csv

def height_db():
  db = {}
  with open('../output/heights.csv', 'rb') as csvfile:
    for row in csv.reader(csvfile, delimiter=','):
      db[row[0]] = row[1]
  return db

def should_add_way(elem,height_db):
  if not elem.tag == 'way':
    return False
  has_building_tag = len(elem.xpath("tag[@k='building' or @k='building:part']")) > 0
  missing_height = (len(elem.xpath("tag[@k='height']")) == 0)
  return has_building_tag and missing_height and height_db.has_key(elem.get("id"))

def changeset(xml_bytes, height_db):
  referenced_nodes = []
  context = etree.iterparse(xml_bytes)
  # collect referenced nodes
  for action, elem in context:
    if should_add_way(elem,height_db):
      referenced_nodes += elem.xpath("nd/@ref")

  xml_bytes.seek(0)
  context = etree.iterparse(xml_bytes)
  for action, elem in context:
    if elem.tag == 'node':
      if not elem.get('id') in referenced_nodes:
        elem.getparent().remove(elem)
    if elem.tag == 'way':
      if should_add_way(elem,height_db):
        height = height_db[elem.get("id")]
        elem.append(etree.Element('tag', k="height", v=str(height)))
        elem.set("action","modify")
      else:
        elem.getparent().remove(elem)
    if elem.tag == 'relation':
        elem.getparent().remove(elem)
  return context.root

if __name__ == '__main__':
  import sys
  with open(sys.argv[1],'r') as f:
    result = changeset(f,height_db())
    print etree.tostring(result)
