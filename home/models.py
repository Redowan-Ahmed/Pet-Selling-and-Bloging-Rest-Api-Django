from django.db import models
from django.contrib.auth.models import User
from .choices import ANIMAL_GENDER_CHOICES
import uuid
from django.utils.text import slugify


class BaseModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        uid = str(uuid.uuid4()).split('-')
        self.slug = slugify(f'{self.category_name} {uid[0]}') + uid[0]
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class AnimalBreed(BaseModel):
    breed_name = models.CharField(max_length=100)

    def __str__(self):
        return self.breed_name


class AnimalColor(BaseModel):
    animal_color = models.CharField(max_length=100)

    def __str__(self):
        return self.animal_color


class Animal(BaseModel):
    animal_name = models.CharField(max_length=100)
    animal_description = models.TextField(max_length=500)
    animal_owner = models.ForeignKey(
        User, models.CASCADE, blank=True, related_name="animal")
    animal_category = models.ForeignKey(
        Category, models.CASCADE, related_name="animal_category")
    animal_gender = models.CharField(
        max_length=100, choices=ANIMAL_GENDER_CHOICES)
    animal_breed = models.ManyToManyField(AnimalBreed,  blank=True)
    animal_color = models.ManyToManyField(AnimalColor,  blank=True)
    animal_views = models.IntegerField(default=0, null=True, blank=True)
    animal_likes = models.IntegerField(default=0, null=True, blank=True)
    animal_slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        uid = str(uuid.uuid4()).split('-')
        self.animal_slug = slugify(self.animal_name) + uid[0]
        super(Animal, self).save(*args, **kwargs)
    def __str__(self):
        return self.animal_name

    def incrementViews(self):
        self.animal_views += int(1)
        self.save()

    def incrementLikes(self):
        self.animal_likes += int(1)
        self.save()


class AnimalLocation(BaseModel):
    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name='animal_locations')
    location = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.animal.animal_name}'s location is {self.location}"


class AnimalImage(BaseModel):
    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name='animal_images')
    image = models.ImageField(upload_to='uploads/animalimages')

    def __str__(self):
        return f'{self.animal.animal_name} Images'
