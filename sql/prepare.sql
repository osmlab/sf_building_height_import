UPDATE building_footprint SET geom = ST_MakeValid(geom);
UPDATE osm_buildings SET geom = ST_MakeValid(geom);
ALTER TABLE building_footprint ADD COLUMN height integer;
