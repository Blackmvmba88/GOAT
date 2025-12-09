#!/usr/bin/env python3
"""
GOAT Módulo de Configuración
Gestiona ajustes y configuración para el reproductor
"""

import json
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class Config:
    """Gestor de configuración para reproductor GOAT"""
    
    DEFAULT_CONFIG = {
        'display': {
            'width': 1280,
            'height': 720,
            'fullscreen': False,
            'fps': 60
        },
        'audio': {
            'frequency': 44100,
            'channels': 2,
            'buffer_size': 512
        },
        'visualization': {
            'mode': 'spectrum',
            'enable_ai': True,
            'particle_count': 100,
            'color_themes': [
                'vibrante',
                'pastel',
                'oscuro',
                'neón'
            ],
            'default_theme': 'vibrante'
        },
        'ai': {
            'enable_mood_detection': True,
            'enable_genre_detection': True,
            'enable_adaptive_visuals': True,
            'enable_smart_playlist': False
        },
        'playback': {
            'auto_play': True,
            'loop': False,
            'shuffle': False
        }
    }
    
    def __init__(self, config_path: str = None):
        """Inicializar configuración"""
        self.config_path = config_path or Path.home() / '.goat' / 'config.json'
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Cargar configuración desde archivo o usar predeterminados"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                # Combinar con predeterminados
                config = self.DEFAULT_CONFIG.copy()
                config.update(user_config)
                logger.info(f"Configuración cargada desde {self.config_path}")
                return config
            else:
                logger.info("Usando configuración predeterminada")
                return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Error al cargar configuración: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self) -> bool:
        """Guardar configuración actual en archivo"""
        try:
            # Crear directorio si no existe
            Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            logger.info(f"Configuración guardada en {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Error al guardar configuración: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtener valor de configuración por clave (soporta notación de puntos)"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """Establecer valor de configuración por clave (soporta notación de puntos)"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        return True
    
    def reset_to_defaults(self):
        """Restablecer configuración a predeterminados"""
        self.config = self.DEFAULT_CONFIG.copy()
        logger.info("Configuración restablecida a predeterminados")


# Temas de color para visualizaciones
COLOR_THEMES = {
    'vibrante': [
        (255, 0, 128),    # Rosa
        (0, 255, 255),    # Cian
        (255, 255, 0),    # Amarillo
        (128, 0, 255),    # Púrpura
        (0, 255, 128),    # Verde
        (255, 128, 0),    # Naranja
    ],
    'pastel': [
        (255, 179, 186),  # Rosa Pastel
        (186, 255, 201),  # Verde Pastel
        (186, 225, 255),  # Azul Pastel
        (255, 223, 186),  # Naranja Pastel
        (230, 190, 255),  # Púrpura Pastel
        (255, 255, 186),  # Amarillo Pastel
    ],
    'oscuro': [
        (139, 0, 0),      # Rojo Oscuro
        (0, 100, 0),      # Verde Oscuro
        (0, 0, 139),      # Azul Oscuro
        (85, 26, 139),    # Púrpura Oscuro
        (139, 69, 19),    # Marrón Oscuro
        (47, 79, 79),     # Gris Pizarra Oscuro
    ],
    'neón': [
        (57, 255, 20),    # Verde Neón
        (255, 20, 147),   # Rosa Neón
        (0, 255, 255),    # Cian Neón
        (255, 255, 0),    # Amarillo Neón
        (255, 0, 255),    # Magenta Neón
        (255, 128, 0),    # Naranja Neón
    ]
}


def get_color_theme(theme_name: str):
    """Obtener tema de color por nombre"""
    return COLOR_THEMES.get(theme_name, COLOR_THEMES['vibrante'])
