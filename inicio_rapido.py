#!/usr/bin/env python3
"""
INICIO RÁPIDO - Patrón Facade

Script para probar rápidamente el proyecto sin configuración adicional.
Usa datos simulados para demostrar el patrón Facade inmediatamente.
"""
import sys
import os

# Añadir el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.facade.informacion_facade import FachadaInformacionCiudad
from colorama import init, Fore, Style

# Inicializar colorama
init()


def main():
    """Demostración rápida del patrón Facade"""
    print(f"{Fore.CYAN}PATRÓN FACADE - INICIO RÁPIDO{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Sistema de Información Multi-API{Style.RESET_ALL}")
    print("=" * 60)
    
    print(f"\n{Fore.YELLOW}Este demo usa datos simulados para mostrar el patrón Facade{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}sin necesidad de configurar APIs reales.{Style.RESET_ALL}\n")
    
    try:
        # Crear la fachada (interfaz unificada)
        print(f"{Fore.BLUE}Inicializando Facade...{Style.RESET_ALL}")
        facade = FachadaInformacionCiudad()
        
        # Demostrar con diferentes ciudades
        ciudades = ["Madrid", "Barcelona", "México"]
        
        for ciudad in ciudades:
            print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}CONSULTANDO: {ciudad.upper()}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
            
            # UNA SOLA LLAMADA obtiene información de múltiples "APIs"
            informacion = facade.obtener_informacion_completa(ciudad)
            
            # Mostrar resumen
            facade.mostrar_resumen(informacion)
            
            if ciudad != ciudades[-1]:  # No pausar en la última ciudad
                input(f"\n{Fore.GREEN}Presiona Enter para continuar con la siguiente ciudad...{Style.RESET_ALL}")
        
        # Mostrar diagnóstico
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}DIAGNÓSTICO DEL SISTEMA{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        facade.verificar_estado_apis()
        
        # Conclusión
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}¡DEMOSTRACIÓN COMPLETADA!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Beneficios del Patrón Facade demostrados:{Style.RESET_ALL}")
        print("   • Una sola interfaz para múltiples APIs complejas")
        print("   • Cliente desacoplado de detalles de implementación")
        print("   • Manejo centralizado de errores y fallbacks")
        print("   • Código limpio y fácil de mantener")
        
        print(f"\n{Fore.CYAN}Para explorar más:{Style.RESET_ALL}")
        print("   • Ejecuta: python ejemplos/demo_completo.py")
        print("   • Ejecuta: python ejemplos/demo_individual.py")
        print("   • Ejecuta: python tests/test_facade.py")
        print("   • Configura APIs reales en .env (opcional)")
        
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 