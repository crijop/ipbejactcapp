# -*- coding: utf-8 -*-
'''
Created on 03/06/2014

@author: Carlos Rijo Palma
@email: carlosrijopalma@hotmail.com
'''
'''
Inicio das vistas dos docentes
''' 
# Página Inicial do utilizador Docente
# Só entra nesta view se o utilizador estiver autentitcado
# e se o utilizador pertencer ao Grupo Docente.

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from distro.Forms.form_extra import ComboxAno
from distro.models import Modulos, UnidadeCurricular, ReducaoServicoDocente, \
    Reducao, Ano, UC_Ano, CursosAno


@login_required(redirect_field_name = 'login_redirectUsers')
@user_passes_test(lambda u:u.groups.filter(name = 'Docente').count())
def indexDocente(request):
    nomeDocente = request.session['nomeDocente']
    nrDocente = request.session['nr_Docente']
    modulos = Modulos.objects.all()
    lista = []
    # numero total de horas que o docente tem de serviço
    numeroTotalHoras = 0
    horasServico = 0
    reducaoHoras = 0
    for modul in modulos:
        if modul.docente_id == nrDocente:
            # nome da unidade curricular que o docente vai dar aulas.
            nomeUnidadeCurricular = UnidadeCurricular.objects.get(id__exact = modul.servico_docente.turma.unidade_curricular_id).nome
            # todas a reduções de serviço referentes ao docente
            reducao = ReducaoServicoDocente.objects.filter(docente_id__exact = nrDocente)
            # se o tamanho for 0 é porque nao existem reduções
            if len(reducao) == 0 :
                # nao faz nada
                pass
            else:
                # obtem o ID da redução
                reducaoId = ReducaoServicoDocente.objects.get(docente_id__exact = nrDocente).reducao_id
                # print "reducao id - ", reducaoId
                # obtem o numero de horas de redução
                reducaoHoras = Reducao.objects.get(id__exact = reducaoId).horas
                pass
            
            # print "docente_n _ ", reducao
            # incrementa as horas de serviço
            horasServico += modul.horas
            numeroTotalHoras = horasServico + reducaoHoras
            lista.append((modul.docente_id, nomeUnidadeCurricular,
                           modul.horas, reducaoHoras))
    numeroTotalTurmas = len(lista)   
    # print "dsfdf - ", reducaoHoras
    return render_to_response("docentes/index.html",
        locals(),
        context_instance = RequestContext(request),
        )
    
    
# Página de apresentação das turmas a que os Docentes pertencem
# Só entra nesta view se o utilizador estiver autentitcado
# e se o utilizador pertencer ao Grupo Docente.
@login_required(redirect_field_name = 'login_redirectUsers')
@user_passes_test(lambda u:u.groups.filter(name = 'Docente').count())
def turmasDocentes(request):    
    form = request.GET
    
    ano_selected = 0
    if form != {}:
        if form['ano'] != "":
            ano_selected = form['ano']
    else:
        ano_selected = str(1) 
        # Ir buscar a data do sistema
    
    listaAnos = Ano.objects.all()
    form_combo = ComboxAno(listaAnos, initial = {"ano":ano_selected})
    ano = ano_selected
    
    if ano != 0:
        anoActual = Ano.objects.get(id = ano)
        anoObj = anoActual
        anoActual = anoActual.ano
        nomeDocente = request.session['nomeDocente']
        nrDocente = request.session['nr_Docente']
        modulosDocente = Modulos.objects.filter(docente = nrDocente)
        listaUnidadesCurricularesDocente = []
        for modulo_Docente in modulosDocente:
            id_unidadeCurricular = UnidadeCurricular.objects.get(id__exact = \
                                                                 modulo_Docente.servico_docente.turma.unidade_curricular_id).id 
            listaUnidadesCurricularesDocente.append(id_unidadeCurricular)
        
        ucAno = UC_Ano.objects.filter(cursosAno__ano__ano = anoObj, unidadeCurricular_id__in = listaUnidadesCurricularesDocente)
        
        lista = []
        for unidadeCurricualarAno in ucAno:
            lista.append([nrDocente, \
                          unidadeCurricualarAno.unidadeCurricular.nome, \
                          unidadeCurricualarAno.cursosAno.curso.nome])
    else:
        anoActual = "(Não selecionou ano)"
        lista = []
    
    
    
    return render_to_response("docentes/turmaDocente.html",
        locals(),
        context_instance = RequestContext(request),
        )    
    
# Página de apresentação das horas de serviço pertencente a cada Docente
# Só entra nesta view se o utilizador estiver autentitcado
# e se o utilizador pertencer ao Grupo Docente.
@login_required(redirect_field_name = 'login_redirectUsers')
@user_passes_test(lambda u:u.groups.filter(name = 'Docente').count())
def horasServico(request):
    nomeDocente = request.session['nomeDocente']
    nrDocente = request.session['nr_Docente']  
    modulos = Modulos.objects.all()
    unidadesCurriculares = UnidadeCurricular.objects.all()
    lista = []
    # numero total de horas que o docente tem de serviço
    numeroTotalHoras = 0
    for modul in modulos:
        if modul.docente_id == nrDocente:
            # nome da unidade curricular que o docente vai dar aulas.
            nomeUnidadeCurricular = UnidadeCurricular.objects.get(id__exact = modul.servico_docente.turma.unidade_curricular_id).nome
            nomeCurso = UnidadeCurricular.objects.get(id__exact = modul.servico_docente.turma.unidade_curricular_id).curso
            numeroTotalHoras += modul.horas       
            lista.append((modul.docente_id, nomeUnidadeCurricular,
                           modul.horas, nomeCurso))
              
    return render_to_response("docentes/horasServico.html",
        locals(),
        context_instance = RequestContext(request),
        )
    
'''
Fim das vistas dos docentes
'''