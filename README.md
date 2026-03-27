# Biblioteca Versión 2
Requisitos:
  - Descargar el contenido en una carpeta
  - Crear un entorno virtual y ejecutar pip install -r requirements.txt
  - Para verificar las pruebas del proyecto utilizar python -m pytest tests/ en la carpeta raíz.

Motivos y lugar:

  - He comentado (con IA porque era mucho texto) las funciones que no había comentado de base, para que sea más fácil de entender que es y que hace cada función, ya que por ejemplo biblioteca yo entiendo bien todo lo que hace si pliego las funciones y busco la que quiero, pero de primeras asusta ver 750 líneas 💀.

  - Patron Singleton: He utilizado un singleton en biblioteca para hacer la biblioteca centralizada, estilo netflix o blockbuster al inicio de la era stream, que desde x lugares pedias a un servidor central la película y la recibías, stock único para todas las bibliotecas, sin pisarse entre ellas con el singleton.

  - Plugins: Incluyo los decoradores de validación como los Mixins, los he centralizado en la misma carpeta para simplificar carpetas de servicios.
  - - Las utilidades son las funciones que se comparte entre todas las clases, como limpiar pantalla, pausar pantalla o generar un menu.
  - - Mixins tenemos los validadores comunes, los utilizamos en libro y usuario.
  - - Estadisticas.py: Es el plugin utilizado en main para calcular estadísticas de libros, usuarios y préstamos.

  - En Servicios meto la lógica que no es de los modelos ni de la interfaz, porque al acabar el ejercicio tenía todo remezclado, como el validar prestamos, que tenía 50 líneas metidas y costaba leer, ahora solo tiene su estado y el servicio se encarga de la lógica.

  - Main: Únicamente tiene la lógica de la interfaz, es quien inicializa todo el programa, en caso de no haber copia, genera una biblioteca estándar de la que partiremos.
  He puesto iconitos porque me parece más visible y bonito cara a un usuario final que solo prints. Tambien utilizo el sleep pero implemento el útil pausa(), para que sea más ameno la navegación.

  - Libro: El ISBN lo he dejado inmutable ya que es como un DNI, no puedes cambiarlo, mientras que el resto de datos si podrías por si hay alguna errata o cambios de estos.
  Incluyo validadores en el autor y el título.
  Cuando se crea un libro, y se selecciona un ISBN que ya existe, da la opción de reemplazar, pero SOLO los datos (nombre y autor).

  - Prestamo: Valor de la multa calculado por variable global, no implementa más tipos de multa, es universal. Se calcula en tiempo real por la fecha en la que se cogió el libro (un .now(), la db subida tiene 1 caso mínimo para testear) 

  - Exportar: Exporto tanto en CSV como JSON, para tener una copia de seguridad de emergencia, en caso de que el JSON no estuviera disponible se cargaría el CSV como respaldo. Todo centralizado en la carpeta DB. hace la carga y descarga automáticamente para no tener que trabajar a mano (al crear o modificar algo, libro, usuario, prestamo), como se haría en una empresa.

  - Tests: Conftest.py se utiliza para reiniciar las pruebas, ya que por cache se guardaban las bibliotecas y las pruebas daban fallo.
  - - 1 biblioteca: Pruebas exhaustivas de cada función para comprobar que no falla nada.
  - - 2 integración: Pruebas de préstamo, que usan varias clases y que singleton comparte datos.
  - - 3 usuario: Pruebas de creación, poder pedir libros, creaciones validas, etc.
  - - 4 préstamo: Calculo de préstamos, de multas, devoluciones y retrasos.
  - - 5 libro: Creación y validación de libros.

<buscar validacion metaclase>

Mejoras:
  - Localización en tiempo real de los libros.
  - Mejora de la representación de los préstamos, estilo usuario / libro.
  - Dar de alta / baja libros.
  - Exportar las Bibliotecas en el CSV y JSON.
  - Posibilidad de la multa aumente pasado mes o similar.


## 📁 Estructura del Proyecto
```
├── 📁 db/                      # Datos persistentes
│   ├── biblioteca.json         # Backup JSON
│   └── *.csv                   # Backups CSV
│
├── 📁 plugins/                 # Plugins y mixins
│   ├── estadisticas.py         # Plugin de estadísticas
│   ├── mixins.py               # Mixins de validación
│   └── utils.py                # Utilidades (UI)
│
├── 📁 servicios/               # Lógica de negocio
│   └── biblioteca_manager.py   # Gestor de múltiples bibliotecas (Singleton por nombre)
│   └── estadistica_service.py  # Cálculos estadísticos
│   ├── prestamo_service.py     # Validaciones de préstamos
│
├── 📁 tests/                   # Tests unitarios
│   ├── conftest.py             # 🔧 Configuración global de pytest y fixtures
│   ├── test_1_biblioteca.py
│   ├── test_2_integracion.py
│   ├── test_3_usuario_avanzado.py
│   ├── test_4_prestamo_avanzado.py
│   └── test_5_libro_avanzado.py
│
├── 📄 biblioteca.py            # Clase principal
├── 📄 libro.py                 # Entidad Libro
├── 📄 main.py                  # Interfaz CLI
├── 📄 prestamo.py              # Entidad Préstamo
└── 📄 README.md                # Este archivo
├── 📄 requirements.txt         # Dependencias
├── 📄 usuario.py               # Entidad Usuario
```