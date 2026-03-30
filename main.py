from biblioteca import *
from servicios.biblioteca_manager import BibliotecaManager
from datetime import date

# ============ MENÚ GESTIÓN BIBLIOTECAS ============

def menu_gestion_bibliotecas():
    """Menú para gestionar múltiples bibliotecas"""
    b.limpiar_pantalla()
    
    while True:
        print("\n" + "="*60)
        print("GESTIÓN DE BIBLIOTECAS")
        print("="*60)
        
        # Mostrar biblioteca actual
        try:
            actual = BibliotecaManager.obtener_biblioteca_actual()
            nombre_actual = BibliotecaManager._biblioteca_actual
            print(f"\n📖 Biblioteca actual: {nombre_actual}")
            print(f"   📚 Libros: {len(actual.libros)} | 👥 Usuarios: {len(actual.usuarios)} | 📋 Préstamos: {len(actual.prestamos)}")
        except RuntimeError:
            print("\n⚠️ No hay bibliotecas creadas")
        
        # Listar todas las bibliotecas
        bibliotecas = BibliotecaManager.listar_bibliotecas()
        if bibliotecas:
            print(f"\n📚 Bibliotecas disponibles ({len(bibliotecas)}):")
            for i, nombre in enumerate(bibliotecas, 1):
                marca = "⭐" if nombre == BibliotecaManager._biblioteca_actual else "  "
                print(f"   {marca} {i}. {nombre}")
        
        print("\n" + "-"*60)
        print(
            "Opciones:\n",
            "  1. Ver biblioteca actual\n",
            "  2. Crear nueva biblioteca\n",
            "  3. Cambiar a otra biblioteca\n",
            "  4. Eliminar biblioteca\n",
            "  99. Volver al menú principal"
        )
        print("="*60)
        
        opcion = input("\n➡️  ").strip()
        
        # Opción 1: Ver biblioteca actual
        if opcion == "1":
            try:
                actual = BibliotecaManager.obtener_biblioteca_actual()
                nombre_actual = BibliotecaManager._biblioteca_actual
                print(f"\n📖 BIBLIOTECA: {nombre_actual}")
                print(f"   📚 Libros: {len(actual.libros)}")
                print(f"   👥 Usuarios: {len(actual.usuarios)}")
                print(f"   📋 Préstamos totales: {len(actual.prestamos)}")
                print(f"   📋 Préstamos activos: {len(actual.prestamos_activos())}")
                b.pausa()
            except RuntimeError as e:
                print(f"\n❌ {e}")
                b.pausa()
        
        # Opción 2: Crear nueva biblioteca
        elif opcion == "2":
            nombre = input("\n📝 Nombre de la nueva biblioteca: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío")
                b.pausa()
                continue
            
            if BibliotecaManager.existe_biblioteca(nombre):
                print(f"❌ Ya existe una biblioteca con el nombre '{nombre}'")
                b.pausa()
                continue
            
            try:
                nueva = BibliotecaManager.crear_biblioteca(nombre)
                nueva.cargar_plugins()
                print(f"✅ Biblioteca '{nombre}' creada y seleccionada como actual")
                b.pausa()
            except Exception as e:
                print(f"❌ Error: {e}")
                b.pausa()
        
        # Opción 3: Cambiar a otra biblioteca
        elif opcion == "3":
            bibliotecas = BibliotecaManager.listar_bibliotecas()
            if not bibliotecas:
                print("\n⚠️ No hay bibliotecas disponibles. Crea una primero.")
                b.pausa()
                continue
            
            print("\n📚 Selecciona biblioteca:")
            for i, nombre in enumerate(bibliotecas, 1):
                marca = "⭐" if nombre == BibliotecaManager._biblioteca_actual else "  "
                print(f"   {marca} {i}. {nombre}")
            
            try:
                sel = input("\nNúmero: ").strip()
                if sel.isdigit():
                    idx = int(sel) - 1
                    if 0 <= idx < len(bibliotecas):
                        nombre = bibliotecas[idx]
                        BibliotecaManager.cambiar_biblioteca(nombre)
                        b.pausa()
                    else:
                        print("❌ Número inválido")
                        b.pausa()
                else:
                    print("❌ Introduce un número")
                    b.pausa()
            except Exception as e:
                print(f"❌ Error: {e}")
                b.pausa()
        
        # Opción 4: Eliminar biblioteca
        elif opcion == "4":
            bibliotecas = BibliotecaManager.listar_bibliotecas()
            if len(bibliotecas) <= 1:
                print("\n⚠️ No se puede eliminar la única biblioteca")
                b.pausa()
                continue
            
            print("\n🗑️ Selecciona biblioteca a eliminar:")
            for i, nombre in enumerate(bibliotecas, 1):
                marca = "⭐" if nombre == BibliotecaManager._biblioteca_actual else "  "
                print(f"   {marca} {i}. {nombre}")
            
            try:
                sel = input("\nNúmero: ").strip()
                if sel.isdigit():
                    idx = int(sel) - 1
                    if 0 <= idx < len(bibliotecas):
                        nombre = bibliotecas[idx]
                        
                        if nombre == BibliotecaManager._biblioteca_actual:
                            print("⚠️ Esta es la biblioteca actual. Se cambiará a otra automáticamente.")
                        
                        confirm = input(f"¿Seguro que quieres eliminar '{nombre}'? (s/N): ").strip().lower()
                        if confirm == 's':
                            BibliotecaManager.eliminar_biblioteca(nombre)
                            b.pausa()
                        else:
                            print("❌ Eliminación cancelada")
                            b.pausa()
                    else:
                        print("❌ Número inválido")
                        b.pausa()
                else:
                    print("❌ Introduce un número")
                    b.pausa()
            except Exception as e:
                print(f"❌ Error: {e}")
                b.pausa()
        
        # Opción 99: Volver
        elif opcion == "99":
            break
        
        else:
            print("❌ Opción no válida")
            b.pausa()
        
        b.limpiar_pantalla()


# ============ INICIALIZACIÓN ============

if not BibliotecaManager.listar_bibliotecas():
    BibliotecaManager.crear_biblioteca("Principal")

b = BibliotecaManager.obtener_biblioteca_actual()
b.cargar_plugins()
print("Plugins cargados...")

if b.cargar_backup() == False:
    print("Generando Datos Base. . .")
    l1 = Libro("1", "pepito el guerrero", "pepito el autor anonimo")
    l2 = Libro("2", "pepito el mago", "pepito el autor anonimo")
    l3 = Libro("3", "pepito el picaro", "pepito el autor anonimo")
    b + l1 + l2 + l3

    u1 = Usuario(1, "pepe", 2)
    b.registrar_usuario(u1)
    b.registrar_usuario(Usuario(2, "pepa", 1))
    b.registrar_usuario(Usuario(3, "pepi", 2))
    u1(b, "1", date.today())
    b.exportar_json(1)
    b.exportar_csv(1)
else:
    print("Cargada Copia de Seguridad")

b.pausa()
b.limpiar_pantalla()
breaker = False
# ============ FIN INICIALIZACIÓN ============

# ============ MENÚ PRINCIPAL ============

while breaker == False:
    # Obtener biblioteca actual
    try:
        b = BibliotecaManager.obtener_biblioteca_actual()
        nombre_actual = BibliotecaManager._biblioteca_actual
        print(f"\n📖 Biblioteca actual: {nombre_actual} | 📚 {len(b.libros)} libros | 👥 {len(b.usuarios)} usuarios")
    except:
        pass
    
    print(
        "\n" + "="*60,
        "📚 BIBLIOTECA 2.0",
        "="*60,
        "\n1 - Menú de Libros",
        "2 - Menú de Usuarios", 
        "3 - Menú de Préstamos",
        "4 - Ver Estadísticas (plugins)",
        "5 - Gestión de Bibliotecas",
        "99 - Salir",
        "="*60,
        sep="\n"
    )

    try:
        seleccion = int(input("\n➡️  Que quieres hacer? "))
        
        # Libros
        if seleccion == 1:
            breaker_lib = True
            b.limpiar_pantalla()
            while breaker_lib:
                print("\n" + "="*60)
                print("GESTIÓN DE LIBROS")
                print("="*60)
                print(
                    "\n",
                    " 1 - Registrar Libro \n",
                    " 2 - Ver/Buscar Todos los Libros de la Biblioteca \n",
                    " 3 - Ver/Buscar los Libros Disponibles \n",
                    " 99 - Volver \n",
                )
                try:
                    seleccion_lib = int(input("➡️  Que quieres hacer? "))
            
                    # Registrar libro
                    if seleccion_lib == 1:
                        while True:
                            isbn = input("Dime el ISBN: ")
                            
                            if b.comprobar_isbn(isbn):
                                print(
                                    f"⚠️ Ya existe un libro con el ISBN '{isbn}'.\n"
                                    "1. Sobrescribir el libro existente\n"
                                    "2. Cancelar y volver a intentar con otro ISBN\n"
                                    "3. Salir al menú principal\n"
                                )
                                
                                opcion = input("Selecciona una opción (1/2/3): ")
                                
                                if opcion == "1":
                                    nombre = input("Dime el Nombre: ")
                                    autor = input("Dime el Autor: ")
                                    libro = Libro(isbn, nombre, autor)
                                    b.registrar_libro(libro)
                                    print(f"✅ Se ha sobrescrito el libro {libro}")
                                    b.exportar_json(1)
                                    b.exportar_csv(1)
                                    b.pausa()
                                    break 

                                elif opcion == "2":
                                    print("❌ Operación cancelada. Introduce otro ISBN.")
                                    continue
                                    
                                elif opcion == "3":
                                    print("❌ Operación cancelada. Volviendo al menú principal...")
                                    break
                                    
                                else:
                                    print("❌ Opción no válida. Intenta de nuevo.")
                                    continue
                            else:
                                nombre = input("Dime el Nombre: ")
                                autor = input("Dime el Autor: ")
                                libro = Libro(isbn, nombre, autor)
                                b.registrar_libro(libro)
                                print(f"✅ Se ha registrado el libro {libro}")
                                b.exportar_json(1)
                                b.exportar_csv(1)
                                b.pausa()
                                break
                        b.limpiar_pantalla()

                    # Ver Libros
                    elif seleccion_lib == 2: 
                        b.ver_libros()
                        b.limpiar_pantalla()

                    # Ver Libros Disponibles
                    elif seleccion_lib == 3: 
                        b.ver_libros(solo_disponibles=True)   
                        b.limpiar_pantalla()         

                    elif seleccion_lib == 99:
                        breaker_lib = False
                        b.limpiar_pantalla()
                    else:
                        print("❌ Opción no válida")
                except ValueError:  
                    print("Elige un número de la lista")
        
        # Usuarios
        elif seleccion == 2:
            breaker_usu = True
            b.limpiar_pantalla()
            while breaker_usu:
                print("\n" + "="*60)
                print("GESTIÓN DE USUARIOS")
                print("="*60)
                print(
                    "\n",
                    " 1 - Registrar Usuario \n",
                    " 2 - Ver Todos los Usuarios \n",
                    " 99 - Volver \n",
                )
                try:
                    seleccion_usu = int(input("➡️  Que quieres hacer? "))
            
                    if seleccion_usu == 1:
                        id = int(input("Dime el ID (numerico): "))
                        nombre = input("Dime el Nombre: ")
                        prestamos = int(input("Dime cuantos prestamos puede hacer: "))
                        usuario = Usuario(id, nombre, prestamos)
                        if b.registrar_usuario(usuario) == True:
                            print(f"✅ Se ha registrado al usuario {usuario}")
                            b.exportar_json(1)
                            b.exportar_csv(1)
                            b.pausa()
                        
                    elif seleccion_usu == 2: 
                        b.limpiar_pantalla()
                        b.ver_usuarios()

                    elif seleccion_usu == 99:
                        breaker_usu = False
                    else:
                        print("❌ Opción no válida")
                except ValueError:  
                    print("Elige un número de la lista")
                b.limpiar_pantalla()

        # Prestamos
        elif seleccion == 3:
            breaker_pre = True
            b.limpiar_pantalla()
            while breaker_pre:
                print("\n" + "="*60)
                print("GESTIÓN DE PRESTAMOS")
                print("="*60)
                print(
                    "\n",
                    " 1 - Prestar Libro \n",
                    " 2 - Ver TODOS los préstamos \n",
                    " 3 - Ver préstamos ACTIVOS \n",
                    " 4 - Ver préstamos DEVUELTOS \n",
                    " 5 - Ver préstamos VENCIDOS (con multa) \n",
                    " 6 - Devolver un Libro \n",
                    " 99 - Volver \n",
                )
                try:
                    seleccion_pre = int(input("➡️  Que quieres hacer? "))
            
                    # Prestar
                    if seleccion_pre == 1:
                        try:
                            libros_disp = b.menu_libros_disponibles()
                            if not libros_disp:
                                raise RuntimeError("❌ No hay libros disponibles para prestar")
                            
                            isbn = b.menu_seleccionar(libros_disp, "libros")

                            if isbn != False:
                                usuario_id = b.menu_seleccionar(b.usuarios, "usuarios")

                                if usuario_id != False:
                                    prestamo = b.prestar_libro(
                                        isbn=isbn, usuario_id=usuario_id, fecha=date.today()
                                    )

                                    print("✅ Préstamo realizado con éxito\n", prestamo)
                                    b.exportar_json(1)
                                    b.exportar_csv(1)
                                    b.pausa()
                                    b.limpiar_pantalla()

                                else:
                                    raise RuntimeError("❌ No se ha realizado el préstamo por error en id elegido")
                            else:
                                raise RuntimeError("❌ Préstamo cancelado.")

                        except Exception as e:
                            print(f"❌ Error: {e}")
                            b.pausa()

                    # Ver préstamos (Todos)
                    elif seleccion_pre == 2:
                        b.ver_prestamos(filtro="todos")
                    
                    # Ver préstamos (Activos)
                    elif seleccion_pre == 3:
                        b.ver_prestamos(filtro="activos")
                    
                    # Ver préstamos (Devueltos)
                    elif seleccion_pre == 4:
                        b.ver_prestamos(filtro="devueltos")
                    
                    # Ver préstamos (con multa)
                    elif seleccion_pre == 5:
                        b.ver_prestamos(filtro="vencidos")
                    
                    # Devoluciones
                    elif seleccion_pre == 6: 
                        if not b.prestamos_activos():
                            print("No hay libros actualmente prestados")
                            b.pausa()
                            b.limpiar_pantalla()
                        else:
                            print("\nLibros actualmente prestados:")
                            print("\nEscribe 'SALIR' para cancelar")

                            for id, prestamo in enumerate(b.prestamos_activos(), start=1):
                                print(
                                    f"{id} - {prestamo.libro.titulo} (ISBN: {prestamo.libro.isbn}) prestado a {prestamo.usuario.nombre}"
                                )

                            breaker_dev = True
                            salir = False
                            while breaker_dev:
                                opcion = input("\nElige ID del libro a devolver: ").strip()

                                if opcion.upper() == "SALIR":
                                    salir = True
                                    break
                                
                                if not opcion.isdigit():
                                    print("Introduce un número válido o SALIR")
                                    continue

                                idx = int(opcion) - 1

                                if 0 <= idx < len(b.prestamos_activos()):
                                    prestamo_seleccionado = b.prestamos_activos()[idx]
                                    breaker_dev = False
                                    break

                                print("ID incorrecto, selecciona uno de la lista")

                            try:
                                if salir == False:
                                    b.devolver_libro(prestamo_seleccionado.libro.isbn, date.today())
                                    
                                    b.exportar_json(1)
                                    b.exportar_csv(1)
                                    print(f"✅ El libro '{prestamo_seleccionado.libro.titulo}' se ha devuelto correctamente")
                                    b.pausa()
                                else:
                                    print("❌ Devolución cancelada.")
                                    b.pausa()

                            except RuntimeError as e:
                                print("Error:", e)
                                b.pausa()

                    elif seleccion_pre == 99:
                        breaker_pre = False
                        b.limpiar_pantalla()

                    else:
                        print("Opción no válida")
                        b.pausa()
                        
                except ValueError:  
                    print("Elige un número de la lista")
                    b.pausa()
                b.limpiar_pantalla()

        # Menu Plugins
        elif seleccion == 4:
            breaker_plug = True
            b.limpiar_pantalla()
            while breaker_plug:
                print("\n" + "="*60)
                print("ESTADISTICAS")
                print("="*60)
                print(
                    "\n",
                    " 1 - Total de Libros \n",
                    " 2 - Total Usuarios \n",
                    " 3 - Total de Prestamos \n",
                    " 99 - Volver \n",
                )
                try:
                    seleccion_plug = int(input("➡️  Que quieres hacer? "))
                    if seleccion_plug == 1:
                        print(b.total_libros())
                        b.pausa()
                        b.limpiar_pantalla()
                    elif seleccion_plug == 2: 
                        print(b.total_usuarios())
                        b.pausa()
                        b.limpiar_pantalla()
                    elif seleccion_plug == 3: 
                        print(b.total_prestamos())
                        b.pausa()
                        b.limpiar_pantalla()
                    elif seleccion_plug == 99:
                        breaker_plug = False
                    else:
                        print("Opción no válida")
                except ValueError:  
                    print("Elige un número de la lista")

        # Menú Gestión Bibliotecas (NUEVO)
        elif seleccion == 5:
            menu_gestion_bibliotecas()
            # Actualizar referencia a la biblioteca actual después de cambiar
            b = BibliotecaManager.obtener_biblioteca_actual()

        # Limpiamos consola y salimos
        elif seleccion == 99:
            b.limpiar_pantalla()
            print("Guardando base de datos")
            for nombre, biblio in BibliotecaManager._bibliotecas.items():
                print(f"   Guardando {nombre}...")
                biblio.exportar_json(1)
                biblio.exportar_csv(1)
            print("✅ Datos guardados correctamente")
            breaker = True

        else:
            print("❌ Opción no válida")
        b.limpiar_pantalla()

    except ValueError:
        print("❌ Error, introduce un número de la lista")
        b.pausa()
        b.limpiar_pantalla()