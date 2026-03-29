import rasterio
import numpy as np
from rasterio.warp import reproject, Resampling

# -------------------------
# INPUT
# -------------------------

ndvi_path = "../data/indices/ndvi_clip2.tif"
ndwi_path = "../data/indices/ndwi_clip2.tif"
dist_path = "../data/results/dist_roads.tif"

# OUTPUT
ndwi_out = "../data/indices/ndwi_clip2_aligned2.tif"
dist_out = "../data/results/dist_roads_aligned2.tif"

# -------------------------
# ФУНКЦИЯ ВЫРАВНИВАНИЯ
# -------------------------

def align_to_target(src_array, src_transform, src_crs, target_profile):
    dst = np.empty(
        (target_profile["height"], target_profile["width"]),
        dtype="float32"
    )

    reproject(
        source=src_array,
        destination=dst,
        src_transform=src_transform,
        src_crs=src_crs,
        dst_transform=target_profile["transform"],
        dst_crs=target_profile["crs"],
        resampling=Resampling.bilinear
    )

    return dst

# -------------------------
# ЧИТАЕМ NDVI (ЭТАЛОН)
# -------------------------

with rasterio.open(ndvi_path) as src:
    ndvi = src.read(1).astype("float32")
    profile = src.profile
    transform = src.transform
    crs = src.crs

print("NDVI loaded → target grid")

# -------------------------
# NDWI → ВЫРАВНИВАЕМ
# -------------------------

with rasterio.open(ndwi_path) as src:
    ndwi_raw = src.read(1).astype("float32")
    ndwi = align_to_target(
        ndwi_raw,
        src.transform,
        src.crs,
        profile
    )

with rasterio.open(ndwi_out, "w", **profile) as dst:
    dst.write(ndwi, 1)

print("NDWI aligned →", ndwi_out)

# -------------------------
# DIST → ВЫРАВНИВАЕМ
# -------------------------

with rasterio.open(dist_path) as src:
    dist_raw = src.read(1).astype("float32")
    dist = align_to_target(
        dist_raw,
        src.transform,
        src.crs,
        profile
    )

with rasterio.open(dist_out, "w", **profile) as dst:
    dst.write(dist, 1)

print("DIST aligned →", dist_out)

# -------------------------
# ПРОВЕРКА
# -------------------------

print("Shapes:")
print("NDVI:", ndvi.shape)
print("NDWI:", ndwi.shape)
print("DIST:", dist.shape)

print("DONE")