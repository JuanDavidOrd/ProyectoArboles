import json
from models.obstaculo import Obstaculo
from models.avl import AVLTree


class JSONLoader:
    def __init__(self, ruta_json: str):
        self.ruta_json = ruta_json

    def cargar(self):
        with open(self.ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        config = data.get("config", {})
        obsts = data.get("obstaculos", [])

        arbol = AVLTree()
        for o in obsts:
            obs = Obstaculo(
                x=int(o["x"]),
                y=int(o["y"]),
                tipo=o.get("tipo", "generico"),
                dano=int(o.get("dano", 0)),
                ancho=int(o.get("ancho", 20)),
                alto=int(o.get("alto", 1))
            )
            try:
                arbol.insertar(obs)
            except ValueError:
                # Ignora duplicados exactos (x,y)
                pass

        return {"config": config, "arbol": arbol}
