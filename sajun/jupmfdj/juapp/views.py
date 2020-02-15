from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from juapp import forms
from juapp.forms import HorarioParaBuscaForm, HorarioParaBuscaRawForm
from juapp.models import Diario, Pagina, HorarioParaBusca, TermoParaBusca, LocalParaBusca


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

    data={'local_para_busca':local_id}
    form = HorarioParaBuscaForm(request.POST or None, initial=data)
    if form.is_valid():
        form.save()
        # form.cleaned_data
    form = HorarioParaBuscaForm(initial=data)
    context = {
        'local': local,
        'form':form
    }
    return render(request, 'local.html', context=context)


@login_required
def delete_horario(request, horario_id):
    horario = get_object_or_404(HorarioParaBusca, id=horario_id)
    local_id = horario.local_para_busca.id
    horario.delete()
    return redirect('local',local_id)

@login_required
def indexAAAA(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)
