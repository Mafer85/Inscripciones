from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from sistema.models import User, Curso, Calificacion, Asignacion
# Register your models here.
admin.site.register(User)
admin.site.register(Curso)
admin.site.register(Calificacion)
admin.site.register(Asignacion)
