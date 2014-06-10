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
        listaModulos = []
        for modulo_Docente in modulosDocente:
            id_unidadeCurricular = UnidadeCurricular.objects.get(id__exact = \
                                                                 modulo_Docente.servico_docente.turma.unidade_curricular_id).id 
            listaUnidadesCurricularesDocente.append(id_unidadeCurricular)
            
            listaModulos.append(modulo_Docente.id)
            
        
        ucAno = UC_Ano.objects.filter(cursosAno__ano__ano = anoObj, unidadeCurricular_id__in = listaUnidadesCurricularesDocente)
        
        lista = []
        numeroTotalHoras = 0
        horasServico = 0
        reducaoHoras = 0

        for count, unidadeCurricualarAno in enumerate(ucAno):
            horas = Modulos.objects.get(id = listaModulos[count]).horas
            horasServico += horas
            lista.append([nrDocente, \
                          unidadeCurricualarAno.unidadeCurricular.nome, \
                          horas, \
                          unidadeCurricualarAno.cursosAno.curso.nome])
        
        try:
            reducaoId = ReducaoServicoDocente.objects.get(docente_id__exact = nrDocente).reducao_id
            reducaoHoras = Reducao.objects.get(id__exact = reducaoId).horas
        except:
            reducaoHoras = 0
        
        
        numeroTotalHoras = horasServico + reducaoHoras
        numeroTotalTurmas = len(lista)
    else:
        anoActual = "(Não selecionou ano)"
        numeroTotalHoras = 0
        horasServico = 0
        reducaoHoras = 0
        numeroTotalTurmas = 0

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
        listaModulos = []
        for modulo_Docente in modulosDocente:
            id_unidadeCurricular = UnidadeCurricular.objects.get(id__exact = \
                                                                 modulo_Docente.servico_docente.turma.unidade_curricular_id).id 
            listaUnidadesCurricularesDocente.append(id_unidadeCurricular)
            
            listaModulos.append(modulo_Docente.id)
            
        
        ucAno = UC_Ano.objects.filter(cursosAno__ano__ano = anoObj, unidadeCurricular_id__in = listaUnidadesCurricularesDocente)
        
        lista = []
        numeroTotalHoras = 0
        for count, unidadeCurricualarAno in enumerate(ucAno):
            horas = Modulos.objects.get(id = listaModulos[count]).horas
            numeroTotalHoras += horas
            lista.append([nrDocente, \
                          unidadeCurricualarAno.unidadeCurricular.nome, \
                          horas, \
                          unidadeCurricualarAno.cursosAno.curso.nome])
    else:
        anoActual = "(Não selecionou ano)"
        lista = []
 
    return render_to_response("docentes/horasServico.html",
        locals(),
        context_instance = RequestContext(request),
        )
    
'''
Fim das vistas dos docentes
'''