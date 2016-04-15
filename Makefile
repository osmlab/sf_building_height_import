create_db:
	createdb us.ca.san_francisco
	psql us.ca.san_francisco -c "CREATE EXTENSION postgis;"
	psql us.ca.san_francisco -c "CREATE EXTENSION hstore;"
	psql us.ca.san_francisco -f sql/srid_102643.sql
	psql us.ca.san_francisco -f sql/postgis2gmap.sql
	shp2pgsql -I -s 102643:3857 ../sources/building_footprint/building_footprint.shp > building_footprint.sql
	psql us.ca.san_francisco -f building_footprint.sql
	rm building_footprint.sql
	imposm3 import -mapping=imposm3_mapping.json -read ../sources/san-francisco_california.osm.pbf -connection=postgres://localhost/us.ca.san_francisco -write -deployproduction -overwritecache
	psql us.ca.san_francisco -f sql/prepare.sql

color_lidar:
	python lidar_coloring.py

create_tables:
	psql us.ca.san_francisco -f sql/create_tables.sql

output/tangram_tiles:
	python create_tangram_tiles.py

output/osmtm_tasks.geojson:
	python create_osmtm_tasks.py > output/osmtm_tasks.geojson

output/sf_building_height_imagery.shp:
	pgsql2shp -f output/sf_building_height_imagery.shp -h /tmp/ us.ca.san_francisco "select geom, height, coloring from building_footprint;"

output/heights.csv:
	psql -d us.ca.san_francisco -t -A -F"," -c "select osm_id, height, round(confidence::numeric,2) from features" > output/heights.csv

sources:
	cd sources
	wget https://s3.amazonaws.com/metro-extracts.mapzen.com/san-francisco_california.osm.pbf
	wget http://apps.sfgov.org/datafiles/view.php?file=sfgis/building_footprint.zip

clean:
	dropdb us.ca.san_francisco
	rm -r output/tangram_tiles
	rm output/*.geojson
