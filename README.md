This repository supports the [San Francisco Building Height Import](https://wiki.openstreetmap.org/wiki/San_Francisco_Building_Height_Import) into OpenStreetMap.

The stuff in here:

* Imports the LIDAR Shapefile into PostGIS.
* Creates a preview tileset that can be rendered in Tangram by automatically conflating LIDAR and OSM. This is useful to see how the data might look when we're done.
* Creates an OSM Tasking Manager task list, that has roughly equally sized tasks of <50 buildings each.
* Defines a Mapnik stylesheet and data sources for the LIDAR imagery tileset that mappers will use in iD. 
