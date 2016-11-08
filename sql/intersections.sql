create table intersections as (
  select
    osm_id, 
    f.geometry as osm_geom,
    w.wkb_geometry as sfdata_geom, 
    st_area(st_intersection(f.geometry, w.wkb_geometry)) as a,
    st_area(st_intersection(f.geometry, w.wkb_geometry)) / st_area(f.geometry) as a_osm_geom,
    st_area(st_intersection(f.geometry, w.wkb_geometry)) / st_area(w.wkb_geometry) as a_sfdata_geom,
    false as is_best_match
	from features f, wm84_bldgfoot_withz_20161005_pgz w 
	where ST_Intersects(f.geometry, w.wkb_geometry))

UPDATE intersections
SET is_best_match = true
 WHERE (osm_id, a_osm_geom) IN (
    SELECT osm_id, max(a_osm_geom)
    FROM intersections
    GROUP BY osm_id
    )
