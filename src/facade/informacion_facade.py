"""
🏛️ FACHADA PRINCIPAL - Patrón Facade

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
    🏛️ FACADE - Interfaz unificada para obtener información completa de ciudades
    
    Esta clase encapsula la complejidad de trabajar con múltiples APIs:
    - OpenWeatherMap (clima)
    - NewsAPI (noticias)  
    - REST Countries (información de países)
    
    El cliente solo necesita conocer esta clase, no los detalles de cada API.
    """
    
    def __init__(self):
        """Inicializa todos los proveedores internos"""
        print(f"{Fore.CYAN}🏛️  Inicializando Fachada de Información...{Style.RESET_ALL}")
        
        # Crear instancias de todos los proveedores
        self.clima_provider = ClimaProvider()
        self.noticias_provider = NoticiasProvider()
        self.pais_provider = PaisProvider()
        
        print(f"{Fore.GREEN}✅ Fachada lista para usar{Style.RESET_ALL}")
    
    def obtener_informacion_completa(self, ciudad: str) -> InformacionCompleta:
        """
        🎯 MÉTODO PRINCIPAL DEL FACADE
        
        Obtiene toda la información disponible sobre una ciudad en una sola llamada.
        Internamente coordina las llamadas a múltiples APIs y maneja errores.
        
        Args:
            ciudad: Nombre de la ciudad a consultar
            
        Returns:
            InformacionCompleta: Objeto con toda la información agregada
        """
        print(f"\n{Fore.YELLOW}🔍 Obteniendo información completa de: {ciudad}{Style.RESET_ALL}")
        print("=" * 60)
        
        # Crear objeto resultado
        resultado = InformacionCompleta(ciudad_consultada=ciudad)
        
        # Determinar país basado en la ciudad
        pais = self.pais_provider.obtener_pais_por_ciudad(ciudad)
        
        # 1. Obtener información climática
        print(f"\n{Fore.BLUE}🌤️  PASO 1: Obteniendo clima...{Style.RESET_ALL}")
        try:
            resultado.clima = self.clima_provider.obtener_clima(ciudad)
            if resultado.clima:
                print(f"{Fore.GREEN}✅ Clima obtenido: {resultado.clima.temperatura}°C{Style.RESET_ALL}")
            else:
                resultado.errores.append("No se pudo obtener información climática")
                print(f"{Fore.RED}❌ Error obteniendo clima{Style.RESET_ALL}")
        except Exception as e:
            resultado.errores.append(f"Error clima: {str(e)}")
            print(f"{Fore.RED}❌ Error clima: {str(e)}{Style.RESET_ALL}")
        
        # 2. Obtener noticias
        print(f"\n{Fore.BLUE}📰 PASO 2: Obteniendo noticias...{Style.RESET_ALL}")
        try:
            resultado.noticias = self.noticias_provider.obtener_noticias(ciudad, pais)
            if resultado.noticias:
                print(f"{Fore.GREEN}✅ Noticias obtenidas: {len(resultado.noticias.noticias)} artículos{Style.RESET_ALL}")
            else:
                resultado.errores.append("No se pudieron obtener noticias")
                print(f"{Fore.RED}❌ Error obteniendo noticias{Style.RESET_ALL}")
        except Exception as e:
            resultado.errores.append(f"Error noticias: {str(e)}")
            print(f"{Fore.RED}❌ Error noticias: {str(e)}{Style.RESET_ALL}")
        
        # 3. Obtener información del país
        print(f"\n{Fore.BLUE}🌍 PASO 3: Obteniendo información del país...{Style.RESET_ALL}")
        try:
            resultado.pais = self.pais_provider.obtener_info_pais(pais)
            if resultado.pais:
                print(f"{Fore.GREEN}✅ País obtenido: {resultado.pais.nombre_comun}{Style.RESET_ALL}")
            else:
                resultado.errores.append("No se pudo obtener información del país")
                print(f"{Fore.RED}❌ Error obteniendo información del país{Style.RESET_ALL}")
        except Exception as e:
            resultado.errores.append(f"Error país: {str(e)}")
            print(f"{Fore.RED}❌ Error país: {str(e)}{Style.RESET_ALL}")
        
        # Resumen final
        print(f"\n{Fore.CYAN}📊 RESUMEN:{Style.RESET_ALL}")
        info_disponible = resultado.informacion_disponible()
        print(f"   Información obtenida: {', '.join(info_disponible) if info_disponible else 'Ninguna'}")
        
        if resultado.tiene_errores():
            print(f"{Fore.YELLOW}⚠️  Se encontraron {len(resultado.errores)} errores{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}🎉 ¡Información completa obtenida exitosamente!{Style.RESET_ALL}")
        
        return resultado
    
    def mostrar_resumen(self, informacion: InformacionCompleta):
        """
        Muestra un resumen bonito de toda la información obtenida
        
        Args:
            informacion: Objeto InformacionCompleta a mostrar
        """
        print(f"\n{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}🏛️  RESUMEN COMPLETO - {informacion.ciudad_consultada.upper()}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
        
        # Mostrar clima
        if informacion.clima:
            print(f"\n{Fore.CYAN}🌤️  CLIMA:{Style.RESET_ALL}")
            print(f"   📍 Ciudad: {informacion.clima.ciudad}, {informacion.clima.pais}")
            print(f"   🌡️  Temperatura: {informacion.clima.temperatura}°C (se siente como {informacion.clima.sensacion_termica}°C)")
            print(f"   ☁️  Condición: {informacion.clima.descripcion}")
            print(f"   💧 Humedad: {informacion.clima.humedad}%")
            if informacion.clima.presion:
                print(f"   📊 Presión: {informacion.clima.presion} hPa")
        
        # Mostrar información del país
        if informacion.pais:
            print(f"\n{Fore.GREEN}🌍 PAÍS:{Style.RESET_ALL}")
            print(f"   {informacion.pais.bandera_emoji} Nombre: {informacion.pais.nombre_comun}")
            print(f"   🏛️  Nombre oficial: {informacion.pais.nombre_oficial}")
            print(f"   🏙️  Capital: {', '.join(informacion.pais.capital)}")
            print(f"   👥 Población: {informacion.pais.poblacion:,} habitantes")
            print(f"   📐 Área: {informacion.pais.area:,} km²")
            print(f"   🗣️  Idiomas: {', '.join(informacion.pais.idiomas)}")
            print(f"   💰 Monedas: {', '.join(informacion.pais.monedas)}")
        
        # Mostrar noticias
        if informacion.noticias and informacion.noticias.noticias:
            print(f"\n{Fore.YELLOW}📰 NOTICIAS RECIENTES ({informacion.noticias.total_resultados}):{Style.RESET_ALL}")
            for i, noticia in enumerate(informacion.noticias.noticias[:3], 1):  # Mostrar solo las primeras 3
                print(f"\n   {i}. {Fore.WHITE}{noticia.titulo}{Style.RESET_ALL}")
                print(f"      📅 Fuente: {noticia.fuente}")
                if noticia.descripcion:
                    descripcion_corta = noticia.descripcion[:100] + "..." if len(noticia.descripcion) > 100 else noticia.descripcion
                    print(f"      📝 {descripcion_corta}")
        
        # Mostrar errores si los hay
        if informacion.tiene_errores():
            print(f"\n{Fore.RED}⚠️  ERRORES ENCONTRADOS:{Style.RESET_ALL}")
            for error in informacion.errores:
                print(f"   • {error}")
        
        print(f"\n{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⏰ Consulta realizada: {informacion.timestamp.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
    
    def verificar_estado_apis(self):
        """
        Verifica el estado de conexión de todas las APIs
        Útil para diagnóstico
        """
        print(f"\n{Fore.CYAN}🔧 VERIFICANDO ESTADO DE LAS APIs...{Style.RESET_ALL}")
        print("-" * 50)
        
        # Mostrar configuración
        Config.mostrar_configuracion()
        
        print(f"\n{Fore.CYAN}🌐 Estado de conexiones:{Style.RESET_ALL}")
        
        # Verificar cada API
        apis = [
            ("Clima (OpenWeatherMap)", self.clima_provider.verificar_conexion()),
            ("Noticias (NewsAPI)", self.noticias_provider.verificar_conexion()),
            ("Países (REST Countries)", self.pais_provider.verificar_conexion())
        ]
        
        for nombre, estado in apis:
            icono = "✅" if estado else "❌"
            color = Fore.GREEN if estado else Fore.RED
            print(f"   {icono} {color}{nombre}: {'Disponible' if estado else 'No disponible'}{Style.RESET_ALL}")
    
    def obtener_solo_clima(self, ciudad: str) -> Optional:
        """Método de conveniencia para obtener solo información climática"""
        return self.clima_provider.obtener_clima(ciudad)
    
    def obtener_solo_noticias(self, ciudad: str, pais: str = None) -> Optional:
        """Método de conveniencia para obtener solo noticias"""
        if not pais:
            pais = self.pais_provider.obtener_pais_por_ciudad(ciudad)
        return self.noticias_provider.obtener_noticias(ciudad, pais)
    
    def obtener_solo_pais(self, pais: str) -> Optional:
        """Método de conveniencia para obtener solo información del país"""
        return self.pais_provider.obtener_info_pais(pais) 