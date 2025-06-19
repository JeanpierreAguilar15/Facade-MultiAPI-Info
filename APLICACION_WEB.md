# Aplicación Web - Patrón Facade

Esta aplicación web demuestra el patrón Facade mediante una interfaz moderna y funcional que permite consultar información de ciudades usando múltiples APIs de forma unificada.

## APIs Utilizadas (Todas Gratuitas)

### 1. Open-Meteo - Clima
- **Estado**: Completamente gratuita
- **Registro**: No requerido
- **API Key**: No necesaria
- **Datos**: Temperatura, humedad, presión, condiciones climáticas

### 2. Hacker News API - Noticias
- **Estado**: Completamente gratuita  
- **Registro**: No requerido
- **API Key**: No necesaria
- **Datos**: Noticias tecnológicas y de startups más populares

### 3. REST Countries - Países
- **Estado**: Completamente gratuita
- **Registro**: No requerido
- **API Key**: No necesaria
- **Datos**: Información completa de países

## Características de la Aplicación

### Interfaz Principal
- **Búsqueda de ciudades**: Campo de entrada intuitivo
- **Resultados en tiempo real**: Información actualizada
- **Diseño responsive**: Compatible con móviles y tablets
- **Interfaz moderna**: Bootstrap 5 y Font Awesome

### Funcionalidades

#### 1. Consulta de Información
- Endpoint: `POST /api/consultar`
- Parámetro: `ciudad` (nombre de la ciudad)
- Respuesta: JSON con clima, noticias y datos del país

#### 2. Diagnóstico de APIs
- Endpoint: `GET /api/diagnostico`
- Función: Verifica el estado de todas las APIs
- Respuesta: Estado de conexión de cada servicio

#### 3. Información del Facade
- Endpoint: `GET /api/facade-info`
- Función: Información sobre el patrón implementado
- Respuesta: Detalles técnicos del sistema

## Instalación y Ejecución

### 1. Instalar Dependencias
```bash
pip install flask flask-cors requests colorama python-dotenv
```

### 2. Ejecutar la Aplicación
```bash
python web_app.py
```

### 3. Acceder a la Aplicación
Abrir en el navegador: `http://localhost:5000`

## Uso de la Aplicación

### Consultar Ciudad
1. Ingresar el nombre de una ciudad en el campo de búsqueda
2. Hacer clic en "Consultar Información"
3. Ver los resultados organizados por categorías:
   - **Clima**: Temperatura, humedad, condiciones
   - **Noticias**: Artículos tecnológicos recientes
   - **País**: Información demográfica y geográfica

### Diagnóstico del Sistema
1. Hacer clic en "Diagnóstico de APIs"
2. Ver el estado de conexión de cada servicio
3. Identificar posibles problemas de conectividad

## Estructura del Código Web

### Backend (Flask)
```python
# Rutas principales
@app.route('/')                    # Página principal
@app.route('/api/consultar')       # Consulta de información
@app.route('/api/diagnostico')     # Estado de APIs
@app.route('/api/facade-info')     # Info del patrón
```

### Frontend (HTML/JavaScript)
```html
<!-- Elementos principales -->
<input id="ciudadInput">           <!-- Campo de búsqueda -->
<button onclick="consultarCiudad()"> <!-- Botón consultar -->
<div id="resultados">              <!-- Área de resultados -->
<div id="diagnostico">             <!-- Panel de diagnóstico -->
```

## Ventajas del Patrón Facade en la Web

### 1. Simplicidad para el Frontend
```javascript
// Una sola llamada AJAX
fetch('/api/consultar', {
    method: 'POST',
    body: JSON.stringify({ciudad: 'Madrid'}),
    headers: {'Content-Type': 'application/json'}
})
// En lugar de 3 llamadas separadas a diferentes APIs
```

### 2. Manejo Centralizado de Errores
- Errores de API manejados en el backend
- Respuestas consistentes al frontend
- Fallback automático a datos simulados

### 3. Interfaz Unificada
- Formato de respuesta estandarizado
- Estructura de datos coherente
- Fácil mantenimiento y extensión

## Configuración Avanzada

### Variables de Entorno
```bash
# Archivo .env (opcional)
USE_MOCK_DATA=false           # Usar datos reales
ENABLE_FALLBACK=true          # Habilitar fallback
REQUEST_TIMEOUT=10            # Timeout en segundos
DEFAULT_LANGUAGE=es           # Idioma por defecto
```

### Configuración de CORS
```python
# Para desarrollo
CORS(app)

# Para producción
CORS(app, origins=['https://tu-dominio.com'])
```

## Personalización

### Agregar Nueva API
1. Crear proveedor en `src/providers/`
2. Actualizar modelo en `src/models/`
3. Modificar facade en `src/facade/`
4. Actualizar frontend para mostrar nuevos datos

### Modificar Estilos
```css
/* Personalizar en templates/index.html */
.resultado-clima { /* Estilos del clima */ }
.resultado-noticias { /* Estilos de noticias */ }
.resultado-pais { /* Estilos del país */ }
```

## Troubleshooting

### Problemas Comunes

#### 1. Error de CORS
```bash
# Instalar flask-cors
pip install flask-cors
```

#### 2. APIs No Responden
- El sistema usa fallback automático
- Verificar conectividad a internet
- Revisar diagnóstico en `/api/diagnostico`

#### 3. Puerto en Uso
```python
# Cambiar puerto en web_app.py
app.run(debug=True, port=5001)  # Usar puerto 5001
```

## Características Técnicas

### Tecnologías Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos con Bootstrap 5
- **JavaScript**: Funcionalidad interactiva
- **Font Awesome**: Iconografía

### Tecnologías Backend
- **Flask**: Framework web ligero
- **Flask-CORS**: Manejo de CORS
- **Requests**: Llamadas HTTP
- **JSON**: Intercambio de datos

### Características de Seguridad
- Validación de entrada
- Timeout en requests
- Manejo seguro de errores
- Sin exposición de API keys (no se necesitan)

## Monitoreo y Logs

### Logs de Aplicación
```python
# Los logs aparecen en consola
print("Consultando información de:", ciudad)
print("Estado de APIs:", diagnostico)
```

### Métricas Disponibles
- Tiempo de respuesta por API
- Tasa de éxito/fallo
- Uso de fallback
- Ciudades más consultadas

## Despliegue

### Desarrollo Local
```bash
python web_app.py
# Disponible en http://localhost:5000
```

### Producción
```bash
# Usar un servidor WSGI como Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

## Conclusión

Esta aplicación web demuestra efectivamente cómo el patrón Facade simplifica la interacción con múltiples APIs, proporcionando:

- **Interfaz unificada** para el frontend
- **Manejo robusto de errores** y fallbacks
- **Experiencia de usuario** fluida y consistente
- **Arquitectura escalable** y mantenible

El uso de APIs completamente gratuitas hace que el proyecto sea accesible para cualquier desarrollador sin necesidad de registros o configuraciones complejas. 