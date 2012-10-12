# -*- coding: utf-8 -*-
'''
Created on 10 de Out de 2012

@author: admin1
'''
from distro.models import Departamento, Turma, UnidadeCurricular, ServicoDocente, \
    Docente, TipoAula
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q
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
    listaAnos = listarAnos(request.session['dep_id'])
    
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
    departamento = Departamento.objects.get(id__exact = request.session['dep_id']).nome
    
    unidadesCurriculares = UnidadeCurricular.objects.filter(departamento_id__exact = request.session['dep_id'])
    
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


'''@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def infoDocenteDep(request, id_docente):
    id_departamento = Docente.objects.get(id__exact=id_docente).departamento_id
    nome_Departamento = Departamento.objects.get(id__exact=id_departamento)
    nomeDocente = Docente.objects.get(id__exact=id_docente)
    escalao = Docente.objects.get(id__exact=id_docente).escalao
    regime_exclusividade = Docente.objects.get(id__exact=id_docente).regime_exclusividade
    email_institucional = Docente.objects.get(id__exact=id_docente).email
    abreviatura = Docente.objects.get(id__exact=id_docente).abreviatura
    
    #print "wsdwd ", abreviatura
    if abreviatura == None:
        abreviatura = ' '
        pass
    
    #atribuir regime exclusividade consoante se é True/False
    if regime_exclusividade == True :
        regimeExclusividade = "Sim"
        pass
    else:
        regimeExclusividade = "Não"
        pass
    
    return render_to_response("departamento/infoDocente.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass'''

@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def infoDocenteDep(request, id_docente):
    
    servicoDocente = ServicoDocente.objects.filter(docente_id__exact = id_docente)
    unidadesCurriculares = UnidadeCurricular.objects.all()
    
    docente_name = Docente.objects.get(id__exact = id_docente).nome_completo
    
    lista = []
    #numero total de horas que o docente tem de serviço
    numeroTotalHoras = 0
    for servDocente in servicoDocente:
       
        #nome da unidade curricular que o docente vai dar aulas.
        nomeUnidadeCurricular = UnidadeCurricular.objects.get(turma__id__exact=servDocente.turma_id).nome
        nomeCurso = UnidadeCurricular.objects.get(turma__id__exact=servDocente.turma_id).curso
        numeroTotalHoras +=servDocente.horas       
        lista.append((servDocente.docente_id, nomeUnidadeCurricular,
                           servDocente.horas, nomeCurso))
              
    return render_to_response("departamento/horasServico.html",
        locals(),
        context_instance=RequestContext(request),
        )
    
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def  listServicoDocente(request, ano):
    listaAnos = listarAnos(request.session['dep_id'])
    
    listaServicoDocente = ServicoDocente.objects.filter(turma__ano__exact = ano).exclude(docente_id__exact = None)
    
    print "valor - ", len(listaServicoDocente)
    
    listToSend = []
    
    for servico in listaServicoDocente:
        turma = Turma.objects.get(id__exact = servico.turma_id)
        
        unidade = UnidadeCurricular.objects.get(id__exact = turma.unidade_curricular_id).nome
    
        docente = Docente.objects.get(id__exact = servico.docente_id).nome_completo
        
        tipo_aula = TipoAula.objects.get(id__exact = turma.tipo_aula_id).tipo
        
        listToSend.append([servico.id, docente, unidade, turma.turno, tipo_aula, servico.horas])
        
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
    
    
    return render_to_response("departamento/listarServicoDocente.html",
        locals(),
        context_instance=RequestContext(request),
        )
    
    

'''
Fim das vistas do Departamento
''' 
