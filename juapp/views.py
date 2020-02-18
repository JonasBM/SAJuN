import os

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from diarioUpdater.diarioUpdater import update_diario
from juapp import forms
from juapp.forms import TermoParaBuscaForm
from juapp.models import Diario, LocalParaBusca, Pagina, TermoParaBusca


@login_required
def start(request):

    if os.getenv('VIRTUAL_ENV'):
        print('Using Virtualenv')
    else:
        print('Not using Virtualenv')

    locais_com_busca = LocalParaBusca.objects.filter(termos_para_busca__in=TermoParaBusca.objects.filter(proprietario=request.user)).distinct()
    locais_sem_busca = LocalParaBusca.objects.exclude(termos_para_busca__in=TermoParaBusca.objects.filter(proprietario=request.user)).distinct()
    context = {
        'locais_com_busca': locais_com_busca,
        'locais_sem_busca':locais_sem_busca,
    }
    return render(request, 'start.html', context=context)



@login_required
def local(request, local_id):
    try:
        local=LocalParaBusca.objects.get(id=local_id)
    except LocalParaBusca.DoesNotExist:
        raise Http404('Local não existente')

    data = {'local_para_busca': local, 'proprietario': request.user}
    termo_form = TermoParaBuscaForm(request.POST or None, initial=data)
    if termo_form.is_valid():
        if not TermoParaBusca.objects.filter(
            Q(proprietario=termo_form.data['proprietario']) & 
            Q(local_para_busca=termo_form.data['local_para_busca']) & 
            Q(string=termo_form.data['string']
        )).exists():
            termo_form.save()
    termo_form = TermoParaBuscaForm(initial=data)

    termos = TermoParaBusca.objects.filter(proprietario=request.user).filter(local_para_busca=local)
    context={
        'local': local,
        'termos': termos,
        'termo_form': termo_form,
    }
    return render(request, 'local.html', context=context)

@login_required
def delete_termo(request, termo_id):
    termo = get_object_or_404(TermoParaBusca, id=termo_id)
    local_id = termo.local_para_busca.id
    termo.delete()
    return redirect('local', local_id)

@login_required
def force_update(request):
    update_diario()
    return HttpResponse('atualizado')


@login_required
def indexAAAA(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits']=num_visits + 1

    context={
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)
