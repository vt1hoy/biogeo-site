import geopandas as gpd

input_path = "output/dakar_walk_edges.geojson"
output_path = "output/dakar_urban_mask.geojson"
target_crs = "EPSG:32628"
buffer_m = 800  # meters

print("1. Loading walk network edges...")
edges = gpd.read_file(input_path)

print("2. Reprojecting to UTM 28N...")
edges = edges.to_crs(target_crs)

print("3. Building buffer around streets...")
buffered = edges.copy()
buffered["geometry"] = buffered.geometry.buffer(buffer_m)

print("4. Dissolving into single urban mask...")
mask_geom = buffered.union_all()

mask = gpd.GeoDataFrame(
    {"name": ["dakar_urban_mask"]},
    geometry=[mask_geom],
    crs=target_crs
)

print("5. Saving...")
mask.to_file(output_path, driver="GeoJSON")

print("Done:")
print(f" - {output_path}")
print(f"Buffer: {buffer_m} m")