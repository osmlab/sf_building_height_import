DROP TABLE IF EXISTS intersections;
DROP TABLE IF EXISTS features;
DROP TABLE IF EXISTS tasks;

UPDATE building_footprint SET height = round(maxheight-minheight)::integer;

/* Conflate the LIDAR and OSM building footprints.
   A OSM building may intersect multiple LIDAR observations. */
CREATE TABLE intersections AS 
  SELECT a.osm_id, 
         b.gid, 
         ST_Area(ST_Intersection(a.geometry,b.geom)) AS area, 
         false AS selected 
  FROM osm_buildings a 
  INNER JOIN building_footprint b 
  ON ST_Intersects(a.geometry,b.geom) 
  WHERE ST_GeometryType(a.geometry) != 'ST_GeometryCollection';

/* Mark the LIDAR observation with the largest intersection
   as "Selected". We'll use this one to create a Feature. */
UPDATE intersections 
  SET selected = true 
  FROM (
    SELECT osm_id, gid FROM intersections WHERE (osm_id, area) IN (
      SELECT osm_id, max(area) FROM intersections GROUP BY osm_id
    )
  ) AS subquery
  WHERE subquery.osm_id = intersections.osm_id AND subquery.gid = intersections.gid;

/* "Features" are our derived building footprints with LIDAR height.
   We'll add some helper columns for which mercator tile they belong to. */
CREATE TABLE features AS
SELECT o.osm_id,
o.geometry, 
b.height,
floor(ST_X(tile_indices_for_lonlat(ST_Transform(ST_Centroid(o.geometry),4326),16)))::integer as z16_x, 
floor(ST_Y(tile_indices_for_lonlat(ST_Transform(ST_Centroid(o.geometry),4326),16)))::integer-1 as z16_y,
floor(ST_X(tile_indices_for_lonlat(ST_Transform(ST_Centroid(o.geometry),4326),17)))::integer as z17_x, 
floor(ST_Y(tile_indices_for_lonlat(ST_Transform(ST_Centroid(o.geometry),4326),17)))::integer-1 as z17_y,
floor(ST_X(tile_indices_for_lonlat(ST_Transform(ST_Centroid(o.geometry),4326),18)))::integer as z18_x, 
floor(ST_Y(tile_indices_for_lonlat(ST_Transform(ST_Centroid(o.geometry),4326),18)))::integer-1 as z18_y,
floor(ST_X(tile_indices_for_lonlat(ST_Transform(ST_Centroid(o.geometry),4326),19)))::integer as z19_x, 
floor(ST_Y(tile_indices_for_lonlat(ST_Transform(ST_Centroid(o.geometry),4326),19)))::integer-1 as z19_y,
FALSE AS z17_task,
FALSE AS z18_task,
FALSE AS z19_task
FROM intersections i 
LEFT JOIN osm_buildings o 
ON i.osm_id = o.osm_id 
LEFT JOIN building_footprint b
ON b.gid = i.gid 
WHERE selected AND area > 10;

/* The bounds of our task are either a zoom 17, 18 or 19 web mercator tile. 
   We use aggregation to determine which size task each feature falls into -
   We want a max of 50 "features" per task. */
UPDATE features SET z17_task = TRUE WHERE (z17_x, z17_y) IN (
  SELECT z17_x, z17_y FROM features GROUP BY z17_x, z17_y HAVING count(*) <= 50
  );
UPDATE features SET z18_task = TRUE WHERE (z18_x, z18_y) IN (
  SELECT z18_x, z18_y FROM features WHERE z17_task IS FALSE GROUP BY z18_x, z18_y HAVING count(*) <= 50
  );
UPDATE features SET z19_task = TRUE WHERE z17_task IS FALSE AND z18_task IS FALSE;

/* Finally, create a list of all tasks from our features table.
   The size of this table is the total # of tasks. */
CREATE TABLE tasks (z integer, x integer, y integer);
INSERT INTO tasks SELECT DISTINCT 17 AS z, z17_x AS x, z17_y AS y FROM features WHERE z17_task;
INSERT INTO tasks SELECT DISTINCT 18 AS z, z18_x AS x, z18_y AS y FROM features WHERE z18_task;
INSERT INTO tasks SELECT DISTINCT 19 AS z, z19_x AS x, z19_y AS y FROM features WHERE z19_task;
