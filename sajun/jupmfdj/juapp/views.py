from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from juapp import forms
from juapp.models import (Diario, LocalParaBusca, Pagina,
                          TermoParaBusca)

@login_required
def start(request):
    context = {
        'locais': LocalParaBusca.objects.all(),
    }
    return render(request, 'start.html', context=context)


@login_required
def local(request, local_id):
    try:
        local = LocalParaBusca.objects.get(id=local_id)
    except LocalParaBusca.DoesNotExist:
        raise Http404('Local não existente')


    print(request.user.id)

    data = {'local_para_busca': local_id}
    context = {
        'local': local,
    }
    return render(request, 'local.html', context=context)


@login_required
def indexAAAA(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)
