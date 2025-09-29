import time

class GameController:
    """
    Controlador principal del juego.
    - Movimiento basado en tiempo real: ~5 m cada 200 ms (ajustable con multiplicador).
    - Colisiones rectangulares por carril.
    - En salto, el carrito ignora colisiones y avanza un poco más rápido.
    """
    def __init__(self, carrito, arbol, distancia_total=1000):
        self.carrito = carrito
        self.arbol = arbol
        self.distancia_total = distancia_total
        self.juego_activo = True
        self._t_prev = time.time()

        # para evitar daño repetido por el mismo obstáculo
        self._ult_colision = None
        self._colision_cooldown = 2.0   # segundos de invulnerabilidad tras un choque
        self._t_ultima_colision = 0

    def avanzar(self):
        ahora = time.time()
        dt = ahora - self._t_prev
        self._t_prev = ahora

        # Movimiento base
        metros_por_seg = (self.carrito.velocidad / 0.2) * 1  

        # Boost horizontal cuando está en el aire
        if self.carrito.en_salto:
            metros_por_seg *= 1.3  

        self.carrito.x += metros_por_seg * dt

        # Colisiones (solo si no está saltando)
        if not self.carrito.en_salto:
            for obs in self.arbol.in_order():
                if self._colisiona(self.carrito, obs):
                    if (ahora - self._t_ultima_colision) > self._colision_cooldown:
                        self.carrito.recibir_dano(obs.dano)
                        self._t_ultima_colision = ahora
                        self._ult_colision = obs

        # Fin del juego
        if self.carrito.x >= self.distancia_total or self.carrito.energia <= 0:
            self.juego_activo = False

    def _colisiona(self, carrito, obs):
        # Rectángulos para la colisión
        cx1, cy1, cx2, cy2 = carrito.get_area()
        ox1, oy1, ox2, oy2 = obs.get_area()

        # superposición en X e Y
        overlap_x = (cx1 < ox2) and (cx2 > ox1)
        overlap_y = (cy1 < oy2) and (cy2 > oy1)

        return overlap_x and overlap_y
