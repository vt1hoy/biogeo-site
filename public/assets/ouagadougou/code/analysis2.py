import rasterio
import numpy as np

# -------------------------
# INPUT
# -------------------------

ndvi_path = "../data/indices/ndvi_2025_cut.tif"
ndwi_path = "../data/indices/ndwi_2025_cut.tif"
dist_path = "../data/results/dist_roads.tif"

# OUTPUT
score_path = "../data/results/agri_score_2025.tif"
class_path = "../data/results/agri_classes_2025.tif"

# -------------------------
# FUNCTIONS
# -------------------------

def clean_nodata(x):
    return np.where(x < -1e20, np.nan, x)

def normalize(x):
    x = clean_nodata(x)
    min_val = np.nanmin(x)
    max_val = np.nanmax(x)

    if max_val > min_val:
        x = (x - min_val) / (max_val - min_val)

    return np.nan_to_num(x)

# -------------------------
# LOAD DATA
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
# NORMALIZATION
# -------------------------

ndvi = normalize(ndvi)
ndwi = normalize(ndwi)
dist = normalize(dist)

# ближе к дороге = лучше
access = 1 - dist

print("Normalized")

# -------------------------
# SUITABILITY MODEL
# -------------------------

score = (
    ndvi * 0.5 +
    ndwi * 0.3 +
    access * 0.2
)

# усиление контраста
score = np.power(score, 1.5)

# финальная нормализация
score = normalize(score)

# -------------------------
# CLASSIFICATION
# -------------------------

classes = np.zeros_like(score)

classes[score <= 0.3] = 1        # Low
classes[(score > 0.3) & (score <= 0.6)] = 2  # Medium
classes[score > 0.6] = 3         # High

# -------------------------
# SAVE OUTPUTS
# -------------------------

profile.update(dtype=rasterio.float32)

with rasterio.open(score_path, "w", **profile) as dst:
    dst.write(score.astype("float32"), 1)

with rasterio.open(class_path, "w", **profile) as dst:
    dst.write(classes.astype("float32"), 1)

print("Saved:")
print(" - Suitability score →", score_path)
print(" - Classes →", class_path)