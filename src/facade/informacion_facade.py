"""
FACHADA PRINCIPAL - Patrón Facade

Esta es la clase principal que implementa el patrón Facade.
Proporciona una interfaz simplificada para acceder a múltiples APIs
de información (clima, noticias, países) sin que el cliente necesite
conocer los detalles de implementación de cada una.
"""
from typing import Optional
from colorama import init, Fore, Style
from ..models.informacion_models import InformacionCompleta
from ..providers.clima_provider import ClimaProvider
from ..providers.noticias_provider import NoticiasProvider
from ..providers.pais_provider import PaisProvider
from ..utils.config import Config

# Inicializar colorama para colores en consola
init()


class FachadaInformacionCiudad:
    """
    FACADE - Interfaz unificada para obtener información completa de ciudades
    
    Esta clase encapsula la complejidad de trabajar con múltiples APIs:
    - Open-Meteo (clima) - Completamente gratuita
    - FreeNewsAPI (noticias) - Completamente gratuita
    - REST Countries (información de países) - Completamente gratuita
    
    El cliente solo necesita conocer esta clase, no los detalles de cada API.
    """
    
    def __init__(self):
        """Inicializa todos los proveedores internos"""
        print("Inicializando Fachada de Información...")
        
        # Crear instancias de todos los proveedores
        self.clima_provider = ClimaProvider()
        self.noticias_provider = NoticiasProvider()
        self.pais_provider = PaisProvider()
        
        print("Fachada lista para usar")
    
    def obtener_informacion_completa(self, ciudad: str) -> InformacionCompleta:
        """
        MÉTODO PRINCIPAL DEL FACADE
        
        Obtiene toda la información disponible sobre una ciudad en una sola llamada.
        Internamente coordina las llamadas a múltiples APIs y maneja errores.
        
        Args:
            ciudad: Nombre de la ciudad a consultar
            
        Returns:
            InformacionCompleta: Objeto con toda la información agregada
        """
        print(f"\nObteniendo información completa de: {ciudad}")
        print("=" * 60)
        
        # Crear objeto resultado
        resultado = InformacionCompleta(ciudad_consultada=ciudad)
        
        # Determinar país basado en la ciudad
        pais = self.pais_provider.obtener_pais_por_ciudad(ciudad)
        
        # 1. Obtener información climática
        print(f"\nPASO 1: Obteniendo clima...")
        try:
            resultado.clima = self.clima_provider.obtener_clima(ciudad)
            if resultado.clima:
                print(f"Clima obtenido: {resultado.clima.temperatura}°C")
            else:
                resultado.errores.append("No se pudo obtener información climática")
                print("Error obteniendo clima")
        except Exception as e:
            resultado.errores.append(f"Error clima: {str(e)}")
            print(f"Error clima: {str(e)}")
        
        # 2. Obtener noticias
        print(f"\nPASO 2: Obteniendo noticias...")
        try:
            resultado.noticias = self.noticias_provider.obtener_noticias(pais)
            if resultado.noticias:
                print(f"Noticias obtenidas: {len(resultado.noticias.noticias)} artículos")
            else:
                resultado.errores.append("No se pudieron obtener noticias")
                print("Error obteniendo noticias")
        except Exception as e:
            resultado.errores.append(f"Error noticias: {str(e)}")
            print(f"Error noticias: {str(e)}")
        
        # 3. Obtener información del país
        print(f"\nPASO 3: Obteniendo información del país...")
        try:
            resultado.pais = self.pais_provider.obtener_info_pais(pais)
            if resultado.pais:
                print(f"País obtenido: {resultado.pais.nombre_comun}")
            else:
                resultado.errores.append("No se pudo obtener información del país")
                print("Error obteniendo información del país")
        except Exception as e:
            resultado.errores.append(f"Error país: {str(e)}")
            print(f"Error país: {str(e)}")
        
        # Resumen final
        print(f"\nRESUMEN:")
        info_disponible = resultado.informacion_disponible()
        print(f"   Información obtenida: {', '.join(info_disponible) if info_disponible else 'Ninguna'}")
        
        if resultado.tiene_errores():
            print(f"Se encontraron {len(resultado.errores)} errores")
        else:
            print("¡Información completa obtenida exitosamente!")
        
        return resultado
    
    def mostrar_resumen(self, informacion: InformacionCompleta):
        """
        Muestra un resumen bonito de toda la información obtenida
        
        Args:
            informacion: Objeto InformacionCompleta a mostrar
        """
        print(f"\n{'='*80}")
        print(f"RESUMEN COMPLETO - {informacion.ciudad_consultada.upper()}")
        print(f"{'='*80}")
        
        # Mostrar clima
        if informacion.clima:
            print(f"\nCLIMA:")
            print(f"   Ciudad: {informacion.clima.ciudad}, {informacion.clima.pais}")
            print(f"   Temperatura: {informacion.clima.temperatura}°C (se siente como {informacion.clima.sensacion_termica}°C)")
            print(f"   Condición: {informacion.clima.descripcion}")
            print(f"   Humedad: {informacion.clima.humedad}%")
            if informacion.clima.presion:
                print(f"   Presión: {informacion.clima.presion} hPa")
        
        # Mostrar información del país
        if informacion.pais:
            print(f"\nPAÍS:")
            print(f"   {informacion.pais.bandera_emoji} Nombre: {informacion.pais.nombre_comun}")
            print(f"   Nombre oficial: {informacion.pais.nombre_oficial}")
            print(f"   Capital: {', '.join(informacion.pais.capital)}")
            print(f"   Población: {informacion.pais.poblacion:,} habitantes")
            print(f"   Área: {informacion.pais.area:,} km²")
            print(f"   Idiomas: {', '.join(informacion.pais.idiomas)}")
            print(f"   Monedas: {', '.join(informacion.pais.monedas)}")
        
        # Mostrar noticias
        if informacion.noticias and informacion.noticias.noticias:
            print(f"\nNOTICIAS RECIENTES ({informacion.noticias.total_resultados}):")
            for i, noticia in enumerate(informacion.noticias.noticias[:3], 1):  # Mostrar solo las primeras 3
                print(f"\n   {i}. {noticia.titulo}")
                print(f"      Fuente: {noticia.fuente}")
                if noticia.descripcion:
                    descripcion_corta = noticia.descripcion[:100] + "..." if len(noticia.descripcion) > 100 else noticia.descripcion
                    print(f"      {descripcion_corta}")
        
        # Mostrar errores si los hay
        if informacion.tiene_errores():
            print(f"\nERRORES ENCONTRADOS:")
            for error in informacion.errores:
                print(f"   • {error}")
        
        print(f"\n{'='*80}")
        print(f"Consulta realizada: {informacion.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def verificar_estado_apis(self):
        """
        Verifica el estado de conexión de todas las APIs
        Útil para diagnóstico
        """
        print(f"\nVERIFICANDO ESTADO DE LAS APIs...")
        print("-" * 50)
        
        # Mostrar configuración
        Config.mostrar_configuracion()
        
        print(f"\nEstado de conexiones:")
        
        # Verificar cada API
        apis = [
            ("Clima (Open-Meteo)", self.clima_provider.verificar_conexion()),
            ("Noticias (FreeNewsAPI)", self.noticias_provider.verificar_conexion()),
            ("Países (REST Countries)", self.pais_provider.verificar_conexion())
        ]
        
        for nombre, estado in apis:
            icono = "[OK]" if estado else "[ERROR]"
            print(f"   {icono} {nombre}: {'Disponible' if estado else 'No disponible'}")
    
    def obtener_solo_clima(self, ciudad: str) -> Optional:
        """Método de conveniencia para obtener solo información climática"""
        return self.clima_provider.obtener_clima(ciudad)
    
    def obtener_solo_noticias(self, pais: str) -> Optional:
        """Método de conveniencia para obtener solo noticias"""
        return self.noticias_provider.obtener_noticias(pais)
    
    def obtener_solo_pais(self, pais: str) -> Optional:
        """Método de conveniencia para obtener solo información del país"""
        return self.pais_provider.obtener_info_pais(pais) 