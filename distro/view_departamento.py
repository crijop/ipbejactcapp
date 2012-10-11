# -*- coding: utf-8 -*-
'''
Created on 10 de Out de 2012

@author: admin1
'''
from distro.models import Departamento, Turma, UnidadeCurricular, ServicoDocente
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext





DepUserTeste = user_passes_test(lambda u:u.groups.filter(Q(name='Departamento') | Q(name='Eng')).count())

'''
Inicio das vistas do Departamento
''' 
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def indexDepartamento(request):
    '''
    1 = alterar por id_departamento
    '''
    listaAnos = listarAnos(1)
    
    return render_to_response("departamento/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass


@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def listarTurmasDepart(request, ano):
    '''
    1 = alterar por id_departamento
    '''
    listaAnos = listarAnos(1)
    listaTurmas = []
    anoReferente = ano
    departamento = Departamento.objects.get(id__exact = 1).nome
    
    unidadesCurriculares = UnidadeCurricular.objects.filter(departamento_id__exact = 1)
    
    for uC in unidadesCurriculares:
        turmas = Turma.objects.filter(unidade_curricular_id__exact = uC.id, ano__exact = ano)
        
        for t in turmas:    
            listaTurmas.append([t.unidade_curricular, t.horas, t.numero_alunos, t.tipo_aula, t.turno])
    
    paginator = Paginator(listaTurmas, 10)
    drange = range( 1, paginator.num_pages + 1)
    
    
    page = request.GET.get('page')
     
    try:
        turmas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        turmas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        turmas = paginator.page(paginator.num_pages)
    
    return render_to_response("departamento/listarTurmas.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

'''
listDocentes - Mostra todos os professores do departamento e as horas que ainda tem por atribuir
e o numero de turmas a que tão associados e o numero de horas que ja tem atribuidas
'''
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def listDocentes(request):
    
    listToSend = []
   
    listDocentes = Docente.objects.filter(departamento_id__exact = request.session['dep_id'])
    
    
    
    for docente in listDocentes:
        listServicoTemp = ServicoDocente.objects.filter(docente_id__exact = docente.id)
        numberHoras = 0
        for h in listServicoTemp:
            numberHoras += h.horas
        
        listToSend.append([docente.id, docente.nome_completo, len(listServicoTemp), numberHoras])
        pass
        
    paginator = Paginator(listToSend, 10)
    drange = range( 1, paginator.num_pages + 1)
    
    
    page = request.GET.get('page')
     
    try:
        listInfo = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        listInfo = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        listInfo = paginator.page(paginator.num_pages)
        
    
    return render_to_response("departamento/listarDocentes.html",
        locals(),
        context_instance=RequestContext(request),
        )
    


def listarAnos(id_departamento):
    listaAnos = []
    unidadesCurriculares = UnidadeCurricular.objects.filter(departamento_id__exact = id_departamento)
    for uC in unidadesCurriculares:
        turmas = Turma.objects.filter(unidade_curricular_id__exact = uC.id)
        for tur in turmas:
            listaAnos.append(tur.ano) 
                
    listaAnos = removeDuplicatedElements(listaAnos)
    return listaAnos
    pass

def removeDuplicatedElements(dataList):
    templist = dataList
    if len(templist) != 0:
        templist.sort()
        last = templist[-1]
        for i in range(len(templist)-2, -1, -1):
            if last == templist[i]:
                del templist[i]
            else:
                last = templist[i]
    return templist

'''
Fim das vistas do Departamento
''' 
