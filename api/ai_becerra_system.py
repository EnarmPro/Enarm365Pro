from django.db import models
from api.models import Preguntas, Respuestas, RegistroRespuestaPreguntas, User, Categorias
import numpy as np
import json
from datetime import datetime, timedelta
import re
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import openai

class PatronBecerra:
    """
    Sistema de análisis de patrones basado en metodología Becerra Φ
    Detecta patrones P+T+N² en preguntas ENARM
    P = Patrón biológico/médico
    T = Trampa psíquica/cognitiva  
    N = Distractor ambiguo
    """
    
    def __init__(self):
        self.phi_coefficient = 1.618  # Golden ratio para cálculos Φ
        self.pattern_weights = {
            'biologico': 0.4,
            'trampa_psiquica': 0.35,
            'distractor_ambiguo': 0.25
        }
        
    def calcular_phi_pattern(self, p_score, t_score, n_score):
        """Calcula [P+T+N]² optimizado con Φ"""
        base_score = (p_score + t_score + n_score) ** 2
        phi_optimization = base_score * (1 + (1/self.phi_coefficient))
        return phi_optimization
    
    def detectar_patron_biologico(self, pregunta_texto):
        """Detecta patrones biológicos/médicos (P)"""
        patrones_bio = [
            r'(enzima|proteína|gen|ADN|ARN)',
            r'(célula|mitocondria|núcleo|membrana)',
            r'(metabolismo|glucólisis|ciclo de krebs)',
            r'(hormona|insulina|cortisol|tiroxina)',
            r'(neurotransmisor|dopamina|serotonina)',
            r'(anticuerpo|inmunoglobulina|antígeno)'
        ]
        
        score = 0
        for patron in patrones_bio:
            matches = len(re.findall(patron, pregunta_texto.lower()))
            score += matches * 0.2
            
        return min(score, 1.0)  # Normalizar a 0-1
    
    def detectar_trampa_psiquica(self, pregunta_texto, opciones_respuesta):
        """Detecta trampas psíquicas/cognitivas (T)"""
        trampas = [
            r'(siempre|nunca|todos|ninguno)',  # Absolutismos
            r'(excepto|salvo|menos)',  # Negaciones
            r'(más probable|menos probable)',  # Probabilidades engañosas
            r'(primer|segundo|tercer) (signo|síntoma)',  # Secuencias
        ]
        
        score = 0
        texto_completo = pregunta_texto + " ".join(opciones_respuesta)
        
        for trampa in trampas:
            matches = len(re.findall(trampa, texto_completo.lower()))
            score += matches * 0.3
            
        return min(score, 1.0)
    
    def detectar_distractor_ambiguo(self, opciones_respuesta):
        """Detecta distractores ambiguos (N)"""
        score = 0
        
        # Calcular similitud entre opciones
        for i, opcion1 in enumerate(opciones_respuesta):
            for j, opcion2 in enumerate(opciones_respuesta[i+1:], i+1):
                similitud = self._calcular_similitud_texto(opcion1, opcion2)
                if similitud > 0.7:  # Alta similitud = ambigüedad
                    score += 0.25
                    
        return min(score, 1.0)
    
    def _calcular_similitud_texto(self, texto1, texto2):
        """Calcula similitud básica entre textos"""
        words1 = set(texto1.lower().split())
        words2 = set(texto2.lower().split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0

class AnalizadorNOMs:
    """Analiza NOMs emergentes y patrones regulatorios"""
    
    def __init__(self):
        self.noms_importantes = {
            'NOM-020': ['diabetes', 'glucosa', 'hemoglobina glucosilada'],
            'NOM-030': ['hipertensión', 'presión arterial', 'antihipertensivos'],
            'NOM-043': ['obesidad', 'IMC', 'sobrepeso'],
            'NOM-017': ['cáncer', 'oncología', 'quimioterapia']
        }
        
    def detectar_nom_en_pregunta(self, pregunta_texto):
        """Detecta si una pregunta está relacionada con NOMs específicas"""
        detecciones = {}
        
        for nom, keywords in self.noms_importantes.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in pregunta_texto.lower():
                    score += 1
            
            detecciones[nom] = score / len(keywords)
            
        return detecciones
    
    def calcular_tendencia_omega(self, preguntas_recientes):
        """Calcula patrón Ω para tendencias institucionales"""
        tendencias = defaultdict(int)
        
        for pregunta in preguntas_recientes:
            noms_detectadas = self.detectar_nom_en_pregunta(pregunta.nombrePregunta)
            for nom, score in noms_detectadas.items():
                if score > 0.5:
                    tendencias[nom] += 1
                    
        return dict(tendencias)

class GeneradorGraficos:
    """Genera gráficos de correlación tiempo-respuestas-errores"""
    
    @staticmethod
    def generar_correlacion_tiempo_errores(user_id, dias=30):
        """Genera gráfico de correlación tiempo vs errores"""
        fecha_inicio = datetime.now() - timedelta(days=dias)
        
        registros = RegistroRespuestaPreguntas.objects.filter(
            fkUser_id=user_id,
            fechaContestacion__gte=fecha_inicio
        ).select_related('fkRespuesta', 'fkPregunta')
        
        datos_tiempo = []
        datos_errores = []
        
        for registro in registros:
            hora = registro.fechaContestacion.hour
            es_correcto = registro.fkRespuesta.statusRespuestas == 'Correcto'
            
            datos_tiempo.append(hora)
            datos_errores.append(0 if es_correcto else 1)
        
        plt.figure(figsize=(12, 6))
        plt.scatter(datos_tiempo, datos_errores, alpha=0.6)
        plt.xlabel('Hora del día')
        plt.ylabel('Error (1) vs Acierto (0)')
        plt.title('Correlación Tiempo-Errores (Últimos 30 días)')
        plt.grid(True, alpha=0.3)
        
        # Guardar gráfico
        plt.savefig('static/img/correlacion_tiempo_errores.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return 'static/img/correlacion_tiempo_errores.png'

class PredictorTendencias:
    """Predictor de tendencias institucionales ENARM 2025"""
    
    def __init__(self):
        self.tendencias_2025 = {
            'medicina_personalizada': 0.8,
            'telemedicina': 0.7,
            'inteligencia_artificial': 0.6,
            'medicina_preventiva': 0.9,
            'enfermedades_emergentes': 0.75
        }
    
    def predecir_preguntas_2025(self):
        """Predice qué tipo de preguntas aparecerán en ENARM 2025"""
        predicciones = []
        
        for tema, probabilidad in self.tendencias_2025.items():
            if probabilidad > 0.6:
                predicciones.append({
                    'tema': tema,
                    'probabilidad': probabilidad,
                    'importancia': 'Alta' if probabilidad > 0.75 else 'Media'
                })
        
        return sorted(predicciones, key=lambda x: x['probabilidad'], reverse=True)
    
    def calcular_desequilibrio_metacircular(self, preguntas_sample):
        """Calcula desequilibrio meta-circular tipo Ω"""
        patron_becerra = PatronBecerra()
        desequilibrios = []
        
        for pregunta in preguntas_sample:
            opciones = list(Respuestas.objects.filter(fkPregunta=pregunta).values_list('nombreRespuestas', flat=True))
            
            p_score = patron_becerra.detectar_patron_biologico(pregunta.nombrePregunta)
            t_score = patron_becerra.detectar_trampa_psiquica(pregunta.nombrePregunta, opciones)
            n_score = patron_becerra.detectar_distractor_ambiguo(opciones)
            
            phi_value = patron_becerra.calcular_phi_pattern(p_score, t_score, n_score)
            
            if phi_value > 3.0:  # Umbral de desequilibrio
                desequilibrios.append({
                    'pregunta_id': pregunta.idPregunta,
                    'phi_value': phi_value,
                    'tipo_desequilibrio': 'Meta-circular Ω'
                })
        
        return desequilibrios

class SistemaBecerraIA:
    """Sistema principal que integra todos los módulos"""
    
    def __init__(self):
        self.patron_becerra = PatronBecerra()
        self.analizador_noms = AnalizadorNOMs()
        self.generador_graficos = GeneradorGraficos()
        self.predictor = PredictorTendencias()
    
    def analizar_pregunta_completa(self, pregunta_id):
        """Análisis completo de una pregunta usando metodología Becerra Φ"""
        try:
            pregunta = Preguntas.objects.get(idPregunta=pregunta_id)
            opciones = list(Respuestas.objects.filter(fkPregunta=pregunta).values_list('nombreRespuestas', flat=True))
            
            # Análisis de patrones P+T+N²
            p_score = self.patron_becerra.detectar_patron_biologico(pregunta.nombrePregunta)
            t_score = self.patron_becerra.detectar_trampa_psiquica(pregunta.nombrePregunta, opciones)
            n_score = self.patron_becerra.detectar_distractor_ambiguo(opciones)
            phi_value = self.patron_becerra.calcular_phi_pattern(p_score, t_score, n_score)
            
            # Análisis de NOMs
            noms_detectadas = self.analizador_noms.detectar_nom_en_pregunta(pregunta.nombrePregunta)
            
            # Resultado integrado
            resultado = {
                'pregunta_id': pregunta_id,
                'phi_value': phi_value,
                'patron_scores': {
                    'biologico': p_score,
                    'trampa_psiquica': t_score,
                    'distractor_ambiguo': n_score
                },
                'noms_relacionadas': noms_detectadas,
                'nivel_dificultad': 'Alto' if phi_value > 2.5 else 'Medio' if phi_value > 1.5 else 'Bajo',
                'recomendaciones': self._generar_recomendaciones(phi_value, p_score, t_score, n_score)
            }
            
            return resultado
            
        except Exception as e:
            return {'error': f'Error en análisis: {str(e)}'}
    
    def _generar_recomendaciones(self, phi_value, p_score, t_score, n_score):
        """Genera recomendaciones basadas en análisis Φ"""
        recomendaciones = []
        
        if p_score < 0.3:
            recomendaciones.append("Reforzar conocimientos de biología molecular y fisiología")
        
        if t_score > 0.7:
            recomendaciones.append("Cuidado con trampas psíquicas - leer cuidadosamente")
        
        if n_score > 0.6:
            recomendaciones.append("Analizar bien los distractores - hay ambigüedad alta")
        
        if phi_value > 3.0:
            recomendaciones.append("Pregunta con desequilibrio meta-circular Ω - requiere análisis profundo")
        
        return recomendaciones
    
    def generar_dashboard_becerra(self, user_id):
        """Genera dashboard completo con metodología Becerra"""
        # Generar gráficos
        grafico_correlacion = self.generador_graficos.generar_correlacion_tiempo_errores(user_id)
        
        # Predicciones 2025
        predicciones = self.predictor.predecir_preguntas_2025()
        
        # Análisis de últimas preguntas contestadas
        ultimas_preguntas = RegistroRespuestaPreguntas.objects.filter(
            fkUser_id=user_id
        ).select_related('fkPregunta').order_by('-fechaContestacion')[:10]
        
        analisis_preguntas = []
        for registro in ultimas_preguntas:
            analisis = self.analizar_pregunta_completa(registro.fkPregunta.idPregunta)
            analisis_preguntas.append(analisis)
        
        dashboard = {
            'grafico_correlacion': grafico_correlacion,
            'predicciones_2025': predicciones,
            'analisis_recientes': analisis_preguntas,
            'resumen_phi': {
                'phi_promedio': np.mean([a.get('phi_value', 0) for a in analisis_preguntas]),
                'desequilibrios_detectados': len([a for a in analisis_preguntas if a.get('phi_value', 0) > 3.0])
            }
        }
        
        return dashboard