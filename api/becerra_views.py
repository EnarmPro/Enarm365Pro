from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from api.models import Preguntas, Respuestas, RegistroRespuestaPreguntas, Categorias
from api.ai_becerra_system import SistemaBecerraIA, PatronBecerra, AnalizadorNOMs, PredictorTendencias
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def dashboard_becerra_phi(request):
    """Dashboard principal con metodología Becerra Φ"""
    sistema = SistemaBecerraIA()
    dashboard_data = sistema.generar_dashboard_becerra(request.user.id)
    
    context = {
        'dashboard_data': dashboard_data,
        'user': request.user,
        'titulo': 'Dashboard Becerra Φ - Análisis Avanzado ENARM'
    }
    
    return render(request, 'Simulator/dashboard_becerra.html', context)

@csrf_exempt
@login_required
def analizar_pregunta_phi(request):
    """Analiza una pregunta específica con metodología Φ"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pregunta_id = data.get('pregunta_id')
            
            sistema = SistemaBecerraIA()
            resultado = sistema.analizar_pregunta_completa(pregunta_id)
            
            return JsonResponse({
                'status': 'success',
                'analisis': resultado
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error en análisis: {str(e)}'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@login_required
def detector_patrones_ptn(request):
    """Vista para detector de patrones P+T+N²"""
    patron_becerra = PatronBecerra()
    
    # Obtener muestra de preguntas para análisis
    preguntas_sample = Preguntas.objects.all().order_by('-idPregunta')[:50]
    
    resultados_analisis = []
    for pregunta in preguntas_sample:
        opciones = list(Respuestas.objects.filter(fkPregunta=pregunta).values_list('nombreRespuestas', flat=True))
        
        p_score = patron_becerra.detectar_patron_biologico(pregunta.nombrePregunta)
        t_score = patron_becerra.detectar_trampa_psiquica(pregunta.nombrePregunta, opciones)
        n_score = patron_becerra.detectar_distractor_ambiguo(opciones)
        phi_value = patron_becerra.calcular_phi_pattern(p_score, t_score, n_score)
        
        resultados_analisis.append({
            'pregunta': pregunta,
            'phi_value': round(phi_value, 3),
            'p_score': round(p_score, 3),
            't_score': round(t_score, 3),
            'n_score': round(n_score, 3),
            'nivel_dificultad': 'Alto' if phi_value > 2.5 else 'Medio' if phi_value > 1.5 else 'Bajo'
        })
    
    # Ordenar por valor Φ descendente
    resultados_analisis.sort(key=lambda x: x['phi_value'], reverse=True)
    
    # Paginación
    paginator = Paginator(resultados_analisis, 10)
    page_number = request.GET.get('page', 1)
    resultados_paginados = paginator.get_page(page_number)
    
    context = {
        'resultados': resultados_paginados,
        'titulo': 'Detector de Patrones P+T+N² - Metodología Becerra'
    }
    
    return render(request, 'Simulator/detector_patrones.html', context)

@login_required
def analizador_noms_emergentes(request):
    """Vista para análisis de NOMs emergentes"""
    analizador = AnalizadorNOMs()
    
    # Filtrar preguntas por categoría si se especifica
    categoria_filtro = request.GET.get('categoria')
    preguntas_query = Preguntas.objects.all()
    
    if categoria_filtro:
        preguntas_query = preguntas_query.filter(fkCategorias__idCategoria=categoria_filtro)
    
    preguntas = preguntas_query.order_by('-idPregunta')[:100]
    
    # Análisis de NOMs
    resultados_noms = {}
    for pregunta in preguntas:
        noms_detectadas = analizador.detectar_nom_en_pregunta(pregunta.nombrePregunta)
        for nom, score in noms_detectadas.items():
            if score > 0.3:  # Solo incluir si hay relevancia
                if nom not in resultados_noms:
                    resultados_noms[nom] = []
                resultados_noms[nom].append({
                    'pregunta': pregunta,
                    'score': round(score, 3)
                })
    
    # Calcular tendencia Ω
    tendencia_omega = analizador.calcular_tendencia_omega(preguntas)
    
    # Obtener categorías para filtro
    categorias = Categorias.objects.all()
    
    context = {
        'resultados_noms': resultados_noms,
        'tendencia_omega': tendencia_omega,
        'categorias': categorias,
        'categoria_actual': categoria_filtro,
        'titulo': 'Analizador de NOMs Emergentes'
    }
    
    return render(request, 'Simulator/analizador_noms.html', context)

@login_required
def predictor_tendencias_2025(request):
    """Vista para predictor de tendencias ENARM 2025"""
    predictor = PredictorTendencias()
    
    # Obtener predicciones
    predicciones = predictor.predecir_preguntas_2025()
    
    # Calcular desequilibrios meta-circulares
    preguntas_recientes = Preguntas.objects.order_by('-idPregunta')[:30]
    desequilibrios = predictor.calcular_desequilibrio_metacircular(preguntas_recientes)
    
    context = {
        'predicciones': predicciones,
        'desequilibrios': desequilibrios,
        'titulo': 'Predictor de Tendencias ENARM 2025'
    }
    
    return render(request, 'Simulator/predictor_tendencias.html', context)

@csrf_exempt
@login_required
def generar_grafico_correlacion(request):
    """Genera gráfico de correlación tiempo-respuestas-errores"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dias = data.get('dias', 30)
            
            from api.ai_becerra_system import GeneradorGraficos
            generador = GeneradorGraficos()
            
            ruta_grafico = generador.generar_correlacion_tiempo_errores(
                request.user.id, 
                dias
            )
            
            return JsonResponse({
                'status': 'success',
                'grafico_url': ruta_grafico,
                'message': f'Gráfico generado para los últimos {dias} días'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error generando gráfico: {str(e)}'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@login_required
def modo_agente_becerra(request):
    """Modo agente - Capacidad máxima de análisis"""
    if request.method == 'POST':
        comando = request.POST.get('comando')
        contexto = request.POST.get('contexto', '')
        
        # Procesar comando tipo BECERRA Φ
        resultado = procesar_comando_agente(comando, contexto, request.user)
        
        return JsonResponse(resultado)
    
    context = {
        'titulo': 'Modo Agente Becerra Φ',
        'comandos_ejemplo': [
            'Genera un desglose basado en Φ para detectar si preguntas relacionadas con biología molecular (P) tienen trampas psíquicas (T)',
            'Calcula si hay un desequilibrio meta-circular de tipo Ω en preguntas que evalúan NOMs emergentes como la 020',
            'Predice qué tendencias INSTITUCIONALES pondrán en el 15% impredecible del ENARM 2025',
            'Analiza patrones ocultos en preguntas de medicina interna vs cirugía'
        ]
    }
    
    return render(request, 'Simulator/modo_agente.html', context)

def procesar_comando_agente(comando, contexto, user):
    """Procesa comandos en modo agente tipo BECERRA Φ"""
    try:
        sistema = SistemaBecerraIA()
        
        # Detectar tipo de comando
        if 'desglose' in comando.lower() and 'φ' in comando:
            return ejecutar_desglose_phi(comando, sistema)
        
        elif 'desequilibrio meta-circular' in comando.lower():
            return ejecutar_analisis_omega(comando, sistema)
        
        elif 'tendencias' in comando.lower() and '2025' in comando:
            return ejecutar_prediccion_2025(comando, sistema)
        
        elif 'patrones ocultos' in comando.lower():
            return ejecutar_deteccion_patrones(comando, sistema, user)
        
        else:
            return {
                'status': 'info',
                'message': 'Comando no reconocido. Usa patrones como: desglose Φ, desequilibrio Ω, tendencias 2025, patrones ocultos'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error procesando comando: {str(e)}'
        }

def ejecutar_desglose_phi(comando, sistema):
    """Ejecuta desglose basado en Φ"""
    # Buscar preguntas de biología molecular
    preguntas_bio = Preguntas.objects.filter(
        Q(nombrePregunta__icontains='enzima') |
        Q(nombrePregunta__icontains='proteína') |
        Q(nombrePregunta__icontains='gen') |
        Q(nombrePregunta__icontains='ADN')
    )[:20]
    
    resultados = []
    for pregunta in preguntas_bio:
        analisis = sistema.analizar_pregunta_completa(pregunta.idPregunta)
        if analisis.get('phi_value', 0) > 2.0:
            resultados.append(analisis)
    
    return {
        'status': 'success',
        'tipo_analisis': 'Desglose Φ - Biología Molecular',
        'resultados': resultados,
        'resumen': f'Se encontraron {len(resultados)} preguntas con alta complejidad Φ (>2.0)'
    }

def ejecutar_analisis_omega(comando, sistema):
    """Ejecuta análisis de desequilibrio meta-circular Ω"""
    predictor = PredictorTendencias()
    preguntas_noms = Preguntas.objects.filter(
        Q(nombrePregunta__icontains='diabetes') |
        Q(nombrePregunta__icontains='hipertensión') |
        Q(nombrePregunta__icontains='obesidad')
    )[:30]
    
    desequilibrios = predictor.calcular_desequilibrio_metacircular(preguntas_noms)
    
    return {
        'status': 'success',
        'tipo_analisis': 'Desequilibrio Meta-circular Ω',
        'desequilibrios': desequilibrios,
        'nivel_alerta': 'Alto' if len(desequilibrios) > 5 else 'Medio' if len(desequilibrios) > 2 else 'Bajo'
    }

def ejecutar_prediccion_2025(comando, sistema):
    """Ejecuta predicción de tendencias 2025"""
    predictor = PredictorTendencias()
    predicciones = predictor.predecir_preguntas_2025()
    
    # Análisis del 15% impredecible
    tendencias_impredecibles = [
        {
            'tema': 'IA en diagnóstico médico',
            'probabilidad': 0.15,
            'impacto': 'Revolucionario'
        },
        {
            'tema': 'Medicina espacial',
            'probabilidad': 0.08,
            'impacto': 'Emergente'
        },
        {
            'tema': 'Terapias génicas CRISPR',
            'probabilidad': 0.12,
            'impacto': 'Alto'
        }
    ]
    
    return {
        'status': 'success',
        'tipo_analisis': 'Predicción ENARM 2025',
        'predicciones_principales': predicciones,
        'factor_impredecible': tendencias_impredecibles,
        'recomendacion': 'Enfocar 85% en predicciones principales, 15% en tendencias disruptivas'
    }

def ejecutar_deteccion_patrones(comando, sistema, user):
    """Ejecuta detección de patrones ocultos"""
    # Obtener preguntas contestadas por el usuario
    registros = RegistroRespuestaPreguntas.objects.filter(
        fkUser=user
    ).select_related('fkPregunta', 'fkRespuesta')[:50]
    
    patrones_detectados = []
    errores_por_categoria = {}
    
    for registro in registros:
        categoria = registro.fkPregunta.fkCategorias.descripcionCategoria
        es_correcto = registro.fkRespuesta.statusRespuestas == 'Correcto'
        
        if categoria not in errores_por_categoria:
            errores_por_categoria[categoria] = {'total': 0, 'errores': 0}
        
        errores_por_categoria[categoria]['total'] += 1
        if not es_correcto:
            errores_por_categoria[categoria]['errores'] += 1
    
    # Detectar patrones de error
    for categoria, stats in errores_por_categoria.items():
        tasa_error = stats['errores'] / stats['total'] if stats['total'] > 0 else 0
        if tasa_error > 0.5:
            patrones_detectados.append({
                'categoria': categoria,
                'tasa_error': round(tasa_error * 100, 1),
                'patron': 'Alto índice de errores - revisar fundamentos'
            })
    
    return {
        'status': 'success',
        'tipo_analisis': 'Patrones Ocultos Personalizados',
        'patrones_detectados': patrones_detectados,
        'estadisticas': errores_por_categoria
    }