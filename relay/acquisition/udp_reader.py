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
        
        self.buffer_ip =[]
        self.buffer_is =[]
        self.is_live = True # Flag para a interface não fechar enquanto houver injeção

    def read_data(self) -> Optional[Dict[str, Any]]:
        # Se a simulação acabou e não há mais janela completa, encerra
        if not self.is_live and len(self.buffer_ip) < self.window_size:
            return None

        while True:
            try:
                data, _ = self.sock.recvfrom(65536)
                parsed = json.loads(data.decode('utf-8'))
                
                # Sinalização de fim de injeção
                if 'stop' in parsed:
                    self.is_live = False
                    break
                    
                self.buffer_ip.append(parsed['ip'])
                self.buffer_is.append(parsed['is'])
            except BlockingIOError:
                break # Sem mais pacotes na fila
            except Exception as e:
                print(f"Erro no UDPReader: {e}")
                break
                
        # Se acumulamos uma janela completa, retornamos e avançamos 1 amostra
        if len(self.buffer_ip) >= self.window_size:
            window_ip = np.array(self.buffer_ip[:self.window_size])
            window_is = np.array(self.buffer_is[:self.window_size])
            
            self.buffer_ip.pop(0)
            self.buffer_is.pop(0)
            
            return {
                'ip': window_ip,
                'is': window_is
            }
            
        return None
