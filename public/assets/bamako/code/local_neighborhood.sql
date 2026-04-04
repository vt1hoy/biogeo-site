SELECT m1.site_name,
       m1.commod1,
       COUNT(m2.*) - 1 AS neighbors_100km
FROM mineral_occurrences m1
JOIN mineral_occurrences m2
  ON ST_DWithin(
       m1.geom::geography,
       m2.geom::geography,
       100000
     )
GROUP BY m1.site_name, m1.commod1
ORDER BY neighbors_100km DESC, m1.site_name;