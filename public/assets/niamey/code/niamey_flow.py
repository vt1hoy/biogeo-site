from whitebox import WhiteboxTools

wbt = WhiteboxTools()

DEM = r"C:\niamey\data\processed\niamey_dem_clipped.tif"

FILLED = r"C:\niamey\data\processed\niamey_dem_filled.tif"
FLOW_ACC = r"C:\niamey\data\processed\niamey_flow_acc.tif"

print("Заполняем депрессии...")
wbt.fill_depressions(DEM, FILLED)

print("Считаем flow accumulation...")
wbt.d8_flow_accumulation(FILLED, FLOW_ACC)

print("ГОТОВО")