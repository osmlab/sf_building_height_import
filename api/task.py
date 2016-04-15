from lxml import etree
import csv

MIN_CONFIDENCE = 0.7

# handle building polygons, don't handle super-relations.

def height_db():
  db = {}
  with open('../output/heights.csv', 'rb') as csvfile:
    for row in csv.reader(csvfile, delimiter=','):
      db[row[0]] = (row[1],float(row[2]))
  return db

def is_building(elem):
  return len(elem.xpath("tag[@k='building' or @k='building:part']")) > 0

def changeset(xml_bytes, height_db):
  referenced_nodes = []
  context = etree.iterparse(xml_bytes)
  # collect referenced nodes
  for action, elem in context:
    if elem.tag == 'way' and is_building(elem):
      referenced_nodes += elem.xpath("nd/@ref")

  xml_bytes.seek(0)
  context = etree.iterparse(xml_bytes)
  for action, elem in context:
    if elem.tag == 'node':
      if not elem.get('id') in referenced_nodes:
        elem.getparent().remove(elem)
    if elem.tag == 'way':
      way_id = elem.get("id")
      if is_building(elem) and height_db.has_key(way_id):
        if height_db[way_id][1] > MIN_CONFIDENCE:
          height = height_db[way_id][0]
          elem.append(etree.Element('tag', k="height", v=str(height)))
          elem.set("action","modify")
        else:
          # retain the building, but do not add a height tag
          pass
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








