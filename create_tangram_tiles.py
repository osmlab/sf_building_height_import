import os
import errno
import json
import psycopg2
from shapely.wkb import loads
from shapely.geometry import mapping

def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(path):
        pass
    else:
        raise

conn = psycopg2.connect(dbname="us.ca.san_francisco")
cur = conn.cursor()
cur.execute("select osm_id, z16_x, z16_y, ST_AsBinary(ST_Transform(geometry,4326)), height_max from features order by z16_x, z16_y")

current_tile = None
features = []
for result in cur:
  tile = (int(result[1]),int(result[2]))
  if current_tile and tile != current_tile:
    print "Writing 16 {0}".format(tile)
    path = 'tangram_tiles/16/{0}'.format(tile[0])
    mkdir_p(path)
    with open(path + "/" + str(tile[1]) + ".json",'w') as f:
      f.write(json.dumps({'buildings':{'type':'FeatureCollection','features':features}}))
    features = []
  current_tile = tile
  features.append({
    'type':'Feature',
    'properties':{'id':result[0],'height':round(result[4])},
    'geometry':mapping(loads(str(result[3])))
  })
