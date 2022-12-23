from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (Animal)
from .serializers import (
    AnimalSerializer, RegisterSerializer, LoginSerializer)
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class AnimalView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Animal.objects.all()
        if request.GET.get('search'):
            search = request.GET.get('search')
            queryset = queryset.filter(
                Q(animal_name__icontains=search) |
                Q(animal_description__icontains=search) |
                Q(animal_breed__breed_name__icontains=search) |
                Q(animal_color__animal_color__icontains=search) |
                Q(animal_gender__iexact=search) |
                Q(animal_category__category_name__icontains=search)
            )
        serialize = AnimalSerializer(queryset, many=True)
        return Response({
            'Status': True,
            'massage': 'Animal Get',
            'data': serialize.data,
        })

    def put(self, request, *args, **kwargs):
        return Response({
            'Status': True,
            'massage': 'Animal put',
        })

    def patch(self, request, *args, **kwargs):
        return Response({
            'Status': True,
            'massage': 'Animal patch',
        })

    def delete(self, request, *args, **kwargs):
        return Response({
            'Status': True,
            'massage': 'Animal delete',
        })


class AnimalDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            get_data = Animal.objects.get(pk=pk)
            get_data.incrementViews()
            serialize = AnimalSerializer(get_data)
            return Response({
                'status': True,
                'massage': 'Success',
                'data': serialize.data,
            })
        except Exception as e:
            print("Error" + str(e))
            return Response({
                'status': 404,
                'massage': 'Something went wrong',
                'Error': str(e),
            })


class RegisterApi(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                user = User.objects.create(
                    username=serializer.data['username'],
                    email=serializer.data['email'],
                )
                user.set_password(serializer.data['password'])
                user.save()
                return Response({
                    'status': 200,
                    'massage': "You're Succcessfully Registered",
                    'data': serializer.data,
                })
            return Response({
                'status': 500,
                'massage': "Please check your inputed data ",
                'error': serializer.errors,
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'massage': "An Error currently occured",
                'error': str(e),
            })


class LoginApi(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                user = authenticate(
                    username=serializer.data['username'], password=serializer.data['password'])
                if user:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({
                        'status': 200,
                        'massage': "You're Succcessfully logged in",
                        'data': {
                            'token': str(token),
                        },
                    })
            return Response({
                'status': False,
                'massage': "Incorrect Password or username",
                'data': serializer.errors,
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'massage': "An Error currently occured",
                'error': str(e),
            })


class AnimalCreateApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            data['animal_owner_id'] = request.user.id
            serialize = AnimalSerializer(data=data)
            if serialize.is_valid():
                serialize.save()
                return Response({
                    'status': True,
                    'massage': 'Successfully created',
                    'data': serialize.data,
                })
            return Response({
                'status': False,
                'massage': 'Failed to create, Some Fields are required',
                'error': serialize.errors,
            })
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'massage': 'An error occurred',
                'error': str(e),
            })
