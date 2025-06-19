"""
Proveedor para obtener información climática de Open-Meteo API (gratuita)
"""
import requests
from typing import Optional
from ..models.informacion_models import InformacionClima
from ..utils.config import Config
from ..utils.mock_data import MockDataProvider


class ClimaProvider:
    """Proveedor de información climática usando Open-Meteo (gratuita)"""
    
    def __init__(self):
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
        self.timeout = Config.REQUEST_TIMEOUT
        
    def obtener_clima(self, ciudad: str) -> Optional[InformacionClima]:
        """
        Obtiene información climática de una ciudad usando Open-Meteo
        
        Args:
            ciudad: Nombre de la ciudad
            
        Returns:
            InformacionClima o None si hay error
        """
        # Si está configurado para usar mock, usar simulación
        if Config.USE_MOCK_DATA:
            print(f"Usando datos simulados para clima de {ciudad}")
            return self._procesar_respuesta_clima_mock(
                MockDataProvider.get_clima_mock(ciudad)
            )
        
        try:
            # Intentar obtener datos reales de Open-Meteo
            print(f"Consultando clima real de {ciudad} con Open-Meteo...")
            
            # Paso 1: Obtener coordenadas de la ciudad
            coordenadas = self._obtener_coordenadas(ciudad)
            if not coordenadas:
                return self._usar_fallback(ciudad)
            
            # Paso 2: Obtener datos climáticos
            respuesta = self._hacer_peticion_clima(coordenadas)
            
            if respuesta:
                return self._procesar_respuesta_clima(respuesta, ciudad, coordenadas)
            else:
                return self._usar_fallback(ciudad)
                
        except Exception as e:
            print(f"Error obteniendo clima: {str(e)}")
            return self._usar_fallback(ciudad)
    
    def _obtener_coordenadas(self, ciudad: str) -> Optional[dict]:
        """Obtiene las coordenadas de una ciudad"""
        try:
            parametros = {
                'name': ciudad,
                'count': 1,
                'language': 'es',
                'format': 'json'
            }
            
            respuesta = requests.get(
                self.geocoding_url,
                params=parametros,
                timeout=self.timeout
            )
            
            if respuesta.status_code == 200:
                data = respuesta.json()
                if data.get('results') and len(data['results']) > 0:
                    resultado = data['results'][0]
                    return {
                        'latitude': resultado['latitude'],
                        'longitude': resultado['longitude'],
                        'name': resultado['name'],
                        'country': resultado.get('country', 'N/A')
                    }
            
            print(f"No se encontraron coordenadas para {ciudad}")
            return None
            
        except Exception as e:
            print(f"Error obteniendo coordenadas: {str(e)}")
            return None
    
    def _hacer_peticion_clima(self, coordenadas: dict) -> Optional[dict]:
        """Hace la petición HTTP a la API de clima de Open-Meteo"""
        try:
            parametros = {
                'latitude': coordenadas['latitude'],
                'longitude': coordenadas['longitude'],
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,pressure_msl',
                'timezone': 'auto',
                'forecast_days': 1
            }
            
            respuesta = requests.get(
                self.weather_url,
                params=parametros,
                timeout=self.timeout
            )
            
            if respuesta.status_code == 200:
                return respuesta.json()
            else:
                print(f"Error API clima: {respuesta.status_code}")
                return None
                
        except Exception as e:
            print(f"Error en petición de clima: {str(e)}")
            return None
    
    def _procesar_respuesta_clima(self, data: dict, ciudad: str, coordenadas: dict) -> InformacionClima:
        """Procesa la respuesta de Open-Meteo y crea el objeto InformacionClima"""
        try:
            current = data['current']
            
            # Mapear códigos de clima a descripciones
            weather_code = current.get('weather_code', 0)
            descripcion = self._obtener_descripcion_clima(weather_code)
            
            return InformacionClima(
                temperatura=round(current['temperature_2m'], 1),
                sensacion_termica=round(current['apparent_temperature'], 1),
                humedad=int(current['relative_humidity_2m']),
                descripcion=descripcion,
                ciudad=coordenadas['name'],
                pais=coordenadas['country'],
                icono=self._obtener_icono_clima(weather_code),
                presion=int(current.get('pressure_msl', 0)),
                visibilidad=10000  # Open-Meteo no proporciona visibilidad, valor por defecto
            )
        except KeyError as e:
            print(f"Error procesando datos de clima: {str(e)}")
            raise
    
    def _procesar_respuesta_clima_mock(self, data: dict) -> InformacionClima:
        """Procesa datos simulados para mantener compatibilidad"""
        try:
            return InformacionClima(
                temperatura=round(data['main']['temp'], 1),
                sensacion_termica=round(data['main']['feels_like'], 1),
                humedad=data['main']['humidity'],
                descripcion=data['weather'][0]['description'].title(),
                ciudad=data['name'],
                pais=data['sys'].get('country', 'N/A'),
                icono=data['weather'][0]['icon'],
                presion=data['main'].get('pressure'),
                visibilidad=data.get('visibility')
            )
        except KeyError as e:
            print(f"Error procesando datos simulados: {str(e)}")
            raise
    
    def _obtener_descripcion_clima(self, weather_code: int) -> str:
        """Convierte códigos de clima de Open-Meteo a descripciones"""
        descripciones = {
            0: "Despejado",
            1: "Principalmente despejado",
            2: "Parcialmente nublado",
            3: "Nublado",
            45: "Niebla",
            48: "Niebla con escarcha",
            51: "Llovizna ligera",
            53: "Llovizna moderada",
            55: "Llovizna intensa",
            61: "Lluvia ligera",
            63: "Lluvia moderada",
            65: "Lluvia intensa",
            71: "Nieve ligera",
            73: "Nieve moderada",
            75: "Nieve intensa",
            95: "Tormenta",
            96: "Tormenta con granizo ligero",
            99: "Tormenta con granizo intenso"
        }
        return descripciones.get(weather_code, "Condiciones variables")
    
    def _obtener_icono_clima(self, weather_code: int) -> str:
        """Convierte códigos de clima a iconos compatibles"""
        iconos = {
            0: "01d",    # Despejado
            1: "02d",    # Principalmente despejado
            2: "03d",    # Parcialmente nublado
            3: "04d",    # Nublado
            45: "50d",   # Niebla
            48: "50d",   # Niebla con escarcha
            51: "09d",   # Llovizna ligera
            53: "09d",   # Llovizna moderada
            55: "09d",   # Llovizna intensa
            61: "10d",   # Lluvia ligera
            63: "10d",   # Lluvia moderada
            65: "10d",   # Lluvia intensa
            71: "13d",   # Nieve ligera
            73: "13d",   # Nieve moderada
            75: "13d",   # Nieve intensa
            95: "11d",   # Tormenta
            96: "11d",   # Tormenta con granizo
            99: "11d"    # Tormenta con granizo intenso
        }
        return iconos.get(weather_code, "01d")
    
    def _usar_fallback(self, ciudad: str) -> Optional[InformacionClima]:
        """Usa datos simulados como fallback"""
        if Config.ENABLE_FALLBACK:
            print(f"API de clima falló, usando datos simulados para {ciudad}")
            return self._procesar_respuesta_clima_mock(
                MockDataProvider.get_clima_mock(ciudad)
            )
        return None
    
    def verificar_conexion(self) -> bool:
        """Verifica si la API está disponible"""
        try:
            respuesta = requests.get(
                self.geocoding_url,
                params={'name': 'Madrid', 'count': 1},
                timeout=5
            )
            return respuesta.status_code == 200
        except:
            return False 