import os
import re
import urllib
from io import BytesIO
from urllib.parse import urlparse

from urllib import request, parse

from PyPDF2 import PdfFileWriter, PdfFileReader
from bs4 import BeautifulSoup

from juapp.models import Diario, Page


def getLinks(url_str):
    # html_page = urllib3.request.urlopen(url)

    data = {'passo': 1, 'mes': 1, 'ano':2020, 'enviar':None}
    data = parse.urlencode(data).encode()
    req = request.Request(url_str, data=data)

    with urllib.request.urlopen(req) as url:
        html_page = url.read()

    soup = BeautifulSoup(html_page, features="html.parser")
    links = []

    domain = urlparse(url_str).netloc

    for link in soup.findAll('a', attrs={'href': re.compile("\.pdf$")}):
        arquivo_pdf = link.get('href')
        arquivo_pdf = arquivo_pdf.replace('../..', 'http://' + domain)
        links.append(arquivo_pdf)
        print(arquivo_pdf)

    return links


def searchPDF(String, pdf_link):

    nome = os.path.basename(urlparse(pdf_link).path)

    num_results = Diario.objects.filter(NOME=nome).count()
    if num_results > 0:
        print(nome)
        return None
    else:
        newdiario = Diario(NOME=nome, URL=pdf_link, LIDO=False, QUANTIDADE_TOTAL=0, DATA=nome[6:10]+'-'+nome[3:5]+'-'+nome[0:2])
        newdiario.save()

        writer = PdfFileWriter()
        with urllib.request.urlopen(pdf_link) as url:
            remoteFile = url.read()
            memoryFile = BytesIO(remoteFile)
            object = PdfFileReader(memoryFile)

            NumPages = object.getNumPages()

            # extract text and do the search
            count = 0

            for i in range(0, NumPages):
                PageObj = object.getPage(i)
                Text = PageObj.extractText()
                thiscount = Text.lower().count(String.lower())
                if thiscount > 0:
                    newpage = Page(PAGINA=i + 1, QUANTIDADE=thiscount, DIARIO=newdiario)
                    newpage.save()
                    count += thiscount
                    print(str(i + 1) + ' (' + str(thiscount) + ')')

            newdiario.QUANTIDADE_TOTAL = count
            newdiario.save()
            print(count)

            outputStream = open("output.pdf", "wb")
            writer.write(outputStream)
            outputStream.close()

            return newdiario


def busca():
    link = "http://www.pmf.sc.gov.br/governo/index.php?pagina=govdiariooficial"
    links = getLinks(link)
    # pdf_link = "http://www.pmf.sc.gov.br/arquivos/diario/pdf/03_02_2020_20.08.23.e9ff07657b035086efa9a46f81775132.pdf"
    #links = "http://192.168.1.10/shp/10_02_2020_21.13.57.d1d6c48ae41723f3d1dfc446173bbc21.pdf"
    String = "Ginklings"

    for link in links:
        newdiario = searchPDF(String, link)
        if newdiario != None:
            if newdiario.QUANTIDADE_TOTAL > 0:
                for page in newdiario.PAGES.all():
                    print('====>'+str(page.PAGINA) + ' ('+str(page.QUANTIDADE) + ')')
