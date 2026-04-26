import socket
import json
import time
import argparse
import sys
import os

# Adiciona o diretório raiz ao path para importar as lógicas e configurações do relé
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from relay.acquisition.simulation_reader import SimulationReader
from relay.config import SAMPLES_PER_CYCLE

def main():
    parser = argparse.ArgumentParser(description="Sandbox - Injetor de Sinais")
    parser.add_argument('--mode', type=str, default='fault', choices=['fault', 'inrush', 'normal'],
                        help="Modo de simulação do injetor")
    args = parser.parse_args()

    print(f"Sandbox (Injetor de Sinais) iniciado! Modo selecionado: {args.mode}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Reaproveita a excelente lógica do gerador existente sem duplicar código
    generator = SimulationReader(window_size=SAMPLES_PER_CYCLE, sim_mode=args.mode)
    ip_data = generator.ip_data
    is_data = generator.is_data
    
    print("\nPronto para injetar sinais!")
    input("Pressione ENTER para iniciar a injeção via UDP na porta 9999...")
    
    print("Enviando amostras...")
    for i in range(len(ip_data)):
        payload = {
            'ip': ip_data[i].tolist(),
            'is': is_data[i].tolist()
        }
        sock.sendto(json.dumps(payload).encode('utf-8'), ('127.0.0.1', 9999))
        
        # Controla a taxa de envio para não estourar o buffer UDP do sistema
        if i % 10 == 0:
            time.sleep(0.005)
            
    # Envia sinal de fim para que a interface trave e mostre o fim
    sock.sendto(json.dumps({'stop': True}).encode('utf-8'), ('127.0.0.1', 9999))
    print("Injeção finalizada!")

if __name__ == "__main__":
    main()
