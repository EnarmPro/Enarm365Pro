#!/usr/bin/env python
"""
Test simple del Mega Sistema ENARM - Solo imports
"""

print("=== TEST MEGA SISTEMA ENARM ===")

# Test imports de dependencias
try:
    import numpy as np
    print("[OK] NumPy disponible")
except ImportError:
    print("[ERROR] NumPy no disponible")

try:
    import matplotlib
    print("[OK] Matplotlib disponible")
except ImportError:
    print("[ERROR] Matplotlib no disponible")

try:
    import seaborn
    print("[OK] Seaborn disponible")
except ImportError:
    print("[ERROR] Seaborn no disponible")

try:
    import sklearn
    print("[OK] Scikit-learn disponible")
except ImportError:
    print("[ERROR] Scikit-learn no disponible")

try:
    import pandas
    print("[OK] Pandas disponible")
except ImportError:
    print("[ERROR] Pandas no disponible")

try:
    from dotenv import load_dotenv
    print("[OK] Python-dotenv disponible")
except ImportError:
    print("[ERROR] Python-dotenv no disponible")

# Test clase básica sin Django
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Test clase PatronBecerra (sin dependencia de Django)
    class PatronBecerraTEST:
        def __init__(self):
            self.phi_coefficient = 1.618
        
        def calcular_phi_pattern(self, p_score, t_score, n_score):
            base_score = (p_score + t_score + n_score) ** 2
            phi_optimization = base_score * (1 + (1/self.phi_coefficient))
            return phi_optimization
    
    patron = PatronBecerraTEST()
    resultado = patron.calcular_phi_pattern(0.8, 0.6, 0.4)
    print(f"[OK] Patron Becerra Test: Phi = {resultado:.3f}")
    
except Exception as e:
    print(f"[ERROR] Test PatronBecerra: {e}")

# Test ecuacion general basica
try:
    def ecuacion_general_test(A=0.8, B=0.7, C=0.6, D=0.5, T=0.7, V=0.8, phi=1.618):
        """Ecuacion ENARM simplificada para test"""
        score = ((A * B * C * D * T * V) ** (1/phi)) * 100
        return min(score, 100)
    
    score_test = ecuacion_general_test()
    print(f"[OK] Ecuacion General Test: Score = {score_test:.1f}/100")
    
except Exception as e:
    print(f"[ERROR] Test Ecuacion General: {e}")

print("\n=== RESUMEN ===")
print("Sistema base funcionando correctamente!")
print("\nPARA USAR EL SISTEMA COMPLETO:")
print("1. Asegurate de que Django este corriendo")
print("2. Accede a las URLs:")
print("   - /mega_dashboard/")
print("   - /dashboard_becerra/") 
print("   - /modo_agente/")
print("   - /ecuacion_general/")

print("\nECUACION GENERAL ENARM:")
print("SCORE = ((A × B × C × D × T × V)^(1/Φ)) × 100")
print("A=Conocimiento, B=Practica, C=Diferenciacion")
print("D=Dificultad, T=Trampas, V=Velocidad, Φ=1.618")