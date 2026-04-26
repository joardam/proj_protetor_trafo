"""
Módulo de Pré-processamento.
"""
import numpy as np
from typing import Dict, Any

class PreProcessor:
    def __init__(self, tap_compensation_factor: float = 1.0):
        self.alpha_t = tap_compensation_factor

    def apply_compensation(self, raw_data: Dict[str, Any]) -> np.ndarray:
        """
        Calcula as correntes diferenciais (Idiff).
        Para esta simplificação inicial, assume que os TCs já estão compensados em ângulo
        e apenas aplica a soma algébrica (Idiff = Ip + Is, assumindo Is já invertido).
        """
        ip_abc = raw_data['ip']
        is_abc = raw_data['is']
        
        # Idiff = Ip + Is (Equação simplificada do relé diferencial)
        idiff_abc = ip_abc + is_abc
        
        return idiff_abc