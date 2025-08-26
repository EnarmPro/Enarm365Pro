"""
CRONOGRAMA DETALLADO 180 DÍAS: DE 15% CONOCIMIENTO A 85+ SCORE ENARM
Plan día a día para primera vez en examen nacional
"""

from datetime import datetime, timedelta
import json

class CronogramaENARM180Dias:
    """
    Cronograma detallado día por día para 180 días de preparación ENARM
    Desde 15% conocimiento hasta 85+ score en examen
    """
    
    def __init__(self, fecha_inicio="2024-03-01", fecha_examen="2024-08-28"):
        self.fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        self.fecha_examen = datetime.strptime(fecha_examen, "%Y-%m-%d")
        self.dias_totales = (self.fecha_examen - self.fecha_inicio).days
        
        # División por fases
        self.fase_1 = 45  # Fundamentos extendidos
        self.fase_2 = 35  # Consolidación + técnica
        self.fase_3 = 40  # Especialización guiada
        self.fase_4 = 30  # Perfeccionamiento
        self.fase_5 = 20  # Optimización
        self.fase_6 = 7   # Preparación final
        # Total: 177 días (3 días buffer)
    
    def generar_cronograma_completo(self):
        """Genera cronograma día a día completo"""
        cronograma = {}
        fecha_actual = self.fecha_inicio
        
        # FASE 1: Días 1-45 - FUNDAMENTOS EXTENDIDOS
        for dia in range(1, self.fase_1 + 1):
            cronograma[dia] = self.generar_dia_fase_1(dia, fecha_actual)
            fecha_actual += timedelta(days=1)
        
        # FASE 2: Días 46-80 - CONSOLIDACIÓN + TÉCNICA
        for dia in range(self.fase_1 + 1, self.fase_1 + self.fase_2 + 1):
            cronograma[dia] = self.generar_dia_fase_2(dia, fecha_actual)
            fecha_actual += timedelta(days=1)
        
        # FASE 3: Días 81-120 - ESPECIALIZACIÓN GUIADA  
        for dia in range(self.fase_1 + self.fase_2 + 1, self.fase_1 + self.fase_2 + self.fase_3 + 1):
            cronograma[dia] = self.generar_dia_fase_3(dia, fecha_actual)
            fecha_actual += timedelta(days=1)
            
        # FASE 4: Días 121-150 - PERFECCIONAMIENTO
        for dia in range(self.fase_1 + self.fase_2 + self.fase_3 + 1, 
                        self.fase_1 + self.fase_2 + self.fase_3 + self.fase_4 + 1):
            cronograma[dia] = self.generar_dia_fase_4(dia, fecha_actual)
            fecha_actual += timedelta(days=1)
        
        # FASE 5: Días 151-170 - OPTIMIZACIÓN
        for dia in range(self.fase_1 + self.fase_2 + self.fase_3 + self.fase_4 + 1,
                        self.fase_1 + self.fase_2 + self.fase_3 + self.fase_4 + self.fase_5 + 1):
            cronograma[dia] = self.generar_dia_fase_5(dia, fecha_actual)
            fecha_actual += timedelta(days=1)
        
        # FASE 6: Días 171-177 - PREPARACIÓN FINAL
        for dia in range(self.fase_1 + self.fase_2 + self.fase_3 + self.fase_4 + self.fase_5 + 1, 178):
            cronograma[dia] = self.generar_dia_fase_6(dia, fecha_actual)
            fecha_actual += timedelta(days=1)
        
        return cronograma
    
    def generar_dia_fase_1(self, dia, fecha):
        """FASE 1: Fundamentos Extendidos (Días 1-45)"""
        dia_semana = fecha.weekday()  # 0=Lunes, 6=Domingo
        
        # Temario rotativo semanal
        temas_por_dia = {
            0: "Medicina Interna - Fundamentos",    # Lunes
            1: "Cirugía General - Básico",          # Martes  
            2: "Ginecología - Fundamentos",         # Miércoles
            3: "Pediatría - Básico",                # Jueves
            4: "Urgencias - Conceptos Base",        # Viernes
            5: "Salud Pública - NOMs Básicas",      # Sábado
            6: "REPASO SEMANAL + SIMULACRO"         # Domingo
        }
        
        tema_del_dia = temas_por_dia[dia_semana]
        
        if dia_semana == 6:  # Domingo - día especial
            horario = {
                "06:00-07:00": "Despertar y ejercicio ligero",
                "07:00-08:00": "Desayuno y preparación",
                "08:00-11:00": "SIMULACRO SEMANAL (50 preguntas cronometradas)",
                "11:00-11:30": "Descanso",
                "11:30-13:30": "Análisis exhaustivo simulacro",
                "13:30-14:30": "Almuerzo",
                "14:30-16:30": "Repaso temas débiles identificados",
                "16:30-17:00": "Descanso",
                "17:00-18:00": "Ejercicio físico",
                "18:00-19:00": "Cena",
                "19:00-21:00": "Tiempo libre / social",
                "21:00-22:00": "Planificación semana siguiente",
                "22:00": "Dormir"
            }
        else:  # Lunes a Sábado - días normales
            horario = {
                "06:00-07:00": "Despertar y ejercicio ligero",
                "07:00-08:00": "Desayuno y revisión día anterior",
                "08:00-13:00": f"Estudio teórico intensivo: {tema_del_dia} (5h)",
                "13:00-14:00": "Almuerzo y descanso",
                "14:00-16:00": "Preguntas básicas tema del día (40-60 preguntas)",
                "16:00-16:30": "Descanso activo",
                "16:30-17:30": "Análisis errores y conceptos no claros",
                "17:30-18:00": "Memorización datos clave del día",
                "18:00-19:00": "Ejercicio físico",
                "19:00-20:00": "Cena",
                "20:00-21:00": "Tiempo libre / social",
                "21:00-22:00": "Repaso ligero y planificación mañana",
                "22:00": "Dormir (8h mínimo)"
            }
        
        # Metas específicas por día
        if dia <= 15:
            meta_aciertos = "25-35%"
            enfoque = "Familiarización con formato preguntas"
        elif dia <= 30:
            meta_aciertos = "35-45%" 
            enfoque = "Consolidación conceptos básicos"
        else:
            meta_aciertos = "45-55%"
            enfoque = "Preparación transición Fase 2"
        
        return {
            "fecha": fecha.strftime("%Y-%m-%d"),
            "dia_numero": dia,
            "fase": "FASE 1 - FUNDAMENTOS",
            "tema_principal": tema_del_dia,
            "horario_detallado": horario,
            "meta_aciertos": meta_aciertos,
            "enfoque_especial": enfoque,
            "recursos_dia": self.recursos_fase_1(tema_del_dia),
            "metricas_seguimiento": {
                "horas_estudio_objetivo": 8,
                "preguntas_minimas": 40 if dia_semana != 6 else 50,
                "conceptos_nuevos_objetivo": 5,
                "paginas_lectura": 50 if dia_semana != 6 else 0
            }
        }
    
    def generar_dia_fase_2(self, dia, fecha):
        """FASE 2: Consolidación + Técnica (Días 46-80)"""
        dia_semana = fecha.weekday()
        
        temas_por_dia = {
            0: "Medicina Interna - Intermedio + Técnica",
            1: "Cirugía - Casos Clínicos Básicos",
            2: "Ginecología - Especialización + Anti-trampas", 
            3: "Pediatría - Avanzado + Velocidad",
            4: "Urgencias - Casos Complejos + Cronometraje",
            5: "Integración Multi-especialidad",
            6: "SIMULACROS DOBLES + ANÁLISIS PROFUNDO"
        }
        
        tema_del_dia = temas_por_dia[dia_semana]
        
        if dia_semana == 6:  # Domingo - simulacros intensivos
            horario = {
                "06:00-07:00": "Despertar y ejercicio",
                "07:00-08:00": "Desayuno",
                "08:00-10:30": "SIMULACRO 1 - Completo (100 preguntas)",
                "10:30-11:00": "Descanso",
                "11:00-13:00": "Análisis detallado Simulacro 1",
                "13:00-14:00": "Almuerzo",
                "14:00-16:30": "SIMULACRO 2 - Completo (100 preguntas)",
                "16:30-17:00": "Descanso",
                "17:00-19:00": "Análisis comparativo ambos simulacros",
                "19:00-20:00": "Cena",
                "20:00-21:00": "Identificación patrones debilidades",
                "21:00-22:00": "Plan ajustes semana siguiente",
                "22:00": "Dormir"
            }
        else:  # Lunes a Sábado
            horario = {
                "06:00-07:00": "Despertar y ejercicio",
                "07:00-08:00": "Desayuno + repaso rápido conceptos",
                "08:00-11:00": f"Estudio avanzado: {tema_del_dia} (3h)",
                "11:00-11:30": "Descanso",
                "11:30-14:30": "Preguntas intermedias cronometradas (80-100 preguntas)",
                "14:30-15:30": "Almuerzo",
                "15:30-16:30": "Casos clínicos básicos tema del día",
                "16:30-17:30": "Análisis errores + técnicas anti-trampas",
                "17:30-18:00": "Práctica velocidad lectora preguntas",
                "18:00-19:00": "Ejercicio físico",
                "19:00-20:00": "Cena",
                "20:00-21:00": "Tiempo libre",
                "21:00-22:00": "Repaso técnicas aprendidas",
                "22:00": "Dormir"
            }
        
        # Progresión de metas
        dias_en_fase = dia - self.fase_1
        if dias_en_fase <= 12:
            meta_aciertos = "50-60%"
            enfoque = "Desarrollo técnica examen básica"
        elif dias_en_fase <= 24:
            meta_aciertos = "60-70%"
            enfoque = "Consolidación conocimientos + velocidad"
        else:
            meta_aciertos = "70-75%"
            enfoque = "Preparación especialización"
        
        return {
            "fecha": fecha.strftime("%Y-%m-%d"),
            "dia_numero": dia,
            "fase": "FASE 2 - CONSOLIDACIÓN + TÉCNICA",
            "tema_principal": tema_del_dia,
            "horario_detallado": horario,
            "meta_aciertos": meta_aciertos,
            "enfoque_especial": enfoque,
            "recursos_dia": self.recursos_fase_2(tema_del_dia),
            "metricas_seguimiento": {
                "horas_estudio_objetivo": 8,
                "preguntas_minimas": 80 if dia_semana != 6 else 200,
                "casos_clinicos_objetivo": 5,
                "tecnicas_anti_trampas": 3
            }
        }
    
    def generar_dia_fase_3(self, dia, fecha):
        """FASE 3: Especialización Guiada (Días 81-120)"""
        dia_semana = fecha.weekday()
        
        # Especialización profunda por día
        especializaciones = {
            0: "MEDICINA INTERNA PROFUNDA",
            1: "CIRUGÍA + URGENCIAS INTEGRADAS", 
            2: "GINECOLOGÍA + OBSTETRICIA AVANZADA",
            3: "PEDIATRÍA + NEONATOLOGÍA",
            4: "SALUD PÚBLICA + EPIDEMIOLOGÍA",
            5: "INTEGRACIÓN CASOS COMPLEJOS",
            6: "SIMULACROS ESPECIALIZADOS + MENTORÍA"
        }
        
        tema_del_dia = especializaciones[dia_semana]
        
        if dia_semana == 6:  # Domingo - mentoría y simulacros especializados
            horario = {
                "06:00-07:00": "Despertar y ejercicio",
                "07:00-08:00": "Desayuno",
                "08:00-10:00": "Simulacro especializado (tema débil semanal)",
                "10:00-11:00": "Sesión con mentor - análisis simulacro",
                "11:00-11:30": "Descanso",
                "11:30-13:00": "Trabajo grupal casos complejos",
                "13:00-14:00": "Almuerzo",
                "14:00-16:00": "Simulacro general cronometrado",
                "16:00-17:00": "Análisis grupal con veteranos",
                "17:00-18:00": "Ejercicio físico",
                "18:00-19:00": "Cena",
                "19:00-20:00": "Tiempo libre",
                "20:00-21:00": "Planificación individual semanal",
                "21:00-22:00": "Preparación mental - visualización",
                "22:00": "Dormir"
            }
        else:  # Lunes a Viernes - especialización profunda
            horario = {
                "06:00-07:00": "Despertar y ejercicio",
                "07:00-08:00": "Desayuno + revisión plan día",
                "08:00-10:00": f"Estudio especializado profundo: {tema_del_dia}",
                "10:00-10:30": "Descanso",
                "10:30-13:30": "Preguntas avanzadas especialidad (100-120 preguntas)",
                "13:30-14:30": "Almuerzo",
                "14:30-16:30": "Casos clínicos complejos especialidad",
                "16:30-17:00": "Descanso",
                "17:00-17:30": "Entrenamiento anti-trampas avanzado",
                "17:30-18:00": "Optimización velocidad específica",
                "18:00-19:00": "Ejercicio físico",
                "19:00-20:00": "Cena",
                "20:00-21:00": "Tiempo libre",
                "21:00-22:00": "Repaso activo del día + notas",
                "22:00": "Dormir"
            }
        
        # Metas progresivas Fase 3
        dias_en_fase = dia - (self.fase_1 + self.fase_2)
        if dias_en_fase <= 15:
            meta_aciertos = "70-78%"
            enfoque = "Especialización inicial profunda"
        elif dias_en_fase <= 30:
            meta_aciertos = "78-82%"
            enfoque = "Dominio especializado + integración"
        else:
            meta_aciertos = "82-85%"
            enfoque = "Preparación perfeccionamiento"
        
        return {
            "fecha": fecha.strftime("%Y-%m-%d"),
            "dia_numero": dia,
            "fase": "FASE 3 - ESPECIALIZACIÓN GUIADA",
            "tema_principal": tema_del_dia,
            "horario_detallado": horario,
            "meta_aciertos": meta_aciertos,
            "enfoque_especial": enfoque,
            "recursos_dia": self.recursos_fase_3(tema_del_dia),
            "metricas_seguimiento": {
                "horas_estudio_objetivo": 8,
                "preguntas_minimas": 100 if dia_semana != 6 else 150,
                "casos_clinicos_objetivo": 8,
                "tecnicas_avanzadas": 5
            }
        }
    
    def generar_dia_fase_4(self, dia, fecha):
        """FASE 4: Perfeccionamiento (Días 121-150)"""
        dia_semana = fecha.weekday()
        
        if dia_semana == 6:  # Domingo - simulacros completos
            horario = {
                "06:00-07:00": "Despertar y ejercicio",
                "07:00-08:00": "Desayuno ligero",
                "08:00-12:00": "SIMULACRO COMPLETO OFICIAL (condiciones reales)",
                "12:00-13:00": "Descanso y almuerzo ligero",
                "13:00-15:00": "Análisis exhaustivo cada pregunta",
                "15:00-16:00": "Identificación patrones errores",
                "16:00-17:00": "Ejercicio relajante",
                "17:00-18:00": "Cena temprana",
                "18:00-20:00": "Tiempo libre - NO estudiar",
                "20:00-21:00": "Relajación y preparación semana",
                "21:00-22:00": "Lectura ligera - NO médica",
                "22:00": "Dormir"
            }
        else:  # Lunes a Sábado - perfeccionamiento
            horario = {
                "06:00-07:00": "Despertar y ejercicio",
                "07:00-08:00": "Desayuno + mentalización día",
                "08:00-09:00": "Repaso teórico dirigido (solo debilidades)",
                "09:00-13:00": "Simulacros parciales cronometrados (4 bloques 50 preguntas)",
                "13:00-14:00": "Almuerzo",
                "14:00-16:00": "Análisis profundo errores cada bloque",
                "16:00-17:00": "Optimización velocidad-precisión",
                "17:00-17:30": "Técnicas relajación durante examen",
                "17:30-18:00": "Descanso",
                "18:00-19:00": "Ejercicio físico",
                "19:00-20:00": "Cena",
                "20:00-21:00": "Tiempo libre",
                "21:00-22:00": "Visualización éxito + relajación",
                "22:00": "Dormir"
            }
        
        dias_en_fase = dia - (self.fase_1 + self.fase_2 + self.fase_3)
        meta_aciertos = "83-87%"
        enfoque = "Perfección técnica + preparación psicológica"
        
        return {
            "fecha": fecha.strftime("%Y-%m-%d"),
            "dia_numero": dia,
            "fase": "FASE 4 - PERFECCIONAMIENTO",
            "tema_principal": "SIMULACROS + PERFECCIÓN TÉCNICA",
            "horario_detallado": horario,
            "meta_aciertos": meta_aciertos,
            "enfoque_especial": enfoque,
            "recursos_dia": self.recursos_fase_4(),
            "metricas_seguimiento": {
                "horas_estudio_objetivo": 7,  # Menos horas, más eficiencia
                "preguntas_simulacro": 200 if dia_semana != 6 else 400,
                "precision_objetivo": 85,
                "velocidad_objetivo": "90 seg/pregunta"
            }
        }
    
    def generar_dia_fase_5(self, dia, fecha):
        """FASE 5: Optimización Final (Días 151-170)"""
        dia_semana = fecha.weekday()
        
        horario = {
            "06:00-07:00": "Despertar y ejercicio suave",
            "07:00-08:00": "Desayuno nutritivo",
            "08:00-12:00": "SIMULACRO OFICIAL DIARIO (condiciones exactas examen)",
            "12:00-13:00": "Análisis rápido errores críticos únicamente",
            "13:00-14:00": "Almuerzo relajado",
            "14:00-15:00": "Repaso ultra-ligero (solo datos clave)",
            "15:00-16:00": "Técnicas manejo estrés examen",
            "16:00-17:00": "Ejercicio relajante (yoga, caminata)",
            "17:00-18:00": "Preparación mental y confianza",
            "18:00-19:00": "Cena",
            "19:00-20:30": "Tiempo libre - actividades placenteras",
            "20:30-21:30": "Relajación profunda",
            "21:30-22:00": "Preparación sueño reparador",
            "22:00": "Dormir (9h mínimo)"
        }
        
        return {
            "fecha": fecha.strftime("%Y-%m-%d"),
            "dia_numero": dia,
            "fase": "FASE 5 - OPTIMIZACIÓN FINAL",
            "tema_principal": "SIMULACROS OFICIALES + PREPARACIÓN MENTAL",
            "horario_detallado": horario,
            "meta_aciertos": "85-88%",
            "enfoque_especial": "Mantenimiento nivel + confianza máxima",
            "recursos_dia": self.recursos_fase_5(),
            "metricas_seguimiento": {
                "horas_estudio_objetivo": 6,  # Reducir para evitar burnout
                "simulacros_oficiales": 1,
                "precision_minima": 85,
                "nivel_confianza": "Alto"
            }
        }
    
    def generar_dia_fase_6(self, dia, fecha):
        """FASE 6: Preparación Final (Días 171-177)"""
        dias_restantes = 178 - dia
        
        if dias_restantes > 3:  # Días 4-7 antes del examen
            horario = {
                "06:00-07:00": "Despertar natural (sin alarma si es posible)",
                "07:00-08:30": "Desayuno tranquilo + rutina relajante",
                "08:30-10:30": "Repaso ultra-ligero (solo fichas resumen)",
                "10:30-11:00": "Descanso",
                "11:00-12:00": "Visualización éxito en examen",
                "12:00-13:00": "Almuerzo",
                "13:00-14:00": "Siesta reparadora",
                "14:00-15:00": "Ejercicio suave",
                "15:00-16:00": "Actividad placentera (música, lectura no médica)",
                "16:00-18:00": "Tiempo libre total",
                "18:00-19:00": "Cena nutritiva",
                "19:00-21:00": "Actividad social relajante",
                "21:00-22:00": "Rutina preparación sueño",
                "22:00": "Dormir temprano"
            }
        else:  # Días 1-3 antes del examen
            horario = {
                "06:00-07:00": "Despertar con rutina exacta del día examen",
                "07:00-08:00": "Desayuno idéntico al planificado para examen",
                "08:00-09:00": "NO ESTUDIAR - Solo relajación",
                "09:00-12:00": "Actividades completamente ajenas al estudio",
                "12:00-13:00": "Almuerzo",
                "13:00-14:00": "Descanso",
                "14:00-16:00": "Preparativos logísticos examen",
                "16:00-18:00": "Ejercicio muy suave",
                "18:00-19:00": "Cena",
                "19:00-21:00": "Tiempo libre - NO pensar en examen",
                "21:00-21:30": "Rutina relajación",
                "21:30": "Dormir MUY temprano (10h+ sueño)"
            }
        
        return {
            "fecha": fecha.strftime("%Y-%m-%d"),
            "dia_numero": dia,
            "fase": "FASE 6 - PREPARACIÓN FINAL",
            "tema_principal": "RELAJACIÓN + PREPARACIÓN LOGÍSTICA",
            "horario_detallado": horario,
            "meta_aciertos": "Mantener nivel - NO evaluar",
            "enfoque_especial": "Descanso total + confianza absoluta",
            "recursos_dia": self.recursos_fase_6(),
            "metricas_seguimiento": {
                "horas_estudio_objetivo": 0 if dias_restantes <= 3 else 2,
                "horas_sueño_objetivo": 10,
                "nivel_relajacion": "Máximo",
                "preparacion_logistica": "Completa"
            }
        }
    
    def recursos_fase_1(self, tema):
        """Recursos específicos Fase 1"""
        recursos_base = {
            "libros": ["Manual CTO", "Fichas resumen especialidad"],
            "digital": ["App preguntas básicas", "Videos fundamentos"],
            "metodologia": "Lectura secuencial + preguntas básicas"
        }
        return recursos_base
    
    def recursos_fase_2(self, tema):
        """Recursos específicos Fase 2"""
        return {
            "libros": ["Manual CTO 2da pasada", "Casos clínicos básicos"],
            "digital": ["Simuladores casos", "Apps cronometraje"],
            "metodologia": "Casos clínicos + técnica anti-trampas"
        }
    
    def recursos_fase_3(self, tema):
        """Recursos específicos Fase 3"""
        return {
            "libros": ["Libros especializados", "Protocolos actualizados"],
            "digital": ["Bancos especializados", "Plataformas avanzadas"],
            "humanos": ["Mentor semanal", "Grupo veteranos"],
            "metodologia": "Especialización profunda + mentoría"
        }
    
    def recursos_fase_4(self):
        """Recursos específicos Fase 4"""
        return {
            "digital": ["Simulacros oficiales únicamente"],
            "tecnicas": ["Optimización velocidad", "Manejo estrés"],
            "metodologia": "Perfección técnica pura"
        }
    
    def recursos_fase_5(self):
        """Recursos específicos Fase 5"""
        return {
            "digital": ["Solo simulacros oficiales"],
            "tecnicas": ["Preparación mental", "Relajación"],
            "metodologia": "Mantenimiento + confianza"
        }
    
    def recursos_fase_6(self):
        """Recursos específicos Fase 6"""
        return {
            "digital": ["Ninguno - NO estudiar"],
            "tecnicas": ["Relajación total", "Visualización"],
            "metodologia": "Descanso absoluto"
        }
    
    def generar_reporte_semanal(self, semana):
        """Genera reporte de progreso semanal"""
        return {
            f"semana_{semana}": {
                "objetivos_cumplidos": "% completado",
                "areas_mejoradas": ["Lista de mejoras"],
                "areas_pendientes": ["Lista pendientes"],
                "ajustes_necesarios": ["Ajustes para próxima semana"],
                "nivel_confianza": "Escala 1-10",
                "prediccion_score": "Score estimado actual"
            }
        }

# Función para generar cronograma personalizado
def generar_cronograma_personalizado(fecha_inicio, fecha_examen, adaptaciones=None):
    """
    Genera cronograma personalizado basado en fechas específicas
    """
    cronograma = CronogramaENARM180Dias(fecha_inicio, fecha_examen)
    plan_completo = cronograma.generar_cronograma_completo()
    
    # Aplicar adaptaciones si las hay
    if adaptaciones:
        # Lógica para adaptar el plan según necesidades específicas
        pass
    
    return {
        "cronograma_completo": plan_completo,
        "resumen_fases": {
            "fase_1": f"Días 1-{cronograma.fase_1}: Fundamentos",
            "fase_2": f"Días {cronograma.fase_1+1}-{cronograma.fase_1+cronograma.fase_2}: Consolidación",
            "fase_3": f"Días {cronograma.fase_1+cronograma.fase_2+1}-{cronograma.fase_1+cronograma.fase_2+cronograma.fase_3}: Especialización",
            "fase_4": "Días siguientes: Perfeccionamiento",
            "fase_5": "Días siguientes: Optimización", 
            "fase_6": "Últimos 7 días: Preparación final"
        },
        "metricas_globales": {
            "total_dias": cronograma.dias_totales,
            "horas_estudio_total": 8 * cronograma.dias_totales * 0.85,  # Factor eficiencia
            "preguntas_estimadas_total": 25000,
            "simulacros_completos_total": 60,
            "score_objetivo_final": "85+ puntos"
        }
    }

if __name__ == "__main__":
    # Ejemplo de uso
    cronograma_personalizado = generar_cronograma_personalizado(
        fecha_inicio="2024-03-01",
        fecha_examen="2024-08-28"
    )
    
    print("📅 CRONOGRAMA DETALLADO GENERADO")
    print(f"🎯 Objetivo: 85+ puntos ENARM")
    print(f"📈 Progresión: 15% → 90% conocimiento")
    print(f"⏰ Duración: 180 días de preparación intensiva")