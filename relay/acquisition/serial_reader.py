"""
Leitor de dados em tempo real utilizando porta Serial (Comunicação com Arduino).
"""
import numpy as np
from typing import Tuple, Optional
from .base_reader import BaseReader

class SerialReader(BaseReader):
    """
    Conecta a uma porta Serial (ex: COM3 ou /dev/ttyUSB0) e monta a janela
    de dados a partir dos bytes recebidos do conversor ADC (Arduino).
    """
    def __init__(self, port: str, baudrate: int, window_size: int = 64):
        """
        :param port: Porta serial do Arduino.
        :param baudrate: Velocidade da comunicação (ex: 115200).
        :param window_size: Tamanho da janela para preencher antes de retornar.
        """
        self.port = port
        self.baudrate = baudrate
        self.window_size = window_size
        
        # Instância da conexão serial (usando a biblioteca pyserial futuramente)
        self.serial_conn = None 
        
        # Buffer temporário para ir acumulando as amostras que chegam
        self._buffer_ip = []
        self._buffer_is = []

    def connect(self):
        """Abre a conexão com a porta serial."""
        pass

    def disconnect(self):
        """Fecha a conexão serial com segurança."""
        pass

    def read_next_window(self) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """
        Lê os dados continuamente da porta serial até preencher uma janela de tamanho 'window_size'.
        (Simula a janela deslizante aguardando o hardware).
        """
        pass
        # Lógica futura:
        # 1. Enquanto len(_buffer) < window_size, lê linha da porta serial.
        # 2. Converter valores (considerando a sensibilidade de 185mV/A mencionada no artigo).
        # 3. Empilhar nas listas.
        # 4. Converter listas para np.ndarray e retornar.
        # return ip_abc, is_abc