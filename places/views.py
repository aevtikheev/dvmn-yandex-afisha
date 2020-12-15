from django.http import HttpResponse
from django.template import loader


def start_page(request):
    places_geojson = {
      'type': 'FeatureCollection',
      'features': [
        {
          'type': 'Feature',
          'geometry': {
            'type': 'Point',
            'coordinates': [37.62, 55.793676]
          },
          'properties': {
            'title': '«Легенды Москвы',
            'placeId': 'moscow_legends',
            'detailsUrl': ''
          }
        },
        {
          'type': 'Feature',
          'geometry': {
            'type': 'Point',
            'coordinates': [37.64, 55.753676]
          },
          'properties': {
            'title': 'Крыши24.рф',
            'placeId': 'roofs24',
            'detailsUrl': ''
          }
        }
      ]
    }
    template = loader.get_template('index.html')
    context = {'places_geojson': places_geojson}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)
