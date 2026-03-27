import osmnx as ox
import geopandas as gpd

# Центр Дакара
place_point = (14.6918, -17.4395)
dist = 10000  # метров

print("1. Downloading walk network from OSM...")
G = ox.graph_from_point(place_point, dist=dist, network_type="walk")

print("2. Converting graph to GeoDataFrames...")
nodes, edges = ox.graph_to_gdfs(G)

print(f"Nodes: {len(nodes)}")
print(f"Edges: {len(edges)}")
print("Nodes CRS:", nodes.crs)
print("Edges CRS:", edges.crs)

# Сохраняем в output
nodes.to_file("output/dakar_walk_nodes.geojson", driver="GeoJSON")
edges.to_file("output/dakar_walk_edges.geojson", driver="GeoJSON")

print("Done. Files saved:")
print(" - output/dakar_walk_nodes.geojson")
print(" - output/dakar_walk_edges.geojson")