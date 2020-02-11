from datetime import datetime
# from datetime import date
from django.db import models


# Create your models here.

class Diario(models.Model):
    NOME = models.CharField(max_length=255)
    URL = models.URLField()
    LIDO = models.BooleanField(default=False)
    QUANTIDADE_TOTAL = models.IntegerField()
    # data = models.DateField(default=date.today, blank=True)
    DATA = models.DateField(default=datetime.now, blank=True)
    BAIXADO_EM = models.DateTimeField(default=datetime.now, blank=True)
    PROCURADO_EM = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.DATA) + ' (' + str(self.QUANTIDADE_TOTAL) + ')'


class Page(models.Model):
    DIARIO = models.ForeignKey(Diario, related_name='PAGES', on_delete=models.CASCADE)
    PAGINA = models.IntegerField()
    QUANTIDADE = models.IntegerField()

    def __str__(self):
        return str(self.DIARIO) + ' - ' + str(self.PAGINA) + '(' + str(self.QUANTIDADE) + ')'
