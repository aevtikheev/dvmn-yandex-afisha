import uuid

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404

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
                'detailsUrl': f'/places/{company.id}/'
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
    company = get_object_or_404(Company, pk=pk)
    details = {
        'title': company.title,
        'imgs': [image.image.url for image in company.images.order_by('position').all()],
        'description_short': company.description_short,
        'description_long': company.description_long,
        'coordinates': {
            'lng': company.longitude,
            'lat': company.latitude
        }
    }
    return JsonResponse(details, json_dumps_params={'ensure_ascii': False, 'indent': 4})
