import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

import config
from ui.main_window import MainWindow

# --- Injeção de Dependência (Escolha seu Reader aqui) ---
from acquisition.udp_reader import UDPReader
# from acquisition.simulation_reader import SimulationReader
# from acquisition.csv_reader import CSVReader
# --------------------------------------------------------

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
        """Alterna entre rodar e pausar a simulação."""
        if self.timer.isActive():
            self.timer.stop()
            self.window.set_play_state(False)
        else:
            self.timer.start(config.TIMER_INTERVAL_MS)
            self.window.set_play_state(True)

    def _process_next_sample(self):
        raw_data = self.data_reader.read_data()
        
        if raw_data is None: 
            # Se for uma fonte ao vivo, apenas aguardamos o próximo ciclo (não para o timer)
            if getattr(self.data_reader, 'is_live', False):
                return 
                
            self.timer.stop()
            self.window.btn_toggle_sim.setText("⏹ Fim")
            self.window.btn_toggle_sim.setEnabled(False)
            return
            
        compensated_data = self.pre_processor.apply_compensation(raw_data)
        incremental_data = self.delta_filter.process_window(compensated_data)
        scm_value, is_trip = self.scm_calculator.calculate(incremental_data)
        
        self.window.update_currents_plot(incremental_data)
        self.window.update_scm_plot(scm_value)
        self.window.update_trip_status(is_trip)

        # Lógica de auto-pause
        if is_trip and self.window.is_auto_pause_enabled():
            self.timer.stop()
            self.window.set_play_state(False)

def main():
    app = QApplication(sys.argv)
    controller = RelayApplicationController()
    controller.window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()