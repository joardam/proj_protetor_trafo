# Projeto Relé Diferencial

Este projeto implementa um sistema de proteção diferencial para transformadores de potência baseado no algoritmo do Segundo Momento Central (SCM). O software é desenvolvido em Python, com foco em uma arquitetura modular que permite execução inicial em simulação (dados em arquivo CSV) e futura implantação em hardware real (Raspberry Pi/Arduino).

## Arquitetura

O sistema é separado em camadas (Separação de Preocupações):
- **Camada de Aquisição (`src/acquisition`):** Responsável por ler correntes de um arquivo `.csv` ou da porta serial.
- **Camada de Algoritmo (`src/algorithm`):** Processamento de sinais e implementação do algoritmo SCM de forma independente de hardware ou UI.
- **Camada de Interface (`src/ui`):** Componentes visuais para exibição de oscilografias e status do relé de proteção (PyQt6/pyqtgraph).

## Instalação e Execução

```bash
pip install -r requirements.txt
python src/main.py
```
