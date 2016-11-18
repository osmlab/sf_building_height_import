# Raster coverage:

# Upper Left  (-122.5168659,  37.8459040) (122d31' 0.72"W, 37d50'45.25"N)
# Lower Left  (-122.5168659,  37.6981374) (122d31' 0.72"W, 37d41'53.29"N)
# Upper Right (-122.3161447,  37.8459040) (122d18'58.12"W, 37d50'45.25"N)
# Lower Right (-122.3161447,  37.6981374) (122d18'58.12"W, 37d41'53.29"N)

import requests
import os
from lxml import etree

if not os.path.isfile("foo.xml"):
  QUERY = """
  [diff:"2012-01-01T00:00:00Z","2016-11-01T00:00:00Z"];
  (
    way["building"](37.6981374,-122.5168659,37.8459040,-122.3161447);
  );
  out tags qt;
  """.strip()

  response = requests.post("https://overpass-api.de/api/interpreter",data=QUERY)

  with open("foo.xml",'wb') as f:
    f.write(response.text.encode("UTF-8"))

tree = etree.parse("foo.xml")

print "Way Changesets in San Francisco with building and height tag"
print "Actions: {0}".format(len(tree.xpath("action")))
print "Actions (type=create): {0}".format(len(tree.xpath("action[@type='create']")))
print "Actions (type=modify): {0}".format(len(tree.xpath("action[@type='modify']")))

# count all actions where OLD does not have a height tag and NEW does.

count = 0
for action in tree.xpath("action[@type='modify']"):
  old_has_height = len(action.xpath("old/way/tag[@k='height']"))
  new_has_height = len(action.xpath("new/way/tag[@k='height']"))
  if not old_has_height and new_has_height:
    count = count + 1

for action in tree.xpath("action[@type='create']"):
  if len(action.xpath("way/tag[@k='height']")):
    count = count + 1

print "Actions that add a building height: {0}".format(count)
