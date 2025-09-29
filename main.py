from controllers.json_loader import JSONLoader
from controllers.game_controller import GameController
from views.menu_view import MenuView
from views.game_view import GameView
from views.end_view import EndView
from models.carrito import Carrito


def main():
    while True:
        # Cargar configuración inicial y árbol desde JSON
        loader = JSONLoader("data/config.json")
        datos = loader.cargar()
        config = datos["config"]
        arbol = datos["arbol"]

        # Menú principal
        menu = MenuView(arbol)
        opcion = menu.mostrar()

        if opcion == "salir" or opcion is None:
            print("[INFO] Saliendo del juego...")
            break

        if opcion == "jugar":
            # Recargar datos (en caso de que se hayan agregado obstáculos en el menú)
            datos = loader.cargar()
            config = datos["config"]
            arbol = datos["arbol"]

            # Crear carrito y lógica del juego
            carrito = Carrito(
                x=0, y=1, energia=100,
                velocidad=config.get("velocidad", 5),
                # Ahora el salto usa duración y altura máxima
                salto_duracion=config.get("salto_duracion", 3.5),
                salto_altura_max=config.get("salto_altura_max", 40)
            )
            juego = GameController(carrito, arbol, config.get("distancia_total", 1000))

            # Iniciar vista del juego
            vista = GameView(juego)
            vista.bucle_principal()

            # Pantalla final
            mensaje = "¡Ganaste! Llegaste a la meta." if carrito.esta_vivo() else "Game Over: Energía agotada."
            end_view = EndView(mensaje)
            opcion_end = end_view.mostrar()

            if opcion_end == "reiniciar":
                continue  # vuelve al inicio del while → recarga el menú y el juego
            elif opcion_end == "menu":
                continue  # regresa al menú principal
            else:  # salir
                break


if __name__ == "__main__":
    main()
