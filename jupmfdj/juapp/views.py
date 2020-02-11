from django.http import HttpResponse
from juapp.services.pdf import *


# Create your views here.

def home(request):

    busca()

    return HttpResponse('aaaa', content_type="text/plain")
