# ProyectoArboles

Este proyecto es un videojuego 2D en Python donde un carrito avanza automáticamente
sobre una carretera y debe esquivar obstáculos.  
Los obstáculos se gestionan con un **árbol AVL** para garantizar eficiencia en búsquedas,
inserciones y visualización.

## Estructura
- `models/` → Lógica de datos (árbol AVL, carrito, obstáculos).
- `controllers/` → Controladores del juego (carga JSON, lógica del juego).
- `views/` → Interfaz gráfica con Pygame.
- `assets/` → Imágenes, sprites, sonidos.
- `data/` → Archivos de configuración JSON.

## Requisitos
- Python 3.10+
- Librerías: `pygame`

## Cómo ejecutar
```bash
python main.py
