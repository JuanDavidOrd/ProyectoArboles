import pygame

ANCHO = 1000
ALTO = 700
FONDO = (24, 24, 24)
COLOR_ARISTA = (180, 180, 180)
COLOR_NODO = (70, 130, 180)
COLOR_TEXTO = (245, 245, 245)
BORDE_NODO = (255, 255, 255)
RADIO = 18
Y_GAP = 90
TOP = 70
LEFT = 40
RIGHT = 40

class AVLVisualizerPG:
    def __init__(self, arbol):
        self.arbol = arbol
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Visualizador AVL")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.small = pygame.font.SysFont("Arial", 14)
        self.pos = {}
        self.edges = []
        self._layout()

    def _contar(self, n):
        if not n: return 0
        return 1 + self._contar(n.izq) + self._contar(n.der)

    def _layout(self):
        raiz = self.arbol.raiz
        total = max(1, self._contar(raiz))
        ancho_util = ANCHO - LEFT - RIGHT
        slot = max(70, ancho_util // (total + 1))
        self._idx = 0
        self._inorder_pos(raiz, 0, slot)

    def _inorder_pos(self, n, depth, slot):
        if not n: return
        self._inorder_pos(n.izq, depth + 1, slot)
        self._idx += 1
        x = LEFT + self._idx * slot
        y = TOP + depth * Y_GAP
        self.pos[n] = (x, y)
        if n.izq: self.edges.append((n, n.izq))
        if n.der: self.edges.append((n, n.der))
        self._inorder_pos(n.der, depth + 1, slot)

    def mostrar(self):
        corriendo = True
        while corriendo:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: corriendo = False
                elif e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_ESCAPE, pygame.K_q): corriendo = False
                    elif e.key == pygame.K_s: pygame.image.save(self.pantalla, "tree.png")

            self.pantalla.fill(FONDO)
            # aristas
            for p, c in self.edges:
                x1, y1 = self.pos[p]; x2, y2 = self.pos[c]
                pygame.draw.line(self.pantalla, COLOR_ARISTA, (x1, y1), (x2, y2), 2)
            # nodos
            for n, (x, y) in self.pos.items():
                pygame.draw.circle(self.pantalla, COLOR_NODO, (x, y), RADIO)
                pygame.draw.circle(self.pantalla, BORDE_NODO, (x, y), RADIO, 2)
                o = n.obstaculo
                t1 = self.font.render(f"({o.x},{o.y})", True, COLOR_TEXTO)
                t2 = self.small.render(f"{o.tipo}", True, COLOR_TEXTO)
                self.pantalla.blit(t1, t1.get_rect(center=(x, y - 2)))
                self.pantalla.blit(t2, t2.get_rect(center=(x, y + 14)))

            hint = self.small.render("ESC/Q: cerrar  |  S: guardar captura", True, (200, 200, 200))
            self.pantalla.blit(hint, (20, ALTO - 30))
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
