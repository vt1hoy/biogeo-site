import rasterio
from rasterio.warp import reproject, Resampling
import geopandas as gpd
import osmnx as ox

# -------------------------
# INPUT
# -------------------------

ndvi_path = "../data/indices/ndvi_2025.tif"
ndwi_path = "../data/indices/ndwi_2025.tif"
aoi_path = "../data/aoi/centr_bou.gpkg"

ndwi_out = "../data/indices/ndwi_aligned.tif"

# -------------------------
# LOAD AOI
# -------------------------

aoi = gpd.read_file(aoi_path).to_crs(epsg=4326)
polygon = aoi.geometry.iloc[0]

# -------------------------
# ALIGN NDWI → NDVI GRID
# -------------------------

with rasterio.open(ndvi_path) as ref:
    ref_meta = ref.meta.copy()
    ref_data = ref.read(1)

with rasterio.open(ndwi_path) as src:
    ndwi_data = src.read(1)
    ndwi_meta = src.meta.copy()

# создаём пустой массив под новую сетку
aligned_ndwi = rasterio.band(
    rasterio.io.MemoryFile().open(**ref_meta),
    1
)

reproject(
    source=ndwi_data,
    destination=aligned_ndwi,
    src_transform=ndwi_meta["transform"],
    src_crs=ndwi_meta["crs"],
    dst_transform=ref_meta["transform"],
    dst_crs=ref_meta["crs"],
    resampling=Resampling.bilinear
)

# -------------------------
# SAVE
# -------------------------

with rasterio.open(ndwi_out, "w", **ref_meta) as dst:
    dst.write(aligned_ndwi, 1)

print("NDWI aligned to NDVI grid")

# -------------------------
# LOAD OSM ROADS
# -------------------------

roads = ox.features_from_polygon(
    polygon,
    tags={"highway": ["primary", "secondary", "tertiary"]}
)

roads = roads[roads.geometry.type.isin(["LineString", "MultiLineString"])]

print("Roads loaded:", len(roads))