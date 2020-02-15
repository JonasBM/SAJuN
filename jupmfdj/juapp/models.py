from datetime import datetime
from django.db import models
from django.db.models import Sum


class LocalParaBusca(models.Model):
    nome = models.CharField(max_length=255)
    logo = models.URLField(null=True, blank=True)
    dias_para_busca = models.PositiveSmallIntegerField(db_index=True)

    class Meta:
        ordering = ['nome']
        verbose_name_plural = "Locais para busca"

    def __str__(self):
        return self.nome


class HorarioParaBusca(models.Model):
    horario = models.TimeField()
    local_para_busca = models.ForeignKey(LocalParaBusca, related_name='horarios_para_busca', on_delete=models.CASCADE)

    class Meta:
        ordering = ['local_para_busca', 'horario']
        verbose_name_plural = "Horarios para busca"

    def __str__(self):
        return str(self.local_para_busca) + ' - ' + str(self.horario)


class TermoParaBusca(models.Model):
    string = models.CharField(max_length=255)
    local_para_busca = models.ForeignKey(LocalParaBusca, related_name='termos_para_busca', on_delete=models.CASCADE)

    class Meta:
        ordering = ['local_para_busca', 'string']
        verbose_name_plural = "Termos para busca"

    def __str__(self):
        return str(self.local_para_busca) + ' - ' + self.string

    @property
    def quantidade_total (self):
        return (self.paginas.all().aggregate(Sum('quantidade'))['quantidade__sum'])

class Diario(models.Model):
    nome = models.CharField(max_length=255)
    url = models.URLField()
    data = models.DateField(default=datetime.now, blank=True)
    baixado_em = models.DateTimeField(default=datetime.now, blank=True)
    procurado_em = models.DateTimeField(default=datetime.now, blank=True)
    termos_buscados = models.ManyToManyField(TermoParaBusca, related_name='diarios')
    local_para_busca = models.ForeignKey(LocalParaBusca, related_name='diarios', on_delete=models.CASCADE)

    class Meta:
        ordering = ['local_para_busca', 'data']

    def __str__(self):
        return str(self.local_para_busca) + ' - ' + str(self.data)

class Pagina(models.Model):
    pagina = models.IntegerField()
    quantidade = models.IntegerField()
    diario = models.ForeignKey(Diario, related_name='paginas', on_delete=models.CASCADE)
    termo_buscado = models.ForeignKey(TermoParaBusca, related_name='paginas', on_delete=models.CASCADE)

    class Meta:
        ordering = ['diario', 'pagina']

    def __str__(self):
        return str(self.diario) + ' - ' + str(self.pagina) + '(' + str(self.quantidade) + ')'
