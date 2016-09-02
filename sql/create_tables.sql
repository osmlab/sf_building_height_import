DROP TABLE IF EXISTS features;
DROP TABLE IF EXISTS tasks;

CREATE table features as SELECT osm_id,
       geometry, 
       round((ST_SummaryStats(ST_Clip(rast,ST_Buffer(geometry,-2),true))).max)::integer as height_max,
       ST_Buffer(geometry,-2) as query_area,
       floor(ST_X(tile_indices_for_lonlat(ST_Transform(ST_Centroid(geometry),4326),16)))::integer as z16_x, 
       floor(ST_Y(tile_indices_for_lonlat(ST_Transform(ST_Centroid(geometry),4326),16)))::integer-1 as z16_y,
       floor(ST_X(tile_indices_for_lonlat(ST_Transform(ST_Centroid(geometry),4326),17)))::integer as z17_x, 
       floor(ST_Y(tile_indices_for_lonlat(ST_Transform(ST_Centroid(geometry),4326),17)))::integer-1 as z17_y,
       floor(ST_X(tile_indices_for_lonlat(ST_Transform(ST_Centroid(geometry),4326),18)))::integer as z18_x, 
       floor(ST_Y(tile_indices_for_lonlat(ST_Transform(ST_Centroid(geometry),4326),18)))::integer-1 as z18_y,
       FALSE AS z16_task,
       FALSE AS z17_task,
       FALSE AS z18_task
FROM sf2014_bldg_height, osm_buildings as foo
WHERE ST_Intersects(rast,ST_Centroid(geometry)) 
AND ST_GeometryType(geometry) != 'ST_GeometryCollection';

DELETE FROM features WHERE height_max IS NULL OR height_max = 0;

/* The bounds of our task are either a zoom 16 or 17 web mercator tile. 
   We use aggregation to determine which size task each feature falls into -
   We want a max of 500 "features" per task. */
UPDATE features SET z16_task = TRUE WHERE (z16_x, z16_y) IN (
  SELECT z16_x, z16_y FROM features GROUP BY z16_x, z16_y HAVING count(*) <= 500
  );
UPDATE features SET z17_task = TRUE WHERE z16_task IS FALSE;

/* Finally, create a list of all tasks from our features table.
   The size of this table is the total # of tasks. */
CREATE TABLE tasks (z integer, x integer, y integer);
INSERT INTO tasks SELECT DISTINCT 16 AS z, z16_x AS x, z16_y AS y FROM features WHERE z16_task;
INSERT INTO tasks SELECT DISTINCT 17 AS z, z17_x AS x, z17_y AS y FROM features WHERE z17_task;
