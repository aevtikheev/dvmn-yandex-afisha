import logging
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from places.models import Place, Image

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class Command(BaseCommand):
    help = 'Uploads data for a place'

    def add_arguments(self, parser):
        parser.add_argument('data_urls', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['data_urls']:
            place_data = requests.get(url).json()
            new_place, _ = Place.objects.get_or_create(
                title=place_data['title'],
                short_description=place_data['description_short'],
                long_description=place_data['description_long'],
                longitude=place_data['coordinates']['lng'],
                latitude=place_data['coordinates']['lat']
            )
            logging.info(f'Place "{new_place.title}" created')

            for image_position, image_url in enumerate(place_data['imgs']):
                new_image, _ = Image.objects.get_or_create(
                    place=new_place,
                    position=image_position
                )

                image_content = ContentFile(requests.get(image_url).content)
                image_name = PurePosixPath(unquote(urlparse(image_url).path)).parts[-1]
                new_image.image.save(image_name, image_content)
                logging.info(f'Image {image_name} for place "{new_place.title}" uploaded')
