# -*- coding: utf-8 -*-
'''
Created on 28/06/2014

@author: Carlos Rijo Palma & Antonio Baião
@email: carlosrijopalma@hotmail.com & baiao@sapo.pt
'''

import cStringIO
import collections
from datetime import datetime
from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader, Context
from django.utils.translation import ugettext, ugettext_lazy as _
import json
import os
from rlextra.rml2pdf import rml2pdf
import trml2pdf

from settings import RML_DIR, WRITE_RML, PROJECT_DIR


# Criar as tabelas para os dois tipos de report
# Para o User Docentes
# tipo Report: 0 = Turmas Docente / 1 = Horas de Servico Docente
def createTable_HorasServDocente(tipoReport, table_json):
    if int(tipoReport) == 0:
        listaHeaders = []
        for key, value in table_json[0].iteritems():
            listaHeaders.append(key)
            
        listaLines = []
        for row in table_json:
            l = []
            for header in listaHeaders:
                l.append(row[header])
            listaLines.append(l)
    elif int(tipoReport) == 1:
        listaHeaders = []
        listaHeaders.append("Curso")
        listaHeaders.append("Turma")
        listaHeaders.append(table_json[0].keys()[1])
        contador = 0
        listaLines = []
        lenTable = len(table_json)
        for count, row in enumerate(table_json):
            l = []
            if count == lenTable - 1:
                for header in listaHeaders:
                    if header != "Turma":
                        if header == table_json[0].keys()[1]:
                            l.append(contador)
                        else:
                            l.append(row[header])
                    else:
                        l.append("")
                listaLines.append(l)
            else:
                for header in listaHeaders:
                    if header == table_json[0].keys()[1]:
                        try:
                            contador += int(row[header])
                        except:
                            pass
                        
                        l.append(row[header])
                    else:
                        l.append(row[header])
                listaLines.append(l)
    
    return listaHeaders, listaLines


# Gerar Pdf
def generate_pdf(request, *args, **kwargs):
    response = HttpResponse(mimetype='application/pdf')
    nameRML = os.path.join(RML_DIR, "Docentes", "rml_index.xml")
    # img relatorio
    name_image = os.path.join(PROJECT_DIR, "distro", "static", "images", "logo.png")
    # data relatorio
    dataGenerateReport = datetime.now().strftime('%d %b %Y %H:%M')    
    # tipo Report: 0 = Turmas Docente / 1 = Horas de Servico Docente
    tipoReport = request.POST["tipoReport"]
    # dados relatorio
    ano = request.POST["ano"]
    user_name = request.POST["user_name"]
    tituloReport = request.POST["tituloReport"]
    
    if int(tipoReport) == 1:
        table_json = json.loads(request.POST["table_json"])
    else:
        table_json = json.loads(request.POST["table_json"], object_pairs_hook=collections.OrderedDict)
    
    listaHeaders, listaLines = createTable_HorasServDocente(tipoReport, table_json)
    
    t = Template(open(nameRML).read())
    c = Context({"ano": ano, \
                 "user_name": user_name, \
                 "tituloReport": tituloReport, \
                 "dataGenerateReport": dataGenerateReport, \
                 "name_image":name_image, \
                 "listaHeaders":listaHeaders, \
                 "listaLines":listaLines, \
                 "tipoReport":tipoReport \
                 })
    
    rml = t.render(c).encode('utf8')
    pdf = trml2pdf.parseString(rml)
    #pdf = trml2pdf.parseString(file(template,'r').read())
    
    response.write(pdf)
    response['Content-Disposition'] = 'attachment; filename=output.pdf'
    return response








# Codigo auxiliar
'''
#rml = t.render(c)

#template = get_rml_trml2pdf("Carlos", request.POST["table_json"])

#tpl = loader.get_template(template)

#pdf = trml2pdf.parseString(tpl)

#===========================================================================
# prompt = None
# context = {}
# if not filename:
#     filename = template+'.pdf'
# cd = []
# if prompt:
#     cd.append('attachment')
# cd.append('filename=%s' % filename)
# response['Content-Disposition'] = '; '.join(cd)
#===========================================================================

#tc = {'filename': filename}
#tc.update(context)
#ctx = Context(tc)
'''


'''
def get_rml_trml2pdf(name, jsonTable):
    nameRML = os.path.join(RML_DIR, "Docentes", "template_report.xml")
    name_image = "/home/admin1/BolsaMerito/ipbejactcapp/distro/static/images/ipbeja_log.JPG"
    
    dataGenerateReport = datetime.now().strftime('%d %b %Y %H:%M')    
    
    print jsonTable, "aaaaaaa", type(jsonTable)
    table_json = json.loads(jsonTable)
    print "aaaaaaaaaa", table_json
    
    listaHeaders = []
    for key, value in table_json[0].iteritems():
        listaHeaders.append(key)
        
    listaLines = []
    for row in table_json:
        l = []
        for header in listaHeaders:
            l.append(row[header])
        listaLines.append(l)
    
    t = Template(open(nameRML).read())
    c = Context({"name": name, \
                 "dataGenerateReport": dataGenerateReport, \
                 "name_image":name_image, \
                 "listaHeaders":listaHeaders, \
                 "listaLines":listaLines \
                 })
    rml = t.render(c)
    #django templates are unicode, and so need to be encoded to utf-8
    return rml.encode('utf8')
'''    

    


#from pyjon.reports.factory import ReportFactory
#===============================================================================
# def generate_pdf(request, *args, **kwargs):
#     print request.POST
#     jsonTable = request.POST["table_json"]
#     
#     
#     testdata = [range(10)] * 100
#     nameRML = os.path.join(RML_DIR, "Docentes", "basic1.xml")
#     
#     
#     factory = ReportFactory()
# 
#     factory.render_template(
#             template_file=nameRML,
#             title=u'THE TITLE',
#             data=testdata,
#             dummy='foo'
#             )
# 
#     factory.render_template(
#             template_file=nameRML,
#             title=u'THE TITLE 2 :)',
#             data=testdata,
#             dummy='foo'
#             )
#     
#     ola = factory.get_template(template_file=nameRML)
#     
#     factory.render_document(
#             'basic1.pdf')
# 
#     factory.cleanup()
#     
#     '''
#     name_image = "/home/admin1/BolsaMerito/ipbejactcapp/distro/static/images/ipbeja_log.JPG"
#     
#     dataGenerateReport = datetime.now().strftime('%d %b %Y %H:%M')    
#     
#     print jsonTable, "aaaaaaa", type(jsonTable)
#     table_json = json.loads(jsonTable)
#     print "aaaaaaaaaa", table_json
#     
#     listaHeaders = []
#     for key, value in table_json[0].iteritems():
#         listaHeaders.append(key)
#         
#     listaLines = []
#     for row in table_json:
#         l = []
#         for header in listaHeaders:
#             l.append(row[header])
#         listaLines.append(l)
#     
#     factory = ReportFactory()
# 
#     factory.render_template(
#             template_file=name_image,
#             name=u'THE TITLE'
#             )
#     
#     a = factory.render_document(
#             'basic1.pdf')
# 
#     factory.cleanup()
#     '''
#     #send the response
#     response = HttpResponse(mimetype='application/pdf')
#     response.write(ola)
#     response['Content-Disposition'] = 'attachment; filename=output.pdf'
#     return response
#===============================================================================
#===============================================================================
# def generate_pdf(request, *args, **kwargs):
#     print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
#      
#     print request.POST
#     rml = get_RML("request.GET['q']", request.POST["table_json"])  
#     buf = cStringIO.StringIO()
#      
#     #create the pdf
#     rml2pdf.go(rml, outputFileName=buf)
#     buf.reset()
#     pdfData = buf.read()
#      
#     #send the response
#     response = HttpResponse(mimetype='application/pdf')
#     response.write(pdfData)
#     response['Content-Disposition'] = 'attachment; filename=output.pdf'
#     return response
#===============================================================================
'''   
def get_RML(name, jsonTable):
    nameRML = os.path.join(RML_DIR, "Docentes", "template_report.xml")
    name_image = "/home/admin1/BolsaMerito/ipbejactcapp/distro/static/images/ipbeja_log.JPG"
    
    dataGenerateReport = datetime.now().strftime('%d %b %Y %H:%M')    
    
    print jsonTable, "aaaaaaa", type(jsonTable)
    table_json = json.loads(jsonTable)
    print "aaaaaaaaaa", table_json
    
    listaHeaders = []
    for key, value in table_json[0].iteritems():
        listaHeaders.append(key)
        
    listaLines = []
    for row in table_json:
        l = []
        for header in listaHeaders:
            l.append(row[header])
        listaLines.append(l)
    
    t = Template(open(nameRML).read())
    c = Context({"name": name, \
                 "dataGenerateReport": dataGenerateReport, \
                 "name_image":name_image, \
                 "listaHeaders":listaHeaders, \
                 "listaLines":listaLines \
                 })
    rml = t.render(c)
    #django templates are unicode, and so need to be encoded to utf-8
    return rml.encode('utf8')
'''