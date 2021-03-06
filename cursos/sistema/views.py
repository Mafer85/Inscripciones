from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.views.generic import CreateView
from .serializers import CursoSerializer, CalificacionSerializer, AsignacionSerializer, LoginSerializer, UserSerializer, RegisterSerializer
from .models import User, Curso, Calificacion, Asignacion
from knox.views import LoginView as KnoxLoginView


"""Listado de cursos, solo deja verlos si se ha iniciado sesion"""
@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_cursos(request):
    user = request.user.id
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        cursos = Curso.objects.all()
        serializer = CursoSerializer(cursos, many=True)
        return JsonResponse({'cursos': serializer.data}, safe=False, status=status.HTTP_200_OK)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')


"""Crear un curso, solo deja crearlos si se ha iniciado sesion"""
@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_curso(request):
    payload = json.loads(request.body)
    user = request.user
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        try:
            curso = Curso.objects.create(
                    nombre_curso=payload["nombre_curso"],
                    info=payload["info"],
                )
            serializer = CursoSerializer(curso)
            return JsonResponse({'curso': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')


"""Actualizar el curso, pide autenticacion"""
@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_curso(request, curso_id):
    user = request.user.id
    payload = json.loads(request.body)
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        try:
            curso_item = Curso.objects.filter(id=curso_id)
            # returns 1 or 0
            curso_item.update(**payload)
            curso = Curso.objects.get(id=curso_id)
            serializer = CursoSerializer(curso)
            return JsonResponse({'curso': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')

"""Eliminar curso, se necesita autenticacion para poder eliminar """
@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_curso(request, curso_id):

    user = request.user.id
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        try:
            curso = Curso.objects.get(id=curso_id)
            curso.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')


"""Listar Estudiantes"""
@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_students(request):
    user = request.user.id
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        students = User.objects.filter(is_student=True)
        serializer = UserSerializer(students, many=True)
        return JsonResponse({'students': serializer.data}, safe=False, status=status.HTTP_200_OK)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')


"""Listar Asignaciones """
@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_asignaciones(request):
    user = request.user.id
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        asignaciones = Asignacion.objects.all()
        serializer = AsignacionSerializer(asignaciones, many=True)
        return JsonResponse({'asignaciones': serializer.data}, safe=False, status=status.HTTP_200_OK)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')


"""Asignar un alumno a un curso"""
@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_asignacion(request):
    payload = json.loads(request.body)
    user = request.user
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        try:
            asignacion = Asignacion.objects.create(
                    curso=Curso.objects.get(id=payload["curso"]),
                    nombre_estudiante=User.objects.get(id=payload["nombre_estudiante"]),
                )
            serializer = AsignacionSerializer(asignacion)
            return JsonResponse({'asignacion': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')

"""Actualizar asignacion de cursos a estudiante"""
@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_asignacion(request, asignacion_id):
    user = request.user.id
    payload = json.loads(request.body)
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        try:
            asignacion_item = Asignacion.objects.filter(id=asignacion_id)
            asignacion_item.update(
                curso=Curso.objects.get(id=payload["curso"]),
                nombre_estudiante=User.objects.get(id=payload["nombre_estudiante"])
            )
            asignacion = Asignacion.objects.get(id=asignacion_id)
            serializer = AsignacionSerializer(asignacion)
            return JsonResponse({'asignacion': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')



"""Eliminar la asignacion de los alumnos al curso"""
@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_asignacion(request, asignacion_id):

    user = request.user.id
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        try:
            asignacion = Asignacion.objects.get(id=asignacion_id)
            asignacion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')



"""Listar calificaciones"""
@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_calificaciones(request):
    user = request.user.id
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        calificaciones = Calificacion.objects.all()
        serializer = CalificacionSerializer(calificaciones, many=True)
        return JsonResponse({'calificaciones': serializer.data}, safe=False, status=status.HTTP_200_OK)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')

"""Asignar una nueva calificacion"""
@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_calificacion(request):
    payload = json.loads(request.body)
    user = request.user
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        try:
            calificacion = Calificacion.objects.create(
                    materia=Curso.objects.get(id=payload["materia"]),
                    estudiante=User.objects.get(id=payload["estudiante"]),
                    calificacion = payload["calificacion"]
                )
            serializer = CalificacionSerializer(calificacion)
            return JsonResponse({'calificacion': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')

"""Actualizar calificacion de un estudiante"""
@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_calificacion(request, calificacion_id):
    user = request.user.id
    payload = json.loads(request.body)
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        try:
            calificacion_item = Calificacion.objects.filter(id=calificacion_id)
            calificacion_item.update(
                materia=Curso.objects.get(id=payload["materia"]),
                estudiante=User.objects.get(id=payload["estudiante"]),
                calificacion = payload["calificacion"]
            )
            calificacion = Calificacion.objects.get(id=calificacion_id)
            serializer = CalificacionSerializer(calificacion)
            return JsonResponse({'calificacion': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')

"""Eliminar calificacion de un estudiante"""
@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_calificacion(request, calificacion_id):

    user = request.user.id
    is_teacher = request.user.is_teacher
    if is_teacher == True:
        try:
            calificacion = Calificacion.objects.get(id=calificacion_id)
            calificacion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response('Usuario de estudiante, no tiene acceso a esta accion')


"""Vista del estudiante: El estudiante solo puede ver sus calificaciones, sin modificar nada"""
@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def estudiante_view(request, id_estudiante):
    user = request.user.id
    is_student = request.user.is_student
    if is_student == True:
        students = Calificacion.objects.filter(estudiante=id_estudiante)
        serializer = CalificacionSerializer(students, many=True)
        return JsonResponse({'students': serializer.data}, safe=False, status=status.HTTP_200_OK)
    else:
        return Response('Usuario de administrador, no tiene acceso a esta accion')




class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class RegistrarUsuario(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
