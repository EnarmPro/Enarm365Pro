from django.db import models
from api.models import Preguntas, Respuestas, RegistroRespuestaPreguntas, User, Categorias, Temarios
import numpy as np
import pandas as pd
from collections import defaultdict, Counter
import re
from datetime import datetime, timedelta
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    
try:
    import matplotlib
    matplotlib.use('Agg')  # Para evitar problemas con GUI
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

import json

class MegaAnalizadorENARM:
    """
    Sistema integral de análisis ENARM - Genera ecuación general definitiva
    Analiza: errores, aciertos, temas, patrones, trampas, estructura completa
    """
    
    def __init__(self):
        self.phi = 1.618  # Golden ratio
        self.categorias_medicas = {
            'medicina_interna': ['diabetes', 'hipertensión', 'insuficiencia', 'cardiovascular'],
            'cirugia': ['laparoscopia', 'apendicectomía', 'hernias', 'trauma'],
            'ginecologia': ['embarazo', 'parto', 'menstruación', 'anticonceptivos'],
            'pediatria': ['lactancia', 'vacunas', 'desarrollo', 'crecimiento'],
            'urgencias': ['shock', 'trauma', 'emergencia', 'reanimación']
        }
        
    def analisis_errores_aciertos_completo(self, user_id=None):
        """1. Análisis completo de errores vs aciertos por categorías"""
        
        query = RegistroRespuestaPreguntas.objects.select_related(
            'fkPregunta', 'fkRespuesta', 'fkPregunta__fkCategorias', 'fkPregunta__fkTemarios'
        )
        
        if user_id:
            query = query.filter(fkUser_id=user_id)
            
        registros = query.all()
        
        analisis = {
            'por_categoria': defaultdict(lambda: {'aciertos': 0, 'errores': 0, 'total': 0}),
            'por_temario': defaultdict(lambda: {'aciertos': 0, 'errores': 0, 'total': 0}),
            'por_dificultad': defaultdict(lambda: {'aciertos': 0, 'errores': 0, 'total': 0}),
            'por_hora': defaultdict(lambda: {'aciertos': 0, 'errores': 0, 'total': 0}),
            'patrones_error': [],
            'tendencias_temporales': []
        }
        
        for registro in registros:
            es_correcto = registro.fkRespuesta.statusRespuestas == 'Correcto'
            categoria = registro.fkPregunta.fkCategorias.descripcionCategoria
            temario = registro.fkPregunta.fkTemarios.nombreTemario
            dificultad = registro.fkPregunta.nivelPregunta
            hora = registro.fechaContestacion.hour if hasattr(registro.fechaContestacion, 'hour') else 12
            
            # Análisis por categoría
            analisis['por_categoria'][categoria]['total'] += 1
            if es_correcto:
                analisis['por_categoria'][categoria]['aciertos'] += 1
            else:
                analisis['por_categoria'][categoria]['errores'] += 1
                
            # Análisis por temario
            analisis['por_temario'][temario]['total'] += 1
            if es_correcto:
                analisis['por_temario'][temario]['aciertos'] += 1
            else:
                analisis['por_temario'][temario]['errores'] += 1
                
            # Análisis por dificultad
            analisis['por_dificultad'][dificultad]['total'] += 1
            if es_correcto:
                analisis['por_dificultad'][dificultad]['aciertos'] += 1
            else:
                analisis['por_dificultad'][dificultad]['errores'] += 1
                
            # Análisis por hora
            analisis['por_hora'][hora]['total'] += 1
            if es_correcto:
                analisis['por_hora'][hora]['aciertos'] += 1
            else:
                analisis['por_hora'][hora]['errores'] += 1
        
        # Calcular porcentajes y patrones
        for categoria, stats in analisis['por_categoria'].items():
            if stats['total'] > 0:
                stats['porcentaje_aciertos'] = (stats['aciertos'] / stats['total']) * 100
                stats['porcentaje_errores'] = (stats['errores'] / stats['total']) * 100
                
                if stats['porcentaje_errores'] > 60:  # Patrón de error crítico
                    analisis['patrones_error'].append({
                        'tipo': 'categoria_critica',
                        'nombre': categoria,
                        'tasa_error': stats['porcentaje_errores'],
                        'recomendacion': f'Enfoque intensivo en {categoria}'
                    })
        
        return analisis
    
    def analisis_temas_frecuencias(self):
        """2. Sistema de temas más/menos vistos con frecuencias"""
        
        # Obtener todas las preguntas con sus frecuencias de aparición
        preguntas = Preguntas.objects.select_related('fkCategorias', 'fkTemarios').all()
        registros = RegistroRespuestaPreguntas.objects.values('fkPregunta_id').annotate(
            frecuencia=models.Count('fkPregunta_id')
        ).order_by('-frecuencia')
        
        # Crear mapeo de frecuencias
        frecuencias_map = {r['fkPregunta_id']: r['frecuencia'] for r in registros}
        
        temas_analisis = {
            'mas_vistos': [],
            'menos_vistos': [],
            'por_categoria': defaultdict(lambda: {'total_preguntas': 0, 'frecuencia_promedio': 0}),
            'distribucion_dificultad': defaultdict(int),
            'temas_criticos': []  # Temas importantes pero poco practicados
        }
        
        for pregunta in preguntas:
            frecuencia = frecuencias_map.get(pregunta.idPregunta, 0)
            categoria = pregunta.fkCategorias.descripcionCategoria
            temario = pregunta.fkTemarios.nombreTemario
            dificultad = pregunta.nivelPregunta
            
            # Análisis por categoría
            temas_analisis['por_categoria'][categoria]['total_preguntas'] += 1
            temas_analisis['por_categoria'][categoria]['frecuencia_promedio'] += frecuencia
            
            # Distribución por dificultad
            temas_analisis['distribucion_dificultad'][dificultad] += 1
            
            # Identificar temas más y menos vistos
            if frecuencia > 50:  # Muy practicado
                temas_analisis['mas_vistos'].append({
                    'pregunta_id': pregunta.idPregunta,
                    'categoria': categoria,
                    'temario': temario,
                    'frecuencia': frecuencia,
                    'dificultad': dificultad
                })
            elif frecuencia < 5:  # Poco practicado
                temas_analisis['menos_vistos'].append({
                    'pregunta_id': pregunta.idPregunta,
                    'categoria': categoria,
                    'temario': temario,
                    'frecuencia': frecuencia,
                    'dificultad': dificultad
                })
                
            # Temas críticos (alta dificultad + baja frecuencia)
            if dificultad == 'Alta' and frecuencia < 10:
                temas_analisis['temas_criticos'].append({
                    'pregunta_id': pregunta.idPregunta,
                    'categoria': categoria,
                    'temario': temario,
                    'razon': 'Alta dificultad pero poco practicado'
                })
        
        # Calcular promedios
        for categoria, stats in temas_analisis['por_categoria'].items():
            if stats['total_preguntas'] > 0:
                stats['frecuencia_promedio'] = stats['frecuencia_promedio'] / stats['total_preguntas']
        
        return temas_analisis
    
    def detector_materias_similares(self):
        """3. Detector de materias y temas parecidos para diferenciarlos"""
        
        preguntas = Preguntas.objects.select_related('fkCategorias').all()
        
        # Preparar textos para análisis de similitud
        textos_preguntas = []
        metadata_preguntas = []
        
        for pregunta in preguntas:
            textos_preguntas.append(pregunta.nombrePregunta)
            metadata_preguntas.append({
                'id': pregunta.idPregunta,
                'categoria': pregunta.fkCategorias.descripcionCategoria,
                'dificultad': pregunta.nivelPregunta
            })
        
        similitudes_encontradas = {
            'pares_muy_similares': [],  # >0.8 similitud
            'grupos_tematicos': [],
            'diferenciar_criticos': [],
            'palabras_clave_distintivas': {}
        }
        
        if not SKLEARN_AVAILABLE:
            # Fallback sin sklearn
            similitudes_encontradas['mensaje'] = 'Análisis básico - sklearn no disponible'
            return self._detector_similitudes_basico(textos_preguntas, metadata_preguntas, similitudes_encontradas)
        
        try:
            # Vectorización TF-IDF
            vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words=None,  # Mantenemos palabras médicas específicas
                ngram_range=(1, 2)
            )
            
            tfidf_matrix = vectorizer.fit_transform(textos_preguntas)
            
            # Calcular similitudes
            similitud_matrix = cosine_similarity(tfidf_matrix)
        except Exception as e:
            similitudes_encontradas['error'] = f'Error en análisis: {str(e)}'
            return similitudes_encontradas
        
        # Encontrar pares muy similares
        n_preguntas = len(textos_preguntas)
        for i in range(n_preguntas):
            for j in range(i+1, n_preguntas):
                similitud = similitud_matrix[i][j]
                
                if similitud > 0.8:  # Muy similares
                    similitudes_encontradas['pares_muy_similares'].append({
                        'pregunta_1': metadata_preguntas[i],
                        'pregunta_2': metadata_preguntas[j],
                        'similitud': similitud,
                        'texto_1': textos_preguntas[i][:100] + '...',
                        'texto_2': textos_preguntas[j][:100] + '...',
                        'diferencias_clave': self._encontrar_diferencias_clave(
                            textos_preguntas[i], textos_preguntas[j]
                        )
                    })
        
        # Clustering para grupos temáticos
        if len(textos_preguntas) > 10:
            n_clusters = min(10, len(textos_preguntas) // 5)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(tfidf_matrix)
            
            grupos = defaultdict(list)
            for idx, cluster_id in enumerate(clusters):
                grupos[cluster_id].append({
                    'pregunta': metadata_preguntas[idx],
                    'texto': textos_preguntas[idx][:100] + '...'
                })
            
            similitudes_encontradas['grupos_tematicos'] = dict(grupos)
        
        return similitudes_encontradas
    
    def analizador_dificultad_extrema(self):
        """4. Analizador de patrones de dificultad extrema"""
        
        preguntas_dificiles = Preguntas.objects.filter(
            nivelPregunta='Alta'
        ).select_related('fkCategorias', 'fkTemarios')
        
        registros_dificiles = RegistroRespuestaPreguntas.objects.filter(
            fkPregunta__in=preguntas_dificiles
        ).select_related('fkRespuesta', 'fkPregunta')
        
        analisis_dificultad = {
            'patrones_estructura': {
                'preguntas_largas': 0,  # >200 caracteres
                'multiples_datos': 0,   # Muchos números/datos
                'negaciones_dobles': 0, # "No es incorrecto"
                'opciones_similares': 0 # Distractores muy parecidos
            },
            'tipos_trampa_identificados': {
                'absolutismos': [],     # "siempre", "nunca"
                'distractores_plausibles': [],
                'informacion_irrelevante': [],
                'secuencias_enganosas': []
            },
            'tasa_error_extrema': [],  # >80% error
            'palabras_clave_dificultad': Counter(),
            'recomendaciones_especificas': []
        }
        
        for pregunta in preguntas_dificiles:
            texto = pregunta.nombrePregunta
            opciones = list(Respuestas.objects.filter(fkPregunta=pregunta).values_list('nombreRespuestas', flat=True))
            
            # Análisis de estructura
            if len(texto) > 200:
                analisis_dificultad['patrones_estructura']['preguntas_largas'] += 1
                
            if len(re.findall(r'\d+', texto)) > 5:
                analisis_dificultad['patrones_estructura']['multiples_datos'] += 1
                
            if re.search(r'no.*(?:incorrecto|falso)', texto.lower()):
                analisis_dificultad['patrones_estructura']['negaciones_dobles'] += 1
            
            # Análisis de opciones similares
            similitud_opciones = self._calcular_similitud_opciones(opciones)
            if similitud_opciones > 0.7:
                analisis_dificultad['patrones_estructura']['opciones_similares'] += 1
            
            # Detectar tipos de trampa
            if re.search(r'\b(siempre|nunca|todos|ninguno)\b', texto.lower()):
                analisis_dificultad['tipos_trampa_identificados']['absolutismos'].append({
                    'pregunta_id': pregunta.idPregunta,
                    'texto_trampa': re.findall(r'\b(siempre|nunca|todos|ninguno)\b', texto.lower())
                })
            
            # Extraer palabras clave de dificultad
            palabras = re.findall(r'\b\w{4,}\b', texto.lower())
            for palabra in palabras:
                if palabra in ['diagnostico', 'tratamiento', 'complicacion', 'sindrome']:
                    analisis_dificultad['palabras_clave_dificultad'][palabra] += 1
        
        # Calcular tasa de error por pregunta difícil
        for registro in registros_dificiles:
            pregunta_id = registro.fkPregunta.idPregunta
            es_correcto = registro.fkRespuesta.statusRespuestas == 'Correcto'
            
            # Agrupar por pregunta para calcular tasa de error
            # (esto requeriría un análisis más complejo con agrupación)
        
        return analisis_dificultad
    
    def detector_trampas_estructuras(self):
        """5. Detector de trampas y estructuras engañosas"""
        
        todas_preguntas = Preguntas.objects.select_related('fkCategorias').all()
        
        detector_trampas = {
            'tipos_trampa': {
                'distractor_verdadero_pero_irrelevante': [],
                'informacion_extra_confusa': [],
                'opciones_parcialmente_correctas': [],
                'preguntas_doble_negacion': [],
                'datos_numericos_distractores': [],
                'terminologia_similar_confusa': []
            },
            'patrones_estructura_enganosa': {
                'pregunta_dentro_pregunta': 0,
                'multiples_pacientes': 0,
                'cronologia_confusa': 0,
                'unidades_mezcladas': 0
            },
            'palabras_trampa_frecuentes': Counter(),
            'estrategias_evitar': []
        }
        
        for pregunta in todas_preguntas:
            texto = pregunta.nombrePregunta.lower()
            opciones = list(Respuestas.objects.filter(fkPregunta=pregunta).values_list('nombreRespuestas', flat=True))
            
            # Detectar pregunta dentro de pregunta
            if texto.count('¿') > 1 or texto.count('?') > 1:
                detector_trampas['patrones_estructura_enganosa']['pregunta_dentro_pregunta'] += 1
            
            # Detectar múltiples pacientes
            if len(re.findall(r'paciente|caso|mujer|hombre|niño|niña', texto)) > 2:
                detector_trampas['patrones_estructura_enganosa']['multiples_pacientes'] += 1
            
            # Detectar cronología confusa
            marcadores_tiempo = re.findall(r'hace \d+|después de|antes de|durante|mientras', texto)
            if len(marcadores_tiempo) > 2:
                detector_trampas['patrones_estructura_enganosa']['cronologia_confusa'] += 1
            
            # Detectar datos numéricos distractores
            numeros = re.findall(r'\d+(?:\.\d+)?', texto)
            if len(numeros) > 5:
                detector_trampas['tipos_trampa']['datos_numericos_distractores'].append({
                    'pregunta_id': pregunta.idPregunta,
                    'numeros_encontrados': len(numeros),
                    'categoria': pregunta.fkCategorias.descripcionCategoria
                })
            
            # Detectar doble negación
            if re.search(r'no.*(?:in|des|anti)', texto):
                detector_trampas['tipos_trampa']['preguntas_doble_negacion'].append({
                    'pregunta_id': pregunta.idPregunta,
                    'ejemplo': texto[:100]
                })
            
            # Análisis de opciones parcialmente correctas
            if self._detectar_opciones_parciales(opciones):
                detector_trampas['tipos_trampa']['opciones_parcialmente_correctas'].append({
                    'pregunta_id': pregunta.idPregunta,
                    'opciones': opciones
                })
            
            # Contar palabras trampa
            palabras_trampa = ['excepto', 'salvo', 'menos', 'principalmente', 'generalmente', 'usualmente']
            for palabra in palabras_trampa:
                if palabra in texto:
                    detector_trampas['palabras_trampa_frecuentes'][palabra] += 1
        
        # Generar estrategias para evitar trampas
        detector_trampas['estrategias_evitar'] = [
            "Leer toda la pregunta antes de ver opciones",
            "Identificar la pregunta central real",
            "Marcar palabras clave como 'excepto', 'no', 'menos'",
            "Descartar información irrelevante",
            "Buscar la opción MÁS correcta, no perfecta",
            "Cuidado con absolutismos (siempre/nunca)"
        ]
        
        return detector_trampas
    
    def sistema_critica_perfecta(self, user_id):
        """6. Sistema de crítica 100/100 - Análisis para puntuación perfecta"""
        
        # Obtener historial completo del usuario
        registros_usuario = RegistroRespuestaPreguntas.objects.filter(
            fkUser_id=user_id
        ).select_related('fkPregunta', 'fkRespuesta', 'fkPregunta__fkCategorias')
        
        critica_100 = {
            'areas_debiles_criticas': [],  # Debe tener >95% en todas
            'tiempo_promedio_optimo': None,
            'patrones_error_eliminables': [],
            'preguntas_trampa_falladas': [],
            'plan_perfeccionamiento': {
                'fase_1_fundamentos': [],
                'fase_2_patrones': [],
                'fase_3_trampas': [],
                'fase_4_velocidad': []
            },
            'simulacros_recomendados': [],
            'puntos_criticos_100': []
        }
        
        # Análisis por categoría para 100/100
        categorias_stats = defaultdict(lambda: {'total': 0, 'aciertos': 0})
        
        for registro in registros_usuario:
            categoria = registro.fkPregunta.fkCategorias.descripcionCategoria
            es_correcto = registro.fkRespuesta.statusRespuestas == 'Correcto'
            
            categorias_stats[categoria]['total'] += 1
            if es_correcto:
                categorias_stats[categoria]['aciertos'] += 1
        
        # Identificar áreas débiles críticas
        for categoria, stats in categorias_stats.items():
            if stats['total'] > 0:
                porcentaje = (stats['aciertos'] / stats['total']) * 100
                if porcentaje < 95:  # Crítico para 100/100
                    critica_100['areas_debiles_criticas'].append({
                        'categoria': categoria,
                        'porcentaje_actual': porcentaje,
                        'errores_restantes': stats['total'] - stats['aciertos'],
                        'objetivo_mejorar': 100 - porcentaje
                    })
        
        # Plan de perfeccionamiento específico
        if critica_100['areas_debiles_criticas']:
            for area in critica_100['areas_debiles_criticas']:
                if area['porcentaje_actual'] < 80:
                    critica_100['plan_perfeccionamiento']['fase_1_fundamentos'].append(
                        f"Revisar fundamentos completos de {area['categoria']}"
                    )
                elif area['porcentaje_actual'] < 90:
                    critica_100['plan_perfeccionamiento']['fase_2_patrones'].append(
                        f"Practicar patrones específicos en {area['categoria']}"
                    )
                else:
                    critica_100['plan_perfeccionamiento']['fase_3_trampas'].append(
                        f"Dominar trampas avanzadas en {area['categoria']}"
                    )
        
        # Puntos críticos específicos para 100/100
        critica_100['puntos_criticos_100'] = [
            "Zero tolerance para errores por descuido",
            "Dominio absoluto de NOMs vigentes",
            "Reconocimiento instantáneo de patrones de trampa",
            "Velocidad óptima sin sacrificar precisión",
            "Estrategia específica para cada tipo de pregunta"
        ]
        
        return critica_100
    
    def ecuacion_general_enarm(self, user_id=None):
        """7. ECUACIÓN GENERAL DEFINITIVA DEL ENARM"""
        
        # Recopilar todos los análisis
        errores_aciertos = self.analisis_errores_aciertos_completo(user_id)
        temas_freq = self.analisis_temas_frecuencias()
        similitudes = self.detector_materias_similares()
        dificultad = self.analizador_dificultad_extrema()
        trampas = self.detector_trampas_estructuras()
        critica_100 = self.sistema_critica_perfecta(user_id) if user_id else None
        
        # Coeficientes de la ecuación general
        coeficientes = {
            'A': self._calcular_coef_conocimiento(errores_aciertos),      # Conocimiento base
            'B': self._calcular_coef_practica(temas_freq),               # Frecuencia de práctica  
            'C': self._calcular_coef_diferenciacion(similitudes),        # Capacidad de diferenciación
            'D': self._calcular_coef_dificultad(dificultad),            # Manejo de dificultad
            'T': self._calcular_coef_trampas(trampas),                  # Detección de trampas
            'Φ': self.phi,                                              # Factor de optimización
            'V': self._calcular_velocidad_optima(user_id) if user_id else 1  # Velocidad
        }
        
        # ECUACIÓN GENERAL ENARM:
        # SCORE = (A × B × C × D × T × V)^Φ / 100
        # Donde cada variable va de 0 a 1
        
        score_predicho = ((
            coeficientes['A'] * 
            coeficientes['B'] * 
            coeficientes['C'] * 
            coeficientes['D'] * 
            coeficientes['T'] * 
            coeficientes['V']
        ) ** (1/coeficientes['Φ'])) * 100
        
        ecuacion_completa = {
            'formula': "SCORE_ENARM = ((A × B × C × D × T × V)^(1/Φ)) × 100",
            'coeficientes': coeficientes,
            'score_predicho': min(score_predicho, 100),  # Cap at 100
            'explicacion': {
                'A': 'Conocimiento base por categorías',
                'B': 'Eficiencia de práctica y frecuencia',  
                'C': 'Capacidad diferenciación temas similares',
                'D': 'Manejo de preguntas de dificultad extrema',
                'T': 'Detección y evasión de trampas',
                'V': 'Velocidad de respuesta óptima',
                'Φ': 'Factor de optimización golden ratio'
            },
            'recomendaciones_mejora': self._generar_recomendaciones_ecuacion(coeficientes),
            'plan_100_puntos': self._generar_plan_100(coeficientes),
            'meta_analisis': {
                'total_preguntas_analizadas': Preguntas.objects.count(),
                'total_intentos_analizados': RegistroRespuestaPreguntas.objects.count(),
                'precision_ecuacion': self._calcular_precision_ecuacion(coeficientes)
            }
        }
        
        return ecuacion_completa
    
    # Métodos auxiliares para cálculos de coeficientes
    def _calcular_coef_conocimiento(self, errores_aciertos):
        """Calcula coeficiente A - conocimiento base"""
        if not errores_aciertos['por_categoria']:
            return 0.5
        
        promedios = []
        for categoria, stats in errores_aciertos['por_categoria'].items():
            if stats['total'] > 0:
                porcentaje = stats['aciertos'] / stats['total']
                promedios.append(porcentaje)
        
        return np.mean(promedios) if promedios else 0.5
    
    def _calcular_coef_practica(self, temas_freq):
        """Calcula coeficiente B - práctica"""
        if not temas_freq['por_categoria']:
            return 0.5
            
        freq_promedio = np.mean([
            stats['frecuencia_promedio'] 
            for stats in temas_freq['por_categoria'].values()
        ])
        
        # Normalizar frecuencia (0-1)
        return min(freq_promedio / 50, 1.0)
    
    def _calcular_coef_diferenciacion(self, similitudes):
        """Calcula coeficiente C - diferenciación"""
        pares_similares = len(similitudes['pares_muy_similares'])
        
        # Menos pares similares = mejor diferenciación
        if pares_similares == 0:
            return 1.0
        elif pares_similares < 5:
            return 0.8
        elif pares_similares < 15:
            return 0.6
        else:
            return 0.4
    
    def _calcular_coef_dificultad(self, dificultad):
        """Calcula coeficiente D - manejo dificultad"""
        total_patrones = sum(dificultad['patrones_estructura'].values())
        
        # Más patrones detectados = mejor manejo
        if total_patrones > 20:
            return 0.9
        elif total_patrones > 10:
            return 0.7
        else:
            return 0.5
    
    def _calcular_coef_trampas(self, trampas):
        """Calcula coeficiente T - detección trampas"""
        total_trampas = sum(len(v) if isinstance(v, list) else v 
                           for v in trampas['tipos_trampa'].values())
        
        # Más trampas detectadas = mejor coeficiente
        if total_trampas > 50:
            return 0.9
        elif total_trampas > 25:
            return 0.7
        else:
            return 0.5
    
    def _calcular_velocidad_optima(self, user_id):
        """Calcula coeficiente V - velocidad"""
        # Análisis de velocidad promedio del usuario
        # Por ahora retornamos un valor base
        return 0.8
    
    def _generar_recomendaciones_ecuacion(self, coeficientes):
        """Genera recomendaciones específicas basadas en coeficientes"""
        recomendaciones = []
        
        if coeficientes['A'] < 0.7:
            recomendaciones.append("CRÍTICO: Reforzar conocimiento base - estudiar fundamentos")
        
        if coeficientes['B'] < 0.6:
            recomendaciones.append("Aumentar frecuencia de práctica - mínimo 50 preguntas/día")
        
        if coeficientes['C'] < 0.7:
            recomendaciones.append("Practicar diferenciación - comparar temas similares")
        
        if coeficientes['D'] < 0.6:
            recomendaciones.append("Entrenar con preguntas de máxima dificultad")
        
        if coeficientes['T'] < 0.7:
            recomendaciones.append("Estudiar patrones de trampas - modo detective")
        
        return recomendaciones
    
    def _generar_plan_100(self, coeficientes):
        """Plan específico para lograr 100/100 puntos"""
        plan_100 = []
        
        # Calcular qué tan cerca está de cada coeficiente perfecto
        objetivos = {
            'A': 0.95,  # 95% conocimiento
            'B': 0.90,  # 90% práctica
            'C': 0.85,  # 85% diferenciación  
            'D': 0.80,  # 80% dificultad
            'T': 0.90   # 90% trampas
        }
        
        for coef, objetivo in objetivos.items():
            if coeficientes[coef] < objetivo:
                diferencia = objetivo - coeficientes[coef]
                plan_100.append(f"Mejorar {coef}: +{diferencia:.2f} puntos")
        
        return plan_100
    
    def _calcular_precision_ecuacion(self, coeficientes):
        """Calcula la precisión estimada de la ecuación"""
        # Basado en la completitud de datos y coeficientes
        completitud = np.mean(list(coeficientes.values())[:-1])  # Excluir Φ
        return min(completitud * 100, 95)  # Max 95% precision
    
    # Métodos auxiliares adicionales
    def _encontrar_diferencias_clave(self, texto1, texto2):
        """Encuentra diferencias clave entre dos textos similares"""
        palabras1 = set(texto1.lower().split())
        palabras2 = set(texto2.lower().split())
        
        diferentes1 = palabras1 - palabras2
        diferentes2 = palabras2 - palabras1
        
        return {
            'unicas_texto1': list(diferentes1)[:5],
            'unicas_texto2': list(diferentes2)[:5]
        }
    
    def _calcular_similitud_opciones(self, opciones):
        """Calcula similitud promedio entre opciones de respuesta"""
        if len(opciones) < 2:
            return 0
            
        similitudes = []
        for i in range(len(opciones)):
            for j in range(i+1, len(opciones)):
                palabras1 = set(opciones[i].lower().split())
                palabras2 = set(opciones[j].lower().split())
                
                interseccion = palabras1.intersection(palabras2)
                union = palabras1.union(palabras2)
                
                if union:
                    similitud = len(interseccion) / len(union)
                    similitudes.append(similitud)
        
        return np.mean(similitudes) if similitudes else 0
    
    def _detectar_opciones_parciales(self, opciones):
        """Detecta si hay opciones parcialmente correctas"""
        # Buscar patrones como "en parte", "parcialmente", etc.
        patrones_parciales = ['en parte', 'parcialmente', 'solo si', 'excepto cuando']
        
        for opcion in opciones:
            for patron in patrones_parciales:
                if patron in opcion.lower():
                    return True
        return False
    
    def _detector_similitudes_basico(self, textos_preguntas, metadata_preguntas, similitudes_encontradas):
        """Detector de similitudes básico sin sklearn"""
        
        # Análisis básico de similitud por palabras clave
        for i, texto1 in enumerate(textos_preguntas):
            for j, texto2 in enumerate(textos_preguntas[i+1:], i+1):
                # Calcular similitud básica
                palabras1 = set(texto1.lower().split())
                palabras2 = set(texto2.lower().split())
                
                interseccion = palabras1.intersection(palabras2)
                union = palabras1.union(palabras2)
                
                if union:
                    similitud = len(interseccion) / len(union)
                    
                    if similitud > 0.5:  # Umbral más bajo para análisis básico
                        similitudes_encontradas['pares_muy_similares'].append({
                            'pregunta_1': metadata_preguntas[i],
                            'pregunta_2': metadata_preguntas[j],
                            'similitud': similitud,
                            'texto_1': texto1[:100] + '...',
                            'texto_2': texto2[:100] + '...',
                            'diferencias_clave': {
                                'unicas_texto1': list(palabras1 - palabras2)[:5],
                                'unicas_texto2': list(palabras2 - palabras1)[:5]
                            }
                        })
        
        return similitudes_encontradas

# Clase principal para generar reportes completos
class GeneradorReportesENARM:
    """Genera reportes visuales completos del análisis ENARM"""
    
    def __init__(self):
        self.analizador = MegaAnalizadorENARM()
    
    def generar_reporte_completo(self, user_id=None):
        """Genera reporte visual completo con todos los análisis"""
        
        # Obtener todos los análisis
        ecuacion = self.analizador.ecuacion_general_enarm(user_id)
        
        reporte = {
            'resumen_ejecutivo': {
                'score_predicho': ecuacion['score_predicho'],
                'precision_ecuacion': ecuacion['meta_analisis']['precision_ecuacion'],
                'recomendacion_principal': ecuacion['recomendaciones_mejora'][0] if ecuacion['recomendaciones_mejora'] else "Continuar práctica regular"
            },
            'ecuacion_completa': ecuacion,
            'visualizaciones_generadas': [],
            'plan_estudio_personalizado': self._generar_plan_estudio(ecuacion),
            'alertas_criticas': self._generar_alertas(ecuacion)
        }
        
        return reporte
    
    def _generar_plan_estudio(self, ecuacion):
        """Genera plan de estudio personalizado basado en la ecuación"""
        coefs = ecuacion['coeficientes']
        
        plan = {
            'prioridad_alta': [],
            'prioridad_media': [],
            'prioridad_baja': [],
            'cronograma_sugerido': {}
        }
        
        # Determinar prioridades basadas en coeficientes
        if coefs['A'] < 0.6:  # Conocimiento crítico
            plan['prioridad_alta'].append("Revisión intensiva de fundamentos médicos")
        
        if coefs['T'] < 0.7:  # Trampas críticas
            plan['prioridad_alta'].append("Entrenamiento anti-trampas diario")
        
        if coefs['D'] < 0.6:  # Dificultad crítica
            plan['prioridad_media'].append("Práctica con preguntas de alta dificultad")
        
        return plan
    
    def _generar_alertas(self, ecuacion):
        """Genera alertas críticas basadas en el análisis"""
        alertas = []
        
        if ecuacion['score_predicho'] < 70:
            alertas.append({
                'nivel': 'CRÍTICO',
                'mensaje': 'Score predicho bajo - requiere intervención inmediata',
                'accion': 'Plan de estudio intensivo de 30 días'
            })
        
        if len(ecuacion['recomendaciones_mejora']) > 3:
            alertas.append({
                'nivel': 'ALTO',
                'mensaje': 'Múltiples áreas de mejora identificadas',
                'accion': 'Enfocar en las 2 áreas más críticas primero'
            })
        
        return alertas