"""
Proveedor para obtener información climática de OpenWeatherMap API
"""
import requests
from typing import Optional
from ..models.informacion_models import InformacionClima
from ..utils.config import Config
from ..utils.mock_data import MockDataProvider


class ClimaProvider:
    """Proveedor de información climática"""
    
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = Config.OPENWEATHER_BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
        
    def obtener_clima(self, ciudad: str) -> Optional[InformacionClima]:
        """
        Obtiene información climática de una ciudad
        
        Args:
            ciudad: Nombre de la ciudad
            
        Returns:
            InformacionClima o None si hay error
        """
        # Si está configurado para usar mock o no hay API key, usar simulación
        if Config.USE_MOCK_DATA or not self.api_key:
            print(f"🎭 Usando datos simulados para clima de {ciudad}")
            return self._procesar_respuesta_clima(
                MockDataProvider.get_clima_mock(ciudad)
            )
        
        try:
            # Intentar obtener datos reales
            print(f"🌤️  Consultando clima real de {ciudad}...")
            respuesta = self._hacer_peticion_clima(ciudad)
            
            if respuesta:
                return self._procesar_respuesta_clima(respuesta)
            else:
                # Fallback a datos simulados
                if Config.ENABLE_FALLBACK:
                    print(f"⚠️  API de clima falló, usando datos simulados para {ciudad}")
                    return self._procesar_respuesta_clima(
                        MockDataProvider.get_clima_mock(ciudad)
                    )
                
        except Exception as e:
            print(f"❌ Error obteniendo clima: {str(e)}")
            
            # Fallback a datos simulados
            if Config.ENABLE_FALLBACK:
                print(f"🎭 Usando datos simulados como fallback para {ciudad}")
                return self._procesar_respuesta_clima(
                    MockDataProvider.get_clima_mock(ciudad)
                )
        
        return None
    
    def _hacer_peticion_clima(self, ciudad: str) -> Optional[dict]:
        """Hace la petición HTTP a la API de clima"""
        parametros = {
            'q': ciudad,
            'appid': self.api_key,
            'units': Config.DEFAULT_UNITS,
            'lang': Config.DEFAULT_LANGUAGE
        }
        
        respuesta = requests.get(
            self.base_url,
            params=parametros,
            timeout=self.timeout
        )
        
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            print(f"❌ Error API clima: {respuesta.status_code} - {respuesta.text}")
            return None
    
    def _procesar_respuesta_clima(self, data: dict) -> InformacionClima:
        """Procesa la respuesta de la API y crea el objeto InformacionClima"""
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
            print(f"❌ Error procesando datos de clima: {str(e)}")
            raise
    
    def verificar_conexion(self) -> bool:
        """Verifica si la API está disponible"""
        if not self.api_key:
            return False
            
        try:
            respuesta = requests.get(
                self.base_url,
                params={'q': 'Madrid', 'appid': self.api_key},
                timeout=5
            )
            return respuesta.status_code == 200
        except:
            return False 