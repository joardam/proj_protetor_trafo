"""
Leitor de dados simulados (Gerador Sintético).
Gera ondas de estado normal, inrush e falha internamente usando equações matemáticas.
"""
import numpy as np
from typing import Dict, Any, Optional
from .base_reader import BaseReader

class SimulationReader(BaseReader):
    def __init__(self, window_size: int = 64, sim_mode: str = 'inrush'):
        """
        Inicializa o gerador de sinais.
        :param window_size: Tamanho da janela de dados (padrão = 64 amostras/ciclo).
        :param sim_mode: 'inrush', 'fault' ou 'normal'.
        """
        self.window_size = window_size
        self.sim_mode = sim_mode.lower()
        self.current_index = 0 
        
        self.ip_data = None
        self.is_data = None
        
        print(f"Gerando dados sintéticos no modo: '{self.sim_mode}'...")
        self._generate_synthetic_data()

    def _generate_synthetic_data(self):
        """Gera dados sintéticos: 50 ciclos normais, seguidos de 50 ciclos com anomalia."""
        freq = 60 # Frequência fundamental (60Hz)
        total_cycles = 100
        total_samples = total_cycles * self.window_size
        
        # Criação do vetor de tempo preciso para 64 amostras por ciclo
        t = np.linspace(0, total_cycles / freq, total_samples, endpoint=False)
        
        # Estado Normal (Ip e Is se anulam perfeitamente, com leve ruído)
        ip = np.column_stack([
            np.sin(2 * np.pi * freq * t),
            np.sin(2 * np.pi * freq * t - 2*np.pi/3),
            np.sin(2 * np.pi * freq * t + 2*np.pi/3)
        ])
        
        # Secundário defasado 180 graus
        is_sec = -ip + np.random.normal(0, 0.01, ip.shape) 
        
        # Índice onde o evento começa (ciclo 50)
        event_start = 50 * self.window_size
        t_event = t[event_start:] - t[event_start] 
        
        if self.sim_mode == 'inrush':
            # Simulação de Inrush
            inrush_wave = (5.0 * np.sin(2 * np.pi * freq * t_event) + 
                           1.5 * np.sin(2 * np.pi * 120 * t_event) + 
                           3.0 * np.exp(-15 * t_event))
            ip[event_start:, 0] += inrush_wave 
            
        elif self.sim_mode == 'fault':
            # Simulação de Falha Interna
            fault_wave = 10.0 * np.sin(2 * np.pi * freq * t_event)
            ip[event_start:, 0] += fault_wave
            is_sec[event_start:, 0] = np.random.normal(0, 0.05, is_sec[event_start:, 0].shape)

        self.ip_data = ip
        self.is_data = is_sec

    def read_data(self) -> Optional[Dict[str, Any]]:
        """Lê a próxima janela avançando 1 amostra por vez."""
        end_index = self.current_index + self.window_size
        
        if end_index > len(self.ip_data):
            return None # Fim da simulação
            
        window_ip = self.ip_data[self.current_index:end_index, :]
        window_is = self.is_data[self.current_index:end_index, :]
        
        self.current_index += 1 
        
        return {
            'ip': window_ip,
            'is': window_is
        }