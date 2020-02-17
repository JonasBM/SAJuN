from django import forms

from juapp.models import TermoParaBusca
from django.utils.translation import ugettext_lazy as _

class TermoParaBuscaForm(forms.ModelForm):
    class Meta:
        model = TermoParaBusca
        fields = ['string','desde','proprietario','local_para_busca']
        widgets = {
            'proprietario':forms.HiddenInput(),
            'local_para_busca':forms.HiddenInput(),
            'string': forms.TextInput(attrs={'placeholder': 'termo a ser encontrado'}),
        }
        labels = {
            'string': _('Termo para busca'),
            'desde': _('Buscar desde'),
        }

# class HorarioParaBuscaForm(forms.ModelForm):
#     class Meta:
#         model = HorarioParaBusca
#         # horario = forms.CharField(widget=forms.HiddenInput(), label='')
#         fields = ['horario','local_para_busca']
#         # widgets = {
#         #     'local_para_busca':forms.HiddenInput(),
#         # }

# class HorarioParaBuscaRawForm(forms.Form):
#     horario = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
#     local_para_busca = forms.IntegerField()

