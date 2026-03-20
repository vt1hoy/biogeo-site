# -*- coding: utf-8 -*-
import os
import re
from qgis.PyQt import uic, QtWidgets
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import (
    QgsProject, QgsRasterLayer
)
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'refu_forest_dialog_base.ui'))

class RefuForestDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(RefuForestDialog, self).__init__(parent)
        self.setupUi(self)

        self.populate_layers()
        QgsProject.instance().layersAdded.connect(lambda _l: self.populate_layers())
        QgsProject.instance().layerWillBeRemoved.connect(lambda _id: self.populate_layers())

        self.pushButtonFilter.clicked.connect(self.filter_ndvi)

    # ---------- вспомогательное ----------
    def populate_layers(self):
        for cb in (self.comboBoxNdvi, self.comboBoxQual):
            cb.clear()
        for lyr in QgsProject.instance().mapLayers().values():
            if isinstance(lyr, QgsRasterLayer):
                # показываем имя, храним ID
                self.comboBoxNdvi.addItem(lyr.name(), lyr.id())
                self.comboBoxQual.addItem(lyr.name(), lyr.id())

    def _selected_raster(self, combo):
        lyr_id = combo.currentData()
        return QgsProject.instance().mapLayer(lyr_id)

    @staticmethod
    def _safe_name(name: str) -> str:
        safe = re.sub(r'[^A-Za-z0-9_.-]+', '_', name)
        return safe[:80]

    # ---------- основное действие ----------
    def filter_ndvi(self):
        """
        Минимальная версия: берём NDVI только там, где QUAL == 0 или 2.
        NDVI делим на 10000; остальное = -9999 (NoData).
        """
        ndvi = self._selected_raster(self.comboBoxNdvi)
        qual = self._selected_raster(self.comboBoxQual)

        if not ndvi or not qual:
            QMessageBox.warning(self, "RefuForest", "Выбери NDVI и QUAL слои.")
            return

        # быстрые проверки совместимости
        if ndvi.crs().authid() != qual.crs().authid():
            QMessageBox.warning(self, "RefuForest",
                                "CRS слоёв не совпадает. Приведи к одной СК (например, оба в EPSG:4326 или оба в EPSG:32637).")
            return
        if (ndvi.width(), ndvi.height()) != (qual.width(), qual.height()):
            QMessageBox.warning(self, "RefuForest",
                                "Размер пикселей/раскладка растров не совпадают (разное WIDTH/HEIGHT).\n"
                                "Выровняй растр QUAL под NDVI (Инструменты обработки → GDAL → Ресэмплинг / Align rasters).")
            return

        # куда пишем (короткий ASCII-путь)
        out_dir = r"C:\RefuForest"
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{self._safe_name(ndvi.name())}_filtered.tif")

        # готовим ссылки на каналы
        entries = []

        e_ndvi = QgsRasterCalculatorEntry()
        e_ndvi.ref = 'ndvi@1'
        e_ndvi.raster = ndvi
        e_ndvi.bandNumber = 1
        entries.append(e_ndvi)

        e_qual = QgsRasterCalculatorEntry()
        e_qual.ref = 'qual@1'
        e_qual.raster = qual
        e_qual.bandNumber = 1
        entries.append(e_qual)

        # выражение калькулятора ядра QGIS (без Processing)
        expr = 'if( ( "qual@1" = 0 OR "qual@1" = 2 ) AND ( "ndvi@1" > -2000 ), "ndvi@1" / 10000.0, -9999 )'

        # параметры сетки берём из NDVI
        extent = ndvi.extent()
        width = ndvi.width()
        height = ndvi.height()

        calc = QgsRasterCalculator(expr, out_path, 'GTiff', extent, width, height, entries)
        result = calc.processCalculation()   # 0 = успех

        if result != 0 or (not os.path.exists(out_path)):
            QMessageBox.warning(self, "RefuForest",
                                f"Расчёт не удался (код {result}) или файл не найден:\n{out_path}")
            return

        out_layer = QgsRasterLayer(out_path, os.path.basename(out_path))
        if out_layer.isValid():
            QgsProject.instance().addMapLayer(out_layer)
            QMessageBox.information(self, "RefuForest", f"Результат сохранён и добавлен:\n{out_path}")
        else:
            QMessageBox.warning(self, "RefuForest", "Файл создан, но слой не загрузился:\n" + out_path)
