class Obstaculo:
    """
    Coord. en 'unidades de mundo'.
    y es carril (0,1,2). alto está en carriles (1 por defecto).
    ancho está en unidades horizontales (pixeles mundo).
    """
    def __init__(self, x, y, tipo="generico", dano=0, ancho=20, alto=1):
        self.x = int(x)
        self.y = int(y)
        self.tipo = tipo
        self.dano = int(dano)
        self.ancho = int(ancho)
        self.alto = int(alto)

    def get_area(self):
        # área en coordenadas lógicas (x horizontal, y carril)
        return (self.x, self.y, self.x + self.ancho, self.y + self.alto)

    def __repr__(self):
        return f"Obstaculo(x={self.x}, y={self.y}, tipo={self.tipo}, dano={self.dano})"
