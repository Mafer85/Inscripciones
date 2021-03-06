from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Curso(models.Model):
    nombre_curso = models.CharField(max_length=30)
    info = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.nombre_curso


class Calificacion(models.Model):
    materia = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion = models.PositiveIntegerField()
    creado_el = models.DateTimeField(auto_now_add=True)
    modificado_el = models.DateTimeField(auto_now=True)


class Asignacion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre_estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
