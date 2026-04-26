"""
Janela principal da aplicação.
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QCheckBox)
from PyQt6.QtCore import Qt
import config
from .indicators import TripIndicator
from .plot_widgets import CurrentsPlotWidget, SCMPlotWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Relé Diferencial SCM - Embarcado (ROPEC 2024)")
        self.resize(800, 600)  # Diminui o tamanho base
        self.showMaximized()   # Força a janela a se adaptar ao tamanho da tela
        self._setup_ui()
        self.resize(1024, 768)
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # -----------------------------------------
        # ZONA SUPERIOR: Controles e Status
        # -----------------------------------------
        top_layout = QHBoxLayout()
        
        # Botão de Play/Pause
        self.btn_toggle_sim = QPushButton("▶ Play")
        self.btn_toggle_sim.setFixedSize(120, 40)
        self.btn_toggle_sim.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        # Novo Checkbox de Auto-Pause
        self.cb_auto_pause = QCheckBox("Pausar automaticamente no Trip")
        self.cb_auto_pause.setChecked(True) # Deixaremos marcado por padrão
        self.cb_auto_pause.setStyleSheet("font-size: 14px; margin-left: 15px;")
        
        self.indicator = TripIndicator()
        
        top_layout.addWidget(self.btn_toggle_sim)
        top_layout.addWidget(self.cb_auto_pause)
        top_layout.addStretch() 
        top_layout.addWidget(self.indicator)
        
        main_layout.addLayout(top_layout)

        # -----------------------------------------
        # ZONA CENTRAL E INFERIOR: Gráficos
        # -----------------------------------------
        self.plot_currents = CurrentsPlotWidget()
        main_layout.addWidget(self.plot_currents, stretch=2)

        self.plot_scm = SCMPlotWidget(threshold_value=config.SCM_THRESHOLD)
        main_layout.addWidget(self.plot_scm, stretch=1)

    # ========================================================
    # Métodos Auxiliares
    # ========================================================
    
    def set_play_state(self, is_playing: bool):
        """Muda a aparência do botão dependendo do estado da simulação."""
        if is_playing:
            self.btn_toggle_sim.setText("⏸ Pause")
        else:
            self.btn_toggle_sim.setText("▶ Play")

    def is_auto_pause_enabled(self) -> bool:
        """Retorna True se o usuário marcou a opção de pausar no Trip."""
        return self.cb_auto_pause.isChecked()

    def update_currents_plot(self, data):
        self.plot_currents.update_plot(data)

    def update_scm_plot(self, scm_value: float):
        self.plot_scm.update_plot(scm_value)

    def update_trip_status(self, is_trip: bool):
        self.indicator.set_trip_status(is_trip)