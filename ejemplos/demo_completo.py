#!/usr/bin/env python3
"""
🎮 DEMO COMPLETO - Patrón Facade en Acción

Este archivo demuestra cómo usar la Fachada para obtener información
completa de ciudades sin conocer los detalles de las APIs individuales.
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.facade.informacion_facade import FachadaInformacionCiudad
from colorama import init, Fore, Style

# Inicializar colorama
init()


def demo_basico():
    """Demostración básica del patrón Facade"""
    print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}🎮 DEMO BÁSICO - Patrón Facade{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
    
    # Crear la fachada (interfaz unificada)
    facade = FachadaInformacionCiudad()
    
    # UNA SOLA LLAMADA obtiene información de múltiples APIs
    ciudad = "Madrid"
    informacion = facade.obtener_informacion_completa(ciudad)
    
    # Mostrar resultados de forma bonita
    facade.mostrar_resumen(informacion)


def demo_multiples_ciudades():
    """Demuestra el uso con múltiples ciudades"""
    print(f"\n{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}🌍 DEMO MÚLTIPLES CIUDADES{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
    
    facade = FachadaInformacionCiudad()
    
    ciudades = ["Barcelona", "México", "Buenos Aires"]
    
    for ciudad in ciudades:
        print(f"\n{Fore.CYAN}🏙️  Consultando: {ciudad}{Style.RESET_ALL}")
        informacion = facade.obtener_informacion_completa(ciudad)
        
        # Mostrar solo un resumen corto
        print(f"\n{Fore.YELLOW}📋 Resumen de {ciudad}:{Style.RESET_ALL}")
        if informacion.clima:
            print(f"   🌤️  {informacion.clima.temperatura}°C - {informacion.clima.descripcion}")
        if informacion.pais:
            print(f"   🌍 {informacion.pais.bandera_emoji} {informacion.pais.nombre_comun}")
        if informacion.noticias:
            print(f"   📰 {len(informacion.noticias.noticias)} noticias disponibles")
        
        print("-" * 40)


def demo_comparacion_sin_facade():
    """Muestra cómo sería SIN usar el patrón Facade"""
    print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.RED}❌ EJEMPLO SIN FACADE (Complejo){Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}Sin Facade, el desarrollador tendría que:{Style.RESET_ALL}")
    print("1. 🔧 Conocer y configurar 3 APIs diferentes")
    print("2. 🔑 Manejar diferentes sistemas de autenticación")
    print("3. 📊 Procesar 3 formatos de respuesta diferentes")
    print("4. ⚠️  Manejar errores de cada API por separado")
    print("5. 🔄 Implementar fallbacks manualmente")
    
    codigo_sin_facade = '''
# Sin Facade - Código complejo y acoplado
import requests

# API 1: Clima (OpenWeatherMap)
weather_response = requests.get(
    "http://api.openweathermap.org/data/2.5/weather",
    params={"q": "Madrid", "appid": "tu_api_key", "units": "metric"}
)
if weather_response.status_code == 200:
    weather_data = weather_response.json()
    temperatura = weather_data['main']['temp']
    # ... procesar respuesta específica de OpenWeatherMap

# API 2: Noticias (NewsAPI)  
news_response = requests.get(
    "https://newsapi.org/v2/everything",
    headers={"X-API-Key": "tu_news_key"},
    params={"q": "Madrid", "language": "es"}
)
if news_response.status_code == 200:
    news_data = news_response.json()
    # ... procesar respuesta específica de NewsAPI

# API 3: País (REST Countries)
country_response = requests.get("https://restcountries.com/v3.1/name/Spain")
if country_response.status_code == 200:
    country_data = country_response.json()[0]
    # ... procesar respuesta específica de REST Countries

# ¡Y esto es solo para UNA ciudad!
'''
    
    print(f"\n{Fore.RED}Código sin Facade:{Style.RESET_ALL}")
    print(codigo_sin_facade)
    
    print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ CON FACADE (Simple){Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
    
    codigo_con_facade = '''
# Con Facade - Código simple y desacoplado
from src.facade.informacion_facade import FachadaInformacionCiudad

facade = FachadaInformacionCiudad()
info = facade.obtener_informacion_completa("Madrid")

# ¡Listo! Toda la información en un objeto estructurado
print(f"Temperatura: {info.clima.temperatura}°C")
print(f"País: {info.pais.nombre_comun}")
print(f"Noticias: {len(info.noticias.noticias)}")
'''
    
    print(f"{Fore.GREEN}Código con Facade:{Style.RESET_ALL}")
    print(codigo_con_facade)


def demo_diagnostico():
    """Demuestra las funciones de diagnóstico"""
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🔧 DEMO DIAGNÓSTICO{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    facade = FachadaInformacionCiudad()
    facade.verificar_estado_apis()


def demo_interactivo():
    """Demo interactivo donde el usuario puede consultar ciudades"""
    print(f"\n{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}🎯 DEMO INTERACTIVO{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
    
    facade = FachadaInformacionCiudad()
    
    print(f"{Fore.YELLOW}¡Consulta información de cualquier ciudad!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Ejemplos: Madrid, Barcelona, México, Buenos Aires, Lima{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Escribe 'salir' para terminar{Style.RESET_ALL}\n")
    
    while True:
        try:
            ciudad = input(f"{Fore.GREEN}🏙️  ¿Qué ciudad quieres consultar? {Style.RESET_ALL}").strip()
            
            if ciudad.lower() in ['salir', 'exit', 'quit', '']:
                print(f"{Fore.YELLOW}¡Hasta luego! 👋{Style.RESET_ALL}")
                break
            
            informacion = facade.obtener_informacion_completa(ciudad)
            facade.mostrar_resumen(informacion)
            
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}¡Hasta luego! 👋{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")


def main():
    """Función principal que ejecuta todos los demos"""
    print(f"{Fore.CYAN}🏛️  DEMOSTRACIÓN DEL PATRÓN FACADE{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Sistema de Información Multi-API{Style.RESET_ALL}")
    
    try:
        # 1. Demo básico
        demo_basico()
        
        # 2. Demo múltiples ciudades
        demo_multiples_ciudades()
        
        # 3. Comparación sin facade
        demo_comparacion_sin_facade()
        
        # 4. Diagnóstico
        demo_diagnostico()
        
        # 5. Demo interactivo (opcional)
        print(f"\n{Fore.YELLOW}¿Quieres probar el demo interactivo? (s/n): {Style.RESET_ALL}", end="")
        respuesta = input().strip().lower()
        
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            demo_interactivo()
        
        print(f"\n{Fore.GREEN}🎉 ¡Demo completado! El patrón Facade simplifica el acceso a múltiples APIs.{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error en el demo: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 