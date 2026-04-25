"""
Arquivo de Configurações Globais (config.py)
Contém as constantes do sistema, parâmetros do transformador e limiares do algoritmo.
"""

# ==========================================
# PARÂMETROS DO SISTEMA ELÉTRICO
# ==========================================
SYSTEM_FREQUENCY = 60.0        # Frequência fundamental do sistema em Hz (Padrão no México/Brasil)
NUM_PHASES = 3                 # Número de fases (A, B, C)

# ==========================================
# PARÂMETROS DA JANELA DE DADOS (Artigo: IV.B)
# ==========================================
SAMPLES_PER_CYCLE = 64         # Número de amostras por ciclo (n = 64)
# A dimensão da matriz deslizante será (SAMPLES_PER_CYCLE x NUM_PHASES) -> 64 x 3

# Frequência de amostragem (Sampling Rate)
# Calculada automaticamente: 64 amostras * 60 Hz = 3840 Hz
SAMPLING_RATE = SAMPLES_PER_CYCLE * SYSTEM_FREQUENCY 

# ==========================================
# PARÂMETROS DO ALGORITMO SCM (Artigo: IV.E e IV.F)
# ==========================================
SCM_THRESHOLD = 0.25           # Limiar de decisão de Bernoulli
# Condição de operação:
# SCM <= 0.25 -> Estado estável, Inrush ou Falla Externa (NÃO OPERAR)
# SCM >  0.25 -> Falla Interna (TRIP)

DDOF = 1                       # Delta Degrees of Freedom (Graus de liberdade para o cálculo da variância)
                               # O artigo especifica o uso de ddof=1 na Seção V (Python / std)

# ==========================================
# PARÂMETROS DA SIMULAÇÃO / INTERFACE GRÁFICA
# ==========================================
TIMER_INTERVAL_MS = 16         # Intervalo de atualização da UI em milissegundos (~60 FPS)

# Cores para a Interface Visual (Opcional, mas útil para o PyQtGraph)
COLOR_PHASE_A = (255, 0, 0)    # Vermelho
COLOR_PHASE_B = (0, 255, 0)    # Verde
COLOR_PHASE_C = (0, 0, 255)    # Azul
COLOR_SCM_LINE = (255, 255, 0) # Amarelo para a curva do SCM
COLOR_THRESHOLD = (255, 255, 255) # Branco tracejado para a linha de 0.25