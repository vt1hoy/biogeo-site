import rasterio
import numpy as np

# =========================
# PATHS
# =========================

FLOW_PATH = r"C:\niamey\data\processed\niamey_flow_acc.tif"
SLOPE_PATH = r"C:\niamey\data\processed\niamey_slope.tif"

OUTPUT_PATH = r"C:\niamey\data\processed\niamey_flood_risk.tif"

# =========================
# LOAD
# =========================

print("Загрузка данных...")

with rasterio.open(FLOW_PATH) as src:
    flow = src.read(1)
    profile = src.profile

with rasterio.open(SLOPE_PATH) as src:
    slope = src.read(1)

# =========================
# CLEAN
# =========================

flow = np.nan_to_num(flow, nan=0)
slope = np.nan_to_num(slope, nan=0)

# =========================
# FLOW: LOG + NORMALIZE
# =========================

print("Обработка flow...")

flow_log = np.log10(flow + 1)

flow_norm = (flow_log - flow_log.min()) / (flow_log.max() - flow_log.min())

# =========================
# SLOPE: CLIP + NORMALIZE
# =========================

print("Обработка slope...")

slope_clipped = np.clip(slope, 0, 10)   # обрезка 0–10°
slope_norm = slope_clipped / 10         # нормализация

# =========================
# INDEX
# =========================

print("Считаем индекс риска...")

risk = flow_norm * (1 - slope_norm)

# =========================
# SAVE
# =========================

profile.update(dtype=rasterio.float32)

with rasterio.open(OUTPUT_PATH, 'w', **profile) as dst:
    dst.write(risk.astype(rasterio.float32), 1)

print("ГОТОВО: niamey_flood_risk.tif")