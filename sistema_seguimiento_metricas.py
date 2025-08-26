"""
SISTEMA COMPLETO DE SEGUIMIENTO Y MÉTRICAS ENARM
Tracking automático del progreso de 15% a 85+ score
"""

import json
from datetime import datetime, timedelta
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict

class SistemaSeguimientoENARM:
    """
    Sistema completo de seguimiento y métricas para preparación ENARM
    Monitorea progreso diario, semanal y mensual con alertas automáticas
    """
    
    def __init__(self, usuario_id, fecha_inicio, objetivo_score=85):
        self.usuario_id = usuario_id
        self.fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        self.objetivo_score = objetivo_score
        self.metricas_diarias = []
        self.alertas_activas = []
        self.hitos_completados = []
        
        # Definir ecuación objetivo por día
        self.coeficientes_objetivo = self._calcular_coeficientes_objetivo()
        
    def _calcular_coeficientes_objetivo(self):
        """Calcula coeficientes objetivo progresivos por día"""
        # Progresión de coeficientes de ecuación desde día 1 hasta día 180
        dias_total = 180
        
        # Valores iniciales (día 1)
        inicial = {
            'A_conocimiento': 0.15,
            'B_practica': 0.20,
            'C_diferenciacion': 0.25,
            'D_dificultad': 0.10,
            'T_trampas': 0.15,
            'V_velocidad': 0.30
        }
        
        # Valores finales (día 180)
        final = {
            'A_conocimiento': 0.90,
            'B_practica': 0.90,
            'C_diferenciacion': 0.90,
            'D_dificultad': 0.85,
            'T_trampas': 0.95,
            'V_velocidad': 0.90
        }
        
        # Generar progresión diaria
        coeficientes_por_dia = {}
        for dia in range(1, dias_total + 1):
            progreso = dia / dias_total  # 0.0 a 1.0
            
            # Curva de progreso no lineal (más lenta al inicio, más rápida al final)
            progreso_ajustado = self._curva_aprendizaje(progreso)
            
            coeficientes_por_dia[dia] = {}
            for coef in inicial.keys():
                valor_inicial = inicial[coef]
                valor_final = final[coef]
                valor_actual = valor_inicial + (valor_final - valor_inicial) * progreso_ajustado
                coeficientes_por_dia[dia][coef] = valor_actual
                
        return coeficientes_por_dia
    
    def _curva_aprendizaje(self, x):
        """
        Curva de aprendizaje realista - lenta al inicio, acelerada al final
        Simula cómo realmente se aprende medicina
        """
        # Curva sigmoidea modificada
        return 1 / (1 + np.exp(-8 * (x - 0.5)))
    
    def registrar_dia(self, dia_numero, metricas_dia):
        """Registra métricas de un día específico"""
        fecha_actual = self.fecha_inicio + timedelta(days=dia_numero - 1)
        
        # Calcular coeficientes actuales de la ecuación
        coeficientes_actuales = self._calcular_coeficientes_actuales(metricas_dia)
        
        # Calcular score actual con ecuación
        score_actual = self._calcular_score_ecuacion(coeficientes_actuales)
        
        # Obtener coeficientes objetivo para este día
        coeficientes_objetivo = self.coeficientes_objetivo.get(dia_numero, {})
        score_objetivo = self._calcular_score_ecuacion(coeficientes_objetivo)
        
        registro_dia = {
            'fecha': fecha_actual.strftime("%Y-%m-%d"),
            'dia_numero': dia_numero,
            'metricas_basicas': metricas_dia,
            'coeficientes_actuales': coeficientes_actuales,
            'coeficientes_objetivo': coeficientes_objetivo,
            'score_actual': score_actual,
            'score_objetivo': score_objetivo,
            'diferencia_objetivo': score_actual - score_objetivo,
            'fase_actual': self._determinar_fase(dia_numero),
            'alertas_generadas': self._generar_alertas(metricas_dia, coeficientes_actuales, score_actual, score_objetivo)
        }
        
        self.metricas_diarias.append(registro_dia)
        return registro_dia
    
    def _calcular_coeficientes_actuales(self, metricas_dia):
        """Calcula coeficientes actuales basados en métricas del día"""
        return {
            'A_conocimiento': self._calcular_coef_A(metricas_dia),
            'B_practica': self._calcular_coef_B(metricas_dia),
            'C_diferenciacion': self._calcular_coef_C(metricas_dia),
            'D_dificultad': self._calcular_coef_D(metricas_dia),
            'T_trampas': self._calcular_coef_T(metricas_dia),
            'V_velocidad': self._calcular_coef_V(metricas_dia)
        }
    
    def _calcular_coef_A(self, metricas):
        """Coeficiente A - Conocimiento basado en % aciertos"""
        porcentaje_aciertos = metricas.get('porcentaje_aciertos', 15)
        return min(porcentaje_aciertos / 100, 1.0)
    
    def _calcular_coef_B(self, metricas):
        """Coeficiente B - Práctica basado en preguntas resueltas y distribución"""
        preguntas_resueltas = metricas.get('preguntas_resueltas', 0)
        preguntas_objetivo = metricas.get('preguntas_objetivo', 50)
        distribucion_temas = metricas.get('distribucion_temas_equilibrada', False)
        
        eficiencia_cantidad = min(preguntas_resueltas / preguntas_objetivo, 1.0)
        bonus_distribucion = 0.2 if distribucion_temas else 0
        
        return min(eficiencia_cantidad + bonus_distribucion, 1.0)
    
    def _calcular_coef_C(self, metricas):
        """Coeficiente C - Diferenciación basado en aciertos en temas similares"""
        aciertos_similares = metricas.get('aciertos_temas_similares', 50)
        return min(aciertos_similares / 100, 1.0)
    
    def _calcular_coef_D(self, metricas):
        """Coeficiente D - Dificultad basado en aciertos en preguntas difíciles"""
        aciertos_dificiles = metricas.get('aciertos_preguntas_dificiles', 20)
        return min(aciertos_dificiles / 100, 1.0)
    
    def _calcular_coef_T(self, metricas):
        """Coeficiente T - Trampas basado en errores evitables"""
        errores_evitables = metricas.get('errores_evitables', 50)
        # Menos errores evitables = mejor coeficiente
        return min((100 - errores_evitables) / 100, 1.0)
    
    def _calcular_coef_V(self, metricas):
        """Coeficiente V - Velocidad basado en tiempo promedio por pregunta"""
        tiempo_promedio = metricas.get('tiempo_promedio_segundos', 120)
        tiempo_objetivo = 90  # 90 segundos por pregunta
        
        if tiempo_promedio <= tiempo_objetivo:
            return 1.0
        else:
            # Penalización por lentitud
            return max(tiempo_objetivo / tiempo_promedio, 0.3)
    
    def _calcular_score_ecuacion(self, coeficientes):
        """Calcula score usando ecuación general ENARM"""
        try:
            A = coeficientes.get('A_conocimiento', 0.15)
            B = coeficientes.get('B_practica', 0.20)
            C = coeficientes.get('C_diferenciacion', 0.25)
            D = coeficientes.get('D_dificultad', 0.10)
            T = coeficientes.get('T_trampas', 0.15)
            V = coeficientes.get('V_velocidad', 0.30)
            phi = 1.618
            
            score = ((A * B * C * D * T * V) ** (1/phi)) * 100
            return min(score, 100)
        except:
            return 0
    
    def _determinar_fase(self, dia_numero):
        """Determina en qué fase está el estudiante"""
        if dia_numero <= 45:
            return "FASE_1_FUNDAMENTOS"
        elif dia_numero <= 80:
            return "FASE_2_CONSOLIDACION"
        elif dia_numero <= 120:
            return "FASE_3_ESPECIALIZACION"
        elif dia_numero <= 150:
            return "FASE_4_PERFECCIONAMIENTO"
        elif dia_numero <= 170:
            return "FASE_5_OPTIMIZACION"
        else:
            return "FASE_6_PREPARACION_FINAL"
    
    def _generar_alertas(self, metricas_dia, coeficientes_actuales, score_actual, score_objetivo):
        """Genera alertas automáticas basadas en el rendimiento"""
        alertas = []
        
        # Alerta 1: Score muy por debajo del objetivo
        if score_actual < score_objetivo - 10:
            alertas.append({
                'tipo': 'CRITICO',
                'mensaje': f'Score actual ({score_actual:.1f}) está {score_objetivo - score_actual:.1f} puntos por debajo del objetivo',
                'accion_recomendada': 'Revisar método de estudio inmediatamente'
            })
        
        # Alerta 2: Coeficiente A (conocimiento) muy bajo
        if coeficientes_actuales['A_conocimiento'] < 0.5:
            alertas.append({
                'tipo': 'URGENTE',
                'mensaje': 'Conocimiento base crítico - menos del 50%',
                'accion_recomendada': 'Aumentar horas de estudio teórico diario'
            })
        
        # Alerta 3: Muchos errores evitables (coeficiente T bajo)
        if coeficientes_actuales['T_trampas'] < 0.4:
            alertas.append({
                'tipo': 'IMPORTANTE',
                'mensaje': 'Demasiados errores evitables - problemas con trampas',
                'accion_recomendada': 'Entrenamiento intensivo anti-trampas'
            })
        
        # Alerta 4: Velocidad muy lenta
        if coeficientes_actuales['V_velocidad'] < 0.6:
            alertas.append({
                'tipo': 'ATENCION',
                'mensaje': 'Velocidad muy lenta - riesgo de no terminar examen',
                'accion_recomendada': 'Práctica cronometrada diaria'
            })
        
        # Alerta 5: Horas de estudio insuficientes
        if metricas_dia.get('horas_estudio', 0) < 6:
            alertas.append({
                'tipo': 'WARNING',
                'mensaje': 'Horas de estudio insuficientes para el objetivo',
                'accion_recomendada': 'Aumentar dedicación diaria'
            })
        
        return alertas
    
    def generar_reporte_semanal(self, semana):
        """Genera reporte completo de la semana"""
        inicio_semana = (semana - 1) * 7 + 1
        fin_semana = min(semana * 7, 180)
        
        metricas_semana = [m for m in self.metricas_diarias 
                          if inicio_semana <= m['dia_numero'] <= fin_semana]
        
        if not metricas_semana:
            return {"error": "No hay datos para esta semana"}
        
        # Calcular promedios semanales
        scores_semana = [m['score_actual'] for m in metricas_semana]
        coeficientes_promedio = self._calcular_coeficientes_promedio(metricas_semana)
        
        # Tendencia de la semana
        tendencia = self._calcular_tendencia(scores_semana)
        
        # Alertas críticas de la semana
        alertas_semana = []
        for m in metricas_semana:
            alertas_semana.extend(m['alertas_generadas'])
        
        alertas_criticas = [a for a in alertas_semana if a['tipo'] in ['CRITICO', 'URGENTE']]
        
        reporte = {
            'semana': semana,
            'periodo': f"Días {inicio_semana}-{fin_semana}",
            'score_promedio': np.mean(scores_semana),
            'score_inicial_semana': scores_semana[0],
            'score_final_semana': scores_semana[-1],
            'mejora_semana': scores_semana[-1] - scores_semana[0],
            'tendencia': tendencia,
            'coeficientes_promedio': coeficientes_promedio,
            'alertas_criticas': alertas_criticas,
            'recomendaciones': self._generar_recomendaciones_semanales(coeficientes_promedio, tendencia),
            'objetivos_proxima_semana': self._generar_objetivos_proxima_semana(semana + 1, coeficientes_promedio)
        }
        
        return reporte
    
    def _calcular_coeficientes_promedio(self, metricas_semana):
        """Calcula coeficientes promedio de la semana"""
        coeficientes_promedio = {}
        coeficientes_keys = ['A_conocimiento', 'B_practica', 'C_diferenciacion', 
                           'D_dificultad', 'T_trampas', 'V_velocidad']
        
        for key in coeficientes_keys:
            valores = [m['coeficientes_actuales'][key] for m in metricas_semana]
            coeficientes_promedio[key] = np.mean(valores)
            
        return coeficientes_promedio
    
    def _calcular_tendencia(self, scores):
        """Calcula tendencia de scores (positiva, negativa, estable)"""
        if len(scores) < 2:
            return "insuficientes_datos"
        
        # Regresión lineal simple
        x = np.arange(len(scores))
        pendiente = np.polyfit(x, scores, 1)[0]
        
        if pendiente > 1.0:
            return "mejora_rapida"
        elif pendiente > 0.3:
            return "mejora_constante"
        elif pendiente > -0.3:
            return "estable"
        elif pendiente > -1.0:
            return "decline_leve"
        else:
            return "decline_critico"
    
    def _generar_recomendaciones_semanales(self, coeficientes, tendencia):
        """Genera recomendaciones específicas para la próxima semana"""
        recomendaciones = []
        
        # Basado en coeficientes más bajos
        coef_ordenados = sorted(coeficientes.items(), key=lambda x: x[1])
        
        for coef_nombre, valor in coef_ordenados[:2]:  # Los 2 más bajos
            if coef_nombre == 'A_conocimiento' and valor < 0.6:
                recomendaciones.append("PRIORIDAD: Aumentar horas estudio teórico +2h diarias")
            elif coef_nombre == 'B_practica' and valor < 0.6:
                recomendaciones.append("PRIORIDAD: Mejorar distribución práctica - enfoque temas menos vistos")
            elif coef_nombre == 'C_diferenciacion' and valor < 0.6:
                recomendaciones.append("PRIORIDAD: Entrenamiento diferenciación - casos similares diarios")
            elif coef_nombre == 'D_dificultad' and valor < 0.6:
                recomendaciones.append("PRIORIDAD: Práctica casos clínicos complejos - mínimo 10 diarios")
            elif coef_nombre == 'T_trampas' and valor < 0.6:
                recomendaciones.append("PRIORIDAD: Entrenamiento anti-trampas - 1h diaria específica")
            elif coef_nombre == 'V_velocidad' and valor < 0.6:
                recomendaciones.append("PRIORIDAD: Práctica cronometrada - todos los ejercicios con timer")
        
        # Basado en tendencia
        if tendencia == "decline_critico":
            recomendaciones.append("URGENTE: Revisión completa método estudio - posible cambio estrategia")
        elif tendencia == "decline_leve":
            recomendaciones.append("Revisar factores externos que puedan estar afectando rendimiento")
        elif tendencia == "estable":
            recomendaciones.append("Mantener rutina actual - considerar pequeños ajustes para acelerar progreso")
        
        return recomendaciones
    
    def _generar_objetivos_proxima_semana(self, semana, coeficientes_actuales):
        """Genera objetivos específicos para la próxima semana"""
        coeficientes_objetivo_semana = {}
        
        for coef, valor_actual in coeficientes_actuales.items():
            # Mejora gradual pero realista
            mejora_semanal = 0.05 if valor_actual < 0.5 else 0.03
            nuevo_objetivo = min(valor_actual + mejora_semanal, 1.0)
            coeficientes_objetivo_semana[coef] = nuevo_objetivo
        
        score_objetivo_semana = self._calcular_score_ecuacion(coeficientes_objetivo_semana)
        
        return {
            'coeficientes_objetivo': coeficientes_objetivo_semana,
            'score_objetivo': score_objetivo_semana,
            'mejora_minima_requerida': score_objetivo_semana - self._calcular_score_ecuacion(coeficientes_actuales)
        }
    
    def generar_grafico_progreso(self, tipo='score_diario'):
        """Genera gráficos de progreso"""
        if not self.metricas_diarias:
            return None
        
        plt.figure(figsize=(12, 8))
        
        if tipo == 'score_diario':
            dias = [m['dia_numero'] for m in self.metricas_diarias]
            scores_actual = [m['score_actual'] for m in self.metricas_diarias]
            scores_objetivo = [m['score_objetivo'] for m in self.metricas_diarias]
            
            plt.plot(dias, scores_actual, label='Score Actual', linewidth=2, color='blue')
            plt.plot(dias, scores_objetivo, label='Score Objetivo', linewidth=2, color='red', linestyle='--')
            plt.fill_between(dias, scores_actual, scores_objetivo, alpha=0.3, color='yellow')
            
            plt.xlabel('Día de Estudio')
            plt.ylabel('Score ENARM')
            plt.title('Progreso Score ENARM vs Objetivo')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
        elif tipo == 'coeficientes':
            # Gráfico de radar con coeficientes actuales vs objetivo
            dias_recientes = self.metricas_diarias[-7:]  # Últimos 7 días
            coef_promedio = self._calcular_coeficientes_promedio(dias_recientes)
            
            categorias = list(coef_promedio.keys())
            valores_actuales = list(coef_promedio.values())
            
            # Obtener objetivo para día actual
            dia_actual = self.metricas_diarias[-1]['dia_numero']
            coef_objetivo = self.coeficientes_objetivo.get(dia_actual, {})
            valores_objetivo = [coef_objetivo.get(cat, 0.5) for cat in categorias]
            
            # Gráfico de radar
            angles = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
            valores_actuales += valores_actuales[:1]  # Cerrar círculo
            valores_objetivo += valores_objetivo[:1]
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
            ax.plot(angles, valores_actuales, 'o-', linewidth=2, label='Actual', color='blue')
            ax.fill(angles, valores_actuales, alpha=0.25, color='blue')
            ax.plot(angles, valores_objetivo, 'o-', linewidth=2, label='Objetivo', color='red')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categorias)
            ax.set_ylim(0, 1)
            ax.set_title('Coeficientes Ecuación ENARM - Actual vs Objetivo')
            ax.legend()
        
        plt.tight_layout()
        return plt
    
    def generar_dashboard_completo(self):
        """Genera dashboard completo con todas las métricas"""
        if not self.metricas_diarias:
            return {"error": "No hay datos registrados"}
        
        ultimo_registro = self.metricas_diarias[-1]
        
        # Estadísticas generales
        dias_estudiados = len(self.metricas_diarias)
        dias_restantes = 180 - dias_estudiados
        progreso_general = dias_estudiados / 180 * 100
        
        # Tendencia últimos 7 días
        ultimos_7_dias = self.metricas_diarias[-7:] if len(self.metricas_diarias) >= 7 else self.metricas_diarias
        scores_recientes = [m['score_actual'] for m in ultimos_7_dias]
        tendencia_reciente = self._calcular_tendencia(scores_recientes)
        
        # Alertas activas
        alertas_activas = ultimo_registro['alertas_generadas']
        alertas_criticas = [a for a in alertas_activas if a['tipo'] in ['CRITICO', 'URGENTE']]
        
        # Predicción score final
        if len(scores_recientes) >= 3:
            score_predicho_final = self._predecir_score_final(scores_recientes, dias_restantes)
        else:
            score_predicho_final = ultimo_registro['score_actual']
        
        dashboard = {
            'resumen_general': {
                'dias_estudiados': dias_estudiados,
                'dias_restantes': dias_restantes,
                'progreso_porcentaje': progreso_general,
                'fase_actual': ultimo_registro['fase_actual'],
                'score_actual': ultimo_registro['score_actual'],
                'score_objetivo_hoy': ultimo_registro['score_objetivo'],
                'diferencia_objetivo': ultimo_registro['diferencia_objetivo'],
                'tendencia_reciente': tendencia_reciente,
                'score_predicho_final': score_predicho_final
            },
            
            'coeficientes_ecuacion': {
                'actual': ultimo_registro['coeficientes_actuales'],
                'objetivo_hoy': ultimo_registro['coeficientes_objetivo'],
                'progreso_por_coeficiente': {
                    coef: {
                        'actual': ultimo_registro['coeficientes_actuales'][coef],
                        'objetivo': ultimo_registro['coeficientes_objetivo'][coef],
                        'progreso': ultimo_registro['coeficientes_actuales'][coef] / ultimo_registro['coeficientes_objetivo'][coef] * 100
                    } for coef in ultimo_registro['coeficientes_actuales'].keys()
                }
            },
            
            'alertas_sistema': {
                'alertas_criticas': alertas_criticas,
                'total_alertas_activas': len(alertas_activas),
                'requiere_atencion_inmediata': len(alertas_criticas) > 0
            },
            
            'recomendaciones_hoy': self._generar_recomendaciones_diarias(ultimo_registro),
            
            'estadisticas_avanzadas': {
                'consistencia_estudio': self._calcular_consistencia(),
                'velocidad_mejora': self._calcular_velocidad_mejora(),
                'areas_mas_fuertes': self._identificar_areas_fuertes(ultimo_registro['coeficientes_actuales']),
                'areas_mas_debiles': self._identificar_areas_debiles(ultimo_registro['coeficientes_actuales'])
            }
        }
        
        return dashboard
    
    def _predecir_score_final(self, scores_recientes, dias_restantes):
        """Predice score final basado en tendencia actual"""
        if len(scores_recientes) < 2:
            return scores_recientes[-1] if scores_recientes else 0
        
        # Regresión lineal para predecir
        x = np.arange(len(scores_recientes))
        pendiente = np.polyfit(x, scores_recientes, 1)[0]
        
        # Proyectar mejora
        mejora_estimada = pendiente * (dias_restantes / 7)  # Mejora por semana
        score_final = scores_recientes[-1] + mejora_estimada
        
        return min(max(score_final, 0), 100)  # Entre 0 y 100
    
    def _calcular_consistencia(self):
        """Calcula qué tan consistente es el estudiante"""
        if len(self.metricas_diarias) < 7:
            return "insuficientes_datos"
        
        # Calcular desviación estándar de scores últimos 14 días
        ultimos_scores = [m['score_actual'] for m in self.metricas_diarias[-14:]]
        desv_std = np.std(ultimos_scores)
        
        if desv_std < 2:
            return "muy_consistente"
        elif desv_std < 5:
            return "consistente"
        elif desv_std < 8:
            return "moderadamente_consistente"
        else:
            return "inconsistente"
    
    def _calcular_velocidad_mejora(self):
        """Calcula velocidad de mejora en puntos por semana"""
        if len(self.metricas_diarias) < 14:
            return 0
        
        scores_inicio = np.mean([m['score_actual'] for m in self.metricas_diarias[:7]])
        scores_recientes = np.mean([m['score_actual'] for m in self.metricas_diarias[-7:]])
        
        semanas_transcurridas = len(self.metricas_diarias) / 7
        mejora_por_semana = (scores_recientes - scores_inicio) / semanas_transcurridas
        
        return mejora_por_semana
    
    def _identificar_areas_fuertes(self, coeficientes):
        """Identifica las 2 áreas más fuertes"""
        coef_ordenados = sorted(coeficientes.items(), key=lambda x: x[1], reverse=True)
        return [coef[0] for coef in coef_ordenados[:2]]
    
    def _identificar_areas_debiles(self, coeficientes):
        """Identifica las 2 áreas más débiles"""
        coef_ordenados = sorted(coeficientes.items(), key=lambda x: x[1])
        return [coef[0] for coef in coef_ordenados[:2]]
    
    def _generar_recomendaciones_diarias(self, registro_dia):
        """Genera recomendaciones específicas para hoy"""
        recomendaciones = []
        
        coeficientes = registro_dia['coeficientes_actuales']
        score_diff = registro_dia['diferencia_objetivo']
        
        if score_diff < -5:
            recomendaciones.append("URGENTE: Aumentar intensidad estudio - estás quedando atrás")
        
        # Recomendaciones por coeficiente más bajo
        coef_mas_bajo = min(coeficientes.items(), key=lambda x: x[1])
        
        if coef_mas_bajo[0] == 'A_conocimiento':
            recomendaciones.append("HOY: Enfócate en estudio teórico - +2 horas fundamentos")
        elif coef_mas_bajo[0] == 'T_trampas':
            recomendaciones.append("HOY: Práctica anti-trampas - analiza cada error evitable")
        elif coef_mas_bajo[0] == 'V_velocidad':
            recomendaciones.append("HOY: Todas las preguntas cronometradas - máximo 90 seg cada una")
        
        return recomendaciones

# Función para inicializar sistema de seguimiento
def inicializar_seguimiento_usuario(usuario_id, fecha_inicio="2024-03-01", objetivo_score=85):
    """
    Inicializa sistema de seguimiento para un usuario específico
    """
    sistema = SistemaSeguimientoENARM(usuario_id, fecha_inicio, objetivo_score)
    
    return {
        'sistema_inicializado': True,
        'usuario_id': usuario_id,
        'fecha_inicio': fecha_inicio,
        'objetivo_score': objetivo_score,
        'coeficientes_objetivo_dia_1': sistema.coeficientes_objetivo[1],
        'score_objetivo_dia_1': sistema._calcular_score_ecuacion(sistema.coeficientes_objetivo[1]),
        'instrucciones': [
            '1. Registrar métricas diariamente usando registrar_dia()',
            '2. Revisar dashboard_completo() semanalmente',
            '3. Seguir recomendaciones automáticas del sistema',
            '4. Generar reportes semanales para análisis profundo',
            '5. Ajustar plan según alertas automáticas'
        ]
    }

if __name__ == "__main__":
    # Ejemplo de uso del sistema
    sistema = inicializar_seguimiento_usuario("usuario_123", "2024-03-01", 85)
    print("📊 SISTEMA DE SEGUIMIENTO INICIALIZADO")
    print("🎯 Objetivo: 85+ puntos ENARM")
    print("📈 Seguimiento automático con ecuación general")
    print("🚨 Alertas automáticas por rendimiento")
    print("📋 Recomendaciones diarias personalizadas")