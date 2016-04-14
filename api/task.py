from lxml import etree
import csv

# handle building polygons, don't handle super-relations.

def height_db():
  db = {}
  with open('../output/heights.csv', 'rb') as csvfile:
    for row in csv.reader(csvfile, delimiter=','):
      db[row[0]] = row[1]
  return db

def changeset(xml_bytes, height_db):
  referenced_nodes = []
  context = etree.iterparse(xml_bytes)
  # collect referenced nodes
  for action, elem in context:
    if elem.tag == 'way' and len(elem.xpath("tag[@k='building' or @k='building:part']")) > 0:
      referenced_nodes += elem.xpath("nd/@ref")

  xml_bytes.seek(0)
  context = etree.iterparse(xml_bytes)
  for action, elem in context:
    if elem.tag == 'node':
      if not elem.get('id') in referenced_nodes:
        elem.getparent().remove(elem)
    if elem.tag == 'way':
      if len(elem.xpath("tag[@k='building' or @k='building:part']")) > 0:
        way_id = elem.get("id")
        if height_db.has_key(way_id):
          height = height_db[way_id]
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








