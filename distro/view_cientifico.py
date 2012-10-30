# -*- coding: utf-8 -*-

'''
Created on 21 de Set de 2012

@author: admin1
'''
from distro.models import Docente, Contrato
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mx.DateTime.DateTime import ctime
from pyExcelerator import Workbook
from pyExcelerator.Style import XFStyle
import time




'''
Inicio das vistas do Ciêntifico
'''
cientificoUserTeste = user_passes_test(lambda u:u.groups.filter(name='Cientifico').count(), login_url='')



@login_required(redirect_field_name='login_redirectUsers')
@cientificoUserTeste
def indexCientifico(request):
    return render_to_response("cientifico/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

@login_required(redirect_field_name='login_redirectUsers')
@cientificoUserTeste
def criarXLS(request):
    
    folhaDocentes1011()
    
    return render_to_response("cientifico/criar_xls.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass


def folhaDocentes1011():
    style = XFStyle()

    wb = Workbook()
    ws0 = wb.add_sheet('0')
    
    lista = []
    lisDocentes = Docente.objects.filter()
    
    listaCAB = ["DEP DOCENTE",
                "NOME DOCENTE",
                "CATEGORIA",
                "%",
                "CURSO, ou indicação de CARGO ou FIM DOUT",
                "Tipo CURSO",
                "UNIDADE de FORMAÇÃO ou UNIDADE CURRICULAR, CARGO ou FIM DOUT",
                "DEP UF ou UC",
                "ID CNAEF",
                "ECTS",
                "ANO",
                "SEM",
                "Época UC",
                "N.º ALUNOS",
                "Horas Cargo ou FIM DOUT",
                "Turmas T",
                "Turmas TP",
                "Turmas PL",
                "Turmas TC",
                "Turmas S",
                "Turmas E",
                "Turmas OT",
                "Turmas O",
                "Horas Lei T",
                "Horas Lei TP",
                "Horas Lei PL",
                "Horas Lei TC",
                "Horas Lei S",
                "Horas LEI E",
                "Horas calc CCAA E",
                "Horas corr CCAA E",
                "Horas Lei OT",
                "Horas Lei O",
                "Horas Doc T",
                "Horas Doc TP",
                "Horas Doc PL",
                "Horas Doc TC",
                "Horas Doc S",
                "Horas Doc E",
                "Horas Doc OT",
                "Horas Doc O",
                "Total Horas DOC na linha",
                "Total Horas DOC na linha corrigida",
                "Horas Total UFou UC",
                "Horas DOC SEM O",
                "Horas DOC SEM P",
                "HORAS CET NÃO CONTADAS",
                "HORAS PL NÃO CONTADAS",
                "Horas DOC ANUAL",
                "Horas DOC ANUAL com cargos ou PROTEC",
                "OBSERVAÇÕES Director de Departamento",
                "OBSERVAÇÕES Director de Escola",
                "OBSERVAÇÕES Presidência",
                "Carga Lectiva",
                "Excesso 360"
                ]
    #Cabeçalhos do XLS
    col = 0
    for lCab in listaCAB:
        ws0.write(0, col, lCab)
        col += 1
    print col
    
    
    for docente in lisDocentes: 
        contratos = Contrato.objects.filter(docente_id__exact = docente.id)
        for c in contratos:
            lista.append([unicode(docente.departamento.nome), unicode(docente.nome_completo), unicode(c.categoria.nome), unicode(docente.escalao)])
    
    lista.sort()
    row = 1
    col = 0
    i = 0 
    print lista
    for l in lista:
        print col, " -> ", i
        ws0.write(row, 0, l[0])
        ws0.write(row, 1, l[1])
        ws0.write(row, 2, l[2])
        ws0.write(row, 3, l[3])
        
        row += 1
        col += 1
        i   += 1
    wb.save('docentes1011.xls')
    pass



'''
Fim das vistas do Ciêntifico
'''