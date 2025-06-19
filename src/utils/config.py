"""
Configuración centralizada para el proyecto
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Config:
    """Configuración centralizada del proyecto"""
    
    # API Keys
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    
    # URLs de las APIs
    OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"
    COUNTRIES_API_BASE_URL = "https://restcountries.com/v3.1/name"
    
    # Configuración general
    USE_MOCK_DATA = os.getenv('USE_MOCK_DATA', 'false').lower() == 'true'
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'es')
    DEFAULT_UNITS = os.getenv('DEFAULT_UNITS', 'metric')
    REQUEST_TIMEOUT = 10  # segundos
    
    # Configuración de fallback
    ENABLE_FALLBACK = True
    MAX_RETRIES = 2
    
    @classmethod
    def tiene_api_keys(cls) -> bool:
        """Verifica si se tienen las API keys configuradas"""
        return bool(cls.OPENWEATHER_API_KEY and cls.NEWS_API_KEY)
    
    @classmethod
    def mostrar_configuracion(cls):
        """Muestra la configuración actual (sin mostrar las API keys completas)"""
        print("🔧 Configuración actual:")
        print(f"   OpenWeather API: {'✅ Configurada' if cls.OPENWEATHER_API_KEY else '❌ No configurada'}")
        print(f"   News API: {'✅ Configurada' if cls.NEWS_API_KEY else '❌ No configurada'}")
        print(f"   Usar datos simulados: {'✅ Sí' if cls.USE_MOCK_DATA else '❌ No'}")
        print(f"   Idioma por defecto: {cls.DEFAULT_LANGUAGE}")
        print(f"   Unidades: {cls.DEFAULT_UNITS}")
        print(f"   Fallback habilitado: {'✅ Sí' if cls.ENABLE_FALLBACK else '❌ No'}") 