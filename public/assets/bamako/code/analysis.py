for lyr in QgsProject.instance().mapLayers().values():
    print(lyr.name(), "|", lyr.type())

for lyr in QgsProject.instance().mapLayers().values():
    if isinstance(lyr, QgsRasterLayer):
        print("Растр:", lyr.name(),"| путь: ", lyr.source())

from qgis.core import QgsVectorLayer
for lyr in QgsProject.instance().mapLayers().values():
    if isinstance(lyr, QgsVectorLayer):
        print("Вектор:", lyr.name(), "| путь:", lyr.sourse())

layer = iface.activeLayer()  # взять активный (выделенный в таблице слоёв)
print("Имя:", layer.name())
print("CRS:", layer.crs().authid())
print("Тип:", "растр" if isinstance(layer, QgsRasterLayer) else "вектор")

for lyr in QgsProject.instance().mapLayers().values():
    print(lyr.name(), "→", lyr.crs().authid())


