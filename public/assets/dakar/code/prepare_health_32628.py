import geopandas as gpd

input_path = "output/dakar_health.geojson"
output_path = "output/dakar_health_32628.geojson"
target_crs = "EPSG:32628"

print("1. Loading health facilities...")
gdf = gpd.read_file(input_path)

print("2. Reprojecting to UTM 28N...")
gdf = gdf.to_crs(target_crs)

print("3. Assigning proxy capacities...")
capacity_map = {
    "hospital": 3,
    "clinic": 2,
    "doctors": 1,
    "health_post": 1
}

gdf["capacity"] = gdf["amenity"].map(capacity_map).fillna(1)

print("Amenity counts:")
print(gdf["amenity"].value_counts())

print("Total capacity:", gdf["capacity"].sum())

print("4. Saving...")
gdf.to_file(output_path, driver="GeoJSON")

print("Done:")
print(f" - {output_path}")