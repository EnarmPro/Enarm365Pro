"""
URL configuration for D27 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import index, registration_view,simulador_free,registrar_preguntas, registrar_intentos, simulador_Personalizado,mostrarTemas,simuladorTema,mostrarTemasEnarm,simuladorEnarmUno,simuladorEnarmSeccionDos,simuladorEnarmSeccionTres,lista_intentos,detalle_intento,dashboard , simulador_diagnostico, seleccionDatosPersonalizado,actualizarDatos, forocomentarios, update_username_form, pricing 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/",include("django.contrib.auth.urls")),
    path("", index, name="index"),
    path("accounts/register/", registration_view, name="register"),
    path("simulator_free/", simulador_free, name="simulator_free"),
    path("registrar_preguntas/", registrar_preguntas, name="registrar_preguntas"),
    path("registrar_intento/", registrar_intentos, name="registrar_intento"),
    path("simulador_personalizado/", simulador_Personalizado, name="simulador_personalizado"),
    path("mostrar_temas/", mostrarTemas, name="mostrar_temas"),
    path("panel_personalizado/", seleccionDatosPersonalizado, name="panel_personalizado"),
    path("simulador_tema/", simuladorTema, name="simulador_tema"),
    path("mostrar_enarm/", mostrarTemasEnarm, name="mostrar_enarm"),
    path("simulador_enarm_uno/", simuladorEnarmUno, name="simulador_enarm_uno"),
    path("simulador_enarm_dos/", simuladorEnarmSeccionDos, name="simulador_enarm_dos"),
    path("simulador_enarm_tres/", simuladorEnarmSeccionTres, name="simulador_enarm_tres"),
    path("resultados/", lista_intentos, name="resultados"),
    path('detalle_intento/<int:numero_intento>/<str:tema>/', detalle_intento, name='detalle_intento'),
    path('dashboard/', dashboard, name='dashboard'),
    path('simulador_diagnostico/', simulador_diagnostico, name='simulador_diagnostico'),
    path('actualizar_datos/', actualizarDatos, name='actualizar_datos'),
    path('foro_comentarios/', forocomentarios, name='foro_comentarios'),
    path('update_username_form/', update_username_form, name='update_username_form'),
    path('pricing/', pricing, name='pricing'),
    
]

