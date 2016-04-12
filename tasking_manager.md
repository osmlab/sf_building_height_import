# Description

## Name of the project

San Francisco Building Height Import

## Short Description

Annotating existing OSM buildings with LIDAR heights - Read the [wiki page](https://wiki.openstreetmap.org/wiki/San_Francisco_Building_Height_Import)

## Description

Building footprints for San Francisco exist in OSM thanks to the [Mapbox Data Team](https://wiki.openstreetmap.org/wiki/Mapbox#Mapbox_Data_Team). SFdata.gov hosts a [CC0-licensed building dataset](https://data.sfgov.org/Geographic-Locations-and-Boundaries/Building-Footprints-Zipped-Shapefile-Format-/jezr-5bxm?) derived from LIDAR that lacks discrete footprints, but includes accurate height observations. We're manually annotating each building with a `height` tag.

If you have questions, post on the [wiki Talk page](https://wiki.openstreetmap.org/wiki/Talk:San_Francisco_Building_Height_Import) or on [GitHub issues](https://github.com/bdon/sf_building_height_import/issues).



## Entities to map

Buildings - ONLY add the `height` tag

## Changeset comment

San Francisco Building Height Import #sfbuildingheights https://wiki.openstreetmap.org/wiki/San_Francisco_Building_Height_Import

## Detailed Instructions

Please [make a new account on the OSM website](https://www.openstreetmap.org/user/new) for the import. If your username is `frankchu` you can make an account called `frankchu_import`. 

We suggest you use our customized iD editor (choose "edit with iD"):

* only `building` features are loaded.
* buildings with `height` tags are colored green instead of the default red.

The only changes you should make are adding the `height=` tag to buildings that don't have them already and overlap a LIDAR observation. Tag heights as whole integers:

* DO tag like `height=30`
* DO NOT tag like `height=30.0` or `height=30 m`

If you want to edit other tags or change building footprints, do that in a separate changeset without the `#sfbuildingheights` comment.

A task can be marked Done when all existing buildings that match a LIDAR observation have a `height` tag. 

If you have questions, post on the [wiki Talk page](https://wiki.openstreetmap.org/wiki/Talk:San_Francisco_Building_Height_Import) or on [GitHub issues](https://github.com/bdon/sf_building_height_import/issues).

## Per Task Instructions

(blank)

