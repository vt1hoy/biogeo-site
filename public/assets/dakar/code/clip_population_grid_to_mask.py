import geopandas as gpd

grid_path = "output/dakar_population_grid_300m.geojson"
mask_path = "output/dakar_urban_mask.geojson"
output_path = "output/dakar_population_grid_300m_urban.geojson"

print("1. Loading population grid...")
grid = gpd.read_file(grid_path)

print("2. Loading urban mask...")
mask = gpd.read_file(mask_path)

print("3. Reprojecting grid to mask CRS if needed...")
if grid.crs != mask.crs:
    grid = grid.to_crs(mask.crs)

print("4. Clipping grid to urban mask...")
clipped = gpd.clip(grid, mask)

print(f"Cells before clip: {len(grid)}")
print(f"Cells after clip: {len(clipped)}")
print(f"Population after clip: {clipped['population'].sum():.2f}")

print("5. Saving...")
clipped.to_file(output_path, driver="GeoJSON")

print("Done:")
print(f" - {output_path}")