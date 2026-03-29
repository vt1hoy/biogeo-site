import rasterio
import numpy as np

# -------------------------
# INPUT
# -------------------------

ndvi_path = "../data/indices/ndvi_clip2.tif"
ndwi_path = "../data/indices/ndwi_clip2_aligned2.tif"
dist_path = "../data/results/dist_roads_aligned2.tif"

# OUTPUT
output_path = "../data/results/agri_score3.tif"

# -------------------------
# ФУНКЦИИ
# -------------------------

def clean_nodata(x):
    # убираем мусорные значения rasterio
    return np.where(x < -1e20, np.nan, x)

def normalize(x):
    x = clean_nodata(x)

    min_val = np.nanmin(x)
    max_val = np.nanmax(x)

    if max_val > min_val:
        x = (x - min_val) / (max_val - min_val)

    # заменяем NaN на 0
    x = np.nan_to_num(x)

    return x

# -------------------------
# ЗАГРУЗКА
# -------------------------

with rasterio.open(ndvi_path) as src:
    ndvi = src.read(1).astype("float32")
    profile = src.profile

with rasterio.open(ndwi_path) as src:
    ndwi = src.read(1).astype("float32")

with rasterio.open(dist_path) as src:
    dist = src.read(1).astype("float32")

print("Data loaded")

# -------------------------
# НОРМАЛИЗАЦИЯ
# -------------------------

ndvi = normalize(ndvi)
ndwi = normalize(ndwi)
dist = normalize(dist)

print("Normalized")

# -------------------------
# МОДЕЛЬ
# -------------------------

# ближе к дороге = лучше
dist_inv = 1 - dist

score = (
    ndvi * 0.5 +
    ndwi * 0.3 +
    dist_inv * 0.2
)

# усиление контраста
score = np.power(score, 1.5)

# финальная нормализация
score = normalize(score)

# -------------------------
# СОХРАНЕНИЕ
# -------------------------

profile.update(dtype=rasterio.float32)

with rasterio.open(output_path, "w", **profile) as dst:
    dst.write(score.astype("float32"), 1)

print("Saved →", output_path)