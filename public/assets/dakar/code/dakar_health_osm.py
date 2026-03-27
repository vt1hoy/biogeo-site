import osmnx as ox
import geopandas as gpd

place_name = "Dakar, Senegal"

print("1. Downloading health facilities from OSM...")

tags = {
    "amenity": ["hospital", "clinic", "doctors", "health_post"]
}

gdf = ox.features_from_place(place_name, tags)

print(f"Total objects: {len(gdf)}")

# Оставляем только точки (если вдруг попадутся полигоны)
gdf = gdf[gdf.geometry.type.isin(["Point", "MultiPoint"])]

print(f"Point features: {len(gdf)}")

# Оставляем нужные поля
gdf = gdf[["amenity", "name", "geometry"]]

# Сохраняем
gdf.to_file("output/dakar_health.geojson", driver="GeoJSON")

print("Done:")
print(" - output/dakar_health.geojson")