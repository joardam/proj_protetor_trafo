from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QGroupBox)
from PyQt6.QtCore import Qt
import pyqtgraph as pg

class SandboxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sandbox Interativo - Injetor de Sinais SCM")
        self.resize(900, 600)
        
        self.history_ip = []
        self.history_is = []
        self.max_history = 64 * 6  # Exibe sempre os últimos 6 ciclos na tela
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # -----------------------------------------
        # PAINEL DE CONTROLE (BOTÕES DE INJEÇÃO)
        # -----------------------------------------
        ctrl_group = QGroupBox("Painel de Controle de Faltas")
        ctrl_group.setStyleSheet("font-weight: bold; font-size: 14px;")
        ctrl_layout = QHBoxLayout(ctrl_group)

        self.btn_normal = QPushButton("▶ Injetar Normal")
        self.btn_normal.setStyleSheet("background-color: #28a745; color: white; padding: 10px; font-weight: bold;")
        
        self.btn_inrush = QPushButton("⚡ Injetar Inrush")
        self.btn_inrush.setStyleSheet("background-color: #ffc107; color: black; padding: 10px; font-weight: bold;")
        
        self.btn_fault = QPushButton("🔥 Injetar Falha Interna")
        self.btn_fault.setStyleSheet("background-color: #dc3545; color: white; padding: 10px; font-weight: bold;")
        
        self.btn_stop = QPushButton("⏹ Parar Injeção")
        self.btn_stop.setStyleSheet("background-color: #6c757d; color: white; padding: 10px; font-weight: bold;")

        for btn in [self.btn_normal, self.btn_inrush, self.btn_fault, self.btn_stop]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            ctrl_layout.addWidget(btn)

        self.status_label = QLabel("STATUS: DESCONECTADO")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            font-weight: bold; color: white; background-color: gray; 
            padding: 10px; border-radius: 5px;
        """)
        ctrl_layout.addWidget(self.status_label)
        
        main_layout.addWidget(ctrl_group)

        # -----------------------------------------
        # GRÁFICO (Monitoramento do envio - Fase A)
        # -----------------------------------------
        self.plot_widget = pg.PlotWidget(title="Sinal Injetado Via UDP (Fase A)")
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setYRange(-15, 15)
        self.plot_widget.addLegend()
        
        # Curva de Ip (Corrente Primária)
        self.curve_ip = self.plot_widget.plot(pen=pg.mkPen('r', width=2), name="Ip (Corrente Primária)")
        # Curva de Is (Corrente Secundária)
        self.curve_is = self.plot_widget.plot(pen=pg.mkPen('b', width=2), name="Is (Corrente Secundária - Refletida)")
        
        main_layout.addWidget(self.plot_widget, stretch=1)

    def set_status(self, text: str, color_hex: str, text_color: str = "white"):
        self.status_label.setText(f"STATUS: {text.upper()}")
        self.status_label.setStyleSheet(f"""
            font-weight: bold; color: {text_color}; background-color: {color_hex}; 
            padding: 10px; border-radius: 5px;
        """)

    def update_plot(self, ip_chunk, is_chunk):
        # Para ficar fácil de visualizar, plotamos só a Fase A (coluna 0)
        self.history_ip.extend(ip_chunk[:, 0])
        self.history_is.extend(is_chunk[:, 0])
        
        # Mantém a janela deslizante no gráfico local
        if len(self.history_ip) > self.max_history:
            self.history_ip = self.history_ip[-self.max_history:]
            self.history_is = self.history_is[-self.max_history:]
            
        self.curve_ip.setData(self.history_ip)
        self.curve_is.setData(self.history_is)
