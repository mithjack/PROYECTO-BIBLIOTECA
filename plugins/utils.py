import os
import subprocess

class UtilsMixin:
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la terminal"""
        comando = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run(comando, shell=True)
    
    def pausa(self, mensaje="Presiona ENTER para continuar..."):
        """Pausa la ejecución hasta que el usuario presione ENTER"""
        input(mensaje)

    def menu_seleccionar(self, menu: dict, texto: str) -> int:
        """
        Menu seleccionador universal

        INPUT:
            menu (dict): Menu del que sacaremos los elementos a elegir (libros o usuarios)
            texto (str): Texto que personaliza los prints de la funcion
        OUTPUT:
            str/int: Si es un libro devuelve el str de su clave, si es un usuario el int de su id
        """

        breaker2 = False

        # Tal como lo tengo, siempre hay uno para elegir, asi que no deberia saltar este error
        if not menu:
            raise RuntimeError(f"No hay {texto} disponibles")

        claves = list(menu.keys())

        print(f"\nSelecciona {texto}:")
        print(f"\nEscribe 'SALIR' para cancelar")

        for i, clave in enumerate(claves, start=1):
            print(f"{i} - {menu[clave]}")

        while breaker2 == False:
            opcion = input(f"{texto}: ")

            if opcion.upper() == "SALIR":
                return False
            
            if not opcion.isdigit():
                raise ValueError("Tienes que introducir un numero de la lista")

            op = int(opcion) - 1

            if 0 <= op < len(claves):
                # print(type(claves[op]))
                return claves[op]

            print("Opción inválida, intenta de nuevo")
