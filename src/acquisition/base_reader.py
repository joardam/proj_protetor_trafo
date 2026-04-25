"""
Define a classe base abstrata para os leitores de dados.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseReader(ABC):
    """
    Classe abstrata que define a interface padrão para qualquer fonte de aquisição de dados.
    """

    @abstractmethod
    def read_data(self) -> Optional[Dict[str, Any]]:
        """
        Lê uma nova amostra ou bloco de amostras da fonte de dados.
        """
        pass