# 🏥 Hospital Carlos Lanfranco La Hoz — Sistema Web de Citas

Sistema web completo para gestión de citas médicas con soporte de IA por voz.

## 📁 Estructura
```
hospital/
├── app.py                  ← Aplicación principal Flask
├── requirements.txt        ← Dependencias Python
├── hospital.db             ← Base de datos SQLite (se crea automáticamente)
└── templates/
    ├── base.html           ← Plantilla base (navbar + footer)
    ├── index.html          ← Página principal
    ├── login.html          ← Inicio de sesión
    ├── registro.html       ← Registro de pacientes
    ├── dashboard.html      ← Panel del paciente
    ├── solicitar_cita.html ← Formulario + Asistente de voz IA
    └── admin.html          ← Panel de administración
```

## 🚀 Instalación y Ejecución

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la aplicación
python app.py

# 3. Abrir en el navegador
http://localhost:5000
```

## 🔑 Credenciales por defecto (Admin)
- **Email:** admin@lanfranco.pe
- **Contraseña:** admin123

## 🗄️ Base de Datos (SQLite — hospital.db)

### Tablas:
| Tabla         | Descripción                              |
|---------------|------------------------------------------|
| `usuarios`    | Pacientes y administradores              |
| `especialidades` | Especialidades médicas disponibles    |
| `medicos`     | Médicos por especialidad                 |
| `citas`       | Citas médicas solicitadas                |

### Agregar datos (ejemplo):
```python
# En el shell de Python con el contexto de la app
from app import app, db, Medico
with app.app_context():
    medico = Medico(nombre='Juan', apellido='Pérez López', cmp='CM-99999', especialidad_id=1)
    db.session.add(medico)
    db.session.commit()
```

## 🤖 IA por Voz
- **Actual:** Reconocimiento de voz nativo del navegador (Web Speech API) en español peruano.
- **Próxima fase:** Integración completa con Claude API para procesamiento inteligente de lenguaje natural, detección de síntomas y agendamiento automático.

## 🌐 Rutas disponibles
| Ruta              | Descripción                    | Acceso     |
|-------------------|--------------------------------|------------|
| `/`               | Página principal               | Público    |
| `/login`          | Inicio de sesión               | Público    |
| `/registro`       | Registro de paciente           | Público    |
| `/dashboard`      | Panel del paciente             | Autenticado|
| `/solicitar-cita` | Solicitar cita (manual + voz)  | Autenticado|
| `/admin`          | Panel de administración        | Admin      |
| `/api/medicos/<id>`| API: médicos por especialidad | Público    |
| `/api/horarios/<med>/<fecha>` | API: horarios disponibles | Público |

## 🔧 Personalización
Para agregar tus propios médicos, especialidades y datos, edita la función
`inicializar_db()` en `app.py` o usa el shell de Flask/SQLite directamente.
