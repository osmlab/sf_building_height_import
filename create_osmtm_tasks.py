import os
import errno
import json
import psycopg2
from shapely.wkb import loads
from shapely.geometry import mapping

conn = psycopg2.connect(dbname="us.ca.san_francisco")
cur = conn.cursor()
cur.execute("select ST_AsBinary(bounds_for_tile_indices(y+1, x, z)), x,y,z as geom from tasks order by x, y;")

task_id = 1
features = []
for result in cur:
  features.append({
    'type':'Feature',
    'properties':{'x':result[1],'y':result[2],'z':result[3]},
    'id':task_id,
    'geometry':mapping(loads(str(result[0])))
  })
  task_id = task_id + 1

print json.dumps({'type':'FeatureCollection','features':features})

