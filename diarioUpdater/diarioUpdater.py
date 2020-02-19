import logging
import os
import re
import urllib
from datetime import date, datetime, timedelta
from io import BytesIO
from logging.handlers import TimedRotatingFileHandler
from threading import local
from tkinter.messagebox import INFO
from urllib import parse, request
from urllib.parse import urlparse

import unidecode
from bs4 import BeautifulSoup
from django.db.models import Q
from django.utils import timezone
from PyPDF2 import PdfFileReader, PdfFileWriter

from juapp.models import Diario, LocalParaBusca, Pagina

logger = logging.getLogger('updater')
logger.setLevel(logging.INFO)
log_format = "%(asctime)s - %(levelname)s - %(message)s"
handler = TimedRotatingFileHandler("logs/updater.log", when="midnight", interval=1)
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
handler.suffix = "%Y%m%d"
handler.extMatch = re.compile(r"^\d{8}$")
logger.addHandler(handler)

def adiciona_mes(data):
    month = data.month + 1
    year = data.year
    if (data.month == 12):
        month = 1
        year = data.year + 1
    return date(year, month, data.day)


def _diarios_PMF():
    url_str = "http://www.pmf.sc.gov.br/governo/index.php?pagina=govdiariooficial"
    links = []
    domain = urlparse(url_str).netloc
    locais = LocalParaBusca.objects.filter(method='diarios_PMF')
    if locais.count() == 1:
        local = locais.first()
        if local.termos_para_busca.all().first() is not None:
            hoje = date.today()
            primeira_data = local.termos_para_busca.order_by('desde').first().desde
            data_pesquisa = date(primeira_data.year, primeira_data.month, 1)
            while hoje >= data_pesquisa:
                data = {'passo': 1, 'mes': data_pesquisa.month, 'ano':data_pesquisa.year, 'enviar':None}
                data = parse.urlencode(data).encode()
                req = request.Request(url_str, data=data)
                with urllib.request.urlopen(req) as url:
                    html_page = url.read()
                soup = BeautifulSoup(html_page, features="html.parser")
                for link in soup.findAll('a', attrs={'href': re.compile("\.pdf$")}):
                    arquivo_pdf = link.get('href')
                    arquivo_pdf = arquivo_pdf.replace('../..', 'http://' + domain)
                    links.append(arquivo_pdf)
                data_pesquisa = adiciona_mes(data_pesquisa)
            return searchLinkPDF(local, links)
        else:
            logger.info('diarios_PMF: Nenhum termo para procurar')
            print('nenhum termo para procurar')
    elif locais.count() > 1:
        logger.error('Multiplos locais: diarios_PMF |', locais)
    else:
        logger.error('Nenhum local: diarios_PMF')
    return None

def searchLinkPDF(local, links):
    primeira_data = local.termos_para_busca.order_by('desde').first().desde
    ultimo_criado = local.termos_para_busca.order_by('-criado_em').first().criado_em
    retorno = True
    for link in links:
        nome = os.path.basename(urlparse(link).path)
        data = date(int(nome[6:10]), int(nome[3:5]), int(nome[0:2]))
        if data >= primeira_data:
            print (data)
            diario = diario = local.diarios.filter(nome=nome).first()
            if diario:
                mudou = False
                if diario.url != link:
                    diario.url = link
                    mudou = True
                if diario.data != data:
                    diario.data = data
                    mudou = True
                if mudou:
                    diario.save()
            else:
                diario = Diario(
                    nome=nome, 
                    url=link, 
                    data=data, 
                    baixado_em=timezone.now(),
                    local_para_busca=local, 
                )
                diario.save()
            if diario is not None:
                if diario.procurado_em <= ultimo_criado:
                    if searchPDF(diario):
                        print('Procurado:', local.method, diario.data)
                    else:
                        retorno = False

            else:
                retorno = False
    return retorno

def searchPDF(diario):
    procura = False
    for termo in diario.local_para_busca.termos_para_busca.all():
        if diario.data > termo.desde and diario.procurado_em <= termo.criado_em:
            procura = True
    if procura:
        writer = PdfFileWriter()
        with urllib.request.urlopen(diario.url) as url:
            remoteFile = url.read()
            memoryFile = BytesIO(remoteFile)
            object = PdfFileReader(memoryFile)
            NumPages = object.getNumPages()
            for i in range(0, NumPages):
                PageObj = object.getPage(i)
                Text = PageObj.extractText()
                for termo in diario.local_para_busca.termos_para_busca.all():
                    if diario.data > termo.desde and diario.procurado_em <= termo.criado_em:
                        texto_limpo = unidecode.unidecode(Text.lower())
                        string_limpa = unidecode.unidecode(termo.string.lower())
                        thiscount = texto_limpo.count(string_limpa)
                        if diario.paginas.filter(Q(pagina=i + 1) & Q(termo_buscado=termo)).exists():
                            pagina = diario.paginas.filter(Q(pagina=i + 1) & Q(termo_buscado=termo)).first()
                            if thiscount > 0:
                                pagina.quantidade=thiscount
                                pagina.criado_em=timezone.now()
                                pagina.save()
                            else:
                                pagina.delete()
                        else:
                            if thiscount > 0:
                                pagina = Pagina(
                                    pagina=i + 1,
                                    quantidade=thiscount,
                                    criado_em=timezone.now(),
                                    diario=diario,
                                    termo_buscado=termo,
                                )
                                pagina.save()
            outputStream = open("output.pdf", "wb")
            writer.write(outputStream)
            outputStream.close()
            diario.procurado_em=timezone.now()
            diario.save()
    return True


def update_diario():
    print('inicio: update_diario')
    if _diarios_PMF():
        logger.info('diarios_PMF completado com sucesso')
    else:
        logger.warning('diarios_PMF não foi completado')
