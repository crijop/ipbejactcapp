# -*- coding: utf-8 -*-
'''
Created on 23/04/2014

@author: Carlos Rijo Palma
@author: António Urbano Baião
'''
from distro.Forms.form_extra import ComboxAno
from distro.models import CursosAno, Ano, UC_Ano, Curso, Turma, Departamento, \
    UnidadeCurricular
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import unicodedata

'''
Inicio das vistas do Ciêntifico
'''

cientificoUserTeste = user_passes_test(lambda u:u.groups.filter(name = 'Cientifico').count(), login_url = '')


# View para apresentar o index do cientifico (presidencia do 
# concelho cientifico)
# só vai entrar nesta view se o utilizador estiver autenticado
# e se pertencer ao grupo do cientifico.
@login_required(redirect_field_name = 'login_redirectUsers')
@cientificoUserTeste
def indexCientifico(request):
    ano = "2012"
    return render_to_response("cientifico_new/index.html",
        locals(),
        context_instance = RequestContext(request),
        )
    
# View para apresentar o index do cientifico (presidencia do 
# concelho cientifico)
# só vai entrar nesta view se o utilizador estiver autenticado
# e se pertencer ao grupo do cientifico.
@login_required(redirect_field_name = 'login_redirectUsers')
@cientificoUserTeste
def listCursos(request, *args, **kwargs):
    # ano = kwargs['ano'] 
    ano = "2012"
    
    
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
        anoActual = anoActual.ano
    else:
        anoActual = "(Não selecionou ano)"
    
    curso_ano = list_Cursos_ano(ano)
    print curso_ano
    
    return render_to_response("cientifico_new/list_cursos.html",
        locals(),
        context_instance = RequestContext(request),
        )
    pass

# Listas de Unidades Curriculares
@login_required(redirect_field_name = 'login_redirectUsers')
@cientificoUserTeste
def listUnidadesCurriculares(request, *args, **kwargs):
     
    ano = kwargs['ano'] 
    curso = kwargs['curso']
    # ano = "2013"
    # curso = 25
    
    
    ano_id = Ano.objects.filter(ano = ano)
    curso_id = Curso.objects.filter(id = curso)
     
    curso_ano = CursosAno.objects.filter(ano = ano_id, \
                                         curso = curso)
    
    listaUC_Ano = UC_Ano.objects.filter(cursosAno = curso_ano)
     
    return render_to_response("cientifico_new/list_uc.html",
        locals(),
        context_instance = RequestContext(request),
        )

# Método responsável por remover elementos
# repetidos numa lista
def removeRepetidosLista(l):
    # cria um dicionario em branco
    dict = {}
    # para cada valor na lista l
    for word in l:
        # adiciona ao dicionario: valor:1
        # note que se for repetido o valor somente sobrescreve ele :)
        dict[word] = 1
    # retorna uma copia das 'keys'
    l[:] = dict.keys()
    return l        
    pass


# lista de cursos num dado ano
def list_Cursos_ano(ano):
    ano_id = Ano.objects.filter(id = ano)
    curso_ano = CursosAno.objects.filter(ano = ano_id)
    return curso_ano


# Listas de Unidades Curriculares
@login_required(redirect_field_name = 'login_redirectUsers')
@cientificoUserTeste
def listUC(request, *args, **kwargs):
    # ano = kwargs['ano']
    
    # Filtros
    
    allDepartamentos = Departamento.objects.all()
    
    # Lista de anos
    listaAnos = Ano.objects.all()
    
    if "curso" in request.GET and "ano" in request.GET:
        keyword = request.GET.get("curso")
        ano_selected = request.GET['ano']
        # Lista de Cursos para os Filtros
        allCursos = list_Cursos_ano(ano_selected)
        form_combo = ComboxAno(listaAnos, initial = {"ano":ano_selected})
        anoActual = Ano.objects.get(id = ano_selected)
        anoActual = anoActual.ano
        
        curso_ano = CursosAno.objects.filter(id = int(keyword), ano__id = ano_selected)
        listaUC_Ano = UC_Ano.objects.filter(cursosAno = curso_ano)

    elif "departamento" in request.GET and "ano" in request.GET:
        keyword = request.GET.get("departamento")
        ano_selected = request.GET['ano']
        # Lista de Cursos para os Filtros
        allCursos = list_Cursos_ano(ano_selected)
        
        # Departamento clicado pelo o utilizador
        departamento = Departamento.objects.get(id = int(keyword))
        form_combo = ComboxAno(listaAnos, initial = {"ano":ano_selected})
        anoActual = Ano.objects.get(id = ano_selected)
        anoActual = anoActual.ano
        
        # Lista de cursos num determinado ano
        curso_ano = list_Cursos_ano(ano_selected)
        
        # Lista de Ids dos cursos
        listaId_cursos = [ id_curso.curso.id for id_curso in curso_ano]
        
        unidades_curriculares = UnidadeCurricular.objects.filter(departamento = departamento, \
                                                                 curso__in = listaId_cursos)        
        listaUC_Ano = UC_Ano.objects.filter(unidadeCurricular__in = unidades_curriculares)
        
    elif request.GET == {}:
        ano_selected = 1
        # Lista de Cursos para os Filtros
        allCursos = list_Cursos_ano(ano_selected)
        form_combo = ComboxAno(listaAnos, initial = {"ano":ano_selected})   
        anoActual = Ano.objects.get(id = ano_selected)
        anoActual = anoActual.ano
        
        curso_ano = list_Cursos_ano(ano_selected)
        listaUC_Ano = UC_Ano.objects.filter(cursosAno__in = curso_ano)
    elif "ano" in request.GET:
        ano_selected = request.GET['ano']
        
        if ano_selected == "":
            form_combo = ComboxAno(listaAnos, initial = {"ano":ano_selected})
            anoActual = "(Não selecionou ano)"
        else:
            # Lista de Cursos para os Filtros
            allCursos = list_Cursos_ano(ano_selected)
            form_combo = ComboxAno(listaAnos, initial = {"ano":ano_selected})   
            
            anoActual = Ano.objects.get(id = ano_selected)
            anoActual = anoActual.ano
            
            curso_ano = list_Cursos_ano(ano_selected)
            listaUC_Ano = UC_Ano.objects.filter(cursosAno__in = curso_ano)
     
    return render_to_response("cientifico_new/list_uc.html",
        locals(),
        context_instance = RequestContext(request),
        )    
