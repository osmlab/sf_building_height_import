create_db:
	createdb us.ca.san_francisco
	psql us.ca.san_francisco -c "CREATE EXTENSION postgis;"
	psql us.ca.san_francisco -c "CREATE EXTENSION hstore;"
	psql us.ca.san_francisco -f sql/srid_102643.sql
	psql us.ca.san_francisco -f sql/postgis2gmap.sql
	imposm3 import -mapping=imposm3_mapping.json -read sources/san-francisco_california.osm.pbf -connection=postgres://localhost/us.ca.san_francisco -write -deployproduction -overwritecache
	psql us.ca.san_francisco -c "UPDATE osm_buildings SET geometry = ST_MakeValid(geometry);"

create_tables:
	psql us.ca.san_francisco -f sql/create_tables.sql

tangram_tiles:
	python create_tangram_tiles.py

output/osmtm_tasks.geojson:
	python create_osmtm_tasks.py > output/osmtm_tasks.geojson

output/heights.csv:
	psql -d us.ca.san_francisco -t -A -F"," -c "select osm_id, height_max from features" > output/heights.csv

output/imagery:
	pgsql2shp -f output/imagery_buildings.shp -h /tmp/ us.ca.san_francisco "select geometry from features;"
	pgsql2shp -f output/imagery_centroids.shp -h /tmp/ us.ca.san_francisco "select height_max, ST_Centroid(geometry) as geometry from features;"
	# shapeindex

sources:
	cd sources
	wget https://s3.amazonaws.com/metro-extracts.mapzen.com/san-francisco_california.osm.pbf
	wget https://sfgis-svc.sfgov.org/sfgis/SF2014_bldg_height_1m.zip
	wget https://sfgis-svc.sfgov.org/sfgis/San_Francisco_Bldg_withZ_20161028.zip

SF2014_bldg_height:
	gdalwarp -s_srs sf13.prj -t_srs EPSG:3857 sources/SF2014_bldg_height_1m/L2014_SF_TreeBldg1m.img SF2014_bldg_height.img
	# tiff is for Mapnik rendering
	gdalwarp -of GTiff SF2014_bldg_height.img output/SF2014_bldg_height.tiff
	raster2pgsql -d -I -t 100x100 SF2014_bldg_height.img > SF2014_bldg_height.sql
	psql us.ca.san_francisco -f SF2014_bldg_height.sql
	rm SF2014_bldg_height.sql
	rm SF2014_bldg_height.img

clean:
	dropdb us.ca.san_francisco
	rm -r output/tangram_tiles
	rm output/*.geojson

zip:
	tar -cvzf api_data.tgz output

# ASCII grid for use with Meshlab
output/mesh:
	gdalwarp -te -122.465629578 37.7567370535 -122.454299927 37.7654225277 -of "AAIGrid" sources/SF2014_bldg_height_1m/L2014_SF_TreeBldg1m.img sunset.asc

