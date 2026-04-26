"""
Leitor de dados a partir de arquivos CSV.
"""
import os
import pandas as pd
from typing import Dict, Any, Optional
from .base_reader import BaseReader

class CSVReader(BaseReader):
    def __init__(self, filepath: str, window_size: int = 64):
        """
        Inicializa o leitor lendo estritamente de um arquivo físico.
        """
        self.filepath = filepath
        self.window_size = window_size
        self.current_index = 0 
        
        self.ip_data = None
        self.is_data = None
        
        self._load_file()

    def _load_file(self):
        if os.path.exists(self.filepath):
            df = pd.read_csv(self.filepath)
            self.ip_data = df[['IpA', 'IpB', 'IpC']].values
            self.is_data = df[['IsA', 'IsB', 'IsC']].values
            print(f"Dados carregados com sucesso de {self.filepath}")
        else:
            # Princípio SRP: Se é um leitor de CSV, ele deve falhar se não há CSV.
            raise FileNotFoundError(f"Arquivo não encontrado no caminho: {self.filepath}")

    def read_data(self) -> Optional[Dict[str, Any]]:
        end_index = self.current_index + self.window_size
        
        if end_index > len(self.ip_data):
            return None
            
        window_ip = self.ip_data[self.current_index:end_index, :]
        window_is = self.is_data[self.current_index:end_index, :]
        
        self.current_index += 1 
        
        return {
            'ip': window_ip,
            'is': window_is
        }