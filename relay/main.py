import sys
import numpy as np
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

import config
from ui.main_window import MainWindow

from acquisition.udp_reader import UDPReader
from algorithm.pre_processing import PreProcessor
from algorithm.delta_filter import DeltaFilter
from algorithm.scm_calculator import SCMCalculator

class RelayApplicationController:
    def __init__(self):
        self.window = MainWindow()
        self.data_reader = UDPReader(port=9999, window_size=config.SAMPLES_PER_CYCLE)
        self.pre_processor = PreProcessor()
        self.delta_filter = DeltaFilter(window_size=config.SAMPLES_PER_CYCLE)
        self.scm_calculator = SCMCalculator(threshold=config.SCM_THRESHOLD, ddof=config.DDOF)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._process_next_sample)
        self.window.btn_toggle_sim.clicked.connect(self.toggle_simulation)

    def toggle_simulation(self):
        if self.timer.isActive():
            self.timer.stop()
            self.window.set_play_state(False)
        else:
            self.timer.start(config.TIMER_INTERVAL_MS)
            self.window.set_play_state(True)

    def _process_next_sample(self):
        processed_any = False
        incremental_data_to_plot = None
        is_trip_final = False

        # 1. ATUALIZA A REDE DE UMA VEZ SÓ (Tira a carga da CPU)
        if hasattr(self.data_reader, 'update_network'):
            self.data_reader.update_network()

        # 2. PROCESSA A MEMÓRIA RAM (Super rápido)
        while True:
            raw_data = self.data_reader.read_data()
            if raw_data is None: 
                break 
                
            processed_any = True
            
            compensated_data = self.pre_processor.apply_compensation(raw_data)
            incremental_data = self.delta_filter.process_window(compensated_data)
            scm_value, is_trip = self.scm_calculator.calculate(incremental_data)
            
            self.window.plot_scm.scm_history.append(scm_value)
            
            incremental_data_to_plot = incremental_data
            is_trip_final = is_trip

            if is_trip and self.window.is_auto_pause_enabled():
                self.timer.stop()
                self.window.set_play_state(False)
                break 

        # 3. ATUALIZA A PLACA DE VÍDEO (Apenas com o resultado final)
        if processed_any:
            self.window.update_currents_plot(incremental_data_to_plot)
            self.window.plot_scm.curve.setData(np.array(self.window.plot_scm.scm_history))
            self.window.update_trip_status(is_trip_final)
            
        if not processed_any and not getattr(self.data_reader, 'is_live', True):
            self.timer.stop()
            self.window.btn_toggle_sim.setText("⏹ Fim")
            self.window.btn_toggle_sim.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    controller = RelayApplicationController()
    controller.window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()