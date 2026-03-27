import geopandas as gpd
import numpy as np
from shapely.geometry import box

input_path = "output/dakar_population_grid.geojson"
output_path = "output/dakar_population_grid_300m.geojson"

target_crs = "EPSG:32628"
cell_size = 300  # meters

print("1. Loading 100m population grid...")
gdf = gpd.read_file(input_path)

print("2. Reprojecting to UTM 28N...")
gdf = gdf.to_crs(target_crs)

print("3. Creating 300m grid...")
minx, miny, maxx, maxy = gdf.total_bounds

x_coords = np.arange(minx, maxx + cell_size, cell_size)
y_coords = np.arange(miny, maxy + cell_size, cell_size)

grid_cells = []
for x in x_coords[:-1]:
    for y in y_coords[:-1]:
        grid_cells.append(box(x, y, x + cell_size, y + cell_size))

grid = gpd.GeoDataFrame(geometry=grid_cells, crs=target_crs)

print(f"Grid cells created: {len(grid)}")

print("4. Calculating centroids of source population cells...")
gdf["centroid"] = gdf.geometry.centroid
centroids = gdf.set_geometry("centroid")[["population", "centroid"]].copy()
centroids = centroids.rename(columns={"centroid": "geometry"})
centroids = gpd.GeoDataFrame(centroids, geometry="geometry", crs=target_crs)

print("5. Spatial join: assigning population points to 300m cells...")
joined = gpd.sjoin(centroids, grid, how="inner", predicate="within")

print("6. Aggregating population by 300m cell...")
pop_by_cell = joined.groupby("index_right")["population"].sum()

grid["population"] = 0.0
grid.loc[pop_by_cell.index, "population"] = pop_by_cell.values

grid = grid[grid["population"] > 0].copy()

print(f"Cells with population: {len(grid)}")
print(f"Total population: {grid['population'].sum():.2f}")

print("7. Saving output...")
grid.to_file(output_path, driver="GeoJSON")

print("Done:")
print(f" - {output_path}")