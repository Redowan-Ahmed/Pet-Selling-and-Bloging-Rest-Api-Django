from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class PostApiView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serialize = PostSerializer(queryset, many=True)
        return Response({
            'status': True,
            'massage': 'Get request recieved successfully',
            'data': serialize.data,
        })

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            get_author = request.user.id
            data['author'] = get_author
            print(get_author)
            serialize = PostSerializer(data=data)
            if serialize.is_valid():
                serialize.save()
                return Response({
                    'status': True,
                    'Massage': 'Successfully posted',
                    'data': serialize.data,
                })
            return Response({
                'status': False,
                'Massage': 'one of the field has problem ',
                'errors': serialize.errors,
            })
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'massage': 'An error occurred',
                'error': str(e),
            })
