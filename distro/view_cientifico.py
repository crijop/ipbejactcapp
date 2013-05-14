# -*- coding: utf-8 -*-

from distro.models import Docente, Contrato, Docente, UnidadeCurricular, Turma, \
    Modulos, TipoAula
from django.contrib.auth.decorators import login_required, user_passes_test, \
    login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, render_to_response
from django.template.context import RequestContext, RequestContext
from mx.DateTime.DateTime import ctime, ctime
from twisted.python.reflect import ObjectNotFound
from types import NoneType
from xlwt import Cell
from xlwt.Formatting import Font, Borders, Pattern
from xlwt.Style import XFStyle, easyxf
from xlwt.Workbook import Workbook
import time
import xlwt



'''
Inicio das vistas do Ciêntifico
'''

cientificoUserTeste = user_passes_test(lambda u:u.groups.filter(name='Cientifico').count(), login_url='')


#View para apresentar o index do cientifico (presidencia do 
#concelho cientifico)
#só vai entrar nesta view se o utilizador estiver autenticado
#e se pertencer ao grupo do cientifico.
@login_required(redirect_field_name='login_redirectUsers')
@cientificoUserTeste
def indexCientifico(request):
    return render_to_response("cientifico/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

#View para criar os XLS da Base dados
#ao entrar nesta vista os XLS são logo criados.
#só vai entrar nesta view se o utilizador estiver autenticado
#e se pertencer ao grupo do cientifico.
@login_required(redirect_field_name='login_redirectUsers')
@cientificoUserTeste
def criarXLS(request):

    wb = Workbook()
    createXLS_sheet0(wb)
    createXLS_sheet1(wb)
    folhaDocentes1011(wb)
    
    wb.save('saida.xls')

    return render_to_response("cientifico/criar_xls.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass


#Metdodo de Criação da folha Matriz_SD do XLS
def createXLS_sheet0(wb):
    #Nome Folha
    ws0 = wb.add_sheet('Matriz_SD')

    #Estilos
    style = xlwt.easyxf('pattern: pattern solid, fore_colour green')
    borders = Borders()
    borders.left    = 5
    borders.right   = 5
    borders.top     = 5
    borders.bottom  = 5
    style.borders = borders
    
    lista = []
    
    listaCAB = ["UO do Curso",
                "DEP DOCENTE",
                "NOME DOCENTE",
                "Convidado ou C. Externo",
                "CATEGORIA",
                "%",
                u"CURSO, ou indicação de CARGO ou FIM DOUT",
                "Tipo CURSO",
                "Regime/Turma CURSO",
                u"UNIDADE de FORMAÇÃO ou UNIDADE CURRICULAR, CARGO ou FIM DOUT",
                "DEP UF ou UC",
                "ID CNAEF",
                "ECTS",
                "ANO",
                "SEM",
                u"Época UC",
                u"N.º ALUNOS",
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
                u"HORAS CET NÃO CONTADAS",
                u"HORAS PL NÃO CONTADAS",
                "Horas DOC ANUAL",
                "Horas DOC ANUAL com cargos ou PROTEC",
                u"OBSERVAÇÕES Director de Departamento",
                u"OBSERVAÇÕES Director de Escola",
                u"OBSERVAÇÕES Presidência",
                "Carga Lectiva",
                "Excesso 360"
                ]
    
    #Cabeçalhos do XLS
    col = 0
    row = 0
    for lCab in listaCAB:
        ws0.write(row, col, lCab, style)
        col += 1
    
    listaModulos = Modulos.objects.all()
    nrHorasDocente = 0
    for modulos in listaModulos:
        #Calcular as horas dos docentes anual...
        nome_departamento = ""
        nome_docente = ""
        nome_categoria = ""
        nome_escalao = ""
        try:
            nome_departamento = modulos.docente.departamento.nome
            nome_docente = modulos.docente.nome_completo
            nome_categoria = Contrato.objects.get(docente_id__exact = modulos.docente_id).categoria.nome
            nome_escalao = modulos.docente.escalao
        except AttributeError:
            nome_departamento = ""
            nome_docente = ""
            nome_categoria = ""
            nome_escalao = ""
            pass
        '''modulos.docente.departamento.nome'''
        #modulos.docente.nome_completo 
        #Contrato.objects.get(docente_id__exact = modulos.docente_id).categoria.nome   
        #modulos.docente.escalao
        lista.append([modulos.servico_docente.turma.unidade_curricular.departamento.sede.abreviatura,\
                      nome_departamento,\
                      nome_docente,\
                      0,\
                      nome_categoria,\
                      nome_escalao,\
                      modulos.servico_docente.turma.unidade_curricular.curso.nome,\
                      modulos.servico_docente.turma.unidade_curricular.curso.tipo_curso.abreviatura,\
                      "", modulos.servico_docente.turma.unidade_curricular.nome,\
                      modulos.servico_docente.turma.unidade_curricular.departamento.nome,
                      modulos.servico_docente.turma.unidade_curricular.cnaef.codigo,
                      modulos.servico_docente.turma.unidade_curricular.ects,
                      modulos.servico_docente.turma.unidade_curricular.ano,
                      modulos.servico_docente.turma.unidade_curricular.semestre,
                      modulos.servico_docente.turma.unidade_curricular.epoca.abreviatura,
                      modulos.servico_docente.turma.numero_alunos, "", "", "", "", "", "", "", "", "",
                      modulos.servico_docente.turma.unidade_curricular.horas_lei_t,
                      modulos.servico_docente.turma.unidade_curricular.horas_lei_tp,
                      modulos.servico_docente.turma.unidade_curricular.horas_lei_pl,
                      modulos.servico_docente.turma.unidade_curricular.horas_lei_tc,
                      modulos.servico_docente.turma.unidade_curricular.horas_lei_s,
                      modulos.servico_docente.turma.unidade_curricular.horas_lei_e,
                      "", "",
                      modulos.servico_docente.turma.unidade_curricular.horas_lei_ot,
                      modulos.servico_docente.turma.unidade_curricular.horas_lei_o,
                      "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", 
                      "-", 
                      modulos.servico_docente.turma.observacoesDirDepartamento, 
                      modulos.servico_docente.turma.observacoesDirEscola,
                      modulos.servico_docente.turma.observacoesPresidencia, "", ""
                      ])
           
           
    lista.sort()
    row = 1
    col = 0
    for linha in lista:
        for l in linha:
            ws0.write(row, col, l)
            col += 1
        col = 0
        row += 1
    #wb.save('decdcd.xls')

#Metdodo de Criação da folha Docentes1011 do XLS
def folhaDocentes1011(wb):
    #Nome Folha
    ws0 = wb.add_sheet('Docentes1011')
    
    #Estilos
    style = xlwt.easyxf('pattern: pattern solid, fore_colour green')
    borders = Borders()
    borders.left    = 5
    borders.right   = 5
    borders.top     = 5
    borders.bottom  = 5
    style.borders = borders
    

    lista = []
    lisDocentes = Docente.objects.filter()
    
    listaCAB = ["DEP DOCENTE",
                "NOME DOCENTE",
                "CATEGORIA",
                "%"
                ]
   
    #Cabeçalhos do XLS
    col = 0
    row = 0
    for lCab in listaCAB:
        ws0.write(row, col, lCab, style)
        col += 1
    
    for docente in lisDocentes: 
        contratos = Contrato.objects.filter(docente_id__exact = docente.id)
        for c in contratos:
            lista.append([unicode(docente.departamento.nome),\
                          unicode(docente.nome_completo), \
                          unicode(c.categoria.nome), \
                          unicode(docente.escalao)]\
                         )
    lista.sort()
    row = 1
    col = 0
    for linha in lista:
        for l in linha:
            ws0.write(row, col, l)
            col += 1
        col = 0
        row += 1
    #wb.save('docentes1011.xls')
    pass

#Metdodo de Criação da folha PCurricularNTurmaFix do XLS
def createXLS_sheet1(wb):
  
    font0 = Font()
    font0.name = 'Arial'
    font0.bold = True
    
    style0 = XFStyle()
    style0.font = font0
    
    borders = Borders()
    borders.left = 2
    borders.right = 2
    borders.top = 2
    borders.bottom = 2
    
    patt = Pattern()
    patt.pattern_back_colour = 5
    
    style0.borders = borders
    style0.pattern = patt

    ws0 = wb.add_sheet('PCurricularNTurmaFix')
    
    listFinal = []
    
    listFinal.append([u"UO do Curso", u"CURSO", u"Tipo CURSO",
                           u"Regime/Turma CURSO", u"UNIDADE de FORMAÇÃO ou UNIDADE CURRICULAR", u"DEP UF ou UC", 
                           u"ID CNAEF", u"ECTS", u"ANO", u"SEM", 
                           u"Época UC",u"Nº Alunos",u"Turmas T",u"Turmas TP","Turmas PL",u"Turmas TC",u"Turmas S",
                           u"Turmas E",u"Turmas OT", u"Turmas O", u"Horas Lei T", 
                           u"Horas Lei TP",u"Horas Lei PL", u"Horas Lei TC",
                             u"Horas Lei S", u"Horas Lei E", u"Horas calc CCAA E",
                             u"Horas corr CCAA E", u"Horas Lei OT",u"Horas Lei O",u"Fundamentação Turmas (Director de Escola)"
                             ,"",u"VER Turmas T",u"VER Turmas TP",u"VER Turmas PL",u"VER Turmas TC","VER Turmas S",u"VER Turmas E"
                             ,u"VER Turmas OT", u"VER Turmas O", u"Erro n.º Turmas", u"Observações"])
    
    allUC = UnidadeCurricular.objects.all()
    
    for uc in allUC:
        try:
            listFinal.append([uc.departamento.sede.abreviatura, uc.curso.nome, uc.curso.tipo_curso.abreviatura, "",
                           uc.nome, uc.departamento.nome, uc.cnaef.codigo, 
                           uc.ects, uc.ano, uc.semestre, uc.epoca.abreviatura, 
                           "",
                           "","","","","","","","", uc.horas_lei_t, uc.horas_lei_tp, 
                           uc.horas_lei_pl,uc.horas_lei_tc, uc.horas_lei_s,
                             uc.horas_lei_e, uc.horas_lei_ot, uc.horas_lei_o,
                             "", "","","","","","","","","","",""])
        except AttributeError:
            listFinal.append([uc.departamento.sede.nome, uc.curso.nome, uc.curso.tipo_curso.abreviatura, "",
                           uc.nome, uc.departamento.nome, "", 
                           uc.ects, uc.ano, uc.semestre, "", 
                           "",
                           "","","","","","","","", uc.horas_lei_t, uc.horas_lei_tp, 
                           uc.horas_lei_pl,uc.horas_lei_tc, uc.horas_lei_s,
                             uc.horas_lei_e, uc.horas_lei_ot, uc.horas_lei_o,
                             "", "","","","","","","","","","",""])
        
        
        
    
    #t0 = time()
    print "Start..."
    rowcount = 0
    colcount = 0
    print "Filling..."
    for ucInfo in listFinal:
        for info in ucInfo:
            if(rowcount == 0):
                
                ws0.write(rowcount, colcount, info, style0)
                colcount += 1
            else:
                ws0.write(rowcount, colcount, info)
                colcount += 1
                
            
            
        colcount = 0
        rowcount += 1
    
   
    print "Storing..."
    #wb.save('big-16Mb.xls')
    
    #t2 = time() - t0
    print "Finished ... "
    pass

@login_required(redirect_field_name='login_redirectUsers')
@cientificoUserTeste
def listaDelegacoes(request):
    
    modulos_delegados = Modulos.objects.exclude(departamento_id__exact = 0).exclude(departamento_id__exact = None).exclude(aprovacao__exact = 1)
    
    listToSend = []
    
    for m in modulos_delegados:
        listToSend.append([m.id, m.servico_docente.turma.unidade_curricular.departamento.nome,  m.servico_docente.turma.unidade_curricular.nome, m.horas, m.departamento.nome ])
    
            
    print modulos_delegados
    return render_to_response("cientifico/listagemModulosDelegados.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

@login_required(redirect_field_name='login_redirectUsers')
@cientificoUserTeste
def aprovarDelegacao(request, id_modulo):
    
    m = Modulos.objects.get(id__exact = id_modulo)
    
    m.aprovacao = 1
    
    m.save()
    
    return render_to_response("cientifico/sucess.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass
    
    
@login_required(redirect_field_name='login_redirectUsers')
@cientificoUserTeste
def reprovarDelegacao(request, id_modulo):
    
    m = Modulos.objects.get(id__exact = id_modulo)
    
    m.departamento_id = 0
    
    m.save()
    
    
    return render_to_response("cientifico/reprove.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass


'''
Nova etapa do trabalho
Data: 14/05/2013
'''

@login_required(redirect_field_name='login_redirectUsers')
@cientificoUserTeste
def definirCursosCET(request):
    return render_to_response("cientifico/definir_Curso_CET.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass



'''
Fim das vistas do Ciêntifico
'''

