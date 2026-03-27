# Biblioteca Version 2
Requisitos:
  - Descargar el contenido en una carpeta
  - Crear un entorno virtual y ejecutar pip install -r requirements.txt
  - Para verificar las pruebas del proyecto utilizar python -m pytest tests/ 


Motivos:
  - Patron Singleton: He utilizado un singleton para hacer la biblioteca centralizada, estilo netflix o blockbuster al inicio de la era stream, que desde x lugares pedias a un servidor central la pelicula y la recibias, stock unico para todas las bibliotecas, sin pisarse entre ellas con el singleton.

  - Plugins: Incluyo los decoradores de validación como los Mixins para incorporarlos, unicamente por centrar carpetas de servicios.
  - - Las utilidades son las funciones que se comparte entre todas las clases, como limpiar pantalla, pausar pantalla o generar un menu.
  - - Mixins tenemos los validadores comunes.

  - En Servicios meto la logica que no es de los modelos ni de la interfaz, porque al acabar el ejercicio tenia todo remezclado, como el validar prestamos, que tenia 50 lineas metidas y costaba leer, ahora solo tiene su estado y el servicio se encarga de la logica.

Mejoras:
  - 


Estructura del Proyecto:
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