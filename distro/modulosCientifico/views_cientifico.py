# -*- coding: utf-8 -*-
'''
Created on 23/04/2014

@author: Carlos Rijo Palma
@author: António Urbano Baião
'''
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
    ano_id = Ano.objects.filter(ano = ano)
    curso_ano = CursosAno.objects.filter(ano = ano_id)
    return curso_ano


# Listas de Unidades Curriculares
@login_required(redirect_field_name = 'login_redirectUsers')
@cientificoUserTeste
def listUC(request, *args, **kwargs):
    ano = "2012"
    # ano = kwargs['ano']
    
    # Filtros
    allCursos = list_Cursos_ano(ano)
    allDepartamentos = Departamento.objects.all()

    ano_id = Ano.objects.filter(ano = ano)
    
    
    if "curso" in request.GET:
        print "Curso"
        keyword = request.GET.get("curso")
        print keyword
        curso_ano = CursosAno.objects.filter(id = int(keyword), ano = ano_id)
        listaUC_Ano = UC_Ano.objects.filter(cursosAno = curso_ano)

    elif "departamento" in request.GET:
        print "Departamento"
        keyword = request.GET.get("departamento")
        
        # Departamento clicado pelo o utilizador
        departamento = Departamento.objects.get(id = int(keyword))
        
        # Lista de cursos num determinado ano
        curso_ano = list_Cursos_ano(ano)
        
        # Lista de Ids dos cursos
        listaId_cursos = [ id_curso.curso.id for id_curso in curso_ano]
        
        unidades_curriculares = UnidadeCurricular.objects.filter(departamento = departamento, \
                                                                 curso__in = listaId_cursos)        
        listaUC_Ano = UC_Ano.objects.filter(unidadeCurricular__in = unidades_curriculares)
        
    elif request.GET == {}:
        curso_ano = list_Cursos_ano(ano)
        listaUC_Ano = UC_Ano.objects.filter(cursosAno__in = curso_ano)
    
     
    return render_to_response("cientifico_new/list_uc.html",
        locals(),
        context_instance = RequestContext(request),
        )








#===============================================================================
# # Listas de Docentes
# @login_required(redirect_field_name = 'login_redirectUsers')
# @cientificoUserTeste
# def listUnidadesCurriculares(request, *args, **kwargs):
#     
#     ano = kwargs['ano']     
#     ano_id = Ano.objects.filter(ano = ano)
#     
#     cursos_ano = CursosAno.objects.filter(ano = ano_id)
#     
#     listaUnidadesCurriculares = []
#     for cursoAno in cursos_ano:
#         listaUC_Ano = UC_Ano.objects.filter(cursosAno = cursoAno.id)
#         listaUnidadesCurriculares.append(listaUC_Ano)
#    
#     if "curso" in request.GET:
#         
#         print "AAAAAAAAAAAAAAAAAAAAA"
#         
#         keyword = request.GET.get("curso")
#         curso_id = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
#         
#         print curso_id
#         
#         for cursoAno in cursos_ano:
#             
#             # tumar_course = unicodedata.normalize('NFKD', t.unidade_curricular.curso.nome.lower()).encode('ASCII', 'ignore')
#             
#             if curso_id == cursoAno.id:
#                 print "ola"   
#                 listaUC_Ano = UC_Ano.objects.filter(cursosAno = cursoAno.id)
#                 listaUnidadesCurriculares.append(listaUC_Ano)
#         
#         
#         
#         
#         
#     
#     return render_to_response("cientifico_new/list_uc.html",
#         locals(),
#         context_instance = RequestContext(request),
#         )
#===============================================================================
    





    
