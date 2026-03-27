# Biblioteca Versión 2
Requisitos:
  - Descargar el contenido en una carpeta
  - Crear un entorno virtual y ejecutar pip install -r requirements.txt
  - Para verificar las pruebas del proyecto utilizar python -m pytest tests/ 


Motivos y lugar:

  - He comentado (con IA porque era mucho texto) las funciones que no habia comentado de base, para que sea más facil de entender que es y que hace cada funcion, ya que por ejemplo biblioteca yo entiendo bien todo lo que hace si pliego las funciones y busco la que quiero, pero de primeras asusta ver 750 lineas 💀.

  - Patron Singleton: He utilizado un singleton en biblioteca para hacer la biblioteca centralizada, estilo netflix o blockbuster al inicio de la era stream, que desde x lugares pedias a un servidor central la pelicula y la recibias, stock unico para todas las bibliotecas, sin pisarse entre ellas con el singleton.

  - Plugins: Incluyo los decoradores de validación como los Mixins, los he centralizado en la misma carpeta para simplificar carpetas de servicios.
  - - Las utilidades son las funciones que se comparte entre todas las clases, como limpiar pantalla, pausar pantalla o generar un menu.
  - - Mixins tenemos los validadores comunes, los utilizamos en libro y usuario.
  - - Estadisticas.py: Es el plugin utilizado en main para calcular estadisticas de libros, usuarios y prestamos.

  - En Servicios meto la logica que no es de los modelos ni de la interfaz, porque al acabar el ejercicio tenia todo remezclado, como el validar prestamos, que tenia 50 lineas metidas y costaba leer, ahora solo tiene su estado y el servicio se encarga de la logica.

  - Main: Unicamente tiene la logica de la interfaz, es quien inicializa todo el programa, en caso de no haber copia, genera una biblioteca estandar de la que partiremos.
  He puesto iconitos porque me parece más visible y bonito cara a un usuario final que solo prints. Tambien utilizo el sleep pero implemento el util pausa(), para que sea más ameno la navegación.

  - Libro: El ISBN lo he dejado inmutable ya que es como un DNI, no puedes cambiarlo, mientras que el resto de datos si podrias por si hay alguna errata o cambios de estos.
  Incluyo validadores en el autor y el titulo.

  - Prestamo: Valor de la multa calculado por variable global, no implementa más tipos de multa, es universal.

  - Exportar: Exporto tanto en CSV como JSON, para tener una copia de seguridad de emergencia, en caso de que el JSON no estuviera disponible se cargaria el CSV como respaldo. Todo centralizado en la carpeta DB.
  También carga y guarda automaticamente para no tener que trabajar a mano, como se haria en una empresa.

  - Tests: Conftest.py se utiliza para reiniciar las pruebas, ya que por cache se guardaban las bibliotecas y las pruebas daban fallo.
  - - 1 biblioteca: Pruebas exaustivas de cada funcion para comprobar que no falla nada.
  - - 2 integración: Pruebas de prestamo, que usan varias clases y que singleton comparte datos.
  - - 3 usuario: Pruebas de creación, poder pedir libros, creaciones validas, etc.
  - - 4 prestamo: Calculo de prestamos, de multas, devoluciones y retrasos.
  - - 5 libro: Creacion y validacion de libros.

--<buscar validacion metaclase>

Mejoras:
  - Localización en tiempo real de los libros.
  - Mejora de la representación de los prestamos, estilo usuario / libro.
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