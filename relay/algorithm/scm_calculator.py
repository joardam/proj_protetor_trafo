import numpy as np

class SCMCalculator:
    def __init__(self, threshold: float = 0.25, ddof: int = 1):
        self.threshold = threshold
        self.ddof = ddof

    def calculate(self, normalized_delta_data: np.ndarray) -> tuple[float, bool]:
        # normalized_delta_data tem formato (64, 3) -> 64 amostras, 3 colunas (Fases A, B, C)
        
        # Calcula a variância (SCM) INDIVIDUALMENTE para cada fase
        scm_a = np.var(normalized_delta_data[:, 0], ddof=self.ddof)
        scm_b = np.var(normalized_delta_data[:, 1], ddof=self.ddof)
        scm_c = np.var(normalized_delta_data[:, 2], ddof=self.ddof)
        
        # O valor do SCM do sistema será o pior caso (o maior valor entre as fases)
        max_scm = max(scm_a, scm_b, scm_c)
        
        # Verifica se passou do limite (Tabela I do Artigo)
        is_trip = max_scm > self.threshold
        
        return max_scm, is_trip