# Relé Diferencial SCM - Embarcado (Python) ⚡

Este projeto é uma implementação em software de um **Relé de Proteção Diferencial para Transformadores de Potência**, baseado no algoritmo do Segundo Momento Central (SMC / SCM). 

A arquitetura foi projetada com forte Separação de Responsabilidades (SRP), permitindo que o algoritmo de proteção rode de forma independente da interface gráfica e da fonte de dados (seja ela um arquivo CSV, um gerador matemático simulado ou, no futuro, dados reais via rede UDP/Serial).

*Baseado no artigo técnico do ROPEC 2024.*

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.8+
* **Interface Gráfica:** PyQt6
* **Plotagem de Alta Performance:** PyQtGraph
* **Processamento Matemático:** NumPy, Pandas

---

## 🚀 Como baixar e instalar

Siga o passo a passo abaixo para rodar o projeto na sua máquina local:

### 1. Clone o repositório
Abra o seu terminal (Prompt de Comando, PowerShell ou Terminal do Linux/Mac) e digite:
```bash
git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
cd NOME_DO_REPOSITORIO
```
(Lembre-se de substituir o link acima pelo link real do seu repositório no GitHub)

### 2. Crie um Ambiente Virtual (Recomendado)

Para não misturar as bibliotecas deste projeto com as do seu computador, crie um ambiente virtual (venv):

No Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

No Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
(Você saberá que deu certo quando aparecer `(venv)` no início da linha do seu terminal).

### 3. Instale as dependências

Com o ambiente ativado, instale as bibliotecas necessárias listadas no `requirements.txt`:
```bash
pip install -r requirements.txt
```

## ▶️ Como rodar o Simulador

Para iniciar a interface gráfica do Relé, execute o arquivo principal:
```bash
python relay/main.py
```

## 🎮 Como testar os diferentes cenários (Inrush vs Trip)

O projeto possui um Gerador de Sinais Sintéticos embutido (`SimulationReader`). Por padrão, ele simula 50 ciclos normais e depois dispara um evento.

Para alternar entre uma onda de Inrush (que NÃO deve gerar Trip) e uma Falha Interna (que DEVE gerar Trip), siga estes passos:

1. Abra o arquivo `relay/main.py` no seu editor de código.
2. Procure a inicialização do `SimulationReader` (por volta da linha 23).
3. Mude o parâmetro `sim_mode`:

Para simular Inrush (Relé bloqueia e não atua):
```python
self.data_reader = SimulationReader(window_size=config.SAMPLES_PER_CYCLE, sim_mode='inrush')
```

Para simular Curto-circuito / Falha Interna (Relé atua e pausa):
```python
self.data_reader = SimulationReader(window_size=config.SAMPLES_PER_CYCLE, sim_mode='fault')
```

4. Salve o arquivo e rode `python relay/main.py` novamente. Na tela da simulação, use a checkbox "Pausar automaticamente no Trip" para analisar o exato ciclo em que a falha foi detectada.

## 📂 Estrutura do Projeto

- `relay/acquisition/`: Contém os leitores de dados (Gerador simulado, CSV). É a nossa porta de entrada de correntes.
- `relay/algorithm/`: O coração do relé. Contém matemática pura (Filtro Delta, Normalização e o cálculo de Variância SCM).
- `relay/ui/`: Todos os componentes visuais, botões e gráficos.
- `relay/main.py`: O orquestrador que une a interface, os dados e a matemática.
