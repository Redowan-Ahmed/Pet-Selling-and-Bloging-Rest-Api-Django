from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AnimalBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalBreed
        fields = ['breed_name']


class AnimalColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalColor
        fields = ['animal_color']


class AnimalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImage
        fields = ['image']


class AnimalLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalLocation
        fields = ['location']


class AnimalSerializer(serializers.ModelSerializer):
    """ animal_category = CategorySerializer() """
    animal_category = serializers.SerializerMethodField()
    animal_color = AnimalColorSerializer(many=True)
    animal_breed = AnimalBreedSerializer(many=True)
    # animal_images = AnimalImageSerializer(many=True)
    animal_locations = AnimalLocationSerializer(many=True)

    def get_animal_category(self, object):
        return object.animal_category.category_name

    """ def to_representation(self, instance):
        payload = {
            'animal_name': instance.animal_name
        }
        return payload """

    def create(self, validated_data):
        animal_breed = validated_data.pop('animal_breed')
        animal_color = validated_data.pop('animal_color')
        animal_locations = validated_data.pop('animal_locations')
        print(validated_data)
        return Animal.objects.create(**validated_data)

    class Meta:
        model = Animal
        exclude = ['updated_at',]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if 'username' in data:
            user = User.objects.filter(username=data['username'])
            if user.exists():
                raise serializers.ValidationError('User already exists')
        if 'email' in data:
            email = User.objects.filter(email=data['email'])
            if email.exists():
                raise serializers.ValidationError(
                    'Email Address already exists')
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if 'username' in data:
            user = User.objects.filter(username=data['username'])
            if not user.exists():
                raise serializers.ValidationError(
                    'User is not authenticated Please register')
        return data
