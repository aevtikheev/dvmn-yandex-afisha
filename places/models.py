from django.db import models


class Company(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField('Краткое описание')
    description_long = models.TextField('Полное описание')
    longitude = models.FloatField('Долгота')
    latitude = models.FloatField('Широта')

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField('Картинка')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания', related_name='images')
    position = models.PositiveIntegerField("Позиция", default=1)

    def __str__(self):
        return f'{self.position} {self.company.title}'
