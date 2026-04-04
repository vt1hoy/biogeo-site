import rasterio
import numpy as np

# =========================
# PATHS
# =========================

DEM_PATH = r"C:\niamey\data\processed\niamey_dem_clipped.tif"
SLOPE_PATH = r"C:\niamey\data\processed\niamey_slope.tif"

# =========================
# LOAD DEM
# =========================

print("Загрузка DEM...")

with rasterio.open(DEM_PATH) as src:
    dem = src.read(1)
    profile = src.profile
    transform = src.transform

# =========================
# PIXEL SIZE
# =========================

pixel_size_x = transform[0]
pixel_size_y = -transform[4]

print(f"Размер пикселя: {pixel_size_x} x {pixel_size_y} м")

# =========================
# GRADIENT
# =========================

print("Считаем градиенты...")

dx = np.gradient(dem, axis=1) / pixel_size_x
dy = np.gradient(dem, axis=0) / pixel_size_y

# =========================
# SLOPE (градусы)
# =========================

print("Считаем slope...")

slope = np.degrees(np.arctan(np.sqrt(dx**2 + dy**2)))

# =========================
# SAVE
# =========================

profile.update(dtype=rasterio.float32)

with rasterio.open(SLOPE_PATH, 'w', **profile) as dst:
    dst.write(slope.astype(rasterio.float32), 1)

print("ГОТОВО: niamey_slope.tif")