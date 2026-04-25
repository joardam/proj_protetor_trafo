"""
Gráficos em tempo real utilizando PyQtGraph.
"""
import pyqtgraph as pg
import numpy as np
from collections import deque

class CurrentsPlotWidget(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.setTitle("Correntes Diferenciais Normalizadas (∆Idiff)", color="w", size="12pt")
        self.showGrid(x=True, y=True)
        self.setYRange(-1.5, 1.5)
        
        self.addLegend()
        self.curve_a = self.plot(pen=pg.mkPen('r', width=2), name="Fase A")
        self.curve_b = self.plot(pen=pg.mkPen('g', width=2), name="Fase B")
        self.curve_c = self.plot(pen=pg.mkPen('b', width=2), name="Fase C")

    def update_plot(self, idiff_data: np.ndarray):
        # idiff_data é (64, 3)
        x_axis = np.arange(idiff_data.shape[0])
        self.curve_a.setData(x_axis, idiff_data[:, 0])
        self.curve_b.setData(x_axis, idiff_data[:, 1])
        self.curve_c.setData(x_axis, idiff_data[:, 2])


class SCMPlotWidget(pg.PlotWidget):
    def __init__(self, threshold_value: float):
        super().__init__()
        self.setTitle("Magnitude do SCM", color="w", size="12pt")
        self.showGrid(x=True, y=True)
        self.setYRange(0, 0.6) # Baseado nas imagens do artigo
        
        # Histórico para fazer o gráfico deslizar (ex: exibe os últimos 200 ciclos)
        self.history_size = 200
        self.scm_history = deque([0.0]*self.history_size, maxlen=self.history_size)
        
        # Linha de Limiar
        self.threshold_line = pg.InfiniteLine(
            pos=threshold_value, angle=0, movable=False, 
            pen=pg.mkPen('w', style=pg.QtCore.Qt.PenStyle.DashLine, width=2)
        )
        self.addItem(self.threshold_line)
        
        self.curve = self.plot(pen=pg.mkPen('y', width=2))

    def update_plot(self, current_scm_value: float):
        self.scm_history.append(current_scm_value)
        self.curve.setData(np.array(self.scm_history))