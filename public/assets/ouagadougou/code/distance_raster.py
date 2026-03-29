import rasterio
import geopandas as gpd
import numpy as np
from scipy.ndimage import distance_transform_edt
from rasterio.features import rasterize

# -------------------------
# INPUT
# -------------------------

template_path = "../data/indices/ndvi_clip.tif"
roads_path = "../data/osm/roads.gpkg"

# OUTPUT
output_path = "../data/results/dist_roads.tif"

# -------------------------
# 1. читаем шаблон растра
# -------------------------

with rasterio.open(template_path) as src:
    profile = src.profile
    transform = src.transform
    shape = (src.height, src.width)
    crs = src.crs

print("Raster loaded")

# -------------------------
# 2. читаем дороги
# -------------------------

roads = gpd.read_file(roads_path)

# приводим к CRS растра
roads = roads.to_crs(crs)

print("Roads loaded:", len(roads))

# -------------------------
# 3. растризация дорог
# -------------------------

road_raster = rasterize(
    [(geom, 1) for geom in roads.geometry],
    out_shape=shape,
    transform=transform,
    fill=0,
    dtype="uint8"
)

print("Road raster created")

# -------------------------
# 4. distance transform
# -------------------------

dist = distance_transform_edt(1 - road_raster)

print("Distance calculated")

# -------------------------
# 5. нормализация
# -------------------------

if dist.max() > 0:
    dist = dist / dist.max()

# -------------------------
# 6. сохранение
# -------------------------

profile.update(dtype=rasterio.float32)

with rasterio.open(output_path, "w", **profile) as dst:
    dst.write(dist.astype(rasterio.float32), 1)

print("Saved →", output_path)