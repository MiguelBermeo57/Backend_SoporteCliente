Sistema de Soporte - API de Tickets 🎫
API REST construida con FastAPI y MySQL para la gestión de usuarios y tickets de soporte técnico.

🚀 Características
Gestión de Usuarios: Registro con validación de correo único.

Tickets: Creación y seguimiento de estados (abierto, en proceso, cerrado).

Base de Datos: Relacional con SQLAlchemy y MySQL.

Pruebas: Configuración lista para pruebas de carga con JMeter.

🛠️ Instalación
Importar los archivos .sql en MySQL.

Configurar credenciales en main.py.

Ejecutar: uvicorn main:app --reload.

📌 Endpoints
POST /usuarios/

POST /tickets/

GET /tickets/{id}.
