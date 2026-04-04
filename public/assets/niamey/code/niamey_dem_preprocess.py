import rasterio
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
import geopandas as gpd

# =========================
# PATHS (твой кейс)
# =========================

DEM_PATH = r"C:\niamey\qgis\dem\output_hh.tif"
AOI_PATH = r"C:\niamey\qgis\niamey_mask.gpkg"

OUTPUT_REPROJECTED = r"C:\niamey\data\processed\niamey_dem_utm.tif"
OUTPUT_CLIPPED = r"C:\niamey\data\processed\niamey_dem_clipped.tif"

TARGET_CRS = "EPSG:32631"

# =========================
# 1. REPROJECT DEM → UTM
# =========================

print("Перепроекция DEM в UTM...")

with rasterio.open(DEM_PATH) as src:
    transform, width, height = calculate_default_transform(
        src.crs, TARGET_CRS, src.width, src.height, *src.bounds
    )

    kwargs = src.meta.copy()
    kwargs.update({
        "crs": TARGET_CRS,
        "transform": transform,
        "width": width,
        "height": height
    })

    with rasterio.open(OUTPUT_REPROJECTED, "w", **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=TARGET_CRS,
                resampling=Resampling.bilinear
            )

print("DEM перепроецирован")

# =========================
# 2. CLIP ПО AOI
# =========================

print("Обрезка по AOI...")

aoi = gpd.read_file(AOI_PATH)

with rasterio.open(OUTPUT_REPROJECTED) as src:
    aoi = aoi.to_crs(src.crs)

    out_image, out_transform = mask(src, aoi.geometry, crop=True)

    out_meta = src.meta.copy()
    out_meta.update({
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    with rasterio.open(OUTPUT_CLIPPED, "w", **out_meta) as dest:
        dest.write(out_image)

print("ГОТОВО: niamey_dem_clipped.tif")