#!/usr/bin/env python3
"""
INICIO RÁPIDO - Patrón Facade para Múltiples APIs

Este script demuestra el uso del patrón Facade para acceder
a información de múltiples APIs de forma simplificada.

APIs utilizadas (todas gratuitas):
- Open-Meteo: Información climática
- FreeNewsAPI: Noticias actuales
- REST Countries: Información de países
"""

import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.facade.informacion_facade import FachadaInformacionCiudad
from src.utils.config import Config


def main():
    """Función principal del script de demostración"""
    print("=" * 80)
    print("PATRÓN FACADE - DEMO DE MÚLTIPLES APIs")
    print("=" * 80)
    print()
    print("Este proyecto demuestra el patrón Facade accediendo a:")
    print("- Open-Meteo (clima) - Completamente gratuita")
    print("- FreeNewsAPI (noticias) - Completamente gratuita") 
    print("- REST Countries (países) - Completamente gratuita")
    print()
    print("VENTAJAS DEL PATRÓN FACADE:")
    print("• Interfaz simplificada para múltiples sistemas complejos")
    print("• El cliente no necesita conocer detalles de cada API")
    print("• Manejo centralizado de errores y fallbacks")
    print("• Fácil mantenimiento y extensión")
    print()
    
    # Crear instancia de la fachada
    print("Inicializando Facade...")
    facade = FachadaInformacionCiudad()
    
    # Mostrar configuración actual
    print("\n" + "=" * 60)
    print("CONFIGURACIÓN DEL SISTEMA")
    print("=" * 60)
    facade.verificar_estado_apis()
    
    # Lista de ciudades para probar
    ciudades_prueba = [
        "Madrid",
        "Londres", 
        "Nueva York",
        "París"
    ]
    
    print("\n" + "=" * 60)
    print("DEMOSTRACIONES")
    print("=" * 60)
    
    for i, ciudad in enumerate(ciudades_prueba, 1):
        print(f"\n[DEMO {i}] Consultando información de {ciudad}")
        print("-" * 50)
        
        try:
            # Usar el Facade para obtener toda la información
            informacion = facade.obtener_informacion_completa(ciudad)
            
            # Mostrar resumen
            facade.mostrar_resumen(informacion)
            
            # Pausa entre consultas
            if i < len(ciudades_prueba):
                input("\nPresiona Enter para continuar con la siguiente ciudad...")
                
        except Exception as e:
            print(f"Error en la demostración: {str(e)}")
            continue
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETADA")
    print("=" * 80)
    print()
    print("BENEFICIOS OBSERVADOS:")
    print("• Una sola llamada obtiene información de múltiples fuentes")
    print("• Manejo automático de errores y fallbacks")
    print("• Interfaz consistente independientemente de las APIs subyacentes")
    print("• Fácil extensión para agregar nuevas fuentes de datos")
    print()
    print("El patrón Facade simplifica significativamente el acceso")
    print("a sistemas complejos y heterogéneos.")
    print()


def demo_individual():
    """Demostración de métodos individuales del Facade"""
    print("\n" + "=" * 60)
    print("DEMO DE MÉTODOS INDIVIDUALES")
    print("=" * 60)
    
    facade = FachadaInformacionCiudad()
    ciudad = "Barcelona"
    
    print(f"\nConsultando información individual de {ciudad}:")
    
    # Solo clima
    print(f"\n1. Solo clima:")
    clima = facade.obtener_solo_clima(ciudad)
    if clima:
        print(f"   Temperatura: {clima.temperatura}°C")
        print(f"   Condición: {clima.descripcion}")
    
    # Solo noticias (por país)
    print(f"\n2. Solo noticias de España:")
    noticias = facade.obtener_solo_noticias("España")
    if noticias and noticias.noticias:
        print(f"   Encontradas: {len(noticias.noticias)} noticias")
        print(f"   Primera: {noticias.noticias[0].titulo[:60]}...")
    
    # Solo país
    print(f"\n3. Solo información del país:")
    pais = facade.obtener_solo_pais("España")
    if pais:
        print(f"   País: {pais.nombre_comun}")
        print(f"   Capital: {', '.join(pais.capital)}")
        print(f"   Población: {pais.poblacion:,}")


if __name__ == "__main__":
    try:
        main()
        
        # Preguntar si quiere ver demo individual
        respuesta = input("\n¿Quieres ver la demo de métodos individuales? (s/n): ")
        if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            demo_individual()
            
    except KeyboardInterrupt:
        print("\n\nDemo interrumpida por el usuario.")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        print("Revisa la configuración y las dependencias.")
    
    print("\nGracias por probar el patrón Facade!") 