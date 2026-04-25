"""
Componentes visuais indicadores de estado.
"""
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class TripIndicator(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(250, 40)
        self._set_safe_style()

    def set_trip_status(self, is_trip: bool):
        if is_trip:
            self.setText("FALHA INTERNA DETECTADA (TRIP)")
            self._set_danger_style()
        else:
            self.setText("SISTEMA NORMAL (SEGURO)")
            self._set_safe_style()

    def _set_safe_style(self):
        self.setStyleSheet("""
            background-color: #28a745; 
            color: white; 
            font-weight: bold; 
            font-size: 14px;
            border-radius: 5px;
        """)

    def _set_danger_style(self):
        self.setStyleSheet("""
            background-color: #dc3545; 
            color: white; 
            font-weight: bold; 
            font-size: 14px;
            border-radius: 5px;
        """)