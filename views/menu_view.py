import pygame
import sys
import json
from views.avl_visualizer import AVLVisualizerPG

# --- Colores y configuración ---
COLOR_FONDO = (25, 25, 25)
COLOR_TEXTO = (255, 255, 255)
COLOR_BOTON = (70, 130, 180)
COLOR_BOTON_HOVER = (100, 160, 210)
COLOR_INPUT = (255, 255, 255)
COLOR_INPUT_TEXTO = (0, 0, 0)

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600


class MenuView:
    def __init__(self, arbol):
        pygame.init()
        self.arbol = arbol
        self.reiniciar_ui()
        self.clock = pygame.time.Clock()

    def reiniciar_ui(self):
        """Reinicia la ventana y fuentes de pygame (tras cerrar el visualizador)."""
        pygame.display.init()
        pygame.font.init()

        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Menú Principal - Juego del Carrito con AVL")
        self.font_titulo = pygame.font.SysFont("Arial", 56, bold=True)
        self.font_boton = pygame.font.SysFont("Arial", 32, bold=True)
        self.font_input = pygame.font.SysFont("Arial", 28)

    def dibujar_texto(self, texto, fuente, x, y, color=COLOR_TEXTO):
        superficie = fuente.render(texto, True, color)
        rect = superficie.get_rect(center=(x, y))
        self.pantalla.blit(superficie, rect)
        return rect

    def mostrar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "salir"
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_jugar.collidepoint(evento.pos):
                        return "jugar"
                    elif boton_obstaculo.collidepoint(evento.pos):
                        self.agregar_obstaculo()
                        from controllers.json_loader import JSONLoader
                        self.arbol = JSONLoader("data/config.json").cargar()["arbol"]
                    elif boton_avl.collidepoint(evento.pos):
                        # Boton Visualizar AVL
                        AVLVisualizerPG(self.arbol).mostrar()
                        self.reiniciar_ui()
                    elif boton_salir.collidepoint(evento.pos):
                        return "salir"

            # Fondo
            self.pantalla.fill(COLOR_FONDO)

            # Título
            self.dibujar_texto("🚗 Juego del Carrito con AVL 🚗",
                               self.font_titulo, ANCHO_PANTALLA // 2, 120)

            mouse_pos = pygame.mouse.get_pos()

            # Botones
            boton_jugar = pygame.Rect(300, 220, 200, 60)
            pygame.draw.rect(self.pantalla,
                                COLOR_BOTON_HOVER if boton_jugar.collidepoint(mouse_pos) else COLOR_BOTON,
                                boton_jugar, border_radius=12)
            self.dibujar_texto("Jugar", self.font_boton, *boton_jugar.center)

            boton_obstaculo = pygame.Rect(300, 300, 200, 60)
            pygame.draw.rect(self.pantalla,
                                COLOR_BOTON_HOVER if boton_obstaculo.collidepoint(mouse_pos) else COLOR_BOTON,
                                boton_obstaculo, border_radius=12)
            self.dibujar_texto("Agregar Obstáculo", self.font_boton, *boton_obstaculo.center)

            boton_avl = pygame.Rect(300, 380, 200, 60)
            pygame.draw.rect(self.pantalla,
                                COLOR_BOTON_HOVER if boton_avl.collidepoint(mouse_pos) else COLOR_BOTON,
                                boton_avl, border_radius=12)
            self.dibujar_texto("Visualizar Árbol", self.font_boton, *boton_avl.center)

            boton_salir = pygame.Rect(300, 460, 200, 60)
            pygame.draw.rect(self.pantalla,
                                COLOR_BOTON_HOVER if boton_salir.collidepoint(mouse_pos) else COLOR_BOTON,
                                boton_salir, border_radius=12)
            self.dibujar_texto("Salir", self.font_boton, *boton_salir.center)

            pygame.display.flip()
            self.clock.tick(30)

    # -------------------------
    # Formulario obstáculo
    # -------------------------
    def agregar_obstaculo(self):
        campos = {"x": "", "y": "", "tipo": "", "dano": ""}
        activo = None
        corriendo = True

        while corriendo:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    for i, key in enumerate(campos.keys()):
                        rect = pygame.Rect(250, 200 + i * 60, 300, 40)
                        if rect.collidepoint(e.pos):
                            activo = key
                    btn_g = pygame.Rect(300, 480, 200, 60)
                    btn_c = pygame.Rect(300, 550, 200, 40)
                    if btn_g.collidepoint(e.pos):
                        if self.guardar_obstaculo(campos):
                            corriendo = False
                    if btn_c.collidepoint(e.pos):
                        corriendo = False
                elif e.type == pygame.KEYDOWN and activo:
                    if e.key == pygame.K_RETURN:
                        activo = None
                    elif e.key == pygame.K_BACKSPACE:
                        campos[activo] = campos[activo][:-1]
                    else:
                        campos[activo] += e.unicode

            # UI
            self.pantalla.fill(COLOR_FONDO)
            self.dibujar_texto("Agregar Obstáculo", self.font_titulo, ANCHO_PANTALLA // 2, 100)

            for i, (k, v) in enumerate(campos.items()):
                rect = pygame.Rect(250, 200 + i * 60, 300, 40)
                pygame.draw.rect(self.pantalla, COLOR_INPUT, rect, border_radius=6)
                txt = self.font_input.render(f"{k}: {v}", True, COLOR_INPUT_TEXTO)
                self.pantalla.blit(txt, (rect.x + 10, rect.y + 8))

            btn_g = pygame.Rect(300, 480, 200, 60)
            pygame.draw.rect(self.pantalla, (0, 180, 0), btn_g, border_radius=12)
            self.dibujar_texto("Guardar", self.font_boton, *btn_g.center)

            btn_c = pygame.Rect(300, 550, 200, 40)
            pygame.draw.rect(self.pantalla, (180, 0, 0), btn_c, border_radius=12)
            self.dibujar_texto("Cancelar", self.font_boton, *btn_c.center)

            pygame.display.flip()
            self.clock.tick(30)

    def guardar_obstaculo(self, campos):
        try:
            x = int(campos["x"])
            y = int(campos["y"])
            tipo = (campos["tipo"] or "generico").strip().lower()
            dano = int(campos["dano"])

            # Validaciones para colocar obstaculos
            if y not in [0, 1, 2]:
                print(f"[ERROR] Carril inválido ({y}). Solo se permiten 0, 1 o 2.")
                return False
            if x < 0:
                print(f"[ERROR] La posición X no puede ser negativa ({x}).")
                return False
            if dano <= 0:
                print(f"[ERROR] El daño debe ser mayor que 0 (valor dado: {dano}).")
                return False

            nuevo = {"x": x, "y": y, "tipo": tipo, "dano": dano, "ancho": 20, "alto": 1}

            with open("data/config.json", "r+", encoding="utf-8") as f:
                data = json.load(f)
                for o in data.get("obstaculos", []):
                    if int(o["x"]) == x and int(o["y"]) == y:
                        print(f"[ERROR] Ya existe un obstáculo en ({x},{y})")
                        return False
                data.setdefault("obstaculos", []).append(nuevo)
                f.seek(0); json.dump(data, f, indent=4); f.truncate()
            print("[INFO] Obstáculo agregado ✅")
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo guardar: {e}")
            return False

