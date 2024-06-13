from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Categorias(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    descripcionCategoria = models.CharField(max_length=200)
    class Meta:
        db_table = 'Categorias'

class Temarios(models.Model):
    idTemarios = models.AutoField(primary_key=True)
    nombreTemario = models.CharField(max_length=300)

    class Meta:
        db_table = 'Temarios'

class Preguntas(models.Model):
    idPregunta = models.AutoField(primary_key=True)
    nombrePregunta = models.TextField()
    nivelPregunta = models.CharField(max_length=300,default='Baja')
    justificacionPregunta = models.TextField(default='')
    fkTemarios = models.ForeignKey(Temarios,on_delete=models.CASCADE,default=1) 
    fkCategorias = models.ForeignKey(Categorias, on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = 'Preguntas'

class Respuestas(models.Model):
    idRespuestas = models.AutoField(primary_key=True)
    nombreRespuestas = models.TextField()
    statusRespuestas = models.TextField(default='Correcto')
    fkPregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    fkCategorias = models.ForeignKey(Categorias, on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = 'Respuestas'

class RegistroRespuestaPreguntas(models.Model):
    idRespuestaPreguntas = models.AutoField(primary_key=True)
    fkUser = models.ForeignKey(User,on_delete=models.CASCADE)
    fkPregunta = models.ForeignKey(Preguntas,on_delete=models.CASCADE)
    fkRespuesta = models.ForeignKey(Respuestas,on_delete=models.CASCADE)
    numeroIntento = models.IntegerField(default=1)
    fechaContestacion = models.DateField(default=timezone.now)
    class Meta:
        db_table = 'RespuestasPreguntas'

class Intentos(models.Model):
    idIntento = models.AutoField(primary_key=True)
    fechaIntento = models.DateField()
    fkCategorias = models.ForeignKey(Categorias, on_delete=models.CASCADE,default=0)
    fkUser = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Intentos'

class ActiveSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.session_key}"


class ForoUsuarios(models.Model):
    idForo = models.AutoField(primary_key=True)
    mensajeForo = models.TextField()
    valorMensaje = models.SmallIntegerField()
    fk_User = models.ForeignKey(User,on_delete=models.CASCADE)
    class meta:
        db_table = 'ForoUsuarios'


class blogTema(models.Model):
    idBlog = models.AutoField(primary_key=True)
    titleTopic = models.TextField()
    fk_User = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = 'blogTema'

class blogComentario(models.Model):
    idBlogComentario = models.AutoField(primary_key=True)
    comentarioTitle = models.TextField()
    fk_Topic = models.ForeignKey(blogTema,on_delete=models.CASCADE)
    fk_User = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = 'blogComentario'

class PaypalPago(models.Model):
    idPayment = models.AutoField(primary_key=True)
    fecha_pago = models.DateTimeField()
    monto_pago = models.CharField(max_length=255)
    status_pago = models.CharField(max_length=255)
    folio_pago = models.CharField(max_length=255)
    tipo_membresia = models.CharField(max_length=255,default='')
    fk_User = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = 'PaypalPago'

class PanelInformation(models.Model):
    idPanel = models.AutoField(primary_key=True)
    titlePanel = models.TextField()
    fechaPanel = models.DateField(default=datetime.date.today)
    texto_uno = models.TextField()
    tituloPanel_dos = models.TextField()
    texto_dos = models.TextField()
    tituloPanel_tres = models.TextField()
    texto_tres = models.TextField()
    texto_referencia = models.TextField(default='')
    tipoBlog = models.TextField(default='')

    class Meta:
        db_table = 'PanelInformation'