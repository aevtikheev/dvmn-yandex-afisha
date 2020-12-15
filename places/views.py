import uuid

from django.http import HttpResponse
from django.template import loader

from places.models import Company


def start_page(request):
    features = []
    for company in Company.objects.all():
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [company.longitude, company.latitude]
            },
            'properties': {
                'title': company.title,
                'placeId': uuid.uuid4(),
                'detailsUrl': ''
            }
        }
        features.append(feature)

    places_geojson = {
      'type': 'FeatureCollection',
      'features': features
    }
    template = loader.get_template('index.html')
    context = {'places_geojson': places_geojson}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)
