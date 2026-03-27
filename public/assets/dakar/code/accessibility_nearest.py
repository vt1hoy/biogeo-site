import geopandas as gpd
import pandas as pd

pop_path = "output/dakar_population_grid_300m_urban.geojson"
health_path = "output/dakar_health_32628.geojson"
output_path = "output/dakar_accessibility_nearest.geojson"

print("1. Loading population grid...")
pop = gpd.read_file(pop_path)

print("2. Loading health facilities...")
health = gpd.read_file(health_path)

print("3. Creating centroids for population cells...")
pop["centroid"] = pop.geometry.centroid
pop_cent = pop.set_geometry("centroid").copy()

print("4. Finding nearest health facility for each population cell...")
joined = gpd.sjoin_nearest(
    pop_cent,
    health[["amenity", "capacity", "geometry"]],
    how="left",
    distance_col="dist_m"
)

print("5. Building simple accessibility score...")
# Чем ближе и мощнее объект, тем выше score
joined["access_score"] = joined["capacity"] / (joined["dist_m"] + 1)

print("6. Restoring original cell geometry...")
joined = joined.set_geometry(pop.geometry.values)
# Фикс ошибки
if "centroid" in joined.columns:
    joined = joined.drop(columns=["centroid"])

print("7. Saving result...")
joined.to_file(output_path, driver="GeoJSON")

print("Done:")
print(f" - {output_path}")
print()
print("Distance stats (m):")
print(joined["dist_m"].describe())
print()
print("Access score stats:")
print(joined["access_score"].describe())