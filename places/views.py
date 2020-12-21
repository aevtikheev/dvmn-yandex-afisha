import uuid

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404

from places.models import Place


def start_page(request):
    features = []
    for place in Place.objects.all():
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.longitude, place.latitude]
            },
            'properties': {
                'title': place.title,
                'placeId': uuid.uuid4(),
                'detailsUrl': f'/places/{place.id}/'
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


def company_details(request, pk):
    place = get_object_or_404(Place, pk=pk)
    details = {
        'title': place.title,
        'imgs': [image.image.url for image in place.images.order_by('position').all()],
        'description_short': place.short_description,
        'long_description': place.long_description,
        'coordinates': {
            'lng': place.longitude,
            'lat': place.latitude
        }
    }
    return JsonResponse(details, json_dumps_params={'ensure_ascii': False, 'indent': 4})
