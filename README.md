# GOAT - Reproductor Multimedia Inteligente

**Tecnología Audiovisual Orgánica Generativa**

Reproductor multimedia inteligente desarrollado bajo el proyecto GOAT. Diseñado para ofrecer una experiencia fluida, visual y sonora de alto rendimiento. Integración modular con IA, audio reactivo y soporte multiplataforma.

## ✨ Características

- 🎵 **Soporte Multi-formato**: Audio (MP3, WAV, OGG, FLAC, M4A) y Video (MP4, AVI, MOV, MKV)
- 🎨 **Visuales Reactivos**: Análisis de audio en tiempo real impulsa visualizaciones dinámicas
- 🤖 **Integración IA**: Detección de estado de ánimo, análisis de género y paletas de colores adaptativas
- 🌈 **Múltiples Modos de Visualización**: Analizador de espectro, forma de onda, sistemas de partículas
- 💻 **Multiplataforma**: Soporte para Windows, macOS, Linux
- ⚡ **Alto Rendimiento**: Renderizado a 60 FPS con análisis de audio optimizado
- 🎯 **Arquitectura Modular**: Fácilmente extensible para características personalizadas

## 🚀 Inicio Rápido

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Blackmvmba88/GOAT.git
cd GOAT

# Instalar dependencias
pip install -r requirements.txt
```

### Uso

```bash
# Iniciar el reproductor
python main.py

# Reproducir un archivo específico
python main.py /ruta/a/tu/musica.mp3

# Tamaño de ventana personalizado
python main.py --width 1920 --height 1080 video.mp4

# Modo pantalla completa
python main.py --fullscreen musica.mp3
```

## 🎮 Controles

- **ESPACIO**: Reproducir/Pausar
- **S**: Detener
- **V**: Cambiar modos de visualización
- **Q**: Salir

## 📖 Documentación

- **[QUICKSTART.md](QUICKSTART.md)** - Comienza en 5 minutos
- **[USAGE.md](USAGE.md)** - Guía de uso detallada y características
- **[INSTALL.md](INSTALL.md)** - Instrucciones de instalación específicas por plataforma
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Diseño del sistema y arquitectura

## 🏗️ Arquitectura

```
GOAT/
├── main.py              # Punto de entrada
├── goat_player.py       # Reproductor principal con visualización
├── ai_module.py         # Integración y análisis IA
├── config.py            # Gestión de configuración
├── requirements.txt     # Dependencias Python
└── USAGE.md            # Documentación detallada
```

## 🎨 Modos de Visualización

1. **Analizador de Espectro**: Barras basadas en frecuencia que responden al audio
2. **Forma de Onda**: Visualización clásica de amplitud
3. **Partículas**: Sistema generativo de partículas impulsado por energía de audio

## 🤖 Características de IA

- **Detección de Estado de Ánimo**: Analiza tempo y características (energético, calmado, animado, ambiental)
- **Paletas Adaptativas**: Los colores cambian según el estado de ánimo detectado
- **Momentos Clave**: Identifica caídas, crescendos y transiciones
- **Clasificación de Género**: Estima el género musical a partir del análisis de audio

## 🛠️ Stack Tecnológico

- **pygame**: Gráficos y reproducción de audio
- **librosa**: Análisis de audio y extracción de características
- **opencv-python**: Procesamiento de video
- **numpy**: Cálculos numéricos
- **matplotlib/scipy**: Visualizaciones avanzadas

## 💡 Ejemplos

### Audio con Visualizaciones
```bash
python main.py tu_cancion.mp3
# Presiona V para alternar entre espectro, forma de onda y partículas
```

### Reproducción de Video
```bash
python main.py tu_video.mp4
# Disfruta de reproducción de video fluida con superposiciones reactivas al audio opcionales
```

## 🌟 Mejoras Futuras

- Efectos de audio en tiempo real y filtros
- Gestión de listas de reproducción y recomendaciones inteligentes
- Integración con servicios de streaming
- Soporte de visualización VR/AR
- Visuales generados por aprendizaje automático
- Soporte de controlador MIDI
- Sistema de plugins para visualizadores personalizados

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Áreas de interés:
- Nuevos algoritmos de visualización
- Modelos de IA mejorados
- Optimizaciones de rendimiento
- Mejoras de UI/UX
- Documentación

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT.

## 🙏 Agradecimientos

GOAT fusiona tecnología, arte y sonido para crear una interfaz viva que responde a tus medios. Experimenta multimedia como debe ser: inteligente, adaptativa y hermosa.

---

**Hecho con ❤️ para el proyecto GOAT**
