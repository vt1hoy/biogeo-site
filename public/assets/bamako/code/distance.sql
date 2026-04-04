SELECT site_name,
       commod1,
       ST_Distance(
           geom::geography,
           ST_SetSRID(ST_MakePoint(-8.0, 12.6), 4326)::geography
       ) AS distance_m
FROM mineral_occurrences
ORDER BY distance_m
LIMIT 10;