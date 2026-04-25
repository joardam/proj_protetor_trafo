import numpy as np

class DeltaFilter:
    def __init__(self, window_size: int = 64):
        self.window_size = window_size
        self.history_buffer = None 

    def process_window(self, current_window: np.ndarray) -> np.ndarray:
        delta_data = self._apply_delta_filter(current_window)
        normalized_data = self._apply_normalization(delta_data)
        return normalized_data

    def _apply_delta_filter(self, window_data: np.ndarray) -> np.ndarray:
        # Se for o primeiro ciclo, não temos histórico. Assume histórico = dados atuais (diferença = 0)
        if self.history_buffer is None:
            self.history_buffer = window_data.copy()
            
        # Equação 4: ΔIdiff(k) = Idiff(k) - Idiff(k - nT)
        # Como o CSVReader avança 1 amostra por vez, history_buffer precisa guardar 
        # as amostras de exatos 1 ciclo (64 amostras) atrás. 
        # (Para simplificar nesta versão de janelas, subtraímos a janela anterior salva).
        delta = window_data - self.history_buffer
        
        # Atualiza o histórico para o PRÓXIMO processamento
        self.history_buffer = window_data.copy()
        
        return delta

    def _apply_normalization(self, delta_data: np.ndarray) -> np.ndarray:
        # Pega o valor absoluto máximo na janela (Equação 5 do artigo)
        max_val = np.max(np.abs(delta_data))
        
        # TRUQUE DE ENGENHARIA PARA EVITAR AMPLIFICAÇÃO DE RUÍDO:
        # Se o máximo for muito pequeno (quase zero, só ruído), 
        # forçamos o max_val para 1.0 para não explodir o ruído na tela.
        if max_val < 0.05: 
            max_val = 1.0
            
        # Equação 5: Normaliza dividindo tudo pelo máximo
        normalized = delta_data / max_val
        
        return normalized