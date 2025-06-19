#!/usr/bin/env python3
"""
🔧 DEMO INDIVIDUAL - Proveedores por Separado

Este archivo demuestra cómo funcionan los proveedores individuales,
mostrando la complejidad que el Facade oculta al cliente.
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.providers.clima_provider import ClimaProvider
from src.providers.noticias_provider import NoticiasProvider
from src.providers.pais_provider import PaisProvider
from colorama import init, Fore, Style

# Inicializar colorama
init()


def test_clima_provider():
    """Prueba el proveedor de clima individualmente"""
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🌤️  PROVEEDOR DE CLIMA (Individual){Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    # El desarrollador debe conocer esta clase específica
    clima_provider = ClimaProvider()
    
    ciudad = "Madrid"
    print(f"🔍 Consultando clima de {ciudad}...")
    
    # Debe conocer el método específico de esta clase
    clima = clima_provider.obtener_clima(ciudad)
    
    if clima:
        print(f"{Fore.GREEN}✅ Clima obtenido:{Style.RESET_ALL}")
        print(f"   📍 {clima.ciudad}, {clima.pais}")
        print(f"   🌡️  {clima.temperatura}°C ({clima.descripcion})")
        print(f"   💧 Humedad: {clima.humedad}%")
    else:
        print(f"{Fore.RED}❌ No se pudo obtener el clima{Style.RESET_ALL}")


def test_noticias_provider():
    """Prueba el proveedor de noticias individualmente"""
    print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📰 PROVEEDOR DE NOTICIAS (Individual){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    
    # El desarrollador debe conocer esta clase específica
    noticias_provider = NoticiasProvider()
    
    ciudad = "Madrid"
    pais = "España"
    print(f"🔍 Consultando noticias de {ciudad}, {pais}...")
    
    # Debe conocer el método específico y sus parámetros
    noticias = noticias_provider.obtener_noticias(ciudad, pais)
    
    if noticias:
        print(f"{Fore.GREEN}✅ Noticias obtenidas:{Style.RESET_ALL}")
        print(f"   📊 Total: {noticias.total_resultados} noticias")
        print(f"   🌍 País: {noticias.pais_consultado}")
        
        for i, noticia in enumerate(noticias.noticias[:2], 1):
            print(f"\n   {i}. {noticia.titulo[:50]}...")
            print(f"      📅 {noticia.fuente}")
    else:
        print(f"{Fore.RED}❌ No se pudieron obtener noticias{Style.RESET_ALL}")


def test_pais_provider():
    """Prueba el proveedor de países individualmente"""
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🌍 PROVEEDOR DE PAÍSES (Individual){Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    
    # El desarrollador debe conocer esta clase específica
    pais_provider = PaisProvider()
    
    pais = "Spain"
    print(f"🔍 Consultando información de {pais}...")
    
    # Debe conocer el método específico
    info_pais = pais_provider.obtener_info_pais(pais)
    
    if info_pais:
        print(f"{Fore.GREEN}✅ Información del país obtenida:{Style.RESET_ALL}")
        print(f"   {info_pais.bandera_emoji} {info_pais.nombre_comun}")
        print(f"   🏛️  {info_pais.nombre_oficial}")
        print(f"   🏙️  Capital: {', '.join(info_pais.capital)}")
        print(f"   👥 Población: {info_pais.poblacion:,}")
        print(f"   💰 Monedas: {', '.join(info_pais.monedas)}")
    else:
        print(f"{Fore.RED}❌ No se pudo obtener información del país{Style.RESET_ALL}")


def demo_sin_facade():
    """Demuestra cómo sería usar los 3 proveedores sin Facade"""
    print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.RED}❌ USANDO MÚLTIPLES PROVEEDORES SIN FACADE{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}El desarrollador debe:{Style.RESET_ALL}")
    print("1. 🧠 Conocer 3 clases diferentes")
    print("2. 🔧 Instanciar cada proveedor por separado")
    print("3. 📞 Llamar métodos específicos de cada uno")
    print("4. 🔄 Coordinar las llamadas manualmente")
    print("5. ⚠️  Manejar errores de cada uno por separado")
    
    ciudad = "Barcelona"
    
    # ❌ CÓDIGO COMPLEJO SIN FACADE
    print(f"\n{Fore.RED}Código sin Facade (complejo):{Style.RESET_ALL}")
    
    # 1. Instanciar cada proveedor (el cliente debe conocer las 3 clases)
    clima_provider = ClimaProvider()
    noticias_provider = NoticiasProvider()
    pais_provider = PaisProvider()
    
    # 2. El cliente debe saber cómo determinar el país
    pais = pais_provider.obtener_pais_por_ciudad(ciudad)
    
    # 3. Hacer 3 llamadas separadas (el cliente debe coordinar)
    print(f"\n{Fore.RED}Código sin Facade (complejo):{Style.RESET_ALL}")
    print(f"🔧 Instanciando 3 proveedores...")
    print(f"📞 Haciendo 3 llamadas separadas para {ciudad}...")
    
    clima = clima_provider.obtener_clima(ciudad)
    noticias = noticias_provider.obtener_noticias(ciudad, pais)
    info_pais = pais_provider.obtener_info_pais(pais)
    
    # 4. El cliente debe procesar cada resultado por separado
    print(f"\n{Fore.YELLOW}Resultados obtenidos por separado:{Style.RESET_ALL}")
    if clima:
        print(f"   🌤️  Clima: {clima.temperatura}°C")
    if noticias:
        print(f"   📰 Noticias: {len(noticias.noticias)} artículos")
    if info_pais:
        print(f"   🌍 País: {info_pais.nombre_comun}")
    
    print(f"\n{Fore.RED}❌ Problemas de este enfoque:{Style.RESET_ALL}")
    print("   • Alto acoplamiento con clases específicas")
    print("   • Cliente debe conocer detalles de implementación")
    print("   • Código repetitivo para cada consulta")
    print("   • Difícil de mantener si cambian las APIs")
    print("   • Cliente debe manejar errores de cada proveedor")


def comparar_con_facade():
    """Compara el uso individual vs Facade"""
    print(f"\n{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ COMPARACIÓN CON FACADE{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}Con Facade (simple):{Style.RESET_ALL}")
    
    # ✅ CÓDIGO SIMPLE CON FACADE
    from src.facade.informacion_facade import FachadaInformacionCiudad
    
    # 1. Una sola clase para conocer
    facade = FachadaInformacionCiudad()
    
    # 2. Una sola llamada
    print(f"🏛️  Usando Facade...")
    info = facade.obtener_informacion_completa("Barcelona")
    
    # 3. Resultado estructurado y completo
    print(f"\n{Fore.GREEN}✅ Ventajas del Facade:{Style.RESET_ALL}")
    print("   • Una sola interfaz para todo")
    print("   • Cliente desacoplado de proveedores específicos")
    print("   • Manejo centralizado de errores")
    print("   • Código más limpio y mantenible")
    print("   • Fácil agregar nuevos proveedores")
    
    print(f"\n{Fore.CYAN}📊 Resultado con Facade:{Style.RESET_ALL}")
    if info.clima:
        print(f"   🌤️  {info.clima.temperatura}°C - {info.clima.descripcion}")
    if info.noticias:
        print(f"   📰 {len(info.noticias.noticias)} noticias")
    if info.pais:
        print(f"   🌍 {info.pais.bandera_emoji} {info.pais.nombre_comun}")


def main():
    """Función principal"""
    print(f"{Fore.MAGENTA}🔧 DEMO PROVEEDORES INDIVIDUALES{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Mostrando la complejidad que Facade oculta{Style.RESET_ALL}")
    
    try:
        # Probar cada proveedor individualmente
        test_clima_provider()
        test_noticias_provider()
        test_pais_provider()
        
        # Demostrar la complejidad sin Facade
        demo_sin_facade()
        
        # Comparar con Facade
        comparar_con_facade()
        
        print(f"\n{Fore.GREEN}🎯 CONCLUSIÓN:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}El patrón Facade simplifica significativamente el uso de múltiples subsistemas complejos.{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 