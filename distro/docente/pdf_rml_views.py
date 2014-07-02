# -*- coding: utf-8 -*-
'''
Created on 28/06/2014

@author: Carlos Rijo Palma & Antonio Baião
@email: carlosrijopalma@hotmail.com & baiao@sapo.pt
'''
import cStringIO
from datetime import datetime
from django.http import HttpResponse
from django.template import Template, Context
import json
import os
from rlextra.rml2pdf import rml2pdf

from settings import RML_DIR, WRITE_RML


def generate_pdf(request, *args, **kwargs):
    print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    print request.POST
    
    rml = get_RML("request.GET['q']", request.POST["table_json"])  
    buf = cStringIO.StringIO()
    
    #create the pdf
    rml2pdf.go(rml, outputFileName=buf)
    buf.reset()
    pdfData = buf.read()
    
    #send the response
    response = HttpResponse(mimetype='application/pdf')
    response.write(pdfData)
    response['Content-Disposition'] = 'attachment; filename=output.pdf'
    return response
    
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