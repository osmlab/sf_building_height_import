import requests
from io import BytesIO
import time
from lxml import etree
f = open("ways.txt","r")

for way_id in f:
  response = requests.get("http://openstreetmap.org/api/0.6/way/{0}".format(way_id.strip()))
  tree = etree.parse(BytesIO(response.content))
  way = tree.xpath("way")[0]
  user = way.get("user")
  uid = way.get("uid")
  print ','.join([way_id.strip(),user.encode('utf-8'),uid])
  time.sleep(0.1)



f.close()
