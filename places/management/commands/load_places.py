from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from places.models import Company, Image


class Command(BaseCommand):
    help = 'Uploads data for a place'

    def add_arguments(self, parser):
        parser.add_argument('data_urls', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['data_urls']:
            company_data = requests.get(url).json()
            new_company, _ = Company.objects.get_or_create(
                title=company_data['title'],
                description_short=company_data['description_short'],
                description_long=company_data['description_long'],
                longitude=company_data['coordinates']['lng'],
                latitude=company_data['coordinates']['lat']
            )

            for image_position, image_url in enumerate(company_data['imgs']):
                new_image, _ = Image.objects.get_or_create(
                    company=new_company,
                    position=image_position
                )

                image_content = ContentFile(requests.get(image_url).content)
                image_name = PurePosixPath(unquote(urlparse(image_url).path)).parts[-1]
                new_image.image.save(image_name, image_content)
