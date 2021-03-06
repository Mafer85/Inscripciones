"""cursos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework import routers
from django.contrib import admin
from django.urls import include, path
from knox import views as knox_views
from sistema.views import estudiante_view,delete_calificacion,update_calificacion,add_calificacion,get_calificaciones,delete_asignacion,update_asignacion,add_asignacion,get_asignaciones,get_cursos,add_curso,get_students,update_curso,delete_curso,LoginAPI, RegistrarUsuario, UserAPI

#router = routers.DefaultRouter()
#router.register(r'asignacion', AsignacionesViewSet)
urlpatterns = [
    #path('', include(router.urls)),
    #Urls cursos
    path('cursos',  get_cursos),
    path('add_curso', add_curso),
    path('update_curso/<int:curso_id>', update_curso),
    path('delete_curso/<int:curso_id>', delete_curso),

    #Urls alumnos
    path('alumnos', get_students),
    path('mis_cursos/<int:id_estudiante>', estudiante_view),
    #Urls asignaciones
    path('asignaciones', get_asignaciones),
    path('asignacion', add_asignacion),
    path('u_asignacion/<int:asignacion_id>', update_asignacion),
    path('d_asignacion/<int:asignacion_id>', delete_asignacion),

    #Urls calificaciones
    path('calificaciones', get_calificaciones),
    path('add_calificacion', add_calificacion),
    path('update_calificacion/<int:calificacion_id>', update_calificacion),
    path('delete_calificacion/<int:calificacion_id>', delete_calificacion),
    #Urls login, registro y admin
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login', LoginAPI.as_view()),
    path('register', RegistrarUsuario.as_view()),
    path('user', UserAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
]
