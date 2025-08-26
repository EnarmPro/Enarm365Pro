"""
PLAN DEFINITIVO: DE 15% CONOCIMIENTO A 100% ENARM
Sistema completo para primera vez en examen nacional
"""

class PlanENARM15a100:
    """
    Plan estratégico completo para ir de 15% a 100% en ENARM
    Diseñado para primera vez en examen nacional
    """
    
    def __init__(self):
        self.nivel_inicial = 15  # 15% conocimiento actual
        self.objetivo_final = 85  # 85% score ENARM (realista para primera vez)
        self.tiempo_total = 180  # 6 meses = 180 días
        self.horas_diarias_disponibles = 8  # 8 horas estudio/día
        
    def analisis_situacion_inicial(self):
        """Análisis completo de la situación inicial"""
        return {
            'conocimiento_actual': {
                'medicina_interna': 10,     # 10%
                'cirugia': 15,             # 15%
                'ginecologia': 20,         # 20%
                'pediatria': 12,           # 12%
                'urgencias': 18,           # 18%
                'salud_publica': 8,        # 8%
                'promedio_general': 15     # 15%
            },
            'coeficientes_ecuacion_inicial': {
                'A_conocimiento': 0.15,     # MUY BAJO
                'B_practica': 0.20,         # MUY BAJO  
                'C_diferenciacion': 0.25,   # BAJO
                'D_dificultad': 0.10,       # CRÍTICO
                'T_trampas': 0.15,          # MUY BAJO
                'V_velocidad': 0.30         # BAJO
            },
            'score_predicho_inicial': 12,   # 12/100 puntos
            'areas_criticas': [
                'Fundamentos médicos básicos',
                'Interpretación casos clínicos',
                'Diferenciación diagnóstica',
                'Manejo de emergencias',
                'NOMs y protocolos'
            ]
        }
    
    def plan_por_fases(self):
        """Plan dividido en 6 fases de 30 días cada una"""
        return {
            'FASE_1_FUNDAMENTOS': {
                'dias': '1-30',
                'objetivo': 'Establecer base sólida - Llegar a 35% conocimiento',
                'coeficientes_objetivo': {
                    'A_conocimiento': 0.35,
                    'B_practica': 0.40,
                    'C_diferenciacion': 0.30,
                    'D_dificultad': 0.20,
                    'T_trampas': 0.25,
                    'V_velocidad': 0.35
                },
                'score_objetivo': 28,
                'actividades_diarias': [
                    '4 horas: Estudio teórico fundamentos',
                    '2 horas: Preguntas básicas (50-70/día)',
                    '1 hora: Revisión errores y conceptos',
                    '1 hora: Memorización datos clave'
                ],
                'recursos_principales': [
                    'Manual CTO completo (lectura secuencial)',
                    'Banco preguntas básicas ENARM',
                    'Fichas resumen por especialidad',
                    'Videos explicativos fundamentos'
                ],
                'metricas_semanales': {
                    'preguntas_contestadas': 350,
                    'porcentaje_aciertos_minimo': 35,
                    'temas_completados': 8,
                    'horas_estudio_efectivo': 56
                }
            },
            
            'FASE_2_CONSOLIDACION': {
                'dias': '31-60', 
                'objetivo': 'Consolidar conocimientos - Llegar a 50% conocimiento',
                'coeficientes_objetivo': {
                    'A_conocimiento': 0.50,
                    'B_practica': 0.55,
                    'C_diferenciacion': 0.45,
                    'D_dificultad': 0.30,
                    'T_trampas': 0.40,
                    'V_velocidad': 0.45
                },
                'score_objetivo': 42,
                'actividades_diarias': [
                    '3 horas: Estudio teórico avanzado',
                    '3 horas: Preguntas intermedias (70-100/día)',
                    '1 hora: Casos clínicos básicos',
                    '1 hora: Análisis errores y patrones'
                ],
                'enfoque_especial': [
                    'Diferenciación entre especialidades',
                    'Casos clínicos estructurados',
                    'Primeras técnicas anti-trampas',
                    'Interpretación estudios básicos'
                ]
            },
            
            'FASE_3_ESPECIALIZACION': {
                'dias': '61-90',
                'objetivo': 'Especialización por áreas - Llegar a 65% conocimiento', 
                'coeficientes_objetivo': {
                    'A_conocimiento': 0.65,
                    'B_practica': 0.70,
                    'C_diferenciacion': 0.60,
                    'D_dificultad': 0.45,
                    'T_trampas': 0.55,
                    'V_velocidad': 0.55
                },
                'score_objetivo': 58,
                'actividades_diarias': [
                    '2 horas: Estudio especializado por área',
                    '3 horas: Preguntas avanzadas (80-120/día)',
                    '2 horas: Casos clínicos complejos', 
                    '1 hora: Entrenamiento anti-trampas'
                ],
                'especializacion_semanal': {
                    'lunes': 'Medicina Interna profunda',
                    'martes': 'Cirugía y urgencias',
                    'miercoles': 'Ginecología y obstetricia',
                    'jueves': 'Pediatría y neonatología',
                    'viernes': 'Salud pública y epidemiología',
                    'sabado': 'Integración y casos complejos',
                    'domingo': 'Repaso debilidades detectadas'
                }
            },
            
            'FASE_4_PERFECCIONAMIENTO': {
                'dias': '91-120',
                'objetivo': 'Perfeccionar técnica - Llegar a 75% conocimiento',
                'coeficientes_objetivo': {
                    'A_conocimiento': 0.75,
                    'B_practica': 0.80,
                    'C_diferenciacion': 0.75,
                    'D_dificultad': 0.60,
                    'T_trampas': 0.70,
                    'V_velocidad': 0.70
                },
                'score_objetivo': 70,
                'actividades_diarias': [
                    '1 hora: Repaso teórico dirigido',
                    '4 horas: Simulacros y preguntas difíciles',
                    '2 horas: Análisis profundo errores',
                    '1 hora: Optimización velocidad'
                ],
                'simulacros_semanales': {
                    'simulacros_completos': 2,
                    'mini_examenes_diarios': 7,
                    'analisis_exhaustivo_errores': 'Obligatorio',
                    'cronometraje_estricto': 'Implementado'
                }
            },
            
            'FASE_5_OPTIMIZACION': {
                'dias': '121-150',
                'objetivo': 'Optimización final - Llegar a 85% conocimiento',
                'coeficientes_objetivo': {
                    'A_conocimiento': 0.85,
                    'B_practica': 0.85,
                    'C_diferenciacion': 0.85,
                    'D_dificultad': 0.75,
                    'T_trampas': 0.85,
                    'V_velocidad': 0.80
                },
                'score_objetivo': 82,
                'actividades_diarias': [
                    '3 horas: Simulacros cronometrados',
                    '2 horas: Casos clínicos extremos',
                    '2 horas: Perfección anti-trampas',
                    '1 hora: Ajustes velocidad-precisión'
                ],
                'entrenamiento_avanzado': [
                    'Simulacros en condiciones reales de examen',
                    'Preguntas tipo "nunca vistas antes"',
                    'Casos clínicos con múltiples variables',
                    'Entrenamiento psicológico bajo presión'
                ]
            },
            
            'FASE_6_MAESTRIA': {
                'dias': '151-180',
                'objetivo': 'Lograr maestría - 90%+ conocimiento para 85+ score',
                'coeficientes_objetivo': {
                    'A_conocimiento': 0.90,
                    'B_practica': 0.90,
                    'C_diferenciacion': 0.90,
                    'D_dificultad': 0.85,
                    'T_trampas': 0.95,
                    'V_velocidad': 0.90
                },
                'score_objetivo': 88,
                'actividades_diarias': [
                    '4 horas: Simulacros oficiales',
                    '2 horas: Casos ultra-complejos',
                    '1 hora: Perfección pura',
                    '1 hora: Preparación psicológica'
                ],
                'preparacion_final': [
                    'Simulacros diarios tipo ENARM real',
                    'Cronometraje perfecto (90 seg/pregunta)',
                    'Zero tolerance para errores evitables',
                    'Confianza psicológica máxima'
                ]
            }
        }
    
    def recursos_por_fase(self):
        """Recursos específicos para cada fase del plan"""
        return {
            'FASE_1': {
                'libros': [
                    'Manual CTO - Lectura completa secuencial',
                    'Harrison Principios Medicina Interna (consulta)',
                    'Fichas resumen especialidades'
                ],
                'digitales': [
                    'App preguntas básicas ENARM',
                    'Videos YouTube fundamentos médicos',
                    'Flashcards digitales Anki',
                    'Simuladores básicos online'
                ],
                'metodologia': 'Construcción base - Cantidad sobre calidad inicial'
            },
            
            'FASE_2': {
                'libros': [
                    'Manual CTO - Segunda pasada enfocada',
                    'Casos clínicos básicos por especialidad',
                    'Guías clínicas principales'
                ],
                'digitales': [
                    'Banco preguntas intermedias',
                    'Simuladores casos clínicos',
                    'Apps diferenciación diagnóstica'
                ],
                'metodologia': 'Consolidación - Calidad mejorando'
            },
            
            'FASE_3': {
                'libros': [
                    'Libros especializados por área',
                    'Protocolos y guías oficiales',
                    'NOMs actualizadas'
                ],
                'digitales': [
                    'Bancos preguntas especializados',
                    'Simuladores avanzados',
                    'Plataformas casos reales'
                ],
                'metodologia': 'Especialización - Profundidad sobre amplitud'
            },
            
            'FASE_4-6': {
                'libros': [
                    'Compendios ENARM años anteriores',
                    'Casos clínicos complejos',
                    'Actualizaciones recientes'
                ],
                'digitales': [
                    'Simulacros oficiales ENARM',
                    'Plataformas premium',
                    'IA para detección debilidades'
                ],
                'metodologia': 'Perfección - Precisión sobre velocidad inicial'
            }
        }
    
    def cronograma_diario_tipo(self, fase):
        """Cronograma diario detallado por fase"""
        cronogramas = {
            'FASE_1': {
                '06:00-07:00': 'Despertar, ejercicio ligero, desayuno',
                '07:00-11:00': 'Estudio teórico intensivo (4h)',
                '11:00-11:30': 'Descanso activo',
                '11:30-13:30': 'Preguntas básicas + revisión (2h)',
                '13:30-14:30': 'Almuerzo y descanso',
                '14:30-15:30': 'Análisis errores y conceptos (1h)',
                '15:30-16:00': 'Descanso',
                '16:00-17:00': 'Memorización y repaso (1h)',
                '17:00-18:00': 'Ejercicio físico',
                '18:00-19:00': 'Cena',
                '19:00-21:00': 'Tiempo libre / social',
                '21:00-22:00': 'Repaso ligero del día',
                '22:00': 'Dormir (8h sueño)'
            },
            
            'FASE_3': {
                '06:00-07:00': 'Despertar, ejercicio, desayuno',
                '07:00-09:00': 'Estudio especializado (2h)',
                '09:00-12:00': 'Preguntas avanzadas (3h)', 
                '12:00-12:30': 'Descanso',
                '12:30-14:30': 'Casos clínicos complejos (2h)',
                '14:30-15:30': 'Almuerzo',
                '15:30-16:30': 'Entrenamiento anti-trampas (1h)',
                '16:30-17:00': 'Descanso',
                '17:00-18:00': 'Ejercicio físico',
                '18:00-19:00': 'Cena',
                '19:00-21:00': 'Tiempo libre',
                '21:00-22:00': 'Repaso y planificación',
                '22:00': 'Dormir'
            },
            
            'FASE_6': {
                '06:00-07:00': 'Despertar, ejercicio, desayuno',
                '07:00-11:00': 'Simulacros oficiales (4h)',
                '11:00-11:30': 'Descanso',
                '11:30-13:30': 'Casos ultra-complejos (2h)',
                '13:30-14:30': 'Almuerzo',
                '14:30-15:30': 'Perfección técnica (1h)',
                '15:30-16:30': 'Preparación psicológica (1h)',
                '16:30-17:00': 'Descanso',
                '17:00-18:00': 'Ejercicio físico',
                '18:00-19:00': 'Cena',
                '19:00-21:00': 'Tiempo libre / relajación',
                '21:00-22:00': 'Visualización y confianza',
                '22:00': 'Dormir'
            }
        }
        return cronogramas.get(fase, cronogramas['FASE_1'])
    
    def metricas_seguimiento(self):
        """Sistema de métricas para seguimiento del progreso"""
        return {
            'metricas_diarias': {
                'horas_estudio_efectivo': 'meta_8h',
                'preguntas_contestadas': 'segun_fase',
                'porcentaje_aciertos': 'objetivo_por_fase',
                'conceptos_nuevos_aprendidos': 'min_5_diarios',
                'errores_analizados': 'todos_obligatorio'
            },
            
            'metricas_semanales': {
                'simulacro_completo': 'min_1_semanal',
                'progreso_coeficientes_ecuacion': 'medicion_objetiva',
                'areas_debiles_identificadas': 'max_3_por_semana',
                'plan_ajustes_necesarios': 'revision_obligatoria'
            },
            
            'metricas_mensuales': {
                'score_ecuacion_general': 'aumento_minimo_15_puntos',
                'simulacro_completo_cronometrado': 'obligatorio',
                'evaluacion_integral_progreso': 'con_ajustes_plan',
                'preparacion_psicologica': 'nivel_confianza_medido'
            },
            
            'indicadores_alarma': {
                'score_sin_mejora_2_semanas': 'CRITICO',
                'porcentaje_aciertos_disminuye': 'REVISAR_METODO',
                'horas_estudio_menos_6h_diarias': 'INSUFICIENTE',
                'errores_repetitivos_misma_area': 'CAMBIAR_ENFOQUE'
            }
        }
    
    def estrategias_especificas_primera_vez(self):
        """Estrategias específicas para primera vez en examen nacional"""
        return {
            'psicologicas': {
                'manejo_ansiedad': [
                    'Técnicas respiración durante estudio',
                    'Visualización éxito en examen',
                    'Simulacros en condiciones reales',
                    'Rutina pre-examen establecida'
                ],
                'construccion_confianza': [
                    'Celebrar pequeños logros diarios',
                    'Tracking progreso visible',
                    'Grupo apoyo estudiantes ENARM',
                    'Mentalidad "ya estoy preparado"'
                ]
            },
            
            'tecnicas_examen': {
                'lectura_pregunta': [
                    'Leer pregunta completa antes opciones',
                    'Identificar palabras clave críticas',
                    'Buscar pistas en enunciado',
                    'Cuidado con negaciones y excepciones'
                ],
                'manejo_tiempo': [
                    '90 segundos promedio por pregunta',
                    'Marcar dudas para revisión final',
                    'No obsesionarse con preguntas difíciles',
                    'Reservar tiempo para repaso'
                ],
                'eliminacion_opciones': [
                    'Descartar obviamente incorrectas',
                    'Buscar la opción MÁS correcta',
                    'Cuidado con absolutismos',
                    'Confiar en primer instinto educado'
                ]
            },
            
            'adaptaciones_primera_vez': {
                'fase_inicial_extendida': [
                    'Más tiempo en fundamentos básicos',
                    'No apresurarse a casos complejos',
                    'Base sólida antes de especialización',
                    'Paciencia con progreso inicial lento'
                ],
                'soporte_adicional': [
                    'Mentor o tutor experimentado',
                    'Grupo estudio con veteranos',
                    'Cursos presenciales si es necesario',
                    'Apoyo psicológico profesional'
                ]
            }
        }
    
    def plan_contingencia(self):
        """Planes de contingencia para diferentes escenarios"""
        return {
            'progreso_lento': {
                'si_score_menor_esperado': [
                    'Extender fase actual 15 días',
                    'Aumentar horas estudio diario +2h',
                    'Cambiar método de estudio',
                    'Buscar tutor especializado'
                ],
                'identificacion_problema': [
                    'Análisis detallado puntos débiles',
                    'Revisión método estudio actual',
                    'Evaluación factores externos',
                    'Ajuste expectativas realistas'
                ]
            },
            
            'progreso_excepcional': {
                'si_score_mayor_esperado': [
                    'Acelerar a siguiente fase',
                    'Introducir contenido más avanzado',
                    'Añadir simulacros adicionales',
                    'Preparar para score >90'
                ]
            },
            
            'emergencias': {
                'problemas_salud': 'Plan reducido mantenimiento',
                'problemas_familiares': 'Flexibilidad horarios',
                'problemas_economicos': 'Recursos gratuitos alternativos',
                'burnout_estudio': 'Descanso planificado 3-5 días'
            }
        }

# Función principal para generar plan personalizado
def generar_plan_personalizado(conocimiento_actual=15, tiempo_disponible=180, horas_diarias=8):
    """
    Genera plan de estudio personalizado basado en parámetros específicos
    """
    plan = PlanENARM15a100()
    
    # Ajustar plan según parámetros
    if conocimiento_actual < 10:
        # Extender Fase 1
        print("⚠️  Conocimiento muy bajo - Plan extendido recomendado")
    elif conocimiento_actual > 25:
        # Acelerar inicio
        print("✅ Conocimiento base bueno - Inicio acelerado posible")
    
    if tiempo_disponible < 120:
        print("🚨 Tiempo insuficiente - Plan intensivo necesario")
    elif tiempo_disponible > 240:
        print("😊 Tiempo amplio - Plan relajado posible")
    
    return {
        'plan_fases': plan.plan_por_fases(),
        'recursos': plan.recursos_por_fase(),
        'metricas': plan.metricas_seguimiento(),
        'estrategias': plan.estrategias_especificas_primera_vez(),
        'contingencia': plan.plan_contingencia()
    }

if __name__ == "__main__":
    # Ejemplo de uso
    plan_completo = generar_plan_personalizado(
        conocimiento_actual=15,
        tiempo_disponible=180, 
        horas_diarias=8
    )
    
    print("🎯 PLAN DE ESTUDIO GENERADO:")
    print(f"📈 Objetivo: 15% → 85% en 180 días")
    print(f"⏰ Dedicación: 8 horas diarias")
    print(f"🏆 Score final esperado: 85+ puntos ENARM")