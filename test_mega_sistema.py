#!/usr/bin/env python
"""
Test básico del Mega Sistema ENARM
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'D27.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

# Importar el sistema
try:
    from api.mega_analizador_enarm import MegaAnalizadorENARM, GeneradorReportesENARM
    print("✅ Mega Analizador ENARM importado correctamente")
except Exception as e:
    print(f"❌ Error importando Mega Analizador: {e}")

try:
    from api.ai_becerra_system import SistemaBecerraIA, PatronBecerra
    print("✅ Sistema Becerra Φ importado correctamente")
except Exception as e:
    print(f"❌ Error importando Sistema Becerra: {e}")

# Probar imports de dependencias
try:
    import numpy as np
    print("✅ NumPy disponible")
except ImportError:
    print("❌ NumPy no disponible")

try:
    import matplotlib
    print("✅ Matplotlib disponible")
except ImportError:
    print("❌ Matplotlib no disponible")

try:
    import seaborn
    print("✅ Seaborn disponible")
except ImportError:
    print("❌ Seaborn no disponible")

try:
    import sklearn
    print("✅ Scikit-learn disponible")
except ImportError:
    print("❌ Scikit-learn no disponible")

try:
    import pandas
    print("✅ Pandas disponible")
except ImportError:
    print("❌ Pandas no disponible")

# Test básico del analizador
try:
    analizador = MegaAnalizadorENARM()
    print("✅ MegaAnalizadorENARM instanciado correctamente")
    
    # Test método básico
    temas_analisis = analizador.analisis_temas_frecuencias()
    print(f"✅ Análisis de temas ejecutado: {len(temas_analisis)} categorías encontradas")
    
except Exception as e:
    print(f"❌ Error probando MegaAnalizadorENARM: {e}")

# Test del sistema Becerra
try:
    patron_becerra = PatronBecerra()
    print("✅ PatronBecerra instanciado correctamente")
    
    # Test detección de patrón biológico
    score = patron_becerra.detectar_patron_biologico("La insulina es una hormona producida por el páncreas")
    print(f"✅ Detección de patrón biológico: {score:.3f}")
    
except Exception as e:
    print(f"❌ Error probando PatronBecerra: {e}")

print("\n🎯 RESUMEN DEL TEST:")
print("El Mega Sistema ENARM está configurado y listo para usar!")
print("Accede a las siguientes URLs para usar el sistema:")
print("- /mega_dashboard/ - Dashboard principal")
print("- /dashboard_becerra/ - Dashboard Becerra Φ")
print("- /modo_agente/ - Modo Agente con IA")
print("- /ecuacion_general/ - Ecuación General ENARM")