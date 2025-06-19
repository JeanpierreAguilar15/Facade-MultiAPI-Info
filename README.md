# Patrón de Diseño Facade - Acceso a Múltiples APIs

Este proyecto implementa el **patrón de diseño Facade** para demostrar cómo simplificar el acceso a múltiples APIs de servicios externos mediante una interfaz unificada.

## Descripción del Proyecto

El sistema consulta información completa de ciudades combinando datos de **tres APIs completamente gratuitas**:

- **Open-Meteo API**: Información meteorológica (temperatura, humedad, condiciones)
- **Hacker News API**: Noticias tecnológicas y de startups más populares
- **REST Countries API**: Información detallada de países (población, idiomas, monedas)

## Patrón Facade Implementado

### Problema que Resuelve
Sin el patrón Facade, el cliente tendría que:
```python
# Código complejo sin Facade
clima_provider = ClimaProvider()
noticias_provider = NoticiasProvider() 
pais_provider = PaisProvider()

# Múltiples llamadas y manejo de errores
try:
    clima = clima_provider.obtener_clima("Madrid")
    noticias = noticias_provider.obtener_noticias("ES")
    pais = pais_provider.obtener_pais("Spain")
    # Coordinar resultados manualmente...
except Exception as e:
    # Manejar errores de cada API por separado...
```

### Solución con Facade
```python
# Código simple con Facade
facade = FachadaInformacionCiudad()
informacion = facade.obtener_informacion_completa("Madrid")
# ¡Una sola llamada para todo!
```

## APIs Utilizadas (Todas Gratuitas)

### 1. Open-Meteo - Información Meteorológica
- **URL**: https://open-meteo.com/
- **Características**: Completamente gratuita, sin registro, sin API key
- **Datos**: Temperatura, humedad, presión, condiciones climáticas

### 2. Hacker News API - Noticias Tecnológicas  
- **URL**: https://hacker-news.firebaseio.com/
- **Características**: Completamente gratuita, sin registro, sin límites
- **Datos**: Noticias más populares sobre tecnología y startups

### 3. REST Countries - Información de Países
- **URL**: https://restcountries.com/
- **Características**: Completamente gratuita, sin límites
- **Datos**: Población, capital, idiomas, monedas, banderas

## Estructura del Proyecto

```
Arquitectura_Facade/
├── src/
│   ├── facade/
│   │   └── informacion_facade.py      # Clase principal Facade
│   ├── providers/
│   │   ├── clima_provider.py          # Proveedor Open-Meteo
│   │   ├── noticias_provider.py       # Proveedor Hacker News
│   │   └── pais_provider.py           # Proveedor REST Countries
│   ├── models/
│   │   └── informacion_models.py      # Modelos de datos
│   └── utils/
│       ├── config.py                  # Configuración
│       └── mock_data.py               # Datos simulados (fallback)
├── ejemplos/
│   ├── demo_completo.py               # Demo completa
│   └── demo_individual.py             # Demo de cada proveedor
├── tests/
│   └── test_facade.py                 # Tests unitarios
├── templates/
│   └── index.html                     # Interfaz web
├── inicio_rapido.py                   # Script de demostración
├── web_app.py                         # Aplicación web Flask
├── requirements.txt                   # Dependencias
└── README.md                          # Este archivo
```

## Instalación y Uso

### 1. Clonar el Repositorio
```bash
git clone https://github.com/TU_USUARIO/Facade-MultiAPI-Info.git
cd Facade-MultiAPI-Info
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar Demo Rápida
```bash
python inicio_rapido.py
```

### 4. Ejecutar Aplicación Web
```bash
python web_app.py
```
Luego abre http://localhost:5000 en tu navegador.

## Ejemplos de Uso

### Uso Básico del Facade
```python
from src.facade.informacion_facade import FachadaInformacionCiudad

# Crear instancia del Facade
facade = FachadaInformacionCiudad()

# Obtener información completa con una sola llamada
info = facade.obtener_informacion_completa("Barcelona")

# Acceder a los datos
print(f"Temperatura: {info.clima.temperatura}°C")
print(f"País: {info.pais.nombre_comun}")
print(f"Noticias: {len(info.noticias.noticias)} artículos")
```

### Uso de Proveedores Individuales
```python
from src.providers.clima_provider import ClimaProvider

# Usar proveedor individual
clima_provider = ClimaProvider()
clima = clima_provider.obtener_clima("Madrid")
print(f"Temperatura en Madrid: {clima.temperatura}°C")
```

## Características Técnicas

### Manejo de Errores Robusto
- **Fallback inteligente**: Si una API falla, usa datos simulados
- **Timeout configurables**: Evita bloqueos por APIs lentas
- **Logging detallado**: Para debugging y monitoreo

### Configuración Flexible
```python
# Configuración en src/utils/config.py
USE_MOCK_DATA = False          # Usar datos reales por defecto
ENABLE_FALLBACK = True         # Habilitar fallback a datos simulados
REQUEST_TIMEOUT = 10           # Timeout en segundos
```

### Sistema de Fallback
Si las APIs externas fallan, el sistema automáticamente usa datos simulados realistas para mantener la funcionalidad.

## Ejecutar Tests

```bash
python -m pytest tests/ -v
```

## Interfaz Web

La aplicación incluye una interfaz web moderna con:
- Búsqueda de ciudades en tiempo real
- Visualización de clima, noticias y datos del país
- Diagnóstico del estado de las APIs
- Interfaz responsive con Bootstrap 5

## Beneficios del Patrón Facade

1. **Simplicidad**: Una sola interfaz para múltiples sistemas
2. **Desacoplamiento**: El cliente no depende de APIs específicas
3. **Mantenibilidad**: Cambios en APIs no afectan al cliente
4. **Robustez**: Manejo centralizado de errores y fallbacks
5. **Extensibilidad**: Fácil agregar nuevas fuentes de datos

## Tecnologías Utilizadas

- **Python 3.7+**
- **Requests**: Para llamadas HTTP
- **Flask**: Aplicación web
- **Colorama**: Colores en consola
- **Python-dotenv**: Manejo de variables de entorno
- **Pytest**: Testing

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## Contacto

Tu Nombre - tu.email@ejemplo.com

Link del Proyecto: https://github.com/TU_USUARIO/Facade-MultiAPI-Info 