import rasterio
from rasterio.mask import mask
import geopandas as gpd

# пути
raster_path = "data/population/senegal_pop.tif"
boundary_path = "data/boundary/dakar_boundary.json"
output_path = "output/dakar_population.tif"

print("1. Loading boundary...")
gdf = gpd.read_file(boundary_path)

# оставляем только регион Дакар
gdf = gdf[gdf["NAME_1"] == "Dakar"]

print("2. Loading raster...")
with rasterio.open(raster_path) as src:
    gdf = gdf.to_crs(src.crs)

    print("3. Clipping raster...")
    out_image, out_transform = mask(src, gdf.geometry, crop=True)

    out_meta = src.meta.copy()

# обновляем метаданные
out_meta.update({
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform
})

# сохраняем
with rasterio.open(output_path, "w", **out_meta) as dest:
    dest.write(out_image)

print("Done:")
print(" - output/dakar_population.tif")