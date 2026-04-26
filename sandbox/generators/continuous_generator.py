import numpy as np

class SignalGenerator:
    def __init__(self, freq=60.0, samples_per_cycle=64):
        self.freq = freq
        self.samples_per_cycle = samples_per_cycle
        self.sample_rate = freq * samples_per_cycle
        self.dt = 1.0 / self.sample_rate
        self.time = 0.0
        self.mode = 'normal'
        self.event_start_time = 0.0

    def set_mode(self, mode: str):
        if mode != self.mode:
            self.mode = mode
            self.event_start_time = self.time

    def get_next_chunk(self, chunk_size=64):
        t = np.linspace(self.time, self.time + chunk_size * self.dt, chunk_size, endpoint=False)
        self.time += chunk_size * self.dt

        # Sinais primários normais (Senóide perfeita trifásica)
        ip = np.column_stack([
            np.sin(2 * np.pi * self.freq * t),
            np.sin(2 * np.pi * self.freq * t - 2 * np.pi / 3),
            np.sin(2 * np.pi * self.freq * t + 2 * np.pi / 3)
        ])
        
        # Secundário defasado 180 graus (estado normal, com ruído mínimo do TC)
        is_sec = -ip + np.random.normal(0, 0.01, ip.shape)

        if self.mode != 'normal':
            t_event = t - self.event_start_time
            # Evita tempos negativos
            t_event[t_event < 0] = 0
            
            if self.mode == 'inrush':
                # Simulação de Inrush (apenas na fase A)
                inrush_wave = (5.0 * np.sin(2 * np.pi * self.freq * t_event) + 
                               1.5 * np.sin(2 * np.pi * 120 * t_event) + 
                               3.0 * np.exp(-15 * t_event))
                ip[:, 0] += inrush_wave
                
            elif self.mode == 'fault':
                # Simulação de Falha Interna (Curto-circuito gigantesco na fase A)
                fault_wave = 10.0 * np.sin(2 * np.pi * self.freq * t_event)
                ip[:, 0] += fault_wave
                # Adiciona descasamento grande ao secundário devido saturação
                is_sec[:, 0] += np.random.normal(0, 0.05, is_sec.shape[0])

        return ip, is_sec
