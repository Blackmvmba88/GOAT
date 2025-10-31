# Guía de Inicio Rápido GOAT

¡Empieza a usar GOAT en menos de 5 minutos!

## Requisitos Previos

- Python 3.8+ instalado
- Dispositivo de salida de audio
- (Opcional) Archivos multimedia para reproducir

## Instalación (Un Comando)

```bash
git clone https://github.com/Blackmvmba88/GOAT.git && cd GOAT && pip install -r requirements.txt
```

## Tu Primera Ejecución

### Opción 1: Modo Demo (No Requiere Medios)

```bash
python demo.py
```

Presiona **ESPACIO** para iniciar la demo, **V** para cambiar visualizaciones, **Q** para salir.

### Opción 2: Reproduce Tu Música

```bash
python main.py /ruta/a/tu/cancion.mp3
```

### Opción 3: Reproduce Video

```bash
python main.py /ruta/a/tu/video.mp4
```

## Controles Esenciales

| Tecla | Acción |
|-------|--------|
| ESPACIO | Reproducir/Pausar |
| S | Detener |
| V | Cambiar Visualización |
| Q | Salir |

## Casos de Uso Comunes

### Visualización de Música en Pantalla Completa

```bash
python main.py --fullscreen --width 1920 --height 1080 musica.mp3
```

### Prueba Diferentes Formatos de Medios

```bash
# Audio
python main.py cancion.mp3    # MP3
python main.py pista.wav      # WAV
python main.py audio.flac     # FLAC

# Video
python main.py video.mp4   # MP4
python main.py clip.mov    # MOV
python main.py pelicula.mkv   # MKV
```

## Solución de Problemas

### Error "Module not found"
```bash
pip install -r requirements.txt
```

### Falla la instalación de PyAudio
**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

### No se reproduce audio
- Verifica el volumen del sistema
- Verifica que el formato del archivo sea compatible
- Prueba con un archivo de audio diferente

## ¿Qué Sigue?

- Lee [USAGE.md](USAGE.md) para características detalladas
- Revisa [ARCHITECTURE.md](ARCHITECTURE.md) para entender el diseño
- Consulta [INSTALL.md](INSTALL.md) para configuración específica por plataforma

## Consejos y Trucos

1. **Mejor Visualización**: Prueba el modo espectro con música electrónica
2. **Rendimiento**: Comienza con 1280x720, aumenta si es fluido
3. **Exploración**: Presiona V varias veces para ver todos los modos
4. **Configuración Personalizada**: Edita `~/.goat/config.json` después de la primera ejecución

## ¿Necesitas Ayuda?

- Revisa los problemas existentes en GitHub
- Consulta la documentación [USAGE.md](USAGE.md)
- Abre un nuevo issue con:
  - Tu sistema operativo y versión de Python
  - Mensaje de error completo
  - Pasos para reproducir

---

**¡Disfruta tu experiencia multimedia inteligente!** 🎵🎨🤖
