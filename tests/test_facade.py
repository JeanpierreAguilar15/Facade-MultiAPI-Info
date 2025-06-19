#!/usr/bin/env python3
"""
🧪 TESTS PARA EL PATRÓN FACADE

Tests básicos para verificar el funcionamiento del patrón Facade
"""
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.facade.informacion_facade import FachadaInformacionCiudad
from src.models.informacion_models import InformacionCompleta, InformacionClima, InformacionNoticias, InformacionPais


class TestFachadaInformacionCiudad(unittest.TestCase):
    """Tests para la clase principal Facade"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.facade = FachadaInformacionCiudad()
        self.ciudad_test = "Madrid"
    
    def test_inicializacion_facade(self):
        """Test que verifica la inicialización correcta del Facade"""
        # Verificar que se inicializan todos los proveedores
        self.assertIsNotNone(self.facade.clima_provider)
        self.assertIsNotNone(self.facade.noticias_provider)
        self.assertIsNotNone(self.facade.pais_provider)
    
    @patch('src.providers.clima_provider.ClimaProvider.obtener_clima')
    @patch('src.providers.noticias_provider.NoticiasProvider.obtener_noticias')
    @patch('src.providers.pais_provider.PaisProvider.obtener_info_pais')
    def test_obtener_informacion_completa_exitoso(self, mock_pais, mock_noticias, mock_clima):
        """Test del método principal cuando todas las APIs funcionan"""
        # Configurar mocks para simular respuestas exitosas
        mock_clima.return_value = MagicMock(spec=InformacionClima)
        mock_clima.return_value.temperatura = 20.5
        mock_clima.return_value.ciudad = "Madrid"
        
        mock_noticias.return_value = MagicMock(spec=InformacionNoticias)
        mock_noticias.return_value.noticias = []
        mock_noticias.return_value.total_resultados = 0
        
        mock_pais.return_value = MagicMock(spec=InformacionPais)
        mock_pais.return_value.nombre_comun = "España"
        
        # Ejecutar el método principal
        resultado = self.facade.obtener_informacion_completa(self.ciudad_test)
        
        # Verificaciones
        self.assertIsInstance(resultado, InformacionCompleta)
        self.assertEqual(resultado.ciudad_consultada, self.ciudad_test)
        self.assertIsNotNone(resultado.clima)
        self.assertIsNotNone(resultado.noticias)
        self.assertIsNotNone(resultado.pais)
        self.assertFalse(resultado.tiene_errores())
    
    @patch('src.providers.clima_provider.ClimaProvider.obtener_clima')
    @patch('src.providers.noticias_provider.NoticiasProvider.obtener_noticias')
    @patch('src.providers.pais_provider.PaisProvider.obtener_info_pais')
    def test_obtener_informacion_con_errores(self, mock_pais, mock_noticias, mock_clima):
        """Test cuando algunas APIs fallan"""
        # Configurar mocks para simular fallos
        mock_clima.return_value = None  # Fallo en clima
        mock_noticias.side_effect = Exception("Error API noticias")  # Excepción en noticias
        mock_pais.return_value = MagicMock(spec=InformacionPais)  # País funciona
        
        # Ejecutar el método
        resultado = self.facade.obtener_informacion_completa(self.ciudad_test)
        
        # Verificaciones
        self.assertTrue(resultado.tiene_errores())
        self.assertIsNone(resultado.clima)
        self.assertIsNone(resultado.noticias)
        self.assertIsNotNone(resultado.pais)
        self.assertGreater(len(resultado.errores), 0)
    
    def test_informacion_disponible(self):
        """Test del método informacion_disponible"""
        info = InformacionCompleta()
        
        # Sin información
        self.assertEqual(info.informacion_disponible(), [])
        
        # Con clima
        info.clima = MagicMock(spec=InformacionClima)
        self.assertIn("clima", info.informacion_disponible())
        
        # Con noticias
        info.noticias = MagicMock(spec=InformacionNoticias)
        self.assertIn("noticias", info.informacion_disponible())
        
        # Con país
        info.pais = MagicMock(spec=InformacionPais)
        self.assertIn("país", info.informacion_disponible())
    
    def test_metodos_individuales(self):
        """Test de los métodos de conveniencia para obtener información individual"""
        # Estos métodos deben existir
        self.assertTrue(hasattr(self.facade, 'obtener_solo_clima'))
        self.assertTrue(hasattr(self.facade, 'obtener_solo_noticias'))
        self.assertTrue(hasattr(self.facade, 'obtener_solo_pais'))
    
    def test_verificar_estado_apis(self):
        """Test del método de diagnóstico"""
        # El método debe ejecutarse sin errores
        try:
            self.facade.verificar_estado_apis()
        except Exception as e:
            self.fail(f"verificar_estado_apis() generó una excepción: {e}")


class TestModelosInformacion(unittest.TestCase):
    """Tests para los modelos de datos"""
    
    def test_informacion_clima_str(self):
        """Test del método __str__ de InformacionClima"""
        clima = InformacionClima(
            temperatura=20.5,
            sensacion_termica=22.0,
            humedad=65,
            descripcion="Soleado",
            ciudad="Madrid",
            pais="ES",
            icono="01d"
        )
        
        str_resultado = str(clima)
        self.assertIn("Madrid", str_resultado)
        self.assertIn("20.5", str_resultado)
        self.assertIn("Soleado", str_resultado)
    
    def test_informacion_completa_tiene_errores(self):
        """Test del método tiene_errores"""
        info = InformacionCompleta()
        
        # Sin errores
        self.assertFalse(info.tiene_errores())
        
        # Con errores
        info.errores.append("Error de prueba")
        self.assertTrue(info.tiene_errores())


class TestIntegracion(unittest.TestCase):
    """Tests de integración usando datos simulados"""
    
    @patch('src.utils.config.Config.USE_MOCK_DATA', True)
    def test_integracion_con_datos_simulados(self):
        """Test de integración completa usando datos simulados"""
        facade = FachadaInformacionCiudad()
        
        # Ejecutar con datos simulados
        resultado = facade.obtener_informacion_completa("Madrid")
        
        # Verificaciones básicas
        self.assertIsInstance(resultado, InformacionCompleta)
        self.assertEqual(resultado.ciudad_consultada, "Madrid")
        
        # Debe tener al menos alguna información (por los datos simulados)
        info_disponible = resultado.informacion_disponible()
        self.assertGreater(len(info_disponible), 0)


def ejecutar_tests():
    """Función para ejecutar todos los tests"""
    print("🧪 Ejecutando tests del patrón Facade...")
    
    # Crear suite de tests
    suite = unittest.TestSuite()
    
    # Añadir tests
    suite.addTest(unittest.makeSuite(TestFachadaInformacionCiudad))
    suite.addTest(unittest.makeSuite(TestModelosInformacion))
    suite.addTest(unittest.makeSuite(TestIntegracion))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    # Mostrar resumen
    if resultado.wasSuccessful():
        print("\n✅ Todos los tests pasaron correctamente!")
    else:
        print(f"\n❌ {len(resultado.failures)} tests fallaron")
        print(f"⚠️  {len(resultado.errors)} tests tuvieron errores")
    
    return resultado.wasSuccessful()


if __name__ == "__main__":
    ejecutar_tests() 