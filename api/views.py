from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django.db.models import Q,Count
from collections import defaultdict
from django.shortcuts import redirect, render
from api.models import Intentos, Preguntas,Categorias,Respuestas,RegistroRespuestaPreguntas,Temarios, ForoUsuarios,blogTema, blogComentario
from django.http import JsonResponse
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from datetime import date,  timedelta
import random, json
from django.db.models.functions import TruncDay
from django.contrib import messages

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
    context = {
        'mostrarTemario':mostrarTemario,
        'contadorTemario':contadorTemario,
        'contadorEnarm':contadorEnarm,
        'comentarioUser': comentarioUser
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

    return render(request,template_name)


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

    return render(request,template_name)

def blogestudio(request):
    template_name = 'blog2.html'

    return render(request,template_name)

def blogmotivado(request):
    template_name = 'blog3.html'

    return render(request,template_name)