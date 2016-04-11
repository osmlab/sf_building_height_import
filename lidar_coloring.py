# Greedy graph coloring

import psycopg2

conn = psycopg2.connect(dbname="us.ca.san_francisco")
cur = conn.cursor()
cur.execute("UPDATE building_footprint SET coloring = null;")

cur.execute("SELECT max(gid) from building_footprint;")
maxgid = int([result[0] for result in cur][0])

MAXCOLORS = 5

def set_coloring(gid, coloring):
  cur.execute("UPDATE building_footprint SET coloring = %s WHERE gid = %s",(coloring,gid))

def assign_color(neighbor_colors):
  for i in xrange(0,MAXCOLORS):
    if i not in neighbor_colors:
      return i
  return None

for gid in xrange(1,maxgid):
  cur.execute("""SELECT b.gid FROM building_footprint a, building_footprint b
                 WHERE a.gid = %s::integer
                 AND ST_DWithin(a.geom,b.geom,1)
                 AND b.gid < a.gid""",(gid,))
  results = [result[0] for result in cur]
  if len(results) > 0:
    cur.execute("SELECT DISTINCT coloring FROM building_footprint WHERE gid IN %s",(tuple(results),))
    neighbor_colors = [result[0] for result in cur]
    color = assign_color(neighbor_colors)
    if color == None:
      print "{0}-coloring failed for gid={0}".format(MAXCOLORS,gid)
    set_coloring(gid,color)
  else:
    set_coloring(gid,0)

conn.commit()
