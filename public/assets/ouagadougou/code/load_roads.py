import os
import osmnx as ox
import geopandas as gpd

# -------------------------
# INPUT
# -------------------------

aoi_path = "../data/aoi/centr_bou.gpkg"
output_path = "../data/osm/roads.gpkg"

os.makedirs("../data/osm", exist_ok=True)

# -------------------------
# AOI
# -------------------------

aoi = gpd.read_file(aoi_path).to_crs(epsg=4326)
polygon = aoi.geometry.iloc[0]

# -------------------------
# ROADS (OSM)
# -------------------------

roads = ox.features_from_polygon(
    polygon,
    tags={
        "highway": [
            
            "primary",
            "secondary",
            "tertiary"
        ]
    }
)

# оставляем только линии
roads = roads[roads.geometry.type.isin(["LineString", "MultiLineString"])]

# -------------------------
# SAVE
# -------------------------

roads.to_file(output_path, driver="GPKG")

print("Roads saved →", output_path)