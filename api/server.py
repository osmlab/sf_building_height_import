from flask import Flask, request, Response
app = Flask(__name__)
import mercantile
import requests
import task
from io import BytesIO
from lxml import etree

height_db = tasks.height_db()

#16,10490,25317
@app.route("/sfbuildingheight_<int:z>_<int:x>_<int:y>.osm")
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
