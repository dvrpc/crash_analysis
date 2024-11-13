select a.objectid as oid_a, b.objectid as oid_b, a.street_nam as name_a, b.street_nam as name_b, a.st_rt_no as st_no_a, b.st_rt_no as st_no_b,st_collectionextract(st_intersection(a.shape, b.shape), 1) as int_geom
from rms_subset a, rms_subset b
where a.objectid <> b.objectid

---returns duplicates at each interseciton with each cross street being both a and b
