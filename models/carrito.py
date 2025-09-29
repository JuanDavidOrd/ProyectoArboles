import time

class Carrito:
    def __init__(self, x=0, y=1, energia=100, velocidad=5, salto_duracion=1.2, salto_altura_max=100, ancho=40, alto=1):
        self.x = float(x)   # pos horizontal en mundo
        self.y = int(y)     # carril (0,1,2)
        self.energia = int(energia)
        self.velocidad = float(velocidad)   # 5m cada 200ms
        self.ancho = int(ancho)  # ancho lógico en X (mundo)
        self.alto = int(alto)    # alto en carriles

        # salto
        self.en_salto = False
        self.altura_salto = 0.0
        self.salto_duracion = float(salto_duracion)   # tiempo total en segundos
        self.salto_altura_max = float(salto_altura_max)  # altura máxima
        self._t_inicio_salto = None

    def mover_y(self, dir):
        if dir == "up" and self.y > 0: 
            self.y -= 1
        elif dir == "down" and self.y < 2: 
            self.y += 1

    def iniciar_salto(self):
        if not self.en_salto:
            self.en_salto = True
            self._t_inicio_salto = time.time()

    def terminar_salto(self):
        self.en_salto = False
        self.altura_salto = 0.0

    def actualizar_salto(self):
        if not self.en_salto:
            return
        t = time.time() - self._t_inicio_salto
        fase = t / self.salto_duracion
        if fase >= 1.0:
            self.terminar_salto()
        else:
            # función tipo campana → sube y baja
            self.altura_salto = self.salto_altura_max * (1 - 4 * (fase - 0.5) ** 2)

    def recibir_dano(self, cantidad):
        self.energia = max(0, self.energia - int(cantidad))

    def esta_vivo(self):
        return self.energia > 0

    # área lógica para colisiones (x horizontal, y en carriles)
    def get_area(self):
        return (self.x, self.y, self.x + self.ancho, self.y + self.alto)
