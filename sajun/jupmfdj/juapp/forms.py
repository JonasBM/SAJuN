from django import forms

from juapp.models import HorarioParaBusca, LocalParaBusca


class HorarioParaBuscaForm(forms.ModelForm):
    class Meta:
        model = HorarioParaBusca
        # horario = forms.CharField(widget=forms.HiddenInput(), label='')
        fields = ['horario','local_para_busca']
        # widgets = {
        #     'local_para_busca':forms.HiddenInput(),
        # }

class HorarioParaBuscaRawForm(forms.Form):
    horario = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    local_para_busca = forms.IntegerField()

