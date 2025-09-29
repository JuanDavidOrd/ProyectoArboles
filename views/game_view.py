import pygame
from controllers.game_controller import GameController

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
COLOR_FONDO = (180, 220, 255)

# Carriles alineados con la textura de carretera (3 posiciones)
CARRILES_Y = [
    ALTO_PANTALLA // 2 - 50,   # carril superior
    ALTO_PANTALLA // 2,        # carril medio
    ALTO_PANTALLA // 2 + 50    # carril inferior
]


class GameView:
    def __init__(self, game_controller: GameController):
        self.juego = game_controller
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Juego del Carrito con AVL")
        self.clock = pygame.time.Clock()

        # Imagen carretera
        self.road_img = pygame.image.load("assets/road.png")
        self.road_img = pygame.transform.scale(self.road_img, (ANCHO_PANTALLA, 200))

        # Carro
        self.carrito_suelo = self._cargar("assets/car.png", (55, 50), (0, 0, 255))
        self.carrito_salto = self._cargar("assets/car_jump.png", (55, 40), (255, 255, 0))

        # Obstáculos
        self.sprites_obst = {
            "piedra": self._cargar("assets/rock.png", (45, 45), (100, 100, 100)),
            "hueco": self._cargar("assets/hole.png", (55, 35), (60, 60, 60)),
            "cono": self._cargar("assets/cone.png", (40, 55), (255, 165, 0)),
            "arbusto": self._cargar("assets/bush.png", (50, 50), (34, 139, 34)),
            "default": self._cargar("assets/default.png", (50, 50), (200, 50, 50)),
        }


        self.font = pygame.font.SysFont("Arial", 18, bold=True)

    def _cargar(self, path, size, fallback_color):
        try:
            if path is None:
                raise FileNotFoundError
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size) # escalado de imagenes
        except Exception:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill(fallback_color)
            return surf


    def dibujar_carretera(self):
        # Dibuja la carretera centrada
        self.pantalla.blit(self.road_img, (0, ALTO_PANTALLA // 2 - 100))

    def dibujar_carrito(self):
        c = self.juego.carrito
        pos_y = CARRILES_Y[c.y] - (c.altura_salto if c.en_salto else 0)
        sprite = self.carrito_salto if c.en_salto else self.carrito_suelo
        self.pantalla.blit(sprite, (50, pos_y))

    def dibujar_obstaculos(self):
        for obs in self.juego.arbol.in_order():
            pos_y = CARRILES_Y[obs.y]
            # Scroll relativo al carrito
            screen_x = 50 + (obs.x - self.juego.carrito.x)
            if -60 <= screen_x <= ANCHO_PANTALLA + 60:  # culling simple
                sprite = self.sprites_obst.get(obs.tipo, self.sprites_obst["default"])
                self.pantalla.blit(sprite, (screen_x, pos_y))

    def dibujar_hud(self):
        energia = self.juego.carrito.energia
        # Barra energía
        ancho_max, alto = 200, 20
        llenado = max(0, int((energia / 100) * ancho_max))
        pygame.draw.rect(self.pantalla, (80, 80, 80), (20, 20, ancho_max, alto))
        color = (0, 200, 0) if energia > 60 else (255, 215, 0) if energia > 30 else (200, 0, 0)
        pygame.draw.rect(self.pantalla, color, (20, 20, llenado, alto))
        pygame.draw.rect(self.pantalla, (255, 255, 255), (20, 20, ancho_max, alto), 2)

        # Textos
        t1 = self.font.render(f"Energía: {int(energia)}%", True, (255, 255, 255))
        self.pantalla.blit(t1, (20, 45))
        dist = int(self.juego.carrito.x)
        total = int(self.juego.distancia_total)
        t2 = self.font.render(f"Distancia: {dist} / {total} m", True, (255, 255, 255))
        self.pantalla.blit(t2, (20, 70))

    def bucle_principal(self):
        corriendo = True
        while corriendo and self.juego.juego_activo:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    corriendo = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP: self.juego.carrito.mover_y("up")
                    elif e.key == pygame.K_DOWN: self.juego.carrito.mover_y("down")
                    elif e.key == pygame.K_SPACE: self.juego.carrito.iniciar_salto()
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_SPACE: self.juego.carrito.terminar_salto()

            self.juego.carrito.actualizar_salto()
            self.juego.avanzar()

            self.pantalla.fill(COLOR_FONDO)
            self.dibujar_carretera()
            self.dibujar_carrito()
            self.dibujar_obstaculos()
            self.dibujar_hud()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
