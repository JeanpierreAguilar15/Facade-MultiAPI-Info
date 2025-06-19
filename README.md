# 🏛️ Patrón Facade - Sistema de Información Multi-API

Este proyecto demuestra la implementación del **Patrón de Diseño Facade** mediante un sistema que unifica el acceso a múltiples APIs de información.

## 🎯 Problemática

Imagina que necesitas obtener información completa sobre una ciudad:
- **Clima actual** (OpenWeatherMap API)
- **Noticias locales** (NewsAPI)
- **Información del país** (REST Countries API)

Cada API tiene:
- Diferentes URLs y endpoints
- Distintos formatos de autenticación
- Estructuras de respuesta diferentes
- Manejo de errores específico

## 🏗️ Solución con Facade

La **FachadaInformacionCiudad** proporciona una interfaz unificada:

```python
# En lugar de manejar 3 APIs diferentes...
facade = FachadaInformacionCiudad()
info = facade.obtener_informacion_completa("Madrid")

# Obtienes todo en un solo objeto estructurado
print(info.clima.temperatura)
print(info.noticias[0].titulo)
print(info.pais.poblacion)
```

## 🔄 Características

- ✅ **APIs Reales**: Consume APIs de producción
- ✅ **Fallback Inteligente**: Si falla una API, usa datos simulados
- ✅ **Interfaz Unificada**: Una sola clase para todo
- ✅ **Manejo de Errores**: Centralizado y consistente
- ✅ **Configuración Flexible**: Variables de entorno para API keys

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/Facade-MultiAPI-Info.git
cd Facade-MultiAPI-Info

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (opcional)
cp .env.example .env
# Editar .env con tus API keys
```

## 🎮 Uso

### Uso Básico
```python
from src.facade.informacion_facade import FachadaInformacionCiudad

facade = FachadaInformacionCiudad()
info = facade.obtener_informacion_completa("Barcelona")
facade.mostrar_resumen(info)
```

### Ejecutar Demo
```bash
python ejemplos/demo_completo.py
```

## 📁 Estructura del Proyecto

```
Facade-MultiAPI-Info/
├── src/
│   ├── facade/
│   │   └── informacion_facade.py     # 🏛️ Clase principal Facade
│   ├── providers/
│   │   ├── clima_provider.py         # 🌤️ Proveedor de clima
│   │   ├── noticias_provider.py      # 📰 Proveedor de noticias
│   │   └── pais_provider.py          # 🌍 Proveedor de países
│   ├── models/
│   │   └── informacion_models.py     # 📊 Modelos de datos
│   └── utils/
│       ├── config.py                 # ⚙️ Configuración
│       └── mock_data.py              # 🎭 Datos de simulación
├── ejemplos/
│   ├── demo_completo.py              # 🎮 Demo principal
│   └── demo_individual.py            # 🔧 Test de cada proveedor
├── tests/
│   └── test_facade.py                # 🧪 Tests unitarios
├── .env.example                      # 📝 Ejemplo de configuración
├── requirements.txt                  # 📦 Dependencias
└── README.md                         # 📚 Documentación
```

## 🔑 APIs Utilizadas

1. **OpenWeatherMap** - Información climática
2. **NewsAPI** - Noticias por país/región  
3. **REST Countries** - Datos de países

## 🎨 Patrón Facade en Acción

### Sin Facade (Complejo)
```python
# Desarrollador debe conocer 3 APIs diferentes
import requests

# API 1: Clima
weather_response = requests.get(
    "http://api.openweathermap.org/data/2.5/weather",
    params={"q": "Madrid", "appid": "tu_api_key", "units": "metric"}
)
weather_data = weather_response.json()

# API 2: Noticias  
news_response = requests.get(
    "https://newsapi.org/v2/everything",
    headers={"X-API-Key": "tu_news_key"},
    params={"q": "Madrid", "language": "es"}
)
news_data = news_response.json()

# API 3: País
country_response = requests.get("https://restcountries.com/v3.1/name/Spain")
country_data = country_response.json()

# Procesar cada respuesta diferente...
```

### Con Facade (Simple)
```python
facade = FachadaInformacionCiudad()
info = facade.obtener_informacion_completa("Madrid")
# ¡Todo listo para usar!
```

## 🧪 Testing

```bash
python -m pytest tests/
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

MIT License - ver archivo LICENSE para detalles. 