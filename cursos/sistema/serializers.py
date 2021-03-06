from rest_framework import serializers
from .models import  Curso, Calificacion, Asignacion
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id','nombre_curso','info']

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ['id','materia', 'estudiante', 'calificacion']

class AsignacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignacion
        fields = ['id','curso', 'nombre_estudiante',]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','email','password','is_student','is_teacher')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.get_or_create(validated_data['first_name'],validated_data['last_name'], validated_data['is_student'], validated_data['is_teacher'],validated_data['username'], validated_data['email'], validated_data['password'])
            return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email','is_student','is_teacher')
