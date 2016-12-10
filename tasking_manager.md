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

## General Setup

1. Please [**make a new account** on the OSM website](https://www.openstreetmap.org/user/new) for the import. If your username is `brandon` you should make an account called `brandon_sfimport`. and post it [here](https://github.com/osmlab/sf_building_height_import/issues/23). If you have questions, post on [GitHub issues](https://github.com/bdon/sf_building_height_import/issues). Join our [Gitter](http://gitter.im/osmlab/sf_building_height_import) channel and say hihi.
2. **JOSM Setup**
   1. Download [JOSM](https://josm.openstreetmap.de). Enable Remote Remote Control in JOSM's **Preferences > Remote Control** , the second to last tab. 
   2. **Add the Map Style** : [buildingheights.css](https://raw.githubusercontent.com/osmlab/sf_building_height_import/master/buildingheights.css). It's a panel in the right sidebar. Make sure it is activated. 
   3. **Add the hillshade imagery** : menu Tab **Imagery > Add TMS entry...**

```
tms:https://s3-us-west-2.amazonaws.com/openmassing/sf_lidar/{z}/{x}/{y}.png
```

3. **QGIS Setup**
   1. Download [QGIS](http://www.qgis.org/en/site/) . Windows and Linux should have binary packages. For macOS, you can install via Homebrew or as a binary+Kyngchaos frameworks. If you need help, ask on Gitter. 
   2. **Download the two raster files**. [Building Layer](https://sfgis-svc.sfgov.org/sfgis/SF2014_bldg_height_1m.zip) and [Hillshade](http://openmassing.s3.amazonaws.com/misc/L2014_SF_TreeBldg1m_hillshade.tif.zip).
   3. Open [lidar_style.qgs](https://github.com/osmlab/sf_building_height_import/blob/master/lidar_style.qgs) - you will be prompted to fix the paths to the two raster images above.
   4. Now you can use the "Identify Features" tool while the `height` layer is selected to identify the height at any pixel. 
   5. I would also recommend installing the QuickMapServices plugin to overlay OpenStreetMap. This will make the map easier to orient.

## Doing a Task

1. Select a task and choose **Start mapping** - it's best to choose an area you're familiar with.
2. Open JOSM, and then in the Task Manager, under "Extra Instructions", click the link to load the changeset into JOSM. JOSM will now have an open changeset of buildings you'll be adding height tags to. 
3. In the Task Manager, click the link to open the Mapillary / OSM comparison tool. Use this street imagery to carefully review each building you're tagging. If you're unsure about a tag, you can remove it - **It is very important that you only remove the tag from the way, and not delete the entire building!**
   * Inspect each building and ensure that its OSM footprint aligns with the LIDAR shape.
   * If the LIDAR footprint is obscured by trees, refer to QGIS to find the correct height, and then edit the "height" value in the right editing panel.
4. If you want to edit other tags or change building footprints, do that in a separate changeset.
5. When you're done, make sure your JOSM is authenticated with your import-specific account. Upload the changeset with the comment:

```San Francisco Building Height Import #sfbuildingheights https://wiki.openstreetmap.org/wiki/San_Francisco_Building_Height_Import```

Finally, make sure to "Mark task as done" in the Task Manager.   

## Validating a Task

1. Claim a "Done" yellow task in the Tasking Manager.
2. In the Task Manager, click the link to open the Mapillary / OSM comparison tool. Use this street imagery to carefully review each building you're tagging. Expect to take at least 15 minutes per task reviewing the height tags in the area.
3. If you need to make changes, click the link in the Task Manager for loading OSM data. This will load all OSM data in the task's area into JOSM. Make any corrections and then upload it using your import-specific account.
4. Finally, mark the task as validated in the Tasking Manager.


## Per Task Instructions

Click **[here](http://openmassing.org/validator/?import_url={import_url})** to view the Mapillary / OSM comparison tool.

** For adding tags **

Click **[here](http://localhost:8111/import?new_layer=true&url={import_url})** to load the changeset into JOSM.

Make sure you retrieve the changeset right before editing. Don't save the .OSM on your local machine - it's created dynamically so will get out of date!

** For validating tags **

Click **[here](http://tiles.openmassing.org/api/josm?url={import_url})** to load OSM data in the task into JOSM.

