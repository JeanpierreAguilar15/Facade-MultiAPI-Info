"""
Proveedor para obtener noticias de Hacker News API (completamente gratuita)
"""
import requests
from typing import Optional, List, Dict, Any
from ..models.informacion_models import InformacionNoticias, Noticia
from ..utils.config import Config
from ..utils.mock_data import MockDataProvider


class NoticiasProvider:
    """Proveedor de noticias usando Hacker News API (completamente gratuita)"""
    
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"
        self.timeout = Config.REQUEST_TIMEOUT
        
    def obtener_noticias(self, pais: str) -> Optional[InformacionNoticias]:
        """
        Obtiene noticias de Hacker News API
        
        Args:
            pais: Código del país (se usa para personalizar el tipo de noticias)
            
        Returns:
            InformacionNoticias con las noticias obtenidas o None si falla
        """
        try:
            print(f"Obteniendo noticias reales de Hacker News...")
            
            # Obtener las mejores historias
            top_stories_url = f"{self.base_url}/topstories.json"
            response = requests.get(top_stories_url, timeout=self.timeout)
            response.raise_for_status()
            
            story_ids = response.json()[:10]  # Obtener las primeras 10 historias
            
            noticias = []
            for story_id in story_ids:
                try:
                    # Obtener detalles de cada historia
                    story_url = f"{self.base_url}/item/{story_id}.json"
                    story_response = requests.get(story_url, timeout=self.timeout)
                    story_response.raise_for_status()
                    
                    story_data = story_response.json()
                    
                    # Verificar que la historia tenga los campos necesarios
                    if not story_data or story_data.get('type') != 'story':
                        continue
                        
                    # Crear objeto Noticia
                    noticia = Noticia(
                        titulo=story_data.get('title', 'Sin título'),
                        descripcion=story_data.get('text', 'Historia de Hacker News')[:200] + "..." if story_data.get('text') else f"Historia sobre tecnología y startup - {story_data.get('score', 0)} puntos",
                        url=story_data.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        fuente="Hacker News",
                        fecha_publicacion=str(story_data.get('time', ''))
                    )
                    noticias.append(noticia)
                    
                except Exception as e:
                    print(f"Error obteniendo historia {story_id}: {e}")
                    continue
            
            if noticias:
                print(f"[OK] Noticias obtenidas: {len(noticias)} artículos de Hacker News")
                return InformacionNoticias(
                    pais=pais,
                    total_resultados=len(noticias),
                    noticias=noticias,
                    fuente_api="Hacker News API"
                )
            else:
                raise Exception("No se pudieron obtener noticias")
                
        except Exception as e:
            print(f"[ERROR] Error obteniendo noticias de Hacker News: {e}")
            return self._usar_datos_simulados(pais)
    
    def _usar_datos_simulados(self, pais: str) -> InformacionNoticias:
        """Fallback a datos simulados si la API falla"""
        print("Usando noticias simuladas para", pais)
        mock_provider = MockDataProvider()
        return mock_provider.obtener_noticias_simuladas(pais)

    def verificar_conexion(self) -> bool:
        """Verifica si la API está disponible"""
        try:
            respuesta = requests.get(
                f"{self.base_url}/topstories.json",
                timeout=5
            )
            return respuesta.status_code == 200
        except:
            return False 