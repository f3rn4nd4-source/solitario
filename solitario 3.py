import os
import random
import arcade

# Título y tamaño de la pantalla
ANCHO_PANTALLA = 1024
ALTO_PANTALLA = 768
TITULO_PANTALLA = "Arrastrar y Soltar Cartas"

# Constantes para el tamaño
ESCALA_CARTA = 0.6

# ¿Qué tan grandes son las cartas?
ANCHO_CARTA = 140 * ESCALA_CARTA
ALTO_CARTA = 190 * ESCALA_CARTA

# ¿Qué tan grande es la alfombrilla donde colocaremos la carta?
PORCENTAJE_SOBRETAMAÑO_ALFOMBRA = 1.25
ALTO_ALFOMBRA = int(ALTO_CARTA * PORCENTAJE_SOBRETAMAÑO_ALFOMBRA)
ANCHO_ALFOMBRA = int(ANCHO_CARTA * PORCENTAJE_SOBRETAMAÑO_ALFOMBRA)

# ¿Cuánto espacio dejamos como margen entre las alfombrillas?
# Hecho como un porcentaje del tamaño de la alfombrilla.
MARGEN_VERTICAL_PORCENTAJE = 0.10
MARGEN_HORIZONTAL_PORCENTAJE = 0.10

# La Y de la fila inferior (2 pilas)
INFERIOR_Y = ALTO_ALFOMBRA / 2 + ALTO_ALFOMBRA * MARGEN_VERTICAL_PORCENTAJE

# La X de donde comenzar a colocar cosas en el lado izquierdo
INICIO_X = ANCHO_ALFOMBRA / 2 + ANCHO_ALFOMBRA * MARGEN_HORIZONTAL_PORCENTAJE

# La Y de la fila superior (4 pilas)
SUPERIOR_Y = ALTO_PANTALLA - ALTO_ALFOMBRA / 2 - ALTO_ALFOMBRA * MARGEN_VERTICAL_PORCENTAJE

# La Y de la fila del medio (7 pilas)
MEDIO_Y = SUPERIOR_Y - ALTO_ALFOMBRA - ALTO_ALFOMBRA * MARGEN_VERTICAL_PORCENTAJE

# Cuánto espacio hay entre cada pila
ESPACIADO_X = ANCHO_ALFOMBRA + ANCHO_ALFOMBRA * MARGEN_HORIZONTAL_PORCENTAJE

# Constantes de las cartas
VALORES_CARTA = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
PALOS_CARTA = ["trebol", "corazon", "pica", "diamante"]

class Carta(arcade.Sprite):
    """ Sprite de carta """

    def __init__(self, palo, valor, escala=1):
        """ Constructor de carta """

        image_dir = "C:\\Users\\feerg\\OneDrive\\Escritorio\\cartas solitario"
        image_file = f"card{palo}{valor}.png"
        self.nombre_archivo_imagen = os.path.join(image_dir, image_file)
        
        # Verificar si el archivo existe y agregar un mensaje de depuración
        if not os.path.exists(self.nombre_archivo_imagen):
            print(f"Archivo no encontrado: {self.nombre_archivo_imagen}")
            raise FileNotFoundError(f"No se puede localizar el recurso: {self.nombre_archivo_imagen}")
        else:
            print(f"Archivo encontrado: {self.nombre_archivo_imagen}")

        # Llamar al constructor de la clase padre
        super().__init__(self.nombre_archivo_imagen, escala, hit_box_algorithm="None")

class MiJuego(arcade.Window):
    """ Clase principal de la aplicación. """

    def __init__(self):
        super().__init__(ANCHO_PANTALLA, ALTO_PANTALLA, TITULO_PANTALLA)

        # Lista de sprites con todas las cartas, sin importar en qué pila están.
        self.lista_cartas = None

        arcade.set_background_color(arcade.color.AMAZON)

        # Lista de cartas que estamos arrastrando con el ratón
        self.cartas_sostenidas = None

        # Posición original de las cartas que estamos arrastrando con el ratón en caso
        # de que tengan que volver.
        self.posicion_original_cartas_sostenidas = None

        # Lista de sprites con todas las alfombrillas en las que se colocan las cartas.
        self.lista_alfombrillas_pilas = None

    def configurar(self):
        """ Configurar el juego aquí. Llamar a esta función para reiniciar el juego. """

        # Lista de cartas que estamos arrastrando con el ratón
        self.cartas_sostenidas = []

        # Posición original de las cartas que estamos arrastrando con el ratón en caso
        # de que tengan que volver.
        self.posicion_original_cartas_sostenidas = []

        # --- Crear las alfombrillas en las que se colocan las cartas.

        # Lista de sprites con todas las alfombrillas en las que se colocan las cartas.
        self.lista_alfombrillas_pilas = arcade.SpriteList()

        # Crear las alfombrillas para las pilas inferiores boca abajo y boca arriba
        pila = arcade.SpriteSolidColor(ANCHO_ALFOMBRA, ALTO_ALFOMBRA, arcade.csscolor.DARK_OLIVE_GREEN)
        pila.position = INICIO_X, INFERIOR_Y
        self.lista_alfombrillas_pilas.append(pila)

        pila = arcade.SpriteSolidColor(ANCHO_ALFOMBRA, ALTO_ALFOMBRA, arcade.csscolor.DARK_OLIVE_GREEN)
        pila.position = INICIO_X + ESPACIADO_X, INFERIOR_Y
        self.lista_alfombrillas_pilas.append(pila)

        # Crear las siete pilas del medio
        for i in range(7):
            pila = arcade.SpriteSolidColor(ANCHO_ALFOMBRA, ALTO_ALFOMBRA, arcade.csscolor.DARK_OLIVE_GREEN)
            pila.position = INICIO_X + i * ESPACIADO_X, MEDIO_Y
            self.lista_alfombrillas_pilas.append(pila)

        # Crear las pilas "de juego" superiores
        for i in range(4):
            pila = arcade.SpriteSolidColor(ANCHO_ALFOMBRA, ALTO_ALFOMBRA, arcade.csscolor.DARK_OLIVE_GREEN)
            pila.position = INICIO_X + i * ESPACIADO_X, SUPERIOR_Y
            self.lista_alfombrillas_pilas.append(pila)

        # --- Crear, barajar y repartir las cartas

        # Crear cada carta
        todas_cartas = []
        for palo_carta in PALOS_CARTA:
            for valor_carta in VALORES_CARTA:
                carta = Carta(palo_carta, valor_carta, ESCALA_CARTA)
                todas_cartas.append(carta)

        # Barajar las cartas
        random.shuffle(todas_cartas)

        # Asignar las cartas barajadas a self.lista_cartas
        self.lista_cartas = arcade.SpriteList()
        self.lista_cartas.extend(todas_cartas)

        # Repartir las cartas en las pilas del tablero
        pilas_tablero = [[] for _ in range(7)]
        indice_carta = 0
        for indice_pila in range(7):
            for cantidad_cartas in range(indice_pila + 1):
                carta = self.lista_cartas[indice_carta]
                carta.position = INICIO_X + indice_pila * ESPACIADO_X, MEDIO_Y - cantidad_cartas * (ALTO_CARTA * 0.3)
                pilas_tablero[indice_pila].append(carta)
                indice_carta += 1

    def on_draw(self):
        """ Renderizar la pantalla. """
        # Limpiar la pantalla
        self.clear()

        # Dibujar las alfombrillas en las que se colocan las cartas
        self.lista_alfombrillas_pilas.draw()

        # Dibujar las cartas
        self.lista_cartas.draw()

    def llevar_a_la_cima(self, carta: arcade.Sprite):
        """ Llevar la carta a la parte superior del orden de renderizado (última en renderizarse, parece estar encima) """

        # Eliminar y añadir al final
        self.lista_cartas.remove(carta)
        self.lista_cartas.append(carta)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Llamado cuando el usuario presiona un botón del ratón. """

        # Obtener la lista de cartas en las que hemos clicado
        cartas = arcade.get_sprites_at_point((x, y), self.lista_cartas)

        # ¿Hemos clicado en una carta?
        if len(cartas) > 0:

            # Podría ser una pila de cartas, obtener la superior
            carta_primaria = cartas[-1]

            # En todos los demás casos, tomar la carta boca arriba en la que estamos clicando
            self.cartas_sostenidas = [carta_primaria]
            # Guardar la posición
            self.posicion_original_cartas_sostenidas = [self.cartas_sostenidas[0].position]
            # Poner en la parte superior del orden de dibujo
            self.llevar_a_la_cima(self.cartas_sostenidas[0])

    def on_mouse_release(self, x: float, y: float, button: int):
        """ Llamado cuando el usuario suelta un botón del ratón. """

        # Si no tenemos cartas, no importa
        if len(self.cartas_sostenidas) == 0:
            return

        # Encontrar la pila más cercana, en caso de que estemos en contacto con más de una
        pila, distancia = arcade.get_closest_sprite(self.cartas_sostenidas[0], self.lista_alfombrillas_pilas)
        resetear_posicion = True

        # Ver si estamos en contacto con la pila más cercana
        if arcade.check_for_collision(self.cartas_sostenidas[0], pila):

            # Para cada carta sostenida, moverla a la pila en la que la dejamos caer
            for i, carta_suelta in enumerate(self.cartas_sostenidas):
                # Mover las cartas a la posición correcta
                carta_suelta.position = pila.center_x, pila.center_y

            # Éxito, no resetear la posición de las cartas
            resetear_posicion = False

        if resetear_posicion:
            # Donde sea que las hayamos dejado caer, no fue válido. Resetear la posición
            # de cada carta a su lugar original.
            for indice_pila, carta in enumerate(self.cartas_sostenidas):
                carta.position = self.posicion_original_cartas_sostenidas[indice_pila]

        # Ya no estamos sosteniendo cartas
        self.cartas_sostenidas = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ Usuario mueve el ratón """

        # Si estamos sosteniendo cartas, moverlas con el ratón
        for carta in self.cartas_sostenidas:
            carta.center_x += dx
            carta.center_y += dy

def main():
    """ Función principal """
    ventana = MiJuego()
    ventana.configurar()
    arcade.run()

if __name__ == "__main__":
    main()
