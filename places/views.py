import uuid

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

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
    return render(request, 'index.html', context={'places_geojson': places_geojson})


def company_details(request, pk):
    place = get_object_or_404(Place, pk=pk)
    details = {
        'title': place.title,
        'imgs': [image.image.url for image in place.images.order_by('position').all()],
        'short_description': place.short_description,
        'long_description': place.long_description,
        'coordinates': {
            'lng': place.longitude,
            'lat': place.latitude
        }
    }
    return JsonResponse(details, json_dumps_params={'ensure_ascii': False, 'indent': 4})
