#!/usr/bin/env python3
"""
GOAT - Reproductor Multimedia Inteligente
Punto de entrada principal con soporte multiplataforma
"""

import sys
import argparse
from pathlib import Path
import pygame
import logging

from goat_player import GOATPlayer

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Punto de entrada principal para el reproductor GOAT"""
    parser = argparse.ArgumentParser(
        description='GOAT - Reproductor Multimedia Inteligente con IA y Visuales Reactivos'
    )
    parser.add_argument(
        'media',
        nargs='?',
        help='Ruta al archivo multimedia (audio o video)'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=1280,
        help='Ancho de ventana (predeterminado: 1280)'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=720,
        help='Alto de ventana (predeterminado: 720)'
    )
    parser.add_argument(
        '--fullscreen',
        action='store_true',
        help='Iniciar en modo pantalla completa'
    )
    
    args = parser.parse_args()
    
    try:
        # Inicializar reproductor
        logger.info("Iniciando Reproductor Multimedia Inteligente GOAT...")
        player = GOATPlayer(width=args.width, height=args.height)
        
        # Cargar medios si se proporcionan
        if args.media:
            if not player.load_media(args.media):
                logger.error("Error al cargar archivo multimedia")
                return 1
            player.play()
        
        # Bucle principal
        running = True
        while running:
            # Manejar eventos
            for event in pygame.event.get():
                if not player.handle_event(event):
                    running = False
                    break
            
            # Renderizar fotograma
            player.render()
        
        # Limpieza
        player.cleanup()
        logger.info("Reproductor GOAT cerrado correctamente")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Interrumpido por el usuario")
        return 0
    except Exception as e:
        logger.error(f"Error fatal: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
