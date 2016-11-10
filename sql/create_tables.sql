DROP TABLE IF EXISTS intersections;
DROP TABLE IF EXISTS features;
DROP TABLE IF EXISTS tasks;

/* Find all intersections of OSM buildings and SFdata footprints */

CREATE table intersections as (
  SELECT
    osm_id, 
    o.geometry as osm_geom,
    w.wkb_geometry as sfdata_geom, 
    st_area(st_intersection(o.geometry, w.wkb_geometry)) as a,
    st_area(st_intersection(o.geometry, w.wkb_geometry)) / st_area(o.geometry) as a_osm_geom,
    st_area(st_intersection(o.geometry, w.wkb_geometry)) / st_area(w.wkb_geometry) as a_sfdata_geom,
    false as is_best_match,
    w.hgt_Median_m as hgt_Median_m
	from osm_buildings o, wm84_bldgfoot_withz_20161005_pgz w 
	where ST_Intersects(o.geometry, w.wkb_geometry))

/* Determine the intersection of maximum area as the "best match" intersection */

UPDATE intersections
SET is_best_match = true
WHERE (osm_id, a) IN (
   SELECT osm_id, max(a)
   FROM intersections
   GROUP BY osm_id
   )

/* Create features table of best-match intersections meeting threshold */

CREATE TABLE features AS 
  SELECT osm_id,
         osm_geom,
         round(hgt_Median_m::numeric,2) as height,
         floor(ST_X(tile_indices_for_lonlat(ST_Transform(ST_Centroid(osm_geom),4326),16)))::integer as z16_x, 
         floor(ST_Y(tile_indices_for_lonlat(ST_Transform(ST_Centroid(osm_geom),4326),16)))::integer as z16_y,
         floor(ST_X(tile_indices_for_lonlat(ST_Transform(ST_Centroid(osm_geom),4326),17)))::integer as z17_x, 
         floor(ST_Y(tile_indices_for_lonlat(ST_Transform(ST_Centroid(osm_geom),4326),17)))::integer as z17_y,
         FALSE AS z16_task,
         FALSE AS z17_task
  FROM intersections
  WHERE is_best_match
  AND (a_osm_geom > 0.7 AND a_sfdata_geom > 0.7)

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
