"""
Modelos de datos para estructurar la información obtenida de las APIs
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class InformacionClima:
    """Modelo para información climática"""
    temperatura: float
    sensacion_termica: float
    humedad: int
    descripcion: str
    ciudad: str
    pais: str
    icono: str
    presion: Optional[int] = None
    visibilidad: Optional[int] = None
    
    def __str__(self):
        return f"{self.ciudad}: {self.temperatura}°C ({self.descripcion})"


@dataclass
class Noticia:
    """Modelo para una noticia individual"""
    titulo: str
    descripcion: str
    url: str
    fuente: str
    fecha_publicacion: Optional[str] = None
    imagen_url: Optional[str] = None
    
    def __str__(self):
        return f"{self.titulo[:50]}... - {self.fuente}"


@dataclass
class InformacionNoticias:
    """Modelo para colección de noticias"""
    noticias: List[Noticia]
    total_resultados: int
    pais: str
    fuente_api: str = "Hacker News API"
    
    def __str__(self):
        return f"{self.total_resultados} noticias de {self.pais}"


@dataclass
class InformacionPais:
    """Modelo para información del país"""
    nombre_comun: str
    nombre_oficial: str
    capital: List[str]
    poblacion: int
    area: float
    region: str
    subregion: str
    idiomas: List[str]
    monedas: List[str]
    codigo_pais: str
    bandera_emoji: str
    
    def __str__(self):
        return f"{self.nombre_comun} - {self.capital[0] if self.capital else 'N/A'}"


@dataclass
class InformacionCompleta:
    """Modelo que agrupa toda la información de una ciudad/país"""
    clima: Optional[InformacionClima] = None
    noticias: Optional[InformacionNoticias] = None
    pais: Optional[InformacionPais] = None
    ciudad_consultada: str = ""
    timestamp: datetime = None
    errores: List[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.errores is None:
            self.errores = []
    
    def tiene_errores(self) -> bool:
        """Verifica si hubo errores al obtener la información"""
        return len(self.errores) > 0
    
    def informacion_disponible(self) -> List[str]:
        """Retorna qué tipos de información están disponibles"""
        disponible = []
        if self.clima:
            disponible.append("clima")
        if self.noticias:
            disponible.append("noticias")
        if self.pais:
            disponible.append("país")
        return disponible
    
    def __str__(self):
        info_tipos = ", ".join(self.informacion_disponible())
        return f"Información de {self.ciudad_consultada}: {info_tipos}" 