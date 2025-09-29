import pygame
import sys

ANCHO = 800
ALTO = 600
COLOR_FONDO = (25, 25, 25)
COLOR_TEXTO = (255, 255, 255)
COLOR_BOTON = (70, 130, 180)
COLOR_BOTON_HOVER = (100, 160, 210)

class EndView:
    def __init__(self, mensaje):
        pygame.init()
        self.mensaje = mensaje
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Fin del Juego")
        self.clock = pygame.time.Clock()
        self.font_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_boton = pygame.font.SysFont("Arial", 32, bold=True)

    def dibujar_texto(self, texto, fuente, x, y, color=COLOR_TEXTO):
        superficie = fuente.render(texto, True, color)
        rect = superficie.get_rect(center=(x, y))
        self.pantalla.blit(superficie, rect)
        return rect

    def mostrar(self):
        corriendo = True
        opcion = None

        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_reiniciar.collidepoint(evento.pos):
                        opcion = "reiniciar"
                        corriendo = False
                    elif boton_menu.collidepoint(evento.pos):
                        opcion = "menu"
                        corriendo = False
                    elif boton_salir.collidepoint(evento.pos):
                        opcion = "salir"
                        corriendo = False

            # Fondo
            self.pantalla.fill(COLOR_FONDO)

            # Mensaje final
            self.dibujar_texto(self.mensaje, self.font_titulo, ANCHO // 2, 200)

            mouse_pos = pygame.mouse.get_pos()

            # Botón Reiniciar
            boton_reiniciar = pygame.Rect(300, 300, 200, 60)
            color_r = COLOR_BOTON_HOVER if boton_reiniciar.collidepoint(mouse_pos) else COLOR_BOTON
            pygame.draw.rect(self.pantalla, color_r, boton_reiniciar, border_radius=12)
            self.dibujar_texto("Reiniciar", self.font_boton, boton_reiniciar.centerx, boton_reiniciar.centery)

            # Botón Menú principal
            boton_menu = pygame.Rect(300, 380, 200, 60)
            color_m = COLOR_BOTON_HOVER if boton_menu.collidepoint(mouse_pos) else COLOR_BOTON
            pygame.draw.rect(self.pantalla, color_m, boton_menu, border_radius=12)
            self.dibujar_texto("Menú", self.font_boton, boton_menu.centerx, boton_menu.centery)

            # Botón Salir
            boton_salir = pygame.Rect(300, 460, 200, 60)
            color_s = COLOR_BOTON_HOVER if boton_salir.collidepoint(mouse_pos) else COLOR_BOTON
            pygame.draw.rect(self.pantalla, color_s, boton_salir, border_radius=12)
            self.dibujar_texto("Salir", self.font_boton, boton_salir.centerx, boton_salir.centery)

            pygame.display.flip()
            self.clock.tick(30)

        return opcion
