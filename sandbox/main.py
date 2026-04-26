import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Adiciona o diretório raiz ao path para podermos importar o config do relé
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sandbox.generators.continuous_generator import SignalGenerator
from sandbox.network.udp_sender import UDPSender
from sandbox.ui.main_window import SandboxWindow
from relay.config import SAMPLES_PER_CYCLE

class SandboxController:
    def __init__(self):
        self.window = SandboxWindow()
        self.generator = SignalGenerator(samples_per_cycle=SAMPLES_PER_CYCLE)
        self.sender = UDPSender()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._process_and_send)
        
        # Conexões dos cliques dos botões
        self.window.btn_normal.clicked.connect(self.inject_normal)
        self.window.btn_inrush.clicked.connect(self.inject_inrush)
        self.window.btn_fault.clicked.connect(self.inject_fault)
        self.window.btn_stop.clicked.connect(self.stop_injection)
        
        self.is_running = False

    def inject_normal(self):
        self.generator.set_mode('normal')
        self.window.set_status("Injetando Sinal Normal", "#28a745") # Verde
        self._start_engine()

    def inject_inrush(self):
        self.generator.set_mode('inrush')
        self.window.set_status("Injetando Inrush", "#ffc107", "black") # Amarelo (fonte preta)
        self._start_engine()

    def inject_fault(self):
        self.generator.set_mode('fault')
        self.window.set_status("Injetando Falha Interna", "#dc3545") # Vermelho
        self._start_engine()

    def stop_injection(self):
        if self.is_running:
            self.timer.stop()
            self.sender.send_stop()
            self.is_running = False
            self.window.set_status("PARADO / DESCONECTADO", "gray")

    def _start_engine(self):
        if not self.is_running:
            self.is_running = True
            # Frequência do pulso em MS: 1 ciclo a 60Hz leva ~16.6ms
            self.timer.start(16)

    def _process_and_send(self):
        # 1. Gera o próximo ciclo de ondas matemáticas
        ip_chunk, is_chunk = self.generator.get_next_chunk(chunk_size=SAMPLES_PER_CYCLE)
        
        # 2. Despacha por UDP
        # CORREÇÃO: Envia o bloco inteiro (64 amostras) de uma única vez.
        # Fim das perdas de pacotes do SO!
        self.sender.send_sample(ip_chunk, is_chunk)
            
        # 3. Desenha na tela do injetor o que acabou de ser enviado
        self.window.update_plot(ip_chunk, is_chunk)

def main():
    app = QApplication(sys.argv)
    controller = SandboxController()
    controller.window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()