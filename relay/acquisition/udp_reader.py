import socket
import json
import numpy as np
from typing import Dict, Any, Optional
from .base_reader import BaseReader

class UDPReader(BaseReader):
    def __init__(self, port: int = 9999, window_size: int = 64):
        self.window_size = window_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('127.0.0.1', port))
        self.sock.setblocking(False)
        
        self.buffer_ip = []
        self.buffer_is =[]
        self.is_live = True

    def update_network(self):
        """Drena a placa de rede de uma só vez para não travar a CPU."""
        while True:
            try:
                data, _ = self.sock.recvfrom(65536)
                parsed = json.loads(data.decode('utf-8'))
                
                if 'stop' in parsed:
                    self.is_live = False
                    break
                    
                if isinstance(parsed['ip'][0], list):
                    self.buffer_ip.extend(parsed['ip'])
                    self.buffer_is.extend(parsed['is'])
                else:
                    self.buffer_ip.append(parsed['ip'])
                    self.buffer_is.append(parsed['is'])
                    
            except BlockingIOError:
                break 
            except Exception as e:
                print(f"Erro no UDPReader: {e}")
                break
        
        # PROTEÇÃO ANTI-LAG E MEMORY LEAK: 
        # Se a janela pausar e o Sandbox continuar enviando, cortamos o excesso
        max_buffer = self.window_size * 10
        if len(self.buffer_ip) > max_buffer:
            self.buffer_ip = self.buffer_ip[-max_buffer:]
            self.buffer_is = self.buffer_is[-max_buffer:]

    def read_data(self) -> Optional[Dict[str, Any]]:
        # A matemática consumirá RAM perfeitamente ciclo a ciclo
        if not self.is_live and len(self.buffer_ip) < self.window_size:
            return None

        if len(self.buffer_ip) >= self.window_size:
            window_ip = np.array(self.buffer_ip[:self.window_size])
            window_is = np.array(self.buffer_is[:self.window_size])
            
            # CORREÇÃO 1: Avança 1 ciclo (64 amostras) de uma vez.
            # Zera o travamento da interface e corrige a matemática do Filtro Delta!
            self.buffer_ip = self.buffer_ip[self.window_size:]
            self.buffer_is = self.buffer_is[self.window_size:]
            
            return {
                'ip': window_ip,
                'is': window_is
            }
            
        return None