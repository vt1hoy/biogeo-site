SELECT m1.site_name,
       COUNT(m2.*) AS neighbors_50km
FROM mineral_occurrences m1
JOIN mineral_occurrences m2
  ON ST_DWithin(m1.geom::geography, m2.geom::geography, 50000)
GROUP BY m1.site_name
ORDER BY neighbors_50km DESC;