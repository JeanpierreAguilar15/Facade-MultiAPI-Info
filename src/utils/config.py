"""
Configuración centralizada para el proyecto
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Config:
    """Configuración centralizada del proyecto"""
    
    # URLs de las APIs (todas gratuitas)
    OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    OPEN_METEO_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
    HACKER_NEWS_API_BASE_URL = "https://hacker-news.firebaseio.com/v0"
    COUNTRIES_API_BASE_URL = "https://restcountries.com/v3.1/name"
    
    # Configuración general
    USE_MOCK_DATA = os.getenv('USE_MOCK_DATA', 'false').lower() == 'true'
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'es')
    DEFAULT_UNITS = os.getenv('DEFAULT_UNITS', 'metric')
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))
    
    # Configuración de fallback
    ENABLE_FALLBACK = os.getenv('ENABLE_FALLBACK', 'true').lower() == 'true'
    
    # Configuración de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def mostrar_configuracion(cls):
        """Muestra la configuración actual"""
        print("CONFIGURACIÓN ACTUAL:")
        print(f"   Usar datos simulados: {'Sí' if cls.USE_MOCK_DATA else 'No'}")
        print(f"   Idioma por defecto: {cls.DEFAULT_LANGUAGE}")
        print(f"   Unidades: {cls.DEFAULT_UNITS}")
        print(f"   Timeout peticiones: {cls.REQUEST_TIMEOUT}s")
        print(f"   Fallback habilitado: {'Sí' if cls.ENABLE_FALLBACK else 'No'}")
        print(f"   APIs utilizadas:")
        print(f"      - Clima: Open-Meteo (gratuita)")
        print(f"      - Noticias: Hacker News (gratuita)")
        print(f"      - Países: REST Countries (gratuita)")
    
    @classmethod
    def usar_datos_simulados(cls):
        """Activa el modo de datos simulados"""
        cls.USE_MOCK_DATA = True
        print("Modo datos simulados activado")
    
    @classmethod
    def usar_datos_reales(cls):
        """Activa el modo de datos reales"""
        cls.USE_MOCK_DATA = False
        print("Modo datos reales activado")
    
    @classmethod
    def alternar_fallback(cls):
        """Alterna el estado del fallback"""
        cls.ENABLE_FALLBACK = not cls.ENABLE_FALLBACK
        estado = "activado" if cls.ENABLE_FALLBACK else "desactivado"
        print(f"Fallback {estado}")
    
    @classmethod
    def get_status_apis(cls):
        """Devuelve el estado de las APIs utilizadas"""
        return {
            "clima": {
                "api": "Open-Meteo",
                "url": cls.OPEN_METEO_WEATHER_URL,
                "gratuita": True,
                "requiere_api_key": False,
                "descripcion": "API completamente gratuita de meteorología"
            },
            "noticias": {
                "api": "Hacker News",
                "url": cls.HACKER_NEWS_API_BASE_URL,
                "gratuita": True,
                "requiere_api_key": False,
                "descripcion": "API gratuita de noticias tecnológicas"
            },
            "paises": {
                "api": "REST Countries",
                "url": cls.COUNTRIES_API_BASE_URL,
                "gratuita": True,
                "requiere_api_key": False,
                "descripcion": "API gratuita de información de países"
            }
        } 