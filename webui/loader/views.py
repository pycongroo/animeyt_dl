from django.shortcuts import render
from django.http import HttpResponse
from . import models

import sys
sys.path.append('../../')
import animeyt_dl.animeyt_dl as anmyt
# Create your views here.
PATH_REAL ="loader/static/images"
PATH_WEB ="http://www.animeyt.tv/files/img/series"

def resultado(res):
    modif = res

    arch = modif['poster'].split('/')[-1]
    #anmyt.net.download_file(modif['poster'], '%s/%s' % (PATH_REAL, arch))
    modif['poster']='/img/poster/%s' % arch
    return modif

def search_list(request):
    criterio = request.GET['criterio']
    results = anmyt.search(criterio)
    print results
    print len(results)
    map(resultado, results)
    return render(request, 'loader/search_list.html', {'results':results})

def home(request):
    return render(request, 'loader/home.html', {})

def serve_image(request, name):
    print '%s' % name
    path_file = "%s/%s" % (PATH_REAL, name)
    print path_file
    anmyt.net.download_file('%s/%s' % (PATH_WEB, name), path_file)
    fsock = open(path_file, 'rb')
    response = HttpResponse(fsock)
    response['Content-Type'] = 'image/jpeg'
    return response

def prueba(request):
    res = models.Resultado('Luis', 22)
    return render(request, 'loader/prueba.html', {'resultado': res})
