# 🏥 Hospital Carlos Lanfranco La Hoz — Sistema Web de Citas

Sistema web completo para la gestión de citas médicas con soporte de IA local para clasificación de síntomas y visualización de reportes estadísticos.

## 📁 Estructura
```
hospital/
├── app.py                      ← Aplicación principal Flask
├── requirements.txt            ← Dependencias Python (Flask, ReportLab, scikit-learn, etc.)
├── correo.py                   ← Módulo de envío de correos de confirmación
├── .env.example                ← Ejemplo de variables de entorno para correo
├── data/
│   └── sintomas_especialidad.csv ← Dataset de síntomas simulados
├── models/
│   ├── modelo_sintomas.pkl     ← Modelo clasificador entrenado (LogisticRegression)
│   └── vectorizer_sintomas.pkl ← Vectorizador TF-IDF entrenado
├── scripts/
│   ├── generar_dataset_sintomas.py ← Script para generar el dataset de síntomas
│   └── entrenar_modelo_sintomas.py ← Script para entrenar y guardar el modelo IA
├── static/
│   ├── CSS/                    ← Hojas de estilo CSS (base, accesibilidad, admin, etc.)
│   └── JS/                     ← Código JavaScript (accesibilidad, reportes)
└── templates/
    ├── base.html               ← Plantilla base (navbar + footer + panel de accesibilidad)
    ├── index.html              ← Página de inicio
    ├── login.html              ← Inicio de sesión
    ├── registro.html           ← Registro de pacientes
    ├── dashboard.html          ← Panel del paciente (mis citas + reprogramar)
    ├── solicitar_cita.html     ← Solicitud de citas (manual + chatbot de síntomas)
    └── admin.html              ← Panel administrativo (citas, usuarios, reportes)
```

## 🚀 Instalación y Ejecución

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno
# Copia .env.example como .env y completa las credenciales de correo (opcional)

# 3. Generar dataset y entrenar el modelo de IA local
python scripts/generar_dataset_sintomas.py
python scripts/entrenar_modelo_sintomas.py

# 4. Ejecutar la aplicación
python app.py

# 5. Abrir en el navegador
http://localhost:5000
```

## 🔑 Credenciales por defecto (Admin)
- **Email:** `admin@lanfranco.pe`
- **Contraseña:** `admin123`

## 🗄️ Base de Datos (MySQL)
La aplicación utiliza una base de datos MySQL configurada en `app.py`. Al iniciar la aplicación, se ejecutará una migración automática que añade la columna `activo` a la tabla `usuarios` y la poblará con valores por defecto.

## 🤖 Motor de IA Local (Clasificador de Síntomas)
El asistente de citas utiliza un modelo local entrenado con **scikit-learn** sobre una base de datos de síntomas redactados en español coloquial peruano. 
- Mapea síntomas descritos por voz o chat a 8 especialidades médicas: `Cardiologia`, `Pediatria`, `Ginecologia`, `Traumatologia`, `Medicina General`, `Oftalmologia`, `Neurologia`, y `Dermatologia`.
- Si la confianza de la predicción es menor al 40%, redirige automáticamente y sugiere `Medicina General` como fallback de seguridad.

## 🌐 Nuevas Rutas y APIs

| Ruta | Método | Descripción | Acceso |
|------|--------|-------------|--------|
| `/` | GET | Página principal | Público |
| `/login` | GET/POST | Inicio de sesión | Público |
| `/registro` | GET/POST | Registro de paciente | Público |
| `/dashboard` | GET | Panel del paciente (mis citas) | Paciente |
| `/solicitar-cita` | GET/POST | Solicitar cita (manual + chatbot) | Paciente |
| `/reprogramar-cita/<id>` | POST | Reprogramar una cita existente | Paciente |
| `/cancelar-cita/<id>` | POST | Cancelar una cita (con redirección inteligente) | Paciente / Admin |
| `/admin` | GET | Panel de administración principal | Admin |
| `/admin/cita/editar/<id>` | POST | Editar médico/fecha/hora de una cita | Admin |
| `/admin/usuario/editar/<id>`| POST | Editar datos del paciente (nombre, correo, telf) | Admin |
| `/admin/usuario/toggle/<id>`| POST | Activar o desactivar (Soft Delete) un usuario | Admin |
| `/admin/reportes/exportar-pdf`| GET | Descargar reporte de citas en PDF (ReportLab) | Admin |
| `/admin/reportes/exportar-excel`| GET | Descargar reporte de citas en Excel (openpyxl) | Admin |
| `/api/medicos/<esp_id>` | GET | Listar médicos disponibles por especialidad | Público |
| `/api/horarios/<med_id>/<fecha>`| GET | Horarios disponibles filtrando citas activas | Público |
| `/api/clasificar-sintomas` | POST | Clasificar síntomas en JSON (IA local) | Público |
