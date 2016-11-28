# Description

## Name of the project

[San Francisco Building Height Import](http://tasks.openstreetmap.us/project/71)

## Short Description

Annotating existing OSM buildings with LIDAR heights - Read the [wiki page](https://wiki.openstreetmap.org/wiki/San_Francisco_Building_Height_Import)

## Description

Building footprints for San Francisco exist in OSM thanks to the [Mapbox Data Team](https://wiki.openstreetmap.org/wiki/Mapbox#Mapbox_Data_Team). SFdata.gov hosts a [CC0-licensed building dataset](https://sfgis-svc.sfgov.org/sfgis/San_Francisco_Bldg_withZ_20161028.zip) derived from LIDAR that includes accurate height observations. We're annotating each building with a `height` tag.

If you have questions, post on the [wiki Talk page](https://wiki.openstreetmap.org/wiki/Talk:San_Francisco_Building_Height_Import) or on [GitHub issues](https://github.com/bdon/sf_building_height_import/issues).

## Entities to map

Buildings - review the automatically added `height` tags

## Changeset comment

```
San Francisco Building Height Import #sfbuildingheights https://wiki.openstreetmap.org/wiki/San_Francisco_Building_Height_Import
```

## Changeset source

```
San Francisco Enterprise Geographic Information Systems Program (SFGIS) Building Footprints, 2016. https://sfgis-svc.sfgov.org/sfgis/San_Francisco_Bldg_withZ_20161028.zip
```

## Detailed Instructions

Please [make a new account on the OSM website](https://www.openstreetmap.org/user/new) for the import. If your username is `brandon` you can make an account called `brandon_sfimport`. and post it [here](https://github.com/osmlab/sf_building_height_import/issues/23)

[Download JOSM](https://josm.openstreetmap.de). Activate Remote Control:  Open it first and enable Remote Control: **Preferences > Remote Control** (second to last tab).

Click **link** provided in the **Extra Instructions**. It should open in JOSM.

Add this Map Style to JOSM: [buildingheights.css](https://raw.githubusercontent.com/osmlab/sf_building_height_import/master/buildingheights.css). It's a panel in the right sidebar. Make sure it is activated. 

Add the LIDAR hillshade: menu Tab **Imagery > Add TMS entry...**

```
tms:https://s3-us-west-2.amazonaws.com/openmassing/sf_lidar/{z}/{x}/{y}.png
```

Make sure it is activated.

The JOSM changeset you will only include buildings that don't currently have heights in OSM.

If you do not think the building should have a height tag, DO NOT DELETE IT FROM THE LAYER! Instead, ONLY remove the height key.

If you want to edit other tags or change building footprints, do that in a separate changeset without the `#sfbuildingheights` comment.

If you have questions, post on the [wiki Talk page](https://wiki.openstreetmap.org/wiki/Talk:San_Francisco_Building_Height_Import) or on [GitHub issues](https://github.com/bdon/sf_building_height_import/issues).

## Per Task Instructions

Click **[here](http://localhost:8111/import?new_layer=true&url={import_url})** to load the changeset into JOSM.

Click **[here](http://tiles.openmassing.org/api/mapillary?url={import_url})** to view Mapillary imagery.

Make sure you retrieve the changeset right before editing. Don't save the .OSM on your local machine - it's created dynamically so will get out of date!
