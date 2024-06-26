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
from django.urls import path, include,re_path
from django.contrib.auth import views as auth_views
from api.views import index, registration_view,simulador_free,registrar_preguntas, registrar_intentos, simulador_Personalizado,mostrarTemas,simuladorTema,mostrarTemasEnarm,simuladorEnarmUno,simuladorEnarmSeccionDos,simuladorEnarmSeccionTres,lista_intentos,detalle_intento,dashboard , simulador_diagnostico, seleccionDatosPersonalizado,actualizarDatos, forocomentarios, update_username_form, pricing,blog, blogtemas,blogcomentarios, registertemascomentarios ,blogansiedad,blogestudio,blogmotivado, paypal, create_order, capture_order,paypalanual,create_order_anual,historialPagos,create_order_trimestral,create_order_semestral, paypalsemestral,paypaltrimestral,PersonasPagos, eliminar_item, eliminar_comentario,revisionPreguntas,insertarPregunta,eliminar_pregunta,obtener_pregunta,editar_pregunta,revisionRespuestas, eliminar_respuesta, obtener_respuesta,actualizar_respuesta,modificarBlogInformativo,adminPagos, obtener_costos, actualizar_pago, cargarPreguntasExcel, cargar_preguntas_excel,error_404


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/",include("django.contrib.auth.urls")),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
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
    path('blog/', blog, name='blog'),
    path('blogtemas/', blogtemas, name='blogtemas'),
    path('blogcomentarios/', blogcomentarios, name='blogcomentarios'),
    path('registrar_comentarios/', registertemascomentarios, name='registrar_comentarios'),
    path('blogansiedad/', blogansiedad, name='blogansiedad'),
    path('blogestudio/', blogestudio, name='blogestudio'),
    path('blogmotivado/', blogmotivado, name='blogmotivado'),
    path('paypal/', paypal, name='paypal'),
    path('orders', create_order, name='create_order'),
    path('orders', create_order, name='create_order'),
    path('create_order_trimestral', create_order_trimestral, name='create_order_trimestral'),
    path('create_order_semestral', create_order_semestral, name='create_order_semestral'),
    path('create_order_anual', create_order_anual, name='create_order_anual'),
    path('orders/<str:order_id>/capture', capture_order, name='capture_order'),
    path('paypalanual/', paypalanual, name='paypalanual'),
    path('paypaltrimestral/', paypaltrimestral, name='paypaltrimestral'),
    path('paypalsemestral/', paypalsemestral, name='paypalsemestral'),
    path('historial_pagos/', historialPagos, name='historial_pagos'),
    path('PersonasPagos/', PersonasPagos, name='PersonasPagos'),
    path('eliminar_item/', eliminar_item, name='eliminar_item'),
    path('eliminar_comentario/', eliminar_comentario, name='eliminar_comentario'),
    path('revisionPreguntas/', revisionPreguntas, name='revisionPreguntas'),
    path('insertarPregunta/', insertarPregunta, name='insertarPregunta'),
    path('eliminar_pregunta/', eliminar_pregunta, name='eliminar_pregunta'),
    path('obtener_pregunta/', obtener_pregunta, name='obtener_pregunta'),
    path('editar_pregunta/', editar_pregunta, name='editar_pregunta'),
    path('revisionRespuestas/', revisionRespuestas, name='revisionRespuestas'),
    path('eliminar_respuesta/', eliminar_respuesta, name='eliminar_respuesta'),
    path('obtener_respuesta/', obtener_respuesta, name='obtener_respuesta'),
    path('actualizar_respuesta/', actualizar_respuesta, name='actualizar_respuesta'),
    path('modificarBlogInformativo/', modificarBlogInformativo, name='modificarBlogInformativo'),
    path('adminPagos/', adminPagos, name='adminPagos'),
    path('obtener_costos/', obtener_costos, name='obtener_costos'),
    path('actualizar_pago/', actualizar_pago, name='actualizar_pago'),
    path('cargarPreguntasExcel/', cargarPreguntasExcel, name='cargarPreguntasExcel'),
    path('cargar_preguntas_excel/', cargar_preguntas_excel, name='cargar_preguntas_excel'),
    re_path(r'^.*/$', error_404),
]

