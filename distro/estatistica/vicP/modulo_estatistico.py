# -*- coding: utf-8 -*-
'''
Created on 26/07/2014

@author: Carlos Rijo Palma
@email: carlosrijopalma@hotmail.com
@author: António Urbano Baião
@email: baiao@sapo.pt
'''
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _

from distro.Forms.form_extra import ComboxAno
from distro.estatistica.vicP.forms import *
from distro.models import Ano


def index_estatisticas(request, *args, **Kwargs):
    print "REQUEST", request.POST
    
    form = request.GET
    ano_selected = 0
    if form != {}:
        if form['ano'] != "":
            ano_selected = form['ano']
    else:
        ano_selected = str(1) 
        # Ir buscar a data do sistema
    
    listaAnos = Ano.objects.all()
    
    if request.method == "POST":
        form_combo = ComboxAno(listaAnos, request.POST, initial = {"ano":ano_selected})
        combobox_geral_Statistics_form = Combobox_geral_Statistics(request.POST)
        #=======================================================================
        # 
        # print request.POST
        # 
        # if form_combo.is_valid() and combobox_geral_Statistics_form.is_valid():
        #     print "ola.------"
        #     u'tipo_docente': [u'1'], \
        #     u'ano': [u'1'], \
        #     u'combobox_Geral_option': [u'4'], \
        #     u'valor': [u'0'], \
        #     u'horas': [u'323']}>
        #=======================================================================
        
    else:
        form_combo = ComboxAno(listaAnos, initial = {"ano":ano_selected})
        combobox_geral_Statistics_form = Combobox_geral_Statistics()
    
    return render_to_response("cientifico/estatisticas/geral.html",
        locals(),
        context_instance = RequestContext(request),
        )

'''
('0', '-----'),
('1', 'Curso'),
('2', 'Turma'),
('3', 'Disciplina'),
('4', 'Docente')
'''
def tipo_estatistica(request, *args, **Kwargs):
    estatistica = request.POST.get('tipo_estatistica')
    if estatistica == "":
        template = "cientifico/estatisticas/null_template.html"
    elif estatistica == "1":
        template = "cientifico/estatisticas/null_template.html"
    elif estatistica == "2":
        template = "cientifico/estatisticas/null_template.html"
    elif estatistica == "3":
        template = "cientifico/estatisticas/null_template.html"
        
    elif estatistica == "4":
        form_estatistica_docente = Estatistica_docente()
        template = "cientifico/estatisticas/docente/combo_docente.html"
    
    return render_to_response(template,
        locals(),
        context_instance = RequestContext(request),
        )
'''
('0', '-----'),
('1', 'Por Hora'),
('2', 'Por Curso'),
('3', 'Por Turma'),
('4', 'Por Disciplina')
'''
def tipo_docente(request, *args, **Kwargs):
    tipo_docente_option = request.POST.get('tipo_docente_option')
    if tipo_docente_option == "":
        template = "cientifico/estatisticas/null_template.html"  
    elif tipo_docente_option == "1":
        docente_hora = Docente_hora() 
        template = "cientifico/estatisticas/docente/docente_hora.html"
        
    elif tipo_docente_option == "2":
        template = "cientifico/estatisticas/null_template.html"
    elif tipo_docente_option == "3":
        template = "cientifico/estatisticas/null_template.html"
        
    elif tipo_docente_option == "4":
        template = "cientifico/estatisticas/null_template.html"
    
    return render_to_response(template,
        locals(),
        context_instance = RequestContext(request),
        )
    
def docente_hora(request, *args, **Kwargs):
    docente_hora_tipo = request.POST.get('docente_hora_tipo')
    if docente_hora_tipo == "0":
        var = 0
        combox_hora_form = Combobox_hora("...")
        template = "cientifico/estatisticas/docente/combox_hora.html"  
    elif docente_hora_tipo == "1":
        var = 0
        combox_hora_form = Combobox_hora("...") 
        template = "cientifico/estatisticas/docente/combox_hora.html"
    elif docente_hora_tipo == "2":
        var = 1
        combox_hora_min_form = Combobox_hora("...") 
        combox_hora_max_form = Combobox_hora("...")
        template = "cientifico/estatisticas/docente/combox_hora.html"
    
    return render_to_response(template,
        locals(),
        context_instance = RequestContext(request),
        )

def search_data(request, *args, **Kwargs):
    print request.POST
    anoObj = Ano.objects.get(id = request.POST.get("id_ano"))
    
    combox_geral_option = request.POST.get("combox_geral_option")
    if combox_geral_option == "4": # Filtro Docente
        id_tipo_docente = request.POST.get("id_tipo_docente")
        if id_tipo_docente == "1": # Por Hora
            radioChoise = request.POST.get("radioChoise")
            if radioChoise == "0": # Docentes com mais de X horas
                pass
            elif radioChoise == "1": # Docentes com menos de X horas
                pass
            elif radioChoise == "2": # Docentes com o numero de horas entre x e y
                pass
            pass
        pass
    pass
        
    