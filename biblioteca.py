from doctest import FAIL_FAST

from usuario import Usuario
from libro import Libro
from prestamo import Prestamo
from datetime import date
import importlib
import os
import time
import csv
import json

# Importar servicios
from servicios.prestamo_service import PrestamoService
from servicios.estadistica_service import EstadisticaService

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
os.makedirs(DB_DIR, exist_ok=True)
PL_DIR = os.path.join(BASE_DIR, "plugins")
os.makedirs(PL_DIR, exist_ok=True)


class Biblioteca:
    """
    Clase principal que gestiona la biblioteca.
    Implementa el patrón Singleton para garantizar una única instancia.
    
    Gestiona:
        - Libros: registro, búsqueda, listado
        - Usuarios: registro, listado
        - Préstamos: crear, devolver, consultar
        - Exportación/Importación: JSON y CSV
        - Plugins: carga dinámica de funcionalidades
    """
    _instancia = None

    def __new__(cls):
        """
        Controla la creación de instancias para implementar el patrón Singleton.
        
        OUTPUT:
            Biblioteca: La única instancia de la clase
        """
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        """
        Inicializa la biblioteca con estructuras de datos vacías y servicios.
        Solo se ejecuta una vez por el patrón Singleton.
        """
        # Evitar reinicialización en Singleton
        if not hasattr(self, '_initialized'):
            self._libros = {}
            self._usuarios = {}
            self._prestamos = []
            
            # Servicios
            self._prestamo_service = PrestamoService()
            self._estadistica_service = EstadisticaService()
            
            self._initialized = True

    def __iter__(self):
        """
        Permite iterar sobre los ISBN de los libros de la biblioteca.
        
        OUTPUT:
            iterator: Iterador sobre las claves del diccionario de libros
        """
        return iter(self._libros)

    def __getitem__(self, index):
        """
        Permite acceder a un libro mediante su ISBN con sintaxis de corchetes.
        
        INPUT:
            index (str): ISBN del libro
        OUTPUT:
            Libro: El libro correspondiente al ISBN
        """
        return self._libros[index]

    def __add__(self, libro: Libro):
        """
        Permite añadir un libro usando el operador +.
        
        INPUT:
            libro (Libro): Objeto libro a añadir
        OUTPUT:
            Biblioteca: La propia instancia para permitir encadenamiento
        """
        if not isinstance(libro, Libro):
            return NotImplemented
        if libro.isbn in self._libros:
            print(f"Ya existe el libro {libro}.")
        else:
            self._libros[libro.isbn] = libro
        return self
    
    def __len__(self) -> int:
        """
        Da el número total de libros en la biblioteca.
        
        OUTPUT:
            int: Cantidad de libros registrados
        """
        return len(self._libros)
    
    @property
    def libros(self) -> dict:
        """
        Saca el diccionario de libros.
        
        OUTPUT:
            dict: Diccionario con ISBN como clave y objeto Libro como valor
        """
        return self._libros
    
    @property
    def usuarios(self) -> dict:
        """
        Saca el diccionario de usuarios.
        
        OUTPUT:
            dict: Diccionario con ID como clave y objeto Usuario como valor
        """
        return self._usuarios
    
    @property
    def prestamos(self) -> list:
        """
        Saca el listado de préstamos.
        
        OUTPUT:
            list: Lista de objetos Prestamo
        """
        return self._prestamos
    
    # ============ FUNCIONES LIBRO ============
    
    def registrar_libro(self, libro: Libro) -> bool:
        """
        Registra un nuevo libro en la biblioteca.
        
        INPUT:
            libro (Libro): Objeto libro a registrar
        OUTPUT:
            bool: True si se registró correctamente, False en caso de error
        """
        try:
            self._libros[libro.isbn] = libro
            return True
        except Exception as e:
            print(f"❌ Error al registrar libro: {e}")
            return False
            
    def ver_libros(self, libros_por_pagina: int = 10, filtro: str = None, solo_disponibles: bool = False):
        """
        Muestra los libros con paginación y filtros.
        Utiliza los plugins limpiar_pantalla() y pausa().
        
        INPUT:
            libros_por_pagina (int): Número de libros por página (default: 10)
            filtro (str): Texto para filtrar por título o autor (default: None)
            solo_disponibles (bool): Si True, muestra solo libros no prestados (default: False)
        """
        # Obtener libros según el criterio
        if solo_disponibles:
            prestados = [p.libro.isbn for p in self._prestamos if p.esta_activo()]
            libros_lista = [libro for libro in self._libros.values() if libro.isbn not in prestados]
            titulo_lista = "LIBROS DISPONIBLES"
            mensaje_vacio = "No hay libros disponibles en este momento."
        else:
            libros_lista = list(self._libros.values())
            titulo_lista = "LISTA DE LIBROS"
            mensaje_vacio = "No hay libros registrados en la biblioteca."
        
        # Aplicar filtro
        if filtro:
            libros_lista = [l for l in libros_lista if filtro.lower() in str(l).lower()]
            if not libros_lista:
                print(f"❌ No se encontraron libros con '{filtro}'")
                input("\nPresiona ENTER para continuar...")
                return
        
        total = len(libros_lista)
        if total == 0:
            print(f"📚 {mensaje_vacio}")
            return
        
        pagina = 0
        total_paginas = (total + libros_por_pagina - 1) // libros_por_pagina
        
        while True:
            self.limpiar_pantalla()
            
            inicio = pagina * libros_por_pagina
            fin = min(inicio + libros_por_pagina, total)
            
            print(f"{'='*70}")
            print(f"📖 {titulo_lista} (Página {pagina + 1}/{total_paginas})")
            print(f"Total: {total} libro(s)")
            if filtro:
                print(f"🔍 Filtro: '{filtro}'")
            print(f"{'='*70}\n")
            
            for i in range(inicio, fin):
                print(f"{i+1}. {libros_lista[i]}")
            
            print(f"\n{'='*70}")
            print("[ENTER] siguiente | [A] anterior | [B] buscar | [Q] salir")
            print(f"{'='*70}")
            
            cmd = input("\n➡️  ").strip().lower()
            
            if cmd == '' or cmd == 'siguiente':
                if pagina + 1 < total_paginas:
                    pagina += 1
                else:
                    print("\n⚠️ Última página")
                    time.sleep(1)
            elif cmd == 'a' or cmd == 'anterior':
                if pagina > 0:
                    pagina -= 1
                else:
                    print("\n⚠️ Primera página")
                    time.sleep(1)
            elif cmd == 'b' or cmd == 'buscar':
                nuevo = input("\n🔍 Buscar: ").strip()
                if nuevo:
                    self.ver_libros(libros_por_pagina, nuevo, solo_disponibles)
                    return
            elif cmd == 'q' or cmd == 'salir':
                break

    def menu_libros_disponibles(self) -> dict:
        """
        Saca los libros disponibles para préstamo.
        
        OUTPUT:
            dict: Diccionario con ISBN como clave y objeto Libro como valor,
                  solo de libros no prestados actualmente
        """
        isbns_ocupados = self.isbns_prestados()
        return {
            isbn: libro
            for isbn, libro in self._libros.items()
            if isbn not in isbns_ocupados
        }
    
    def buscar_libro(self, texto: str) -> list:
        """
        Busca libros por título o autor (coincidencia parcial, insensible a mayúsculas).
        
        INPUT:
            texto (str): Texto a buscar en título o autor
        OUTPUT:
            list: Lista de objetos Libro que coinciden con la búsqueda
        """
        resultados = []
        texto_lower = texto.lower()

        for libro in self._libros.values():
            if texto_lower in libro.titulo.lower() or texto_lower in libro.autor.lower():
                resultados.append(libro)

        return resultados
    
    def comprobar_isbn(self, isbn: str) -> bool:
        """
        Verifica si un ISBN ya existe en la biblioteca.
        
        INPUT:
            isbn (str): ISBN a verificar
        OUTPUT:
            bool: True si existe, False en caso contrario
        """
        return isbn in self._libros
    
    # ============ FUNCIONES USUARIO ============
    
    def registrar_usuario(self, usuario: Usuario, confirmar_reemplazo: bool = True) -> bool:
        """
        Registra un nuevo usuario en la biblioteca.
        Si el ID ya existe, permite reemplazar o cancelar según confirmar_reemplazo.
        
        INPUT:
            usuario (Usuario): Objeto usuario a registrar
            confirmar_reemplazo (bool): Si True, pregunta antes de reemplazar;
                                        Si False, cancela automáticamente (default: True)
        OUTPUT:
            bool: True si se registró correctamente, False en caso contrario
        """
        try:
            if usuario.id in self._usuarios:
                if confirmar_reemplazo:
                    print(f"⚠️ El usuario con ID '{usuario.id}' ya existe.")
                    print("1. Reemplazar")
                    print("2. Cancelar")
                    
                    opcion = input("Opción: ").strip()
                    if opcion == "1":
                        self._usuarios[usuario.id] = usuario
                        print(f"✅ Usuario '{usuario.id}' reemplazado.")
                        return True
                    else:
                        print("❌ Registro cancelado.")
                        return False
                else:
                    print(f"❌ El usuario '{usuario.id}' ya existe. Registro cancelado.")
                    return False
            else:
                self._usuarios[usuario.id] = usuario
                print(f"✅ Usuario '{usuario.id}' registrado correctamente.")
                return True
        except Exception as e:
            print(f"❌ Error al registrar usuario: {e}")
            return False

    def ver_usuarios(self, usuarios_por_pagina: int = 10):
        """
        Muestra los usuarios registrados con paginación.
        
        INPUT:
            usuarios_por_pagina (int): Número de usuarios por página (default: 10)
        """
        self.limpiar_pantalla()
        
        usuarios_lista = list(self._usuarios.values())
        total_usuarios = len(usuarios_lista)
        
        if total_usuarios == 0:
            print("⚠️ No hay usuarios registrados.")
            return
        
        pagina_actual = 0
        total_paginas = (total_usuarios + usuarios_por_pagina - 1) // usuarios_por_pagina
        
        while True:           
            inicio = pagina_actual * usuarios_por_pagina
            fin = min(inicio + usuarios_por_pagina, total_usuarios)
            
            print(f"{'='*60}")
            print(f"LISTA DE USUARIOS (Página {pagina_actual + 1}/{total_paginas})")
            print(f"Total de usuarios: {total_usuarios}")
            print(f"{'='*60}\n")
            
            for i in range(inicio, fin):
                print(f"{i+1}. {usuarios_lista[i]}")
            
            print(f"\n{'='*60}")
            print("Comandos:")
            print("  [ENTER] - Siguiente página")
            print("  [A] - Página anterior")
            print("  [Q] - Salir")
            print(f"{'='*60}")
            
            comando = input("\n➡️:  ").strip().lower()
            
            if comando == '' or comando == 'siguiente' or comando == 's':
                if pagina_actual + 1 < total_paginas:
                    pagina_actual += 1
                else:
                    print("\n⚠️ Ya estás en la última página.")
                    time.sleep(1)
            elif comando == 'a' or comando == 'anterior':
                if pagina_actual > 0:
                    pagina_actual -= 1
                else:
                    print("\n⚠️ Ya estás en la primera página.")
                    time.sleep(1)
            elif comando == 'q' or comando == 'salir':
                break

    # ============ FUNCIONES PRESTAMO ============
    
    def prestar_libro(self, isbn: str, usuario_id: int, fecha: date, dias_maximos: int = 7):
        """
        Realiza el préstamo de un libro a un usuario.
        Utiliza el servicio PrestamoService para las validaciones.
        
        INPUT:
            isbn (str): ISBN del libro a prestar
            usuario_id (int): ID del usuario que realiza el préstamo
            fecha (date): Fecha del préstamo
            dias_maximos (int): Días máximos de préstamo (default: 7)
        OUTPUT:
            Prestamo: Objeto préstamo creado
        RAISE:
            ValueError: Si el libro o usuario no existen
            RuntimeError: Si el libro ya está prestado o el usuario supera el límite
        """
        # Usar servicio para validar
        self._prestamo_service.validar_prestamo(self, isbn, usuario_id)
        
        libro = self._libros[isbn]
        usuario = self._usuarios[usuario_id]
        prestamo = Prestamo(libro, usuario, fecha, dias_maximos)
        self._prestamos.append(prestamo)
        return prestamo
    
    def ver_prestamos(self):
        """
        Muestra todos los préstamos registrados (activos y devueltos).
        """
        if not self._prestamos:
            print("No hay préstamos registrados.")
            return

        for prestamo in self._prestamos:
            print(prestamo)

    def devolver_libro(self, isbn: str, fecha: date):
        """
        Devuelve un libro prestado.
        
        INPUT:
            isbn (str): ISBN del libro a devolver
            fecha (date): Fecha de devolución
        OUTPUT:
            Prestamo: Objeto préstamo actualizado con la fecha de devolución
        RAISE:
            RuntimeError: Si el libro no tiene un préstamo activo
        """
        prestamos_activos = self.prestamos_activos()
        prestamo = self._prestamo_service.obtener_prestamo_activo(isbn, prestamos_activos)
        
        if not prestamo:
            raise RuntimeError(f"Libro {isbn} no tiene préstamo activo")
        
        return prestamo.devolver(fecha)

    def prestamos_activos(self) -> list:
        """
        Saca los préstamos que están actualmente activos (no devueltos).
        
        OUTPUT:
            list: Lista de objetos Prestamo activos
        """
        return [p for p in self._prestamos if p.esta_activo()]

    def isbns_prestados(self) -> set:
        """
        Saca los ISBN de los libros actualmente prestados.
        
        OUTPUT:
            set: Conjunto de ISBN de libros prestados
        """
        return {p.libro.isbn for p in self.prestamos_activos()}
    
    # ============ FUNCIONES ESTADÍSTICAS (usando servicio) ============
    
    def resumen_biblioteca(self, fecha_actual: date = None) -> dict:
        """
        Genera un resumen estadístico completo de la biblioteca.
        
        INPUT:
            fecha_actual (date): Fecha para calcular multas y vencimientos (default: date.today())
        OUTPUT:
            dict: Diccionario con las siguientes claves:
                - total_libros: Número total de libros
                - total_usuarios: Número total de usuarios
                - total_prestamos: Número total de préstamos históricos
                - prestamos_activos: Número de préstamos activos
                - libros_disponibles: Número de libros disponibles
                - libros_prestados: Número de libros prestados
                - prestamos_vencidos: Número de préstamos vencidos
                - multas_totales: Total de multas pendientes
        """
        if fecha_actual is None:
            fecha_actual = date.today()
        
        return self._estadistica_service.resumen_biblioteca(
            self._libros,
            self._usuarios,
            self._prestamos,
            fecha_actual
        )
    
    def libros_mas_prestados(self, top_n: int = 5) -> list:
        """
        Saca los libros más prestados.
        
        INPUT:
            top_n (int): Número de libros que devuelve (default: 5)
        OUTPUT:
            list: Lista de tuplas (isbn, número_de_préstamos)
        """
        return self._estadistica_service.libros_mas_prestados(self._prestamos, top_n)
    
    def usuarios_mas_activos(self, top_n: int = 5) -> list:
        """
        Saca los usuarios con más préstamos.
        
        INPUT:
            top_n (int): Número de usuarios que devuelve (default: 5)
        OUTPUT:
            list: Lista de tuplas (Usuario, número_de_préstamos)
        """
        return self._estadistica_service.usuarios_mas_activos(
            self._prestamos, self._usuarios, top_n
        )
    
    def multas_pendientes(self, fecha_actual: date = None) -> dict:
        """
        Calcula las multas pendientes por usuario.
        
        INPUT:
            fecha_actual (date): Fecha para calcular multas (default: date.today())
        OUTPUT:
            dict: Diccionario con usuario como clave y total de multa como valor
        """
        if fecha_actual is None:
            fecha_actual = date.today()
        
        prestamos_activos = self.prestamos_activos()
        return self._estadistica_service.multas_pendientes(prestamos_activos, fecha_actual)
    
    def disponibilidad_libros(self) -> dict:
        """
        Saca la disponibilidad de cada libro.
        
        OUTPUT:
            dict: Diccionario con ISBN como clave y bool (True=disponible) como valor
        """
        isbns_prestados = self.isbns_prestados()
        return self._estadistica_service.disponibilidad_libros(self._libros, isbns_prestados)
    
    def prestamos_vencidos(self, fecha_actual: date = None) -> list:
        """
        Saca los préstamos activos que están vencidos.
        
        INPUT:
            fecha_actual (date): Fecha para verificar vencimiento (default: date.today())
        OUTPUT:
            list: Lista de objetos Prestamo vencidos
        """
        if fecha_actual is None:
            fecha_actual = date.today()
        
        prestamos_activos = self.prestamos_activos()
        return self._estadistica_service.prestamos_vencidos(prestamos_activos, fecha_actual)
    
    # ============ EXPORTAR/IMPORTAR ============
    
    def exportar_csv(self, oculto=False):
        """
        Exporta los datos de la biblioteca a archivos CSV en la carpeta db/.
        Crea tres archivos: libros.csv, usuarios.csv, prestamos.csv.
        
        INPUT:
            oculto (bool): Si True, no muestra mensaje de confirmación (default: False)
        """
        libros_csv = os.path.join(DB_DIR, "libros.csv")
        usuarios_csv = os.path.join(DB_DIR, "usuarios.csv")
        prestamos_csv = os.path.join(DB_DIR, "prestamos.csv")

        with open(libros_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["isbn","titulo","autor"])
            for l in self._libros.values():
                writer.writerow([l.isbn, l.titulo, l.autor])

        with open(usuarios_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id","nombre","max_prestamos"])
            for u in self._usuarios.values():
                writer.writerow([u.id, u.nombre, u.max_prestamos])

        with open(prestamos_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["isbn","usuario","fecha","dias","devolucion"])

            for p in self._prestamos:
                writer.writerow([
                    p.libro.isbn,
                    p.usuario.id,
                    p._fecha_alquiler,
                    p._dias_maximos,
                    p._devolucion
                ])
        if not oculto:
            print("Backup CSV guardado en carpeta db/ con exito")

    def exportar_json(self, oculto=False):
        """
        Exporta los datos de la biblioteca a un archivo JSON en la carpeta db/.
        
        INPUT:
            oculto (bool): Si True, no muestra mensaje de confirmación (default: False)
        """
        archivo = os.path.join(DB_DIR, "biblioteca.json")
        datos = {
            "libros": [
                {
                    "isbn": l.isbn,
                    "titulo": l.titulo,
                    "autor": l.autor
                }
                for l in self._libros.values()
            ],

            "usuarios": [
                {
                    "id": u.id,
                    "nombre": u.nombre,
                    "max_prestamos": u.max_prestamos
                }
                for u in self._usuarios.values()
            ],

            "prestamos": [
                {
                    "isbn": p.libro.isbn,
                    "usuario_id": p.usuario.id,
                    "fecha": p._fecha_alquiler.isoformat(),
                    "dias": p._dias_maximos,
                    "devolucion": None if p._devolucion is None else p._devolucion.isoformat()
                }
                for p in self._prestamos
            ]
        }

        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

        if not oculto:
            print("Backup JSON guardado en carpeta db/ con exito")

    def cargar_backup(self) -> bool:
        """
        Carga los datos desde archivos de backup en la carpeta db/.
        Prioridad: JSON > CSV
        
        OUTPUT:
            bool: True si se cargó correctamente, False si no hay backup
        """
        json_file = os.path.join(DB_DIR, "biblioteca.json")
        libros_csv = os.path.join(DB_DIR, "libros.csv")
        usuarios_csv = os.path.join(DB_DIR, "usuarios.csv")
        prestamos_csv = os.path.join(DB_DIR, "prestamos.csv")

        # Intentar cargar JSON
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                datos = json.load(f)

            self._libros.clear()
            self._usuarios.clear()
            self._prestamos.clear()

            for l in datos.get("libros", []):
                libro = Libro(l["isbn"], l["titulo"], l["autor"])
                self._libros[libro.isbn] = libro

            for u in datos.get("usuarios", []):
                usuario = Usuario(u["id"], u["nombre"], u["max_prestamos"])
                self._usuarios[usuario.id] = usuario

            for p in datos.get("prestamos", []):
                libro = self._libros[p["isbn"]]
                usuario = self._usuarios[p["usuario_id"]]

                prestamo = Prestamo(
                    libro,
                    usuario,
                    date.fromisoformat(p["fecha"]),
                    p["dias"]
                )

                if p.get("devolucion"):
                    prestamo._devolucion = date.fromisoformat(p["devolucion"])

                self._prestamos.append(prestamo)

            print("Backup cargado desde JSON")
            return True

        # Intentar cargar CSV
        if os.path.exists(libros_csv) and os.path.exists(usuarios_csv):
            self._libros.clear()
            self._usuarios.clear()
            self._prestamos.clear()

            # Libros
            with open(libros_csv, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    libro = Libro(row["isbn"], row["titulo"], row["autor"])
                    self._libros[libro.isbn] = libro

            # Usuarios
            with open(usuarios_csv, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    usuario = Usuario(
                        int(row["id"]),
                        row["nombre"],
                        int(row["max_prestamos"])
                    )
                    self._usuarios[usuario.id] = usuario

            # Préstamos
            if os.path.exists(prestamos_csv):
                with open(prestamos_csv, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        libro = self._libros[row["isbn"]]
                        usuario = self._usuarios[int(row["usuario"])]

                        prestamo = Prestamo(
                            libro,
                            usuario,
                            date.fromisoformat(row["fecha"]),
                            int(row["dias"])
                        )

                        if row["devolucion"] and row["devolucion"] != "None":
                            prestamo._devolucion = date.fromisoformat(row["devolucion"])

                        self._prestamos.append(prestamo)

            print("Backup cargado desde CSV")
            return True

        # No hay backup
        print("No existe backup en db/")
        return False
    
    # ============ PLUGINS ============
    
    def cargar_plugins(self):
        """
        Carga dinámicamente los plugins desde la carpeta plugins/.
        """
        if not os.path.exists(PL_DIR):
            print("Carpeta de plugins no encontrada")
            return

        for archivo in os.listdir(PL_DIR):
            if archivo.endswith(".py") and not archivo.startswith("__"):
                nombre_modulo = f"plugins.{archivo[:-3]}"
                try:
                    modulo = importlib.import_module(nombre_modulo)
                    for atributo in dir(modulo):
                        clase = getattr(modulo, atributo)
                        if isinstance(clase, type):
                            for metodo in dir(clase):
                                if not metodo.startswith("_"):
                                    funcion = getattr(clase, metodo)
                                    setattr(self.__class__, metodo, funcion)
                    print(f"Plugin cargado: {archivo}")
                except Exception as e:
                    print(f"Error cargando plugin {archivo}: {e}")