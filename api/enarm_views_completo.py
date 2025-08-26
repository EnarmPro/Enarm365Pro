from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from api.models import Preguntas, Respuestas, RegistroRespuestaPreguntas, Categorias
from api.mega_analizador_enarm import MegaAnalizadorENARM, GeneradorReportesENARM
from django.core.paginator import Paginator
import numpy as np
from io import BytesIO
import base64

try:
    import matplotlib
    matplotlib.use('Agg')  # Para evitar problemas con GUI
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

@login_required 
def mega_dashboard_enarm(request):
    """Dashboard principal con análisis completo ENARM"""
    
    generador = GeneradorReportesENARM()
    reporte_completo = generador.generar_reporte_completo(request.user.id)
    
    context = {
        'reporte': reporte_completo,
        'user': request.user,
        'titulo': '🎯 Mega Dashboard ENARM - Análisis Definitivo'
    }
    
    return render(request, 'Simulator/mega_dashboard.html', context)

@login_required
def analisis_errores_aciertos(request):
    """Vista detallada de análisis de errores vs aciertos"""
    
    analizador = MegaAnalizadorENARM()
    analisis = analizador.analisis_errores_aciertos_completo(request.user.id)
    
    # Generar gráfico de errores por categoría
    grafico_errores = generar_grafico_errores_categoria(analisis['por_categoria'])
    grafico_tendencias = generar_grafico_tendencias_hora(analisis['por_hora'])
    
    context = {
        'analisis': analisis,
        'grafico_errores': grafico_errores,
        'grafico_tendencias': grafico_tendencias,
        'titulo': '📊 Análisis Errores vs Aciertos'
    }
    
    return render(request, 'Simulator/analisis_errores.html', context)

@login_required
def temas_frecuencias(request):
    """Vista de temas más/menos vistos"""
    
    analizador = MegaAnalizadorENARM()
    temas_analisis = analizador.analisis_temas_frecuencias()
    
    # Paginación para temas más vistos
    paginator_mas = Paginator(temas_analisis['mas_vistos'], 20)
    page_mas = request.GET.get('page_mas', 1)
    temas_mas_paginados = paginator_mas.get_page(page_mas)
    
    # Paginación para temas menos vistos
    paginator_menos = Paginator(temas_analisis['menos_vistos'], 20)
    page_menos = request.GET.get('page_menos', 1)
    temas_menos_paginados = paginator_menos.get_page(page_menos)
    
    # Generar gráfico de distribución
    grafico_distribucion = generar_grafico_distribucion_frecuencias(temas_analisis)
    
    context = {
        'temas_analisis': temas_analisis,
        'temas_mas_vistos': temas_mas_paginados,
        'temas_menos_vistos': temas_menos_paginados,
        'grafico_distribucion': grafico_distribucion,
        'titulo': '📈 Análisis de Frecuencias de Temas'
    }
    
    return render(request, 'Simulator/temas_frecuencias.html', context)

@login_required
def detector_similitudes(request):
    """Vista del detector de materias similares"""
    
    analizador = MegaAnalizadorENARM()
    similitudes = analizador.detector_materias_similares()
    
    # Paginación para pares similares
    paginator = Paginator(similitudes['pares_muy_similares'], 10)
    page_number = request.GET.get('page', 1)
    pares_paginados = paginator.get_page(page_number)
    
    context = {
        'similitudes': similitudes,
        'pares_similares': pares_paginados,
        'grupos_tematicos': similitudes['grupos_tematicos'],
        'titulo': '🔍 Detector de Similitudes - Diferenciación Crítica'
    }
    
    return render(request, 'Simulator/detector_similitudes.html', context)

@login_required
def analizador_dificultad(request):
    """Vista del analizador de dificultad extrema"""
    
    analizador = MegaAnalizadorENARM()
    dificultad_analisis = analizador.analizador_dificultad_extrema()
    
    # Generar gráfico de patrones de dificultad
    grafico_patrones = generar_grafico_patrones_dificultad(dificultad_analisis)
    
    context = {
        'dificultad': dificultad_analisis,
        'grafico_patrones': grafico_patrones,
        'titulo': '⚡ Analizador de Dificultad Extrema'
    }
    
    return render(request, 'Simulator/analizador_dificultad.html', context)

@login_required
def detector_trampas(request):
    """Vista del detector de trampas"""
    
    analizador = MegaAnalizadorENARM()
    trampas_analisis = analizador.detector_trampas_estructuras()
    
    # Generar gráfico de tipos de trampa
    grafico_trampas = generar_grafico_tipos_trampa(trampas_analisis)
    
    context = {
        'trampas': trampas_analisis,
        'grafico_trampas': grafico_trampas,
        'titulo': '🕵️ Detector de Trampas y Estructuras Engañosas'
    }
    
    return render(request, 'Simulator/detector_trampas.html', context)

@login_required
def critica_100_puntos(request):
    """Vista del sistema de crítica para 100/100"""
    
    analizador = MegaAnalizadorENARM()
    critica = analizador.sistema_critica_perfecta(request.user.id)
    
    # Generar gráfico de progreso hacia 100
    grafico_progreso = generar_grafico_progreso_100(critica)
    
    context = {
        'critica': critica,
        'grafico_progreso': grafico_progreso,
        'titulo': '🎯 Sistema de Crítica 100/100 Puntos'
    }
    
    return render(request, 'Simulator/critica_100.html', context)

@login_required
def ecuacion_general_view(request):
    """Vista principal de la ecuación general ENARM"""
    
    analizador = MegaAnalizadorENARM()
    ecuacion = analizador.ecuacion_general_enarm(request.user.id)
    
    # Generar visualización de la ecuación
    grafico_ecuacion = generar_grafico_ecuacion_general(ecuacion)
    grafico_coeficientes = generar_grafico_coeficientes(ecuacion['coeficientes'])
    
    context = {
        'ecuacion': ecuacion,
        'grafico_ecuacion': grafico_ecuacion,
        'grafico_coeficientes': grafico_coeficientes,
        'titulo': '🧮 ECUACIÓN GENERAL DEFINITIVA ENARM'
    }
    
    return render(request, 'Simulator/ecuacion_general.html', context)

@csrf_exempt
@login_required
def ejecutar_analisis_completo(request):
    """Ejecuta análisis completo vía AJAX"""
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tipo_analisis = data.get('tipo')
            parametros = data.get('parametros', {})
            
            analizador = MegaAnalizadorENARM()
            
            if tipo_analisis == 'errores_aciertos':
                resultado = analizador.analisis_errores_aciertos_completo(request.user.id)
            elif tipo_analisis == 'temas_frecuencias':
                resultado = analizador.analisis_temas_frecuencias()
            elif tipo_analisis == 'similitudes':
                resultado = analizador.detector_materias_similares()
            elif tipo_analisis == 'dificultad':
                resultado = analizador.analizador_dificultad_extrema()
            elif tipo_analisis == 'trampas':
                resultado = analizador.detector_trampas_estructuras()
            elif tipo_analisis == 'critica_100':
                resultado = analizador.sistema_critica_perfecta(request.user.id)
            elif tipo_analisis == 'ecuacion_general':
                resultado = analizador.ecuacion_general_enarm(request.user.id)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Tipo de análisis no reconocido'
                })
            
            return JsonResponse({
                'status': 'success',
                'resultado': resultado,
                'tipo': tipo_analisis
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': f'Error en análisis: {str(e)}'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@csrf_exempt
@login_required
def generar_plan_estudio_ia(request):
    """Genera plan de estudio personalizado con IA"""
    
    if request.method == 'POST':
        try:
            analizador = MegaAnalizadorENARM()
            ecuacion = analizador.ecuacion_general_enarm(request.user.id)
            
            # Generar plan basado en debilidades detectadas
            plan_personalizado = {
                'objetivo_score': 85,  # Objetivo mínimo
                'tiempo_estimado': '60 días',
                'plan_diario': [],
                'plan_semanal': [],
                'recursos_recomendados': [],
                'simulacros_cronograma': []
            }
            
            # Análisis de coeficientes para plan personalizado
            coefs = ecuacion['coeficientes']
            
            if coefs['A'] < 0.7:  # Conocimiento bajo
                plan_personalizado['plan_diario'].append({
                    'actividad': 'Revisión de fundamentos',
                    'tiempo': '2 horas',
                    'prioridad': 'ALTA'
                })
            
            if coefs['T'] < 0.6:  # Trampas
                plan_personalizado['plan_diario'].append({
                    'actividad': 'Entrenamiento anti-trampas',
                    'tiempo': '30 minutos',
                    'prioridad': 'CRÍTICA'
                })
            
            if coefs['B'] < 0.5:  # Práctica
                plan_personalizado['plan_diario'].append({
                    'actividad': 'Banco de preguntas',
                    'tiempo': '1.5 horas',
                    'cantidad': '50-80 preguntas',
                    'prioridad': 'ALTA'
                })
            
            # Plan semanal
            plan_personalizado['plan_semanal'] = [
                'Lunes: Medicina Interna + Simulacro diagnóstico',
                'Martes: Cirugía + Análisis de errores',
                'Miércoles: Ginecología + Entrenamiento trampas',
                'Jueves: Pediatría + Revisión de similitudes',
                'Viernes: Urgencias + Simulacro completo',
                'Sábado: Repaso áreas débiles',
                'Domingo: Simulacro ENARM completo'
            ]
            
            # Recursos recomendados basados en debilidades
            areas_debiles = [k for k, v in coefs.items() if v < 0.6 and k != 'Φ']
            
            for area in areas_debiles:
                if area == 'A':  # Conocimiento
                    plan_personalizado['recursos_recomendados'].append('Manual CTO actualizado')
                elif area == 'T':  # Trampas
                    plan_personalizado['recursos_recomendados'].append('Banco anti-trampas ENARM')
                elif area == 'D':  # Dificultad
                    plan_personalizado['recursos_recomendados'].append('Casos clínicos complejos')
            
            return JsonResponse({
                'status': 'success',
                'plan': plan_personalizado,
                'ecuacion_base': ecuacion,
                'mensaje': f'Plan generado para score objetivo de {plan_personalizado["objetivo_score"]} puntos'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error generando plan: {str(e)}'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

# Funciones auxiliares para generar gráficos

def generar_grafico_errores_categoria(datos_categoria):
    """Genera gráfico de errores por categoría"""
    if not MATPLOTLIB_AVAILABLE:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    plt.figure(figsize=(12, 6))
    
    categorias = list(datos_categoria.keys())
    porcentajes_error = [datos_categoria[cat].get('porcentaje_errores', 0) for cat in categorias]
    
    bars = plt.bar(categorias, porcentajes_error, color=['red' if p > 50 else 'orange' if p > 30 else 'green' for p in porcentajes_error])
    
    plt.title('Porcentaje de Errores por Categoría', fontsize=16, fontweight='bold')
    plt.xlabel('Categorías')
    plt.ylabel('Porcentaje de Errores')
    plt.xticks(rotation=45, ha='right')
    
    # Agregar valores en las barras
    for bar, porcentaje in zip(bars, porcentajes_error):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{porcentaje:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Convertir a base64 para template
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"

def generar_grafico_tendencias_hora(datos_hora):
    """Genera gráfico de tendencias por hora"""
    if not MATPLOTLIB_AVAILABLE:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    plt.figure(figsize=(10, 6))
    
    horas = sorted(datos_hora.keys())
    errores_por_hora = [datos_hora[h].get('porcentaje_errores', 0) for h in horas]
    
    plt.plot(horas, errores_por_hora, marker='o', linewidth=2, markersize=6)
    plt.title('Tendencia de Errores por Hora del Día')
    plt.xlabel('Hora')
    plt.ylabel('Porcentaje de Errores')
    plt.grid(True, alpha=0.3)
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"

def generar_grafico_distribucion_frecuencias(temas_analisis):
    """Genera gráfico de distribución de frecuencias"""
    if not MATPLOTLIB_AVAILABLE:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    plt.figure(figsize=(12, 8))
    
    # Crear histograma de frecuencias
    frecuencias = []
    for tema in temas_analisis['mas_vistos'] + temas_analisis['menos_vistos']:
        frecuencias.append(tema['frecuencia'])
    
    plt.hist(frecuencias, bins=20, edgecolor='black', alpha=0.7)
    plt.title('Distribución de Frecuencias de Práctica')
    plt.xlabel('Frecuencia de Práctica')
    plt.ylabel('Cantidad de Temas')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"

def generar_grafico_patrones_dificultad(dificultad_analisis):
    """Genera gráfico de patrones de dificultad"""
    if not MATPLOTLIB_AVAILABLE:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    plt.figure(figsize=(10, 6))
    
    patrones = list(dificultad_analisis['patrones_estructura'].keys())
    valores = list(dificultad_analisis['patrones_estructura'].values())
    
    plt.bar(patrones, valores, color='darkred', alpha=0.7)
    plt.title('Patrones de Dificultad Extrema Detectados')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Cantidad Detectada')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"

def generar_grafico_tipos_trampa(trampas_analisis):
    """Genera gráfico de tipos de trampa"""
    if not MATPLOTLIB_AVAILABLE:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    plt.figure(figsize=(12, 8))
    
    tipos = []
    cantidades = []
    
    for tipo, items in trampas_analisis['tipos_trampa'].items():
        tipos.append(tipo.replace('_', ' ').title())
        cantidades.append(len(items) if isinstance(items, list) else items)
    
    plt.barh(tipos, cantidades, color='orange', alpha=0.7)
    plt.title('Tipos de Trampas Detectadas')
    plt.xlabel('Cantidad')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"

def generar_grafico_progreso_100(critica):
    """Genera gráfico de progreso hacia 100 puntos"""
    if not MATPLOTLIB_AVAILABLE:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    plt.figure(figsize=(10, 6))
    
    if critica['areas_debiles_criticas']:
        areas = [area['categoria'] for area in critica['areas_debiles_criticas']]
        porcentajes = [area['porcentaje_actual'] for area in critica['areas_debiles_criticas']]
        
        bars = plt.bar(areas, porcentajes, color=['red' if p < 80 else 'orange' if p < 90 else 'yellow' for p in porcentajes])
        
        # Línea objetivo en 95%
        plt.axhline(y=95, color='green', linestyle='--', label='Objetivo 95%')
        
        plt.title('Progreso hacia 100/100 por Área')
        plt.ylabel('Porcentaje Actual')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        
        for bar, porcentaje in zip(bars, porcentajes):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{porcentaje:.1f}%', ha='center', va='bottom')
    else:
        plt.text(0.5, 0.5, '¡Felicidades!\nTodas las áreas > 95%', 
                ha='center', va='center', fontsize=20, transform=plt.gca().transAxes)
        plt.title('Estado Perfecto - Listo para 100/100')
    
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"

def generar_grafico_ecuacion_general(ecuacion):
    """Genera visualización de la ecuación general"""
    if not MATPLOTLIB_AVAILABLE:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    plt.figure(figsize=(12, 8))
    
    # Gráfico de radar para coeficientes
    coefs = ecuacion['coeficientes']
    variables = ['A\n(Conocimiento)', 'B\n(Práctica)', 'C\n(Diferenciación)', 
                'D\n(Dificultad)', 'T\n(Trampas)', 'V\n(Velocidad)']
    valores = [coefs['A'], coefs['B'], coefs['C'], coefs['D'], coefs['T'], coefs['V']]
    
    # Convertir a gráfico polar
    angles = np.linspace(0, 2*np.pi, len(variables), endpoint=False).tolist()
    valores += valores[:1]  # Cerrar el polígono
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    ax.plot(angles, valores, 'o-', linewidth=2, color='blue')
    ax.fill(angles, valores, alpha=0.25, color='blue')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(variables)
    ax.set_ylim(0, 1)
    ax.set_title(f'ECUACIÓN GENERAL ENARM\nScore Predicho: {ecuacion["score_predicho"]:.1f}/100', 
                y=1.08, fontsize=16, fontweight='bold')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"

def generar_grafico_coeficientes(coeficientes):
    """Genera gráfico de barras de coeficientes"""
    if not MATPLOTLIB_AVAILABLE:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    plt.figure(figsize=(12, 6))
    
    coefs_mostrar = {k: v for k, v in coeficientes.items() if k != 'Φ'}
    
    nombres = list(coefs_mostrar.keys())
    valores = list(coefs_mostrar.values())
    
    colors = ['red' if v < 0.5 else 'orange' if v < 0.7 else 'green' for v in valores]
    bars = plt.bar(nombres, valores, color=colors)
    
    plt.title('Coeficientes de la Ecuación General ENARM')
    plt.ylabel('Valor del Coeficiente')
    plt.ylim(0, 1)
    
    # Líneas de referencia
    plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Crítico')
    plt.axhline(y=0.7, color='orange', linestyle='--', alpha=0.5, label='Mejorable')
    plt.axhline(y=0.9, color='green', linestyle='--', alpha=0.5, label='Óptimo')
    
    # Valores en barras
    for bar, valor in zip(bars, valores):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{valor:.3f}', ha='center', va='bottom')
    
    plt.legend()
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"