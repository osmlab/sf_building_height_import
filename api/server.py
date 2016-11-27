from flask import Flask, request, Response, redirect
app = Flask(__name__)
import mercantile
import requests
import task
from io import BytesIO
from lxml import etree

height_db = task.height_db()

@app.route("/api")
def status():
  return "OK"

# example: /api/mapillary/16/10491/25321
@app.route("/api/mapillary/<int:z>/<int:x>/<int:y>")
def mapillary(z,x,y):
  bb = mercantile.bounds(x,y,z)
  centroid = [(bb.west + bb.east) / 2, (bb.north + bb.south) / 2]
  return redirect("https://www.mapillary.com/app/?lat={0}&lng={1}&z={2}".format(centroid[1],centroid[0],z))

# example: /api/sfbuildingheight_16_10490_25317.osm
@app.route("/api/sfbuildingheight_<int:z>_<int:x>_<int:y>.osm")
def changeset(z,x,y):
  if z < 16:
    print "Too big"
    raise Exception
  bb = mercantile.bounds(x,y,z)
  bb = [str(f) for f in [bb.west,bb.south,bb.east,bb.north]]
  url = "http://openstreetmap.org/api/0.6/map?bbox=" + ','.join(bb)
  osm_api_response = requests.get(url)
  changeset = task.changeset(BytesIO(osm_api_response.content),height_db)

  filename = "sfbuildingheight_{0}_{1}_{2}.osm".format(z,x,y)
  return Response(etree.tostring(changeset,pretty_print=True),
    mimetype="text/xml",
    headers={
    'Content-Disposition':'attachment; filename={0}'.format(filename)
  })

if __name__ == "__main__":
  app.debug = True
  app.run()
