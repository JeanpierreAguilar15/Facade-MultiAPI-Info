"""
Datos simulados para usar como fallback cuando las APIs no están disponibles
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any


class MockDataProvider:
    """Proveedor de datos simulados para todas las APIs"""
    
    @staticmethod
    def get_clima_mock(ciudad: str) -> Dict[str, Any]:
        """Genera datos de clima simulados"""
        temperaturas_base = {
            'madrid': 18, 'barcelona': 20, 'valencia': 22, 'sevilla': 25,
            'bilbao': 15, 'zaragoza': 17, 'malaga': 24, 'palma': 23,
            'las palmas': 26, 'murcia': 21, 'mexico': 20, 'bogota': 16,
            'buenos aires': 19, 'lima': 18, 'santiago': 17, 'caracas': 28,
            'quito': 15, 'la paz': 12, 'montevideo': 18, 'asuncion': 26
        }
        
        ciudad_lower = ciudad.lower()
        temp_base = temperaturas_base.get(ciudad_lower, random.randint(10, 30))
        
        # Añadir variación aleatoria
        temperatura = temp_base + random.randint(-5, 5)
        
        descripciones = [
            "cielo despejado", "pocas nubes", "nubes dispersas", 
            "muy nuboso", "lluvia ligera", "soleado"
        ]
        
        iconos = ["01d", "02d", "03d", "04d", "09d", "01d"]
        
        return {
            "main": {
                "temp": temperatura,
                "feels_like": temperatura + random.randint(-3, 3),
                "humidity": random.randint(40, 80),
                "pressure": random.randint(1000, 1020)
            },
            "weather": [{
                "description": random.choice(descripciones),
                "icon": random.choice(iconos)
            }],
            "name": ciudad.title(),
            "sys": {"country": "ES"},
            "visibility": random.randint(5000, 10000)
        }
    
    @staticmethod
    def get_noticias_mock(pais: str = "España") -> Dict[str, Any]:
        """Genera noticias simuladas"""
        noticias_templates = [
            {
                "title": f"Nuevas inversiones en tecnología llegan a {pais}",
                "description": f"El sector tecnológico de {pais} recibe una importante inyección de capital para proyectos innovadores.",
                "source": {"name": "TechNews"},
                "url": "https://example.com/tech-news-1",
                "urlToImage": "https://via.placeholder.com/400x200"
            },
            {
                "title": f"Crecimiento económico sostenido en {pais}",
                "description": f"Los indicadores económicos de {pais} muestran una tendencia positiva en el último trimestre.",
                "source": {"name": "EconomíaHoy"},
                "url": "https://example.com/economia-news-1",
                "urlToImage": "https://via.placeholder.com/400x200"
            },
            {
                "title": f"Nuevo proyecto de infraestructura en {pais}",
                "description": f"Se anuncia una importante obra de infraestructura que beneficiará a varias regiones de {pais}.",
                "source": {"name": "InfraNews"},
                "url": "https://example.com/infra-news-1",
                "urlToImage": "https://via.placeholder.com/400x200"
            },
            {
                "title": f"Avances en energías renovables en {pais}",
                "description": f"{pais} continúa su apuesta por las energías limpias con nuevos parques solares y eólicos.",
                "source": {"name": "EnergyToday"},
                "url": "https://example.com/energy-news-1",
                "urlToImage": "https://via.placeholder.com/400x200"
            },
            {
                "title": f"Innovación educativa en {pais}",
                "description": f"Las universidades de {pais} implementan nuevos programas de formación digital.",
                "source": {"name": "EduNews"},
                "url": "https://example.com/edu-news-1",
                "urlToImage": "https://via.placeholder.com/400x200"
            }
        ]
        
        # Seleccionar 3-5 noticias aleatorias
        noticias_seleccionadas = random.sample(noticias_templates, random.randint(3, 5))
        
        # Añadir fechas recientes
        for noticia in noticias_seleccionadas:
            dias_atras = random.randint(0, 7)
            fecha = datetime.now() - timedelta(days=dias_atras)
            noticia["publishedAt"] = fecha.isoformat()
        
        return {
            "status": "ok",
            "totalResults": len(noticias_seleccionadas),
            "articles": noticias_seleccionadas
        }
    
    @staticmethod
    def get_pais_mock(pais: str) -> List[Dict[str, Any]]:
        """Genera información de país simulada"""
        paises_data = {
            'spain': {
                "name": {
                    "common": "España",
                    "official": "Reino de España"
                },
                "capital": ["Madrid"],
                "population": 47351567,
                "area": 505992,
                "region": "Europe",
                "subregion": "Southern Europe",
                "languages": {"spa": "Spanish"},
                "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
                "cca2": "ES",
                "flag": "🇪🇸"
            },
            'mexico': {
                "name": {
                    "common": "México",
                    "official": "Estados Unidos Mexicanos"
                },
                "capital": ["Ciudad de México"],
                "population": 128932753,
                "area": 1964375,
                "region": "Americas",
                "subregion": "North America",
                "languages": {"spa": "Spanish"},
                "currencies": {"MXN": {"name": "Mexican peso", "symbol": "$"}},
                "cca2": "MX",
                "flag": "🇲🇽"
            },
            'argentina': {
                "name": {
                    "common": "Argentina",
                    "official": "República Argentina"
                },
                "capital": ["Buenos Aires"],
                "population": 45376763,
                "area": 2780400,
                "region": "Americas",
                "subregion": "South America",
                "languages": {"spa": "Spanish"},
                "currencies": {"ARS": {"name": "Argentine peso", "symbol": "$"}},
                "cca2": "AR",
                "flag": "🇦🇷"
            }
        }
        
        pais_lower = pais.lower()
        
        # Buscar por nombre
        for key, data in paises_data.items():
            if key in pais_lower or pais_lower in data["name"]["common"].lower():
                return [data]
        
        # Si no se encuentra, devolver datos genéricos
        return [{
            "name": {
                "common": pais.title(),
                "official": f"República de {pais.title()}"
            },
            "capital": [f"Capital de {pais.title()}"],
            "population": random.randint(1000000, 50000000),
            "area": random.randint(50000, 2000000),
            "region": "Americas",
            "subregion": "South America",
            "languages": {"spa": "Spanish"},
            "currencies": {"USD": {"name": "US Dollar", "symbol": "$"}},
            "cca2": "XX",
            "flag": "🏳️"
        }] 