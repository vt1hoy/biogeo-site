import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import box

raster_path = "output/dakar_population.tif"
output_path = "output/dakar_population_grid.geojson"

print("1. Loading raster...")

with rasterio.open(raster_path) as src:
    print("Pixel size:", src.res)
    
    data = src.read(1)
    transform = src.transform
    crs = src.crs

rows, cols = data.shape

print("2. Building grid...")

polygons = []
values = []

for row in range(rows):
    for col in range(cols):
        value = data[row, col]

        if value <= 0:
            continue

        x1, y1 = transform * (col, row)
        x2, y2 = transform * (col + 1, row + 1)

        geom = box(x1, y2, x2, y1)

        polygons.append(geom)
        values.append(float(value))

gdf = gpd.GeoDataFrame(
    {"population": values},
    geometry=polygons,
    crs=crs
)

print(f"Cells: {len(gdf)}")

gdf.to_file(output_path, driver="GeoJSON")

print("Done:")
print(" - output/dakar_population_grid.geojson")