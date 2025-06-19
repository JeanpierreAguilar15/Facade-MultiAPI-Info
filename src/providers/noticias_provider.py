"""
Proveedor para obtener noticias de NewsAPI
"""
import requests
from typing import Optional
from ..models.informacion_models import InformacionNoticias, Noticia
from ..utils.config import Config
from ..utils.mock_data import MockDataProvider


class NoticiasProvider:
    """Proveedor de noticias"""
    
    def __init__(self):
        self.api_key = Config.NEWS_API_KEY
        self.base_url = Config.NEWS_API_BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
        
    def obtener_noticias(self, ciudad: str, pais: str = "España") -> Optional[InformacionNoticias]:
        """
        Obtiene noticias relacionadas con una ciudad/país
        
        Args:
            ciudad: Nombre de la ciudad
            pais: Nombre del país
            
        Returns:
            InformacionNoticias o None si hay error
        """
        # Si está configurado para usar mock o no hay API key, usar simulación
        if Config.USE_MOCK_DATA or not self.api_key:
            print(f"🎭 Usando noticias simuladas para {pais}")
            return self._procesar_respuesta_noticias(
                MockDataProvider.get_noticias_mock(pais), pais
            )
        
        try:
            # Intentar obtener noticias reales
            print(f"📰 Consultando noticias reales de {pais}...")
            respuesta = self._hacer_peticion_noticias(ciudad, pais)
            
            if respuesta:
                return self._procesar_respuesta_noticias(respuesta, pais)
            else:
                # Fallback a datos simulados
                if Config.ENABLE_FALLBACK:
                    print(f"⚠️  API de noticias falló, usando datos simulados para {pais}")
                    return self._procesar_respuesta_noticias(
                        MockDataProvider.get_noticias_mock(pais), pais
                    )
                
        except Exception as e:
            print(f"❌ Error obteniendo noticias: {str(e)}")
            
            # Fallback a datos simulados
            if Config.ENABLE_FALLBACK:
                print(f"🎭 Usando noticias simuladas como fallback para {pais}")
                return self._procesar_respuesta_noticias(
                    MockDataProvider.get_noticias_mock(pais), pais
                )
        
        return None
    
    def _hacer_peticion_noticias(self, ciudad: str, pais: str) -> Optional[dict]:
        """Hace la petición HTTP a la API de noticias"""
        # Buscar noticias por ciudad y país
        query = f"{ciudad} OR {pais}"
        
        parametros = {
            'q': query,
            'language': Config.DEFAULT_LANGUAGE,
            'sortBy': 'publishedAt',
            'pageSize': 5  # Limitar a 5 noticias
        }
        
        headers = {
            'X-API-Key': self.api_key
        }
        
        respuesta = requests.get(
            self.base_url,
            params=parametros,
            headers=headers,
            timeout=self.timeout
        )
        
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            print(f"❌ Error API noticias: {respuesta.status_code} - {respuesta.text}")
            return None
    
    def _procesar_respuesta_noticias(self, data: dict, pais: str) -> InformacionNoticias:
        """Procesa la respuesta de la API y crea el objeto InformacionNoticias"""
        try:
            noticias_lista = []
            
            for articulo in data.get('articles', [])[:5]:  # Máximo 5 noticias
                if articulo.get('title') and articulo.get('description'):
                    noticia = Noticia(
                        titulo=articulo['title'],
                        descripcion=articulo['description'] or "Sin descripción disponible",
                        url=articulo.get('url', ''),
                        fuente=articulo.get('source', {}).get('name', 'Fuente desconocida'),
                        fecha_publicacion=articulo.get('publishedAt'),
                        imagen_url=articulo.get('urlToImage')
                    )
                    noticias_lista.append(noticia)
            
            return InformacionNoticias(
                noticias=noticias_lista,
                total_resultados=len(noticias_lista),
                pais_consultado=pais
            )
            
        except Exception as e:
            print(f"❌ Error procesando noticias: {str(e)}")
            raise
    
    def verificar_conexion(self) -> bool:
        """Verifica si la API está disponible"""
        if not self.api_key:
            return False
            
        try:
            headers = {'X-API-Key': self.api_key}
            respuesta = requests.get(
                self.base_url,
                params={'q': 'test', 'pageSize': 1},
                headers=headers,
                timeout=5
            )
            return respuesta.status_code == 200
        except:
            return False 