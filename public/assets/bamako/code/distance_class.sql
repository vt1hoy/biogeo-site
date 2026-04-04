SELECT site_name,
       commod1,
       ROUND(
         ST_Distance(
           geom::geography,
           ST_SetSRID(ST_MakePoint(-8.0, 12.6), 4326)::geography
         ) / 1000
       ) AS distance_km,
       CASE
         WHEN ST_Distance(
           geom::geography,
           ST_SetSRID(ST_MakePoint(-8.0, 12.6), 4326)::geography
         ) < 200000 THEN 'high'
         WHEN ST_Distance(
           geom::geography,
           ST_SetSRID(ST_MakePoint(-8.0, 12.6), 4326)::geography
         ) < 400000 THEN 'medium'
         ELSE 'low'
       END AS bamako_access
FROM mineral_occurrences
ORDER BY distance_km;