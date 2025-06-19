#!/usr/bin/env python3
"""
APLICACIÓN WEB - Patrón Facade

Aplicación Flask que demuestra el patrón Facade mediante una interfaz web moderna.
Permite consultar información de ciudades usando múltiples APIs de forma unificada.
"""
import sys
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

# Añadir el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.facade.informacion_facade import FachadaInformacionCiudad
from src.utils.config import Config

# Crear aplicación Flask
app = Flask(__name__)
CORS(app)  # Permitir CORS para desarrollo

# Instancia global del Facade
facade = FachadaInformacionCiudad()


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/consultar', methods=['POST'])
def consultar_ciudad():
    """
    API endpoint que usa el patrón Facade para obtener información completa
    """
    try:
        data = request.get_json()
        ciudad = data.get('ciudad', '').strip()
        
        if not ciudad:
            return jsonify({
                'success': False,
                'error': 'Por favor ingresa el nombre de una ciudad'
            }), 400
        
        print(f"Consultando información de: {ciudad}")
        
        # AQUÍ ES DONDE SE USA EL PATRÓN FACADE
        # Una sola llamada obtiene información de múltiples APIs
        informacion = facade.obtener_informacion_completa(ciudad)
        
        # Convertir a formato JSON para la respuesta
        resultado = {
            'success': True,
            'ciudad': informacion.ciudad_consultada,
            'timestamp': informacion.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'clima': None,
            'noticias': None,
            'pais': None,
            'errores': informacion.errores,
            'info_disponible': informacion.informacion_disponible()
        }
        
        # Procesar información climática
        if informacion.clima:
            resultado['clima'] = {
                'temperatura': informacion.clima.temperatura,
                'sensacion_termica': informacion.clima.sensacion_termica,
                'humedad': informacion.clima.humedad,
                'descripcion': informacion.clima.descripcion,
                'ciudad': informacion.clima.ciudad,
                'pais': informacion.clima.pais,
                'icono': informacion.clima.icono,
                'presion': informacion.clima.presion
            }
        
        # Procesar noticias
        if informacion.noticias:
            resultado['noticias'] = {
                'total_resultados': informacion.noticias.total_resultados,
                'pais_consultado': informacion.noticias.pais_consultado,
                'articulos': []
            }
            
            for noticia in informacion.noticias.noticias[:5]:  # Máximo 5 noticias
                resultado['noticias']['articulos'].append({
                    'titulo': noticia.titulo,
                    'descripcion': noticia.descripcion,
                    'url': noticia.url,
                    'fuente': noticia.fuente,
                    'fecha_publicacion': noticia.fecha_publicacion
                })
        
        # Procesar información del país
        if informacion.pais:
            resultado['pais'] = {
                'nombre_comun': informacion.pais.nombre_comun,
                'nombre_oficial': informacion.pais.nombre_oficial,
                'capital': informacion.pais.capital,
                'poblacion': informacion.pais.poblacion,
                'area': informacion.pais.area,
                'region': informacion.pais.region,
                'subregion': informacion.pais.subregion,
                'idiomas': informacion.pais.idiomas,
                'monedas': informacion.pais.monedas,
                'codigo_pais': informacion.pais.codigo_pais,
                'bandera_emoji': informacion.pais.bandera_emoji
            }
        
        return jsonify(resultado)
        
    except Exception as e:
        print(f"Error en consulta: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500


@app.route('/api/diagnostico')
def diagnostico():
    """Endpoint para obtener el estado de las APIs"""
    try:
        # Verificar estado de cada proveedor
        estado_apis = {
            'clima': facade.clima_provider.verificar_conexion(),
            'noticias': facade.noticias_provider.verificar_conexion(),
            'pais': facade.pais_provider.verificar_conexion()
        }
        
        # Configuración actual
        configuracion = {
            'tiene_api_keys': Config.tiene_api_keys(),
            'usa_mock_data': Config.USE_MOCK_DATA,
            'idioma': Config.DEFAULT_LANGUAGE,
            'unidades': Config.DEFAULT_UNITS,
            'fallback_habilitado': Config.ENABLE_FALLBACK
        }
        
        return jsonify({
            'success': True,
            'estado_apis': estado_apis,
            'configuracion': configuracion
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/facade-info')
def facade_info():
    """Endpoint que explica el patrón Facade"""
    return jsonify({
        'patron': 'Facade',
        'descripcion': 'Proporciona una interfaz unificada a un conjunto de interfaces en un subsistema',
        'beneficios': [
            'Simplifica el uso de subsistemas complejos',
            'Desacopla el cliente de los subsistemas',
            'Facilita el mantenimiento y evolución',
            'Centraliza el manejo de errores'
        ],
        'implementacion': {
            'facade_class': 'FachadaInformacionCiudad',
            'subsistemas': [
                'ClimaProvider (OpenWeatherMap API)',
                'NoticiasProvider (NewsAPI)',
                'PaisProvider (REST Countries API)'
            ],
            'metodo_principal': 'obtener_informacion_completa()',
            'fallback': 'MockDataProvider (datos simulados)'
        },
        'ejemplo_uso': {
            'sin_facade': [
                'clima_provider = ClimaProvider()',
                'noticias_provider = NoticiasProvider()',
                'pais_provider = PaisProvider()',
                '# 3 llamadas separadas + coordinación manual'
            ],
            'con_facade': [
                'facade = FachadaInformacionCiudad()',
                'info = facade.obtener_informacion_completa("Madrid")',
                '# ¡Una sola llamada para todo!'
            ]
        }
    })


if __name__ == '__main__':
    print("Iniciando aplicación web del patrón Facade...")
    print("Accede a: http://localhost:5000")
    print("Demostrando el patrón Facade con interfaz web moderna")
    
    # Configurar para desarrollo
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    ) 