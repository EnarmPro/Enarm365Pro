from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django.db.models import Q,Count
from collections import defaultdict
from django.shortcuts import redirect, render
from api.models import Intentos, Preguntas,Categorias,Respuestas,RegistroRespuestaPreguntas,Temarios, ForoUsuarios,blogTema, blogComentario, PaypalPago
from django.http import JsonResponse
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from datetime import date,  timedelta
from django.utils import timezone
import random, json
from django.db.models.functions import TruncDay
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model=User
        fields = ["username","email", "password1", "password2"]


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else: 
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form":form})

def index(request):
    template_name = 'index.html'
    
    mostrarTemario = Temarios.objects.exclude(Q(nombreTemario='Gratuito') | Q(nombreTemario='Personalizado')| Q(nombreTemario='Diagnostico')| Q(nombreTemario='Enarm 25') | Q(nombreTemario='Enarm 50')| Q(nombreTemario='Enarm 100')).order_by('-idTemarios')
    contadorTemario = Temarios.objects.exclude(Q(nombreTemario='Gratuito') | Q(nombreTemario='Personalizado')).order_by('-idTemarios').count()
    contadorEnarm = Temarios.objects.exclude(Q(nombreTemario='Gratuito') | Q(nombreTemario='Personalizado') | Q(nombreTemario='Urgencias')| Q(nombreTemario='Cirugía')| Q(nombreTemario='Ginecología')| Q(nombreTemario='Medicina Interna')| Q(nombreTemario='Pediatría')).order_by('-idTemarios').count()
    comentarioUser = ForoUsuarios.objects.all().order_by('-idForo')
    
    if request.user.is_authenticated:
        user = request.user
        
        try:
            # Obtener el registro más reciente de PaypalPago para el usuario actual
            ultimo_pago = PaypalPago.objects.filter(fk_User=user).latest('fecha_pago')

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            # Calcular la diferencia de tiempo entre la fecha del último pago y la fecha actual
            diferencia_tiempo = fecha_actual - ultimo_pago.fecha_pago

            if ultimo_pago.tipo_membresia == 'Mensual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 30
            elif ultimo_pago.tipo_membresia == 'Trimestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 90
            elif ultimo_pago.tipo_membresia == 'Semestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 180
            elif ultimo_pago.tipo_membresia == 'Anual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 365

        except PaypalPago.DoesNotExist:
            # Manejar el caso en el que no exista ningún registro de PaypalPago para el usuario actual
            es_mayor_a_30_dias = True
        try:
            # Obtener el último intento del usuario actual
            ultimo_intento = Intentos.objects.filter(fkUser=user,fkCategorias=5).latest('fechaIntento')

            # Obtener la fecha actual
            fecha_actual = date.today()
            
            # Obtener la fecha del último intento
            fecha_ultimo_intento = ultimo_intento.fechaIntento
            # Calcular la fecha hace 24 horas
            fecha_hace_45_horas = fecha_actual + timedelta(days=45)
            # Verificar si ha pasado más de 24 horas desde el último intento
            revisionIntento =    fecha_ultimo_intento > fecha_hace_45_horas

        except ObjectDoesNotExist:
            revisionIntento = True
    else:
        es_mayor_a_30_dias = True
        revisionIntento = None
        
    context = {
        'mostrarTemario':mostrarTemario,
        'contadorTemario':contadorTemario,
        'contadorEnarm':contadorEnarm,
        'comentarioUser': comentarioUser,
        'es_mayor_a_30_dias':es_mayor_a_30_dias,
        'revisionIntento':revisionIntento,
        
    }

    return render(request, template_name, context)



def simulador_free(request):
    template_name = 'Simulator/simulator_free.html'
    
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener el usuario autenticado
        user = request.user
        
        try:
            # Obtener el último intento del usuario actual
            ultimo_intento = Intentos.objects.filter(fkUser=user,fkCategorias=1).latest('fechaIntento')

            # Obtener la fecha actual
            fecha_actual = date.today()

            # Obtener la fecha del último intento
            fecha_ultimo_intento = ultimo_intento.fechaIntento
            # Calcular la fecha hace 24 horas
            fecha_hace_24_horas = fecha_actual
            # Verificar si ha pasado más de 24 horas desde el último intento
            revisionIntento =   fecha_ultimo_intento < fecha_hace_24_horas

        except ObjectDoesNotExist:
            revisionIntento = True
        # Obtener el nombre de usuario
        userName = user.username
    else:
        # Si el usuario no está autenticado, establecer userName como None
        userName = None
        revisionIntento = None

    if request.user.is_authenticated:
        user = request.user
        
        try:
            # Obtener el registro más reciente de PaypalPago para el usuario actual
            ultimo_pago = PaypalPago.objects.filter(fk_User=user).latest('fecha_pago')

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            # Calcular la diferencia de tiempo entre la fecha del último pago y la fecha actual
            diferencia_tiempo = fecha_actual - ultimo_pago.fecha_pago

            if ultimo_pago.tipo_membresia == 'Mensual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 30
            elif ultimo_pago.tipo_membresia == 'Trimestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 90
            elif ultimo_pago.tipo_membresia == 'Semestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 180
            elif ultimo_pago.tipo_membresia == 'Anual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 365

        except PaypalPago.DoesNotExist:
            # Manejar el caso en el que no exista ningún registro de PaypalPago para el usuario actual
            es_mayor_a_30_dias = True
    else:
        es_mayor_a_30_dias = True
    

    # Obtener todas las preguntas gratuitas
    preguntas_gratuitas = Preguntas.objects.filter(fkCategorias__descripcionCategoria='Gratuito')[:10]

    # Obtener todas las respuestas disponibles
    respuestas_todas = Respuestas.objects.filter(fkCategorias=1)

        # Lista para almacenar las preguntas con sus respuestas mezcladas
    preguntas_con_respuestas_mezcladas = []

        # Iterar sobre cada pregunta gratuita
    for pregunta in preguntas_gratuitas:
            # Obtener la respuesta correcta asociada a la pregunta
        respuesta_correcta = Respuestas.objects.get(fkPregunta=pregunta)
            
            # Obtener tres respuestas incorrectas aleatorias de entre todas las respuestas disponibles,
            # excluyendo la respuesta correcta
        respuestas_incorrectas = random.sample(list(respuestas_todas.exclude(pk=respuesta_correcta.pk)), 3)
            
            # Combinar la respuesta correcta con las respuestas incorrectas
        respuestas_mezcladas = [respuesta_correcta] + respuestas_incorrectas
            
            # Mezclar aleatoriamente las respuestas
        random.shuffle(respuestas_mezcladas)
            
            # Agregar la pregunta y sus respuestas mezcladas a la lista
        preguntas_con_respuestas_mezcladas.append((pregunta, respuestas_mezcladas))

        # Mezclar aleatoriamente las preguntas con sus respuestas
        random.shuffle(preguntas_con_respuestas_mezcladas)

    context = {
            'userName': userName,
            'Intento': revisionIntento,
            'preguntas_con_respuestas_mezcladas': preguntas_con_respuestas_mezcladas,
            'es_mayor_a_30_dias':es_mayor_a_30_dias
        }

    return render(request, template_name, context)

def simulador_Personalizado(request):
    template_name = 'Simulator/simulator_personalizado.html'
    if request.method == "POST":
        tipo_tiempo = request.POST.get('tiempo')
        preguntas_cantidad = request.POST.get('numero')
        id_tema = request.POST.get('id_tema')
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Obtener el usuario autenticado
            user = request.user
            
            # Obtener el nombre de usuario
            userName = user.username
        else:
            # Si el usuario no está autenticado, establecer userName como None
            userName = None
            

        # Obtener todas las preguntas gratuitas
        preguntas_gratuitas = Preguntas.objects.filter(fkTemarios=id_tema)[:int(preguntas_cantidad)]

        # Obtener todas las respuestas disponibles
        respuestas_todas = Respuestas.objects.all()

            # Lista para almacenar las preguntas con sus respuestas mezcladas
        preguntas_con_respuestas_mezcladas = []

            # Iterar sobre cada pregunta gratuita
        for pregunta in preguntas_gratuitas:
                # Obtener la respuesta correcta asociada a la pregunta
            respuesta_correcta = Respuestas.objects.get(fkPregunta=pregunta)
                
                # Obtener tres respuestas incorrectas aleatorias de entre todas las respuestas disponibles,
                # excluyendo la respuesta correcta
            respuestas_incorrectas = random.sample(list(respuestas_todas.exclude(pk=respuesta_correcta.pk)), 3)
                
                # Combinar la respuesta correcta con las respuestas incorrectas
            respuestas_mezcladas = [respuesta_correcta] + respuestas_incorrectas
                
                # Mezclar aleatoriamente las respuestas
            random.shuffle(respuestas_mezcladas)
                
                # Agregar la pregunta y sus respuestas mezcladas a la lista
            preguntas_con_respuestas_mezcladas.append((pregunta, respuestas_mezcladas))

            # Mezclar aleatoriamente las preguntas con sus respuestas
            random.shuffle(preguntas_con_respuestas_mezcladas)

        context = {
                'userName': userName,
                'preguntas_con_respuestas_mezcladas': preguntas_con_respuestas_mezcladas,
                'tipo_tiempo':tipo_tiempo,
                'preguntas_cantidad':preguntas_cantidad
            }

    return render(request, template_name, context)

def registrar_preguntas(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        user_id = request.user

        data = json.loads(request.body)
        
        # Extraer los datos necesarios
        fk_pregunta_id = data.get('pregunta_id')
        fk_respuesta_id = data.get('respuesta_id')
        intento = data.get('intento', 1)  # Obtener el número de intento si se proporciona, de lo contrario, predeterminado a 1
        
        preguntaInstance = Preguntas.objects.get(idPregunta=fk_pregunta_id)
        respuestaInstance = Respuestas.objects.get(idRespuestas=fk_respuesta_id)
        
        # Verificar si ya existe un registro con el mismo usuario, pregunta y número de intento
        registro_existente = RegistroRespuestaPreguntas.objects.filter(
            fkUser=user_id,
            fkPregunta=preguntaInstance,
            numeroIntento=intento
        ).exists()

        # Si ya existe un registro con el mismo usuario, pregunta e intento, incrementar el intento en 1
        if registro_existente:
            intento_anterior = RegistroRespuestaPreguntas.objects.filter(
                fkUser=user_id,
                fkPregunta=preguntaInstance
            ).aggregate(Max('numeroIntento'))['numeroIntento__max']
            intento = intento_anterior + 1 if intento_anterior is not None else 1

        # Crear una instancia de RegistroRespuestaPreguntas y guardarla en la base de datos
        respuesta_pregunta = RegistroRespuestaPreguntas(
            fkUser=user_id,
            fkPregunta=preguntaInstance,
            fkRespuesta=respuestaInstance,
            numeroIntento=intento  # Asignar el número de intento al registro
        )
        respuesta_pregunta.save()

        # Obtener la respuesta correcta para la pregunta
        respuesta_correcta = Respuestas.objects.filter(fkPregunta=preguntaInstance).first()

        return JsonResponse({
            'mensaje': 'Respuesta registrada con éxito',
            'respuesta_correcta': respuesta_correcta.nombreRespuestas if respuesta_correcta else 'No se encontró respuesta correcta'
        })
    else:
        return JsonResponse({'error': 'Solicitud no válida'})

"""
def registrar_preguntas(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        user_id = request.user

        data = json.loads(request.body)
        
        # Extraer los datos necesarios
        fk_pregunta_id = data.get('pregunta_id')
        fk_respuesta_id = data.get('respuesta_id')
        intento = data.get('intento')  # Obtener el número de intento si se proporciona, de lo contrario, predeterminado a 1
        
        preguntaInstance = Preguntas.objects.get(idPregunta=fk_pregunta_id)
        respuestaInstance = Respuestas.objects.get(idRespuestas=fk_respuesta_id)
        # Verificar si ya existe un registro con el mismo usuario, pregunta y número de intento
        registro_existente = RegistroRespuestaPreguntas.objects.filter(
            fkUser=user_id,
            fkPregunta=preguntaInstance,
            numeroIntento=intento
        ).exists()

        # Si ya existe un registro con el mismo usuario, pregunta e intento, incrementar el intento en 1
        if registro_existente:
            intento_anterior = RegistroRespuestaPreguntas.objects.filter(
                fkUser=user_id,
                fkPregunta=preguntaInstance
            ).aggregate(Max('numeroIntento'))['numeroIntento__max']
            intento = intento_anterior + 1 if intento_anterior is not None else 1

        # Crear una instancia de RegistroRespuestaPreguntas y guardarla en la base de datos
        respuesta_pregunta = RegistroRespuestaPreguntas(
            fkUser=user_id,
            fkPregunta=preguntaInstance,
            fkRespuesta=respuestaInstance,
            numeroIntento=intento  # Asignar el número de intento al registro
        )
        respuesta_pregunta.save()

        return JsonResponse({'mensaje': 'Respuesta registrada con éxito'})
    else:
        return JsonResponse({'error': 'Solicitud no válida'})"""
    
def registrar_intentos(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        user_id = request.user

        data = json.loads(request.body)
        
        # Extraer los datos necesarios
        fk_categoria_id = data.get('categoria_id')
        
        # Instancia de categorias
        fk_categoria_instancia = Categorias.objects.get(descripcionCategoria=fk_categoria_id)

        # Obtener la fecha actual
        fecha_completado = date.today()
        
        # Crear una instancia de RegistroRespuestaPreguntas y guardarla en la base de datos
        registrar_grautito = Intentos(

            fechaIntento = fecha_completado,
            fkCategorias = fk_categoria_instancia,
            fkUser_id=user_id.id,
            
        
            
        )
        registrar_grautito.save()

    

        return JsonResponse({'mensaje': 'Intento registrado con éxito'})
    else:
        return JsonResponse({'error': 'Solicitud no válida'})


def mostrarTemas(request):
    template_name = 'Simulator/portal_topic.html'
    mostrarTemario = Temarios.objects.exclude(Q(nombreTemario='Gratuito') | Q(nombreTemario='Personalizado') | Q(nombreTemario='Diagnostico') | Q(nombreTemario='Enarm 25') | Q(nombreTemario='Enarm 50') | Q(nombreTemario='Enarm 100')).order_by('-idTemarios')
    contadorTemario = Temarios.objects.all().order_by('-idTemarios').count()

    context = {
        'mostrarTemario':mostrarTemario,
        'contadorTemario':contadorTemario
    }

    return render(request, template_name, context)

def simuladorTema(request):
    template_name = 'Simulator/simulator_topic.html'
    id_tema = request.GET.get('id_tema')
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener el usuario autenticado
        user = request.user
        
        # Obtener el nombre de usuario
        userName = user.username
    else:
        # Si el usuario no está autenticado, establecer userName como None
        userName = None
        
    tema = Temarios.objects.get(idTemarios=id_tema)
    # Obtener todas las preguntas gratuitas
    preguntas_gratuitas = Preguntas.objects.filter(fkTemarios=id_tema)[:56]

    # Obtener todas las respuestas disponibles
    respuestas_todas = Respuestas.objects.filter()

        # Lista para almacenar las preguntas con sus respuestas mezcladas
    preguntas_con_respuestas_mezcladas = []

        # Iterar sobre cada pregunta gratuita
    for pregunta in preguntas_gratuitas:
            # Obtener la respuesta correcta asociada a la pregunta
        respuesta_correcta = Respuestas.objects.get(fkPregunta=pregunta)
            
            # Obtener tres respuestas incorrectas aleatorias de entre todas las respuestas disponibles,
            # excluyendo la respuesta correcta
        respuestas_incorrectas = random.sample(list(respuestas_todas.exclude(pk=respuesta_correcta.pk)), 3)
            
            # Combinar la respuesta correcta con las respuestas incorrectas
        respuestas_mezcladas = [respuesta_correcta] + respuestas_incorrectas
            
            # Mezclar aleatoriamente las respuestas
        random.shuffle(respuestas_mezcladas)
            
            # Agregar la pregunta y sus respuestas mezcladas a la lista
        preguntas_con_respuestas_mezcladas.append((pregunta, respuestas_mezcladas))

        # Mezclar aleatoriamente las preguntas con sus respuestas
        preguntas_con_respuestas_mezcladas

    context = {
            'userName': userName,
            'preguntas_con_respuestas_mezcladas': preguntas_con_respuestas_mezcladas,
            'tema':tema
        }

    return render(request,template_name,context)


def seleccionDatosPersonalizado(request):
    template_name = 'Simulator/panel_personalizado.html'
    id_tema = request.GET.get('id_tema')
    nombre_tema = Temarios.objects.get(idTemarios   =id_tema)
    context ={
        'nombre_tema':nombre_tema
    }
    
    return render(request,template_name,context)

def mostrarTemasEnarm(request):
    template_name = 'Simulator/portal_enarm.html'
    mostrarTemarioEnarmUno = Temarios.objects.get(nombreTemario = 'Enarm 25')
    mostrarTemarioEnarmDos = Temarios.objects.get(nombreTemario = 'Enarm 50')
    mostrarTemarioEnarmTres = Temarios.objects.get(nombreTemario = 'Enarm 100')


    context = {
        'mostrarTemarioEnarmUno':mostrarTemarioEnarmUno,
        'mostrarTemarioEnarmDos':mostrarTemarioEnarmDos,
        'mostrarTemarioEnarmTres':mostrarTemarioEnarmTres,
    }

    return render(request, template_name, context)


def simuladorEnarmUno(request):
    template_name = 'Simulator/simulator_enarm.html'
    id_tema = request.GET.get('id_tema')
    tipo_tiempo = request.GET.get('tipo_tiempo')
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener el usuario autenticado
        user = request.user
        
        # Obtener el nombre de usuario
        userName = user.username
    else:
        # Si el usuario no está autenticado, establecer userName como None
        userName = None
        
    tema = Temarios.objects.get(idTemarios=id_tema)
    # Obtener todas las preguntas gratuitas

    
    preguntas_gratuitas = Preguntas.objects.filter(fkTemarios=id_tema)[:70]

    # Obtener todas las respuestas disponibles
    respuestas_todas = Respuestas.objects.filter()

        # Lista para almacenar las preguntas con sus respuestas mezcladas
    preguntas_con_respuestas_mezcladas = []

        # Iterar sobre cada pregunta gratuita
    for pregunta in preguntas_gratuitas:
            # Obtener la respuesta correcta asociada a la pregunta
        respuesta_correcta = Respuestas.objects.get(fkPregunta=pregunta)
            
            # Obtener tres respuestas incorrectas aleatorias de entre todas las respuestas disponibles,
            # excluyendo la respuesta correcta
        respuestas_incorrectas = random.sample(list(respuestas_todas.exclude(pk=respuesta_correcta.pk)), 3)
            
            # Combinar la respuesta correcta con las respuestas incorrectas
        respuestas_mezcladas = [respuesta_correcta] + respuestas_incorrectas
            
            # Mezclar aleatoriamente las respuestas
        random.shuffle(respuestas_mezcladas)
            
            # Agregar la pregunta y sus respuestas mezcladas a la lista
        preguntas_con_respuestas_mezcladas.append((pregunta, respuestas_mezcladas))

        # Mezclar aleatoriamente las preguntas con sus respuestas
        random.shuffle(preguntas_con_respuestas_mezcladas)

    context = {
            'userName': userName,
            'preguntas_con_respuestas_mezcladas': preguntas_con_respuestas_mezcladas,
            'tema':tema,
            'tipo_tiempo':tipo_tiempo
        }

    return render(request,template_name,context)


def simuladorEnarmSeccionDos(request):
    template_name = 'Simulator/simulator_enarm_dos.html'
    id_tema = request.GET.get('id_tema')
    tipo_tiempo = request.GET.get('tipo_tiempo')
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener el usuario autenticado
        user = request.user
        
        # Obtener el nombre de usuario
        userName = user.username
    else:
        # Si el usuario no está autenticado, establecer userName como None
        userName = None
        
    tema = Temarios.objects.get(idTemarios=id_tema)
    # Obtener todas las preguntas gratuitas

    preguntas_gratuitas = Preguntas.objects.filter(fkTemarios=id_tema)[:140]


    # Obtener todas las respuestas disponibles
    respuestas_todas = Respuestas.objects.filter()

        # Lista para almacenar las preguntas con sus respuestas mezcladas
    preguntas_con_respuestas_mezcladas = []

        # Iterar sobre cada pregunta gratuita
    for pregunta in preguntas_gratuitas:
            # Obtener la respuesta correcta asociada a la pregunta
        respuesta_correcta = Respuestas.objects.get(fkPregunta=pregunta)
            
            # Obtener tres respuestas incorrectas aleatorias de entre todas las respuestas disponibles,
            # excluyendo la respuesta correcta
        respuestas_incorrectas = random.sample(list(respuestas_todas.exclude(pk=respuesta_correcta.pk)), 3)
            
            # Combinar la respuesta correcta con las respuestas incorrectas
        respuestas_mezcladas = [respuesta_correcta] + respuestas_incorrectas
            
            # Mezclar aleatoriamente las respuestas
        random.shuffle(respuestas_mezcladas)
            
            # Agregar la pregunta y sus respuestas mezcladas a la lista
        preguntas_con_respuestas_mezcladas.append((pregunta, respuestas_mezcladas))

        # Mezclar aleatoriamente las preguntas con sus respuestas
        random.shuffle(preguntas_con_respuestas_mezcladas)

    context = {
            'userName': userName,
            'preguntas_con_respuestas_mezcladas': preguntas_con_respuestas_mezcladas,
            'tema':tema,
            'tipo_tiempo':tipo_tiempo
        }

    return render(request,template_name,context)


def simuladorEnarmSeccionTres(request):
    template_name = 'Simulator/simulator_enarm_tres.html'
    id_tema = request.GET.get('id_tema')
    tipo_tiempo = request.GET.get('tipo_tiempo')
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener el usuario autenticado
        user = request.user
        
        # Obtener el nombre de usuario
        userName = user.username
    else:
        # Si el usuario no está autenticado, establecer userName como None
        userName = None
        
    tema = Temarios.objects.get(idTemarios=id_tema)
    # Obtener todas las preguntas gratuitas

    preguntas_gratuitas = Preguntas.objects.filter(fkTemarios=id_tema)[:280]


    # Obtener todas las respuestas disponibles
    respuestas_todas = Respuestas.objects.filter()

        # Lista para almacenar las preguntas con sus respuestas mezcladas
    preguntas_con_respuestas_mezcladas = []

        # Iterar sobre cada pregunta gratuita
    for pregunta in preguntas_gratuitas:
            # Obtener la respuesta correcta asociada a la pregunta
        respuesta_correcta = Respuestas.objects.get(fkPregunta=pregunta)
            
            # Obtener tres respuestas incorrectas aleatorias de entre todas las respuestas disponibles,
            # excluyendo la respuesta correcta
        respuestas_incorrectas = random.sample(list(respuestas_todas.exclude(pk=respuesta_correcta.pk)), 3)
            
            # Combinar la respuesta correcta con las respuestas incorrectas
        respuestas_mezcladas = [respuesta_correcta] + respuestas_incorrectas
            
            # Mezclar aleatoriamente las respuestas
        random.shuffle(respuestas_mezcladas)
            
            # Agregar la pregunta y sus respuestas mezcladas a la lista
        preguntas_con_respuestas_mezcladas.append((pregunta, respuestas_mezcladas))

        # Mezclar aleatoriamente las preguntas con sus respuestas
        random.shuffle(preguntas_con_respuestas_mezcladas)

    context = {
            'userName': userName,
            'preguntas_con_respuestas_mezcladas': preguntas_con_respuestas_mezcladas,
            'tema':tema,
            'tipo_tiempo':tipo_tiempo
        }

    return render(request,template_name,context)


def detalles_intento(request, intento_id):
    intentos = RegistroRespuestaPreguntas.objects.filter(numeroIntento=intento_id).select_related(
        'fkPregunta', 'fkRespuesta', 'fkPregunta__fkCategorias', 'fkUser'
    )

    datos = []
    for resultado in intentos:
        pregunta = resultado.fkPregunta
        respuesta_correcta = Respuestas.objects.get(fkPregunta=pregunta)
        es_correcta = (resultado.fkRespuesta == respuesta_correcta)

        datos.append({
            'categoria': pregunta.fkCategorias.descripcionCategoria,
            'pregunta': pregunta.nombrePregunta,
            'respuesta': resultado.fkRespuesta.nombreRespuestas,
            'es_correcta': es_correcta,
            'justificacion': pregunta.justificacionPregunta,
            'usuario': resultado.fkUser.username,
        })

    context = {
        'intento_id': intento_id,
        'datos': datos
    }
    return render(request, 'mostrar_intento.html', context)

def lista_intentos(request):
    intentos = RegistroRespuestaPreguntas.objects.filter(fkUser=request.user).values(
        'numeroIntento', 'fkPregunta__fkTemarios__nombreTemario','fechaContestacion'
    ).distinct().order_by('fkPregunta__fkTemarios__nombreTemario', 'numeroIntento')
    
    context = {
        'intentos': intentos
    }
    return render(request, 'Estadisticos/resultados.html', context)


def detalle_intento(request, numero_intento, tema):
    intentos = RegistroRespuestaPreguntas.objects.filter(fkUser=request.user, numeroIntento=numero_intento, fkPregunta__fkTemarios__nombreTemario=tema)

    # Contador para respuestas correctas
    respuestas_correctas = 0

    for intento in intentos:
        pregunta = intento.fkPregunta
        respuesta_correcta = Respuestas.objects.get(fkPregunta=pregunta)
        es_correcta = (intento.fkRespuesta == respuesta_correcta)
        

        # Actualizar el campo 'es_correcta' del intento
        intento.es_correcta = es_correcta

        # Incrementar el contador si la respuesta es correcta
        if es_correcta:
            respuestas_correctas += 1

        # Agregar la justificación si la respuesta es incorrecta
        if not es_correcta:
            justificacion = pregunta.justificacionPregunta
            intento.justificacion = justificacion

    context = {
        'intentos': intentos,
        'numero_intento': numero_intento,
        'tema': tema,
        'respuestas_correctas': respuestas_correctas,  # Pasar el conteo al contexto
        
    }
    return render(request, 'Estadisticos/detalles_intento.html', context)



def dashboard(request):
    user = request.user
    intentos = RegistroRespuestaPreguntas.objects.filter(fkUser=user).select_related(
        'fkPregunta', 'fkRespuesta', 'fkPregunta__fkCategorias', 'fkPregunta__fkTemarios'
    )

    total_intentos = RegistroRespuestaPreguntas.objects.filter(fkUser=user).values(
        'numeroIntento', 'fkPregunta__fkTemarios__nombreTemario'
    ).distinct().order_by('fkPregunta__fkTemarios__nombreTemario', 'numeroIntento').count()

    total_respuestas = intentos.count()

    total_correctas = 0
    intentos_por_categoria = {}
    intentos_por_tema = {}

    for intento in intentos:
        pregunta = intento.fkPregunta
        respuesta_correcta = Respuestas.objects.get(fkPregunta=pregunta)
        es_correcta = (intento.fkRespuesta == respuesta_correcta)

        if es_correcta:
            total_correctas += 1

        categoria = pregunta.fkCategorias.descripcionCategoria
        if categoria not in intentos_por_categoria:
            intentos_por_categoria[categoria] = {'total': 0, 'correctas': 0}
        intentos_por_categoria[categoria]['total'] += 1
        if es_correcta:
            intentos_por_categoria[categoria]['correctas'] += 1

        tema = pregunta.fkTemarios.nombreTemario
        if tema not in intentos_por_tema:
            intentos_por_tema[tema] = 0
        intentos_por_tema[tema] += 1

    total_incorrectas = total_respuestas - total_correctas

    if total_respuestas > 0:
        porcentaje_correctas = (total_correctas / total_respuestas) * 100
    else:
        porcentaje_correctas = 0

    intentos_por_categoria_list = [{'categoria': k, 'total': v['total'], 'correctas': v['correctas'], 'porcentaje_correctas': (v['correctas'] / v['total']) * 100} for k, v in intentos_por_categoria.items()]
    intentos_por_tema_list = [{'tema': k, 'total': v} for k, v in intentos_por_tema.items()]

    # Datos para la gráfica de barras
    categorias = [item['categoria'] for item in intentos_por_categoria_list]
    totales = [item['total'] for item in intentos_por_categoria_list]

    context = {
        'total_intentos': total_intentos,
        'total_respuestas': total_respuestas,
        'total_correctas': total_correctas,
        'total_incorrectas': total_incorrectas,
        'porcentaje_correctas': porcentaje_correctas,
        'intentos_por_categoria': intentos_por_categoria_list,
        'intentos_por_tema': intentos_por_tema_list,
        'categorias': categorias,
        'totales': totales,
        'user': user
    }

    return render(request, 'Estadisticos/dashboard.html', context)


def simulador_diagnostico(request):
    template_name = 'Simulator/simulator_diagnostico.html'
    
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener el usuario autenticado
        user = request.user
        
        try:
            # Obtener el último intento del usuario actual
            ultimo_intento = Intentos.objects.filter(fkUser=user,fkCategorias=5).latest('fechaIntento')

            # Obtener la fecha actual
            fecha_actual = date.today()
            
            # Obtener la fecha del último intento
            fecha_ultimo_intento = ultimo_intento.fechaIntento
            # Calcular la fecha hace 24 horas
            fecha_hace_45_horas = fecha_actual + timedelta(days=45)
            # Verificar si ha pasado más de 24 horas desde el último intento
            revisionIntento =    fecha_ultimo_intento > fecha_hace_45_horas

        except ObjectDoesNotExist:
            revisionIntento = True
        # Obtener el nombre de usuario
        userName = user.username
    else:
        # Si el usuario no está autenticado, establecer userName como None
        userName = None
        revisionIntento = None

    # Obtener todas las preguntas gratuitas
    preguntas_gratuitas = Preguntas.objects.filter(fkCategorias__descripcionCategoria='Diagnostico')[:100]

    # Obtener todas las respuestas disponibles
    respuestas_todas = Respuestas.objects.filter(fkCategorias=5)

        # Lista para almacenar las preguntas con sus respuestas mezcladas
    preguntas_con_respuestas_mezcladas = []

        # Iterar sobre cada pregunta gratuita
    for pregunta in preguntas_gratuitas:
            # Obtener la respuesta correcta asociada a la pregunta
        respuesta_correcta = Respuestas.objects.get(fkPregunta=pregunta)
            
            # Obtener tres respuestas incorrectas aleatorias de entre todas las respuestas disponibles,
            # excluyendo la respuesta correcta
        respuestas_incorrectas = random.sample(list(respuestas_todas.exclude(pk=respuesta_correcta.pk)), 3)
            
            # Combinar la respuesta correcta con las respuestas incorrectas
        respuestas_mezcladas = [respuesta_correcta] + respuestas_incorrectas
            
            # Mezclar aleatoriamente las respuestas
        random.shuffle(respuestas_mezcladas)
            
            # Agregar la pregunta y sus respuestas mezcladas a la lista
        preguntas_con_respuestas_mezcladas.append((pregunta, respuestas_mezcladas))

        # Mezclar aleatoriamente las preguntas con sus respuestas
        random.shuffle(preguntas_con_respuestas_mezcladas)

    context = {
            'userName': userName,
            'Intento': revisionIntento,
            'preguntas_con_respuestas_mezcladas': preguntas_con_respuestas_mezcladas,
        }

    return render(request, template_name, context)



def actualizarDatos(request):
    user = request.user

    if request.method == 'POST':
        if 'username' in request.POST:
            actualizar_username(request, user)
        elif 'email' in request.POST:
            actualizar_email(request, user)
        elif 'password' in request.POST:
            actualizar_password(request, user)

        messages_html = []
        for message in messages.get_messages(request):
            messages_html.append(str(message))

        message = None
        if messages_html:
            message = messages_html[0]

        
        return JsonResponse({'message': message})

    return render(request, 'Perfil/actualizar_datos.html', {'userProfile': user})

def actualizar_username(request, user):
    if 'username' in request.POST:
        user.username = request.POST['username']
        user.save()
        messages.success(request, 'Nombre de usuario actualizado con éxito')

def actualizar_email(request, user):
    if 'email' in request.POST:
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'Correo electrónico actualizado con éxito')

def actualizar_password(request, user):
    if 'password' in request.POST:
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user.set_password(password)
            user.save()
            messages.success(request, 'Contraseña actualizada con éxito')
        else:
            messages.error(request, 'Las contraseñas no coinciden')

def forocomentarios(request):
    template_name = 'forocomentarios.html'
    comentarioUser = ForoUsuarios.objects.all().order_by('-idForo')
    context = {
        'comentarioUser':comentarioUser
    }
    return render(request,template_name,context)

def update_username_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comentario = data.get('comentario')
        puntuacion = data.get('puntuacion')
        user = request.user

        ForoUsuarios.objects.create(
            mensajeForo=comentario,
            valorMensaje=puntuacion,
            fk_User=user
        )
        return JsonResponse({'success': True})

    return render(request, 'tu_template.html')

def pricing(request):
    template_name = 'pricing.html'

    if request.user.is_authenticated:
        user = request.user
        try:
            # Obtener el registro más reciente de PaypalPago para el usuario actual
            ultimo_pago = PaypalPago.objects.filter(fk_User=user).latest('fecha_pago')

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            # Calcular la diferencia de tiempo entre la fecha del último pago y la fecha actual
            diferencia_tiempo = fecha_actual - ultimo_pago.fecha_pago

            if ultimo_pago.tipo_membresia == 'Mensual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 30
            elif ultimo_pago.tipo_membresia == 'Trimestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 90
            elif ultimo_pago.tipo_membresia == 'Semestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 180
            elif ultimo_pago.tipo_membresia == 'Anual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 365

        except PaypalPago.DoesNotExist:
            # Manejar el caso en el que no exista ningún registro de PaypalPago para el usuario actual
            es_mayor_a_30_dias = True
            ultimo_pago = None  # Ajustar a None si no hay registro

    else:
        es_mayor_a_30_dias = True
        ultimo_pago = None  # Ajustar a None si el usuario no está autenticado

    context = {
        'es_mayor_a_30_dias': es_mayor_a_30_dias,
        'ultimo_pago': ultimo_pago
    }

    return render(request, template_name, context)


def blog(request):
    template_name ='blog.html'
    topics = blogTema.objects.all()

    context = {
        'topics':topics
    }
    return render(request,template_name,context)

def blogtemas(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        topico = data.get('topico')
        
        user = request.user

        blogTema.objects.create(
            titleTopic=topico,
            fk_User=user
        )
        return JsonResponse({'success': True})

    return render(request, 'tu_template.html')

def blogcomentarios(request):
    template_name ='blogcomentarios.html'
    id_tema = request.GET.get('id_tema')
    topics = blogTema.objects.get(idBlog=id_tema)
    comentarios = blogComentario.objects.filter(fk_Topic=id_tema).order_by('-idBlogComentario')
    context = {
        'topics':topics,
        'comentarios':comentarios
    }
    return render(request,template_name,context)

def registertemascomentarios(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_tema = data.get('id_tema')
        comentario = data.get('comentario')
        instance_tema = blogTema.objects.get(idBlog=id_tema)
        user = request.user

        blogComentario.objects.create(
            comentarioTitle=comentario,
            fk_Topic=instance_tema,
            fk_User=user
        )
        return JsonResponse({'success': True})

    return render(request, 'tu_template.html')

def blogansiedad(request):
    template_name = 'blog1.html'
    if request.user.is_authenticated:
        user = request.user
        
        try:
            # Obtener el registro más reciente de PaypalPago para el usuario actual
            ultimo_pago = PaypalPago.objects.filter(fk_User=user).latest('fecha_pago')

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            # Calcular la diferencia de tiempo entre la fecha del último pago y la fecha actual
            diferencia_tiempo = fecha_actual - ultimo_pago.fecha_pago

            if ultimo_pago.tipo_membresia == 'Mensual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 30
            elif ultimo_pago.tipo_membresia == 'Trimestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 90
            elif ultimo_pago.tipo_membresia == 'Semestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 180
            elif ultimo_pago.tipo_membresia == 'Anual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 365

        except PaypalPago.DoesNotExist:
            # Manejar el caso en el que no exista ningún registro de PaypalPago para el usuario actual
            es_mayor_a_30_dias = True
    else:
        es_mayor_a_30_dias = True

    context = {
        'es_mayor_a_30_dias':es_mayor_a_30_dias
    }
    return render(request,template_name,context)

def blogestudio(request):
    template_name = 'blog2.html'
    if request.user.is_authenticated:
        user = request.user
        
        try:
            # Obtener el registro más reciente de PaypalPago para el usuario actual
            ultimo_pago = PaypalPago.objects.filter(fk_User=user).latest('fecha_pago')

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            # Calcular la diferencia de tiempo entre la fecha del último pago y la fecha actual
            diferencia_tiempo = fecha_actual - ultimo_pago.fecha_pago

            if ultimo_pago.tipo_membresia == 'Mensual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 30
            elif ultimo_pago.tipo_membresia == 'Trimestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 90
            elif ultimo_pago.tipo_membresia == 'Semestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 180
            elif ultimo_pago.tipo_membresia == 'Anual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 365

        except PaypalPago.DoesNotExist:
            # Manejar el caso en el que no exista ningún registro de PaypalPago para el usuario actual
            es_mayor_a_30_dias = True
    else:
        es_mayor_a_30_dias = True

    context = {
        'es_mayor_a_30_dias':es_mayor_a_30_dias
    }
    return render(request,template_name,context)



def blogmotivado(request):
    template_name = 'blog3.html'
    if request.user.is_authenticated:
        user = request.user
        
        try:
            # Obtener el registro más reciente de PaypalPago para el usuario actual
            ultimo_pago = PaypalPago.objects.filter(fk_User=user).latest('fecha_pago')

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            # Calcular la diferencia de tiempo entre la fecha del último pago y la fecha actual
            diferencia_tiempo = fecha_actual - ultimo_pago.fecha_pago

            if ultimo_pago.tipo_membresia == 'Mensual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 30
            elif ultimo_pago.tipo_membresia == 'Trimestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 90
            elif ultimo_pago.tipo_membresia == 'Semestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 180
            elif ultimo_pago.tipo_membresia == 'Anual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 365

        except PaypalPago.DoesNotExist:
            # Manejar el caso en el que no exista ningún registro de PaypalPago para el usuario actual
            es_mayor_a_30_dias = True
    else:
        es_mayor_a_30_dias = True

    context = {
        'es_mayor_a_30_dias':es_mayor_a_30_dias
    }
    return render(request,template_name,context)

# -------------------Paypal--------------------

# URL de la API de PayPal
PAYPAL_API_URL = "https://api.paypal.com"  # Utiliza el endpoint de producción
PAYPAL_CLIENT_ID = "AQ775mnIfb4xNzjBsFfuDh67Ubatx_Hu_Ek5wur3MpoBeR8LIeX1UvZqdgcBoChKHgV7RTjD-Sh6PA_b"  # Reemplaza con tu client ID de PayPal
PAYPAL_SECRET = "EL6vnaSKnNJLvK1mOG19lBMTx7uYXbK-q4yO9SmRr4SvyXydu6AcG3aWDUspi1G28qrPIT7fCVKqnsmF"  # Reemplaza con tu secret de PayPal

def get_paypal_access_token():
    response = requests.post(
        f"{PAYPAL_API_URL}/v1/oauth2/token",
        headers={"Accept": "application/json", "Accept-Language": "en_US"},
        data={"grant_type": "client_credentials"},
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
    )
    response.raise_for_status()
    return response.json()["access_token"]


def paypal(request):
    template_name = 'pagomensual.html'
    if request.user.is_authenticated:
        user = request.user
        
        try:
            # Obtener el registro más reciente de PaypalPago para el usuario actual
            ultimo_pago = PaypalPago.objects.filter(fk_User=user).latest('fecha_pago')

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            # Calcular la diferencia de tiempo entre la fecha del último pago y la fecha actual
            diferencia_tiempo = fecha_actual - ultimo_pago.fecha_pago

            if ultimo_pago.tipo_membresia == 'Mensual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 30
            elif ultimo_pago.tipo_membresia == 'Trimestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 90
            elif ultimo_pago.tipo_membresia == 'Semestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 180
            elif ultimo_pago.tipo_membresia == 'Anual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 365

        except PaypalPago.DoesNotExist:
            # Manejar el caso en el que no exista ningún registro de PaypalPago para el usuario actual
            es_mayor_a_30_dias = True
    else:
        es_mayor_a_30_dias = True

    context ={
        'es_mayor_a_30_dias':es_mayor_a_30_dias
    }

    return render(request,template_name, context)

def paypaltrimestral(request):
    template_name = 'pagotrimestral.html'
    if request.user.is_authenticated:
        user = request.user
        
        try:
            # Obtener el registro más reciente de PaypalPago para el usuario actual
            ultimo_pago = PaypalPago.objects.filter(fk_User=user).latest('fecha_pago')

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            # Calcular la diferencia de tiempo entre la fecha del último pago y la fecha actual
            diferencia_tiempo = fecha_actual - ultimo_pago.fecha_pago

            if ultimo_pago.tipo_membresia == 'Mensual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 30
            elif ultimo_pago.tipo_membresia == 'Trimestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 90
            elif ultimo_pago.tipo_membresia == 'Semestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 180
            elif ultimo_pago.tipo_membresia == 'Anual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 365

        except PaypalPago.DoesNotExist:
            # Manejar el caso en el que no exista ningún registro de PaypalPago para el usuario actual
            es_mayor_a_30_dias = True
    else:
        es_mayor_a_30_dias = True

    context ={
        'es_mayor_a_30_dias':es_mayor_a_30_dias
    }

    return render(request,template_name, context)

def paypalsemestral(request):
    template_name = 'pagosemestral.html'
    if request.user.is_authenticated:
        user = request.user
        
        try:
            # Obtener el registro más reciente de PaypalPago para el usuario actual
            ultimo_pago = PaypalPago.objects.filter(fk_User=user).latest('fecha_pago')

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            # Calcular la diferencia de tiempo entre la fecha del último pago y la fecha actual
            diferencia_tiempo = fecha_actual - ultimo_pago.fecha_pago

            if ultimo_pago.tipo_membresia == 'Mensual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 30
            elif ultimo_pago.tipo_membresia == 'Trimestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 90
            elif ultimo_pago.tipo_membresia == 'Semestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 180
            elif ultimo_pago.tipo_membresia == 'Anual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 365

        except PaypalPago.DoesNotExist:
            # Manejar el caso en el que no exista ningún registro de PaypalPago para el usuario actual
            es_mayor_a_30_dias = True
    else:
        es_mayor_a_30_dias = True

    context ={
        'es_mayor_a_30_dias':es_mayor_a_30_dias
    }

    return render(request,template_name, context)

def paypalanual(request):
    template_name = 'pagoanual.html'
    if request.user.is_authenticated:
        user = request.user
        
        try:
            # Obtener el registro más reciente de PaypalPago para el usuario actual
            ultimo_pago = PaypalPago.objects.filter(fk_User=user).latest('fecha_pago')

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            # Calcular la diferencia de tiempo entre la fecha del último pago y la fecha actual
            diferencia_tiempo = fecha_actual - ultimo_pago.fecha_pago

            if ultimo_pago.tipo_membresia == 'Mensual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 30
            elif ultimo_pago.tipo_membresia == 'Trimestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 90
            elif ultimo_pago.tipo_membresia == 'Semestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 180
            elif ultimo_pago.tipo_membresia == 'Anual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 365

        except PaypalPago.DoesNotExist:
            # Manejar el caso en el que no exista ningún registro de PaypalPago para el usuario actual
            es_mayor_a_30_dias = True
    else:
        es_mayor_a_30_dias = True

    context ={
        'es_mayor_a_30_dias':es_mayor_a_30_dias
    }

    return render(request,template_name,context)



def create_order(request):
    if request.method == 'POST':
        access_token = get_paypal_access_token()
        data = json.loads(request.body)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "MXN",
                    "value": "299.0"  # Ajusta según el precio total de los productos
                }
            }]
        }

        response = requests.post(
            f"{PAYPAL_API_URL}/v2/checkout/orders",
            headers=headers,
            json=payload
        )

        order_data = response.json()
        return JsonResponse(order_data)
    return JsonResponse({"error": "Invalid request"}, status=400)

def create_order_anual(request):
    if request.method == 'POST':
        access_token = get_paypal_access_token()
        data = json.loads(request.body)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "MXN",
                    "value": "3000.0"  # Ajusta según el precio total de los productos
                }
            }]
        }
        
        response = requests.post(
            f"{PAYPAL_API_URL}/v2/checkout/orders",
            headers=headers,
            json=payload
        )
        
        order_data = response.json()
        return JsonResponse(order_data)
    return JsonResponse({"error": "Invalid request"}, status=400)

def create_order_trimestral(request):
    if request.method == 'POST':
        access_token = get_paypal_access_token()
        data = json.loads(request.body)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "MXN",
                    "value": "629.0"  # Ajusta según el precio total de los productos
                }
            }]
        }
        
        response = requests.post(
            f"{PAYPAL_API_URL}/v2/checkout/orders",
            headers=headers,
            json=payload
        )
        
        order_data = response.json()
        return JsonResponse(order_data)
    return JsonResponse({"error": "Invalid request"}, status=400)

def create_order_semestral(request):
    if request.method == 'POST':
        access_token = get_paypal_access_token()
        data = json.loads(request.body)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "MXN",
                    "value": "1500.0"  # Ajusta según el precio total de los productos
                }
            }]
        }
        
        response = requests.post(
            f"{PAYPAL_API_URL}/v2/checkout/orders",
            headers=headers,
            json=payload
        )
        
        order_data = response.json()
        return JsonResponse(order_data)
    return JsonResponse({"error": "Invalid request"}, status=400)


def capture_order(request, order_id):
    if request.method == 'POST':
        access_token = get_paypal_access_token()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        
        response = requests.post(
            f"{PAYPAL_API_URL}/v2/checkout/orders/{order_id}/capture",
            headers=headers,
        )
        
        user = request.user
        capture_data = response.json()
        create_time = capture_data['purchase_units'][0]['payments']['captures'][0]['create_time']
        value_coin = capture_data['purchase_units'][0]['payments']['captures'][0]['amount']['value']
        transaction_status = capture_data['purchase_units'][0]['payments']['captures'][0]['status']
        transaction_id = capture_data['purchase_units'][0]['payments']['captures'][0]['id']

        if float(value_coin) < 310:
            # Crear una instancia de RegistroRespuestaPreguntas y guardarla en la base de datos
            registro_pago = PaypalPago.objects.create(
                fecha_pago=create_time,
                monto_pago=value_coin,
                status_pago=transaction_status,
                folio_pago=transaction_id,
                tipo_membresia='Mensual',
                fk_User=user  # Asignar el número de intento al registro
            )
        elif float(value_coin) > 310 and float(value_coin) < 700:
               registro_pago = PaypalPago.objects.create(
                fecha_pago=create_time,
                monto_pago=value_coin,
                status_pago=transaction_status,
                folio_pago=transaction_id,
                tipo_membresia='Trimestral',
                fk_User=user  # Asignar el número de intento al registro
            )
        elif float(value_coin) > 700 and float(value_coin) < 1600:
             # Crear una instancia de RegistroRespuestaPreguntas y guardarla en la base de datos
            registro_pago = PaypalPago.objects.create(
                fecha_pago=create_time,
                monto_pago=value_coin,
                status_pago=transaction_status,
                folio_pago=transaction_id,
                tipo_membresia='Semestral',
                fk_User=user  # Asignar el número de intento al registro
            )

        else:
            # Crear una instancia de RegistroRespuestaPreguntas y guardarla en la base de datos
            registro_pago = PaypalPago.objects.create(
                fecha_pago=create_time,
                monto_pago=value_coin,
                status_pago=transaction_status,
                folio_pago=transaction_id,
                tipo_membresia='Anual',
                fk_User=user  # Asignar el número de intento al registro
            )

        return JsonResponse(capture_data)
    return JsonResponse({"error": "Invalid request"}, status=400)



def historialPagos(request):
    template_name = 'payments.html'

    user = request.user

    historial_pagos = PaypalPago.objects.filter(fk_User=user)

    context ={
        'historial_pagos':historial_pagos
    }

    return render(request,template_name,context)

def PersonasPagos(request):
    template_name = 'adminTable.html'
    # Obtener todos los usuarios con pagos y sin pagos
    usuarios_con_pago = PaypalPago.objects.values_list('fk_User', flat=True).distinct()
    usuarios_con_pago = User.objects.filter(pk__in=usuarios_con_pago)
    usuarios_sin_pago = User.objects.exclude(pk__in=usuarios_con_pago)

    # Obtener los últimos pagos asociados a los usuarios con pago
    pagos_por_usuario = {}
    for usuario in usuarios_con_pago:
        ultimo_pago = PaypalPago.objects.filter(fk_User=usuario).aggregate(ultimo_pago=Max('fecha_pago'))
        if ultimo_pago['ultimo_pago']:
            pagos_por_usuario[usuario] = PaypalPago.objects.filter(fk_User=usuario, fecha_pago=ultimo_pago['ultimo_pago'])
    
    if request.user.is_authenticated:
        user = request.user
        
        try:
            # Obtener el registro más reciente de PaypalPago para el usuario actual
            ultimo_pago = PaypalPago.objects.filter(fk_User=user).latest('fecha_pago')

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            # Calcular la diferencia de tiempo entre la fecha del último pago y la fecha actual
            diferencia_tiempo = fecha_actual - ultimo_pago.fecha_pago

            if ultimo_pago.tipo_membresia == 'Mensual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 30
            elif ultimo_pago.tipo_membresia == 'Trimestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 90
            elif ultimo_pago.tipo_membresia == 'Semestral':
                es_mayor_a_30_dias = diferencia_tiempo.days > 180
            elif ultimo_pago.tipo_membresia == 'Anual':
                es_mayor_a_30_dias = diferencia_tiempo.days > 365

        except PaypalPago.DoesNotExist:
            # Manejar el caso en el que no exista ningún registro de PaypalPago para el usuario actual
            es_mayor_a_30_dias = True

    
    context = {
        'usuarios_con_pago': usuarios_con_pago,
        'usuarios_sin_pago': usuarios_sin_pago,
        'pagos_por_usuario': pagos_por_usuario,
        'es_mayor_a_30_dias':es_mayor_a_30_dias
    }

    return render(request, template_name, context)

def eliminar_item(request):
    if request.method == 'POST' and request.user.is_superuser:
        item_type = request.POST.get('item_type')
        item_id = request.POST.get('item_id')
        if item_type == 'topic':
            item = get_object_or_404(blogTema, idBlog=item_id)
        elif item_type == 'comment':
            item = get_object_or_404(blogComentario, idBlogComentario=item_id)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid item type'}, status=400)
        
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def eliminar_comentario(request):
    if request.method == 'POST' and request.user.is_superuser:
        id_comentario = request.POST.get('id_comentario')
        comentario = get_object_or_404(blogComentario, idBlogComentario=id_comentario)
        comentario.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
