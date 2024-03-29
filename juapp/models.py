from datetime import datetime, date
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class LocalParaBusca(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    logo = models.URLField(null=True, blank=True)
    method = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name_plural = "Locais para busca"

    def __str__(self):
        return self.nome


class TermoParaBusca(models.Model):
    string = models.CharField(max_length=255)
    desde = models.DateField(default=date.today, blank=True)
    criado_em = models.DateTimeField(default=timezone.now)
    proprietario = models.ForeignKey(User, related_name='termos_para_busca', on_delete=models.CASCADE)
    local_para_busca = models.ForeignKey(
        LocalParaBusca, related_name='termos_para_busca', on_delete=models.CASCADE)

    class Meta:
        ordering = ['local_para_busca', 'string']
        verbose_name_plural = "Termos para busca"

    def __str__(self):
        return str(self.local_para_busca) + ' - ' + self.string

    @property
    def quantidade_total(self):
        return (self.paginas.all().aggregate(Sum('quantidade'))['quantidade__sum'])


class Diario(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    data = models.DateField(default=date.today)
    baixado_em = models.DateTimeField(default=timezone.now)
    procurado_em = models.DateTimeField(default=timezone.make_aware(datetime(1001, 1, 1)))
    local_para_busca = models.ForeignKey(
        LocalParaBusca, related_name='diarios', on_delete=models.CASCADE)

    class Meta:
        ordering = ['local_para_busca', 'data']

    def __str__(self):
        return str(self.local_para_busca) + ' - ' + str(self.data)


class Pagina(models.Model):
    pagina = models.IntegerField()
    quantidade = models.IntegerField()
    criado_em = models.DateTimeField(default=timezone.now)
    diario = models.ForeignKey(
        Diario, related_name='paginas', on_delete=models.CASCADE)
    termo_buscado = models.ForeignKey(
        TermoParaBusca, related_name='paginas', on_delete=models.CASCADE)

    class Meta:
        ordering = ['diario', 'pagina']

    def __str__(self):
        return str(self.diario) + ' - ' + str(self.pagina) + '(' + str(self.quantidade) + ')'
