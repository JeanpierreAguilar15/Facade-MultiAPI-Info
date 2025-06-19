"""
Proveedor para obtener información de países de REST Countries API
"""
import requests
from typing import Optional
from ..models.informacion_models import InformacionPais
from ..utils.config import Config
from ..utils.mock_data import MockDataProvider


class PaisProvider:
    """Proveedor de información de países"""
    
    def __init__(self):
        self.base_url = Config.COUNTRIES_API_BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
        
    def obtener_info_pais(self, pais: str) -> Optional[InformacionPais]:
        """
        Obtiene información de un país
        
        Args:
            pais: Nombre del país
            
        Returns:
            InformacionPais o None si hay error
        """
        # Si está configurado para usar mock, usar simulación
        if Config.USE_MOCK_DATA:
            print(f"🎭 Usando información simulada del país {pais}")
            return self._procesar_respuesta_pais(
                MockDataProvider.get_pais_mock(pais)[0]
            )
        
        try:
            # Intentar obtener datos reales
            print(f"🌍 Consultando información real del país {pais}...")
            respuesta = self._hacer_peticion_pais(pais)
            
            if respuesta and len(respuesta) > 0:
                return self._procesar_respuesta_pais(respuesta[0])
            else:
                # Fallback a datos simulados
                if Config.ENABLE_FALLBACK:
                    print(f"⚠️  API de países falló, usando datos simulados para {pais}")
                    return self._procesar_respuesta_pais(
                        MockDataProvider.get_pais_mock(pais)[0]
                    )
                
        except Exception as e:
            print(f"❌ Error obteniendo información del país: {str(e)}")
            
            # Fallback a datos simulados
            if Config.ENABLE_FALLBACK:
                print(f"🎭 Usando información simulada como fallback para {pais}")
                return self._procesar_respuesta_pais(
                    MockDataProvider.get_pais_mock(pais)[0]
                )
        
        return None
    
    def _hacer_peticion_pais(self, pais: str) -> Optional[list]:
        """Hace la petición HTTP a la API de países"""
        url = f"{self.base_url}/{pais}"
        
        respuesta = requests.get(url, timeout=self.timeout)
        
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            print(f"❌ Error API países: {respuesta.status_code} - {respuesta.text}")
            return None
    
    def _procesar_respuesta_pais(self, data: dict) -> InformacionPais:
        """Procesa la respuesta de la API y crea el objeto InformacionPais"""
        try:
            # Extraer idiomas
            idiomas = []
            if 'languages' in data:
                idiomas = list(data['languages'].values())
            
            # Extraer monedas
            monedas = []
            if 'currencies' in data:
                for currency_info in data['currencies'].values():
                    moneda_texto = currency_info.get('name', '')
                    simbolo = currency_info.get('symbol', '')
                    if simbolo:
                        moneda_texto += f" ({simbolo})"
                    monedas.append(moneda_texto)
            
            return InformacionPais(
                nombre_comun=data['name']['common'],
                nombre_oficial=data['name']['official'],
                capital=data.get('capital', ['N/A']),
                poblacion=data.get('population', 0),
                area=data.get('area', 0.0),
                region=data.get('region', 'N/A'),
                subregion=data.get('subregion', 'N/A'),
                idiomas=idiomas,
                monedas=monedas,
                codigo_pais=data.get('cca2', 'XX'),
                bandera_emoji=data.get('flag', '🏳️')
            )
            
        except KeyError as e:
            print(f"❌ Error procesando datos del país: {str(e)}")
            raise
    
    def obtener_pais_por_ciudad(self, ciudad: str) -> str:
        """
        Intenta determinar el país basado en el nombre de la ciudad
        Es una aproximación simple, en un proyecto real usarías una API de geocoding
        """
        ciudades_paises = {
            'madrid': 'Spain',
            'barcelona': 'Spain',
            'valencia': 'Spain',
            'sevilla': 'Spain',
            'bilbao': 'Spain',
            'zaragoza': 'Spain',
            'malaga': 'Spain',
            'palma': 'Spain',
            'las palmas': 'Spain',
            'murcia': 'Spain',
            'mexico': 'Mexico',
            'ciudad de mexico': 'Mexico',
            'guadalajara': 'Mexico',
            'monterrey': 'Mexico',
            'puebla': 'Mexico',
            'tijuana': 'Mexico',
            'bogota': 'Colombia',
            'medellin': 'Colombia',
            'cali': 'Colombia',
            'buenos aires': 'Argentina',
            'cordoba': 'Argentina',
            'rosario': 'Argentina',
            'lima': 'Peru',
            'santiago': 'Chile',
            'caracas': 'Venezuela',
            'quito': 'Ecuador',
            'la paz': 'Bolivia',
            'montevideo': 'Uruguay',
            'asuncion': 'Paraguay'
        }
        
        ciudad_lower = ciudad.lower()
        return ciudades_paises.get(ciudad_lower, 'Spain')  # Default a España
    
    def verificar_conexion(self) -> bool:
        """Verifica si la API está disponible"""
        try:
            respuesta = requests.get(
                f"{self.base_url}/Spain",
                timeout=5
            )
            return respuesta.status_code == 200
        except:
            return False 