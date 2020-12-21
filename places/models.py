from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    short_description = models.TextField('Краткое описание')
    long_description = HTMLField('Полное описание')
    longitude = models.FloatField('Долгота')
    latitude = models.FloatField('Широта')

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField('Картинка')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name='Место', related_name='images')
    position = models.PositiveIntegerField("Позиция", default=0)

    class Meta(object):
        ordering = ['position']

    def __str__(self):
        return f'{self.position} {self.place.title}'
