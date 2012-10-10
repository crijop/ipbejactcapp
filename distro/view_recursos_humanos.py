# -*- coding: utf-8 -*-

'''
Created on 25 de Set de 2012

@author: António
'''
from datetime import timedelta, date
from distro.forms import EditarDocenteForm, AdicionarDocenteForm
from distro.models import Departamento, Docente, Contrato, Categoria, \
    TipoContrato, DocenteLogs
from django.contrib.auth import models
from django.contrib.auth.decorators import login_required, permission_required, \
    user_passes_test
from django.contrib.auth.models import Group
from django.contrib.formtools.preview import FormPreview
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.datetime_safe import datetime
from pydoc import Doc
import unicodedata

'''
Inicio das vistas dos Recursos Humanos


''' 
'''
Metodo reposavel por ratar o pediodo AJAX de aparecimento do filtro de ordenação por
uma letra do alfabeto
presente na lista de docentes e lista de contratos
'''
def filter_abc(request):

    if request.is_ajax():
       
        alfabeto = map(chr , range(65, 91))
        
        return render_to_response("recursosHumanos/filter_abc.html",
        locals(),
        context_instance=RequestContext(request),
        )
        
'''
Responsavel por tratar o pedido ajax para o aparecimento da filtragem por departamentos
'''        
def filter_dep(request):

    if request.is_ajax():
       
        allDepartamentos = Departamento.objects.all()
        
        return render_to_response("recursosHumanos/filter_dep.html",
        locals(),
        context_instance=RequestContext(request),
        )
'''
Responsavel por tratar o pedido ajax para o aparecimento da filtragem por categorias
'''
def filter_cat(request):

    if request.is_ajax():
       
        allCategories = Categoria.objects.all()
        
        return render_to_response("recursosHumanos/filter_cat.html",
        locals(),
        context_instance=RequestContext(request),
        )
        

def filter_date_start(request):

  
    if request.is_ajax():
        
        if request.method == 'GET':
            
            print "oal" 
       
            print request.GET
         
        
        
        return render_to_response("recursosHumanos/filter_date_start.html",
        locals(),
        context_instance=RequestContext(request),
        )

def ajax(request):
    print "falhou"
    if request.is_ajax():
       
        
        
        return render_to_response("recursosHumanos/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    

'''
Trata da pagina de index dos recursos humanos onde são apresentadas algumas estatisticas
como por exemplo a numero de contratos a terminar nos proximos 60 ou 120 dias
'''

@login_required(redirect_field_name='Teste_home')
@user_passes_test(lambda u:u.groups.filter(name='RecusosHumanos').count())
def indexRecursosHumanos(request):
    allDocentes = Docente.objects.all()
   
    listaContracts = []
    actualState = ""
    nrDocentesEndContractTwoMonths = 0
    nrDocentesEndContractFourMonths = 0
    #dois meses
    twoMonths = 60
    #quatro meses
    fourMonths = 120
    
    dateActual = datetime.today()
    dateActualFormatPrint = datetime.today().strftime("%d de %B de %Y")
    
    #convertedDate = datetime.strptime(dateActual, "%d-%m-%Y")
    
    intervalFourMonths = timedelta(fourMonths)
    intervalTwoMonths = timedelta(twoMonths) 
    
    date_upTwoMonths = dateActual + intervalTwoMonths
    
    date_upFourMonths = dateActual + intervalFourMonths
    
    
    for docente in allDocentes:
        departamento_id = docente.departamento_id
        departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
        id_Docente = docente.id
                     
        try:
                
            contrato = Contrato.objects.get(docente__id=id_Docente)
            #contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
            contract_end = contrato.data_fim.strftime("%d-%m-%Y")
            contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
            #percent = contrato.percentagem 
            #print contrato.categoria.id
            nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
        except ObjectDoesNotExist:
            contract_start = "---"
            contract_end = "---"
            contract_type = "---"
            percent = "---"
            nomeCategoria = "Sem Categoria"
        
        if not(contract_end.startswith("---")):
        
            date_contract_end = datetime.strptime(contract_end, "%d-%m-%Y")
            
            if unicode(contract_type).startswith("Termo Certo") :
                if date_contract_end < date_upTwoMonths and date_contract_end > dateActual:
                    nrDocentesEndContractTwoMonths += 1
                    pass
                pass
            elif unicode(contract_type).startswith("Sem Termo"):
                if date_contract_end < date_upFourMonths and date_contract_end > dateActual:
                    nrDocentesEndContractFourMonths +=1
                    pass
                pass
            pass
    pass
    
    #converter dataActual em str
    dateActualSTR = datetime.today().strftime("%d-%m-%Y")
    
    return render_to_response("recursosHumanos/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    
    pass


@login_required(redirect_field_name='Teste_home')
def listDocente_RecursosHumanos(request):
    
    allDocentes = Docente.objects.all()
    
    
    #nomesDepartamentos = {dep.nome for dep in allDepartamentos}
   
    listaDocentes = []
    actualState = ""
    #print "get - ", request.GET
    
    if "searchField" in request.GET or request.GET.get("actualState") == "searchField":
        
        keyword = request.GET.get("searchField")
        actualState = "actualState=searchField&searchField="
        actualState += str(keyword.encode('utf-8'))
        
        if keyword == None:
            keyword = ""
        
        if keyword == "":
            for docente in allDocentes:
            
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                
                exlcusividade = ""
                
                if docente.regime_exclusividade is True:
                    exlcusividade = "Sim"
                    pass
                else:
                    exlcusividade = "Não"
                    pass
                
                try:
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    nomeCategoria = "Sem Categoria"
                
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente, nomeCategoria, regime_exlusividade(docente), contract_end])
        else:
            finalkeyword = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
            listaTempoDocente = search_docente(finalkeyword,allDocentes, 0)
            listaTempoDep = search_depertamento(finalkeyword,allDocentes, 0)
            listaTempoCat = search_category(finalkeyword, allDocentes, 0)
            
            tempList = listaTempoDocente + listaTempoDep + listaTempoCat
        
            
            tempList = removeDuplicatedElements(tempList)
            
            if len(tempList) != 0:
                #listaTemp = search_docente(finalkeyword,allDocentes, listaDocentes)
                #listaDocentes.append(item for item in listaTemp)
                listaDocentes += tempList
      
               
                    
       
    elif "departamento" in request.GET or request.GET.get("actualState") == "departamento":
        keyword = request.GET.get("departamento")
        actualState = "actualState=departamento&departamento=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
       
          
        for docente in allDocentes:
              
            departamento_id = docente.departamento_id
            departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
            
            departamentoNome_final = unicodedata.normalize('NFKD', departamentoNome.lower()).encode('ASCII', 'ignore')
   
            exlcusividade = ""
                
            if docente.regime_exclusividade is True:
                exlcusividade = "Sim"
                pass
            else:
                exlcusividade = "Não"
                pass
   
            if departamentoNome_final == letter:
                
                id_Docente = docente.id
                try:
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    nomeCategoria = "Sem Categoria"
                    
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente, nomeCategoria,  regime_exlusividade(docente), contract_end])
        pass
    
    elif "category" in request.GET or request.GET.get("actualState") == "category":
        keyword = request.GET.get("category")
        actualState = "actualState=category&category=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
       
         
        for docente in allDocentes:
              
            departamento_id = docente.departamento_id
            departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
            
           
            exlcusividade = ""
                
            if docente.regime_exclusividade is True:
                exlcusividade = "Sim"
                pass
            else:
                exlcusividade = "Não"
                pass
            
                
            id_Docente = docente.id
            try:
                contrato = Contrato.objects.get(docente__id=id_Docente)
                contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                    #print contrato.categoria.id
                nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id).nome
                
            except ObjectDoesNotExist:
                nomeCategoria = u'Sem Categoria'
            
            nomeCategoria_final = unicodedata.normalize('NFKD', nomeCategoria.lower()).encode('ASCII', 'ignore')
                    
            if nomeCategoria_final == letter:
                    
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente, nomeCategoria,  regime_exlusividade(docente), contract_end])
        pass
        
        
    elif "letra" in request.GET or request.GET.get("actualState") == "letra":
        
        keyword = request.GET.get("letra")
        actualState = "actualState=letra&letra=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
        
          
        for docente in allDocentes:
                
            nomeDocente = unicodedata.normalize('NFKD', docente.nome_completo.lower()).encode('ASCII', 'ignore')
            if nomeDocente.startswith(letter):
              
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                
                exlcusividade = ""
                
                if docente.regime_exclusividade is True:
                    exlcusividade = "Sim"
                    pass
                else:
                    exlcusividade = "Não"
                    pass
                
             
                
                try:
                    
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    nomeCategoria = u'Sem Categoria'
                    contract_end = u'---'
                    
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente, nomeCategoria,  regime_exlusividade(docente), contract_end])
        
        pass
    elif 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"
        for docente in allDocentes:
                
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                
                exlcusividade = ""
                
                if docente.regime_exclusividade is True:
                    exlcusividade = "Sim"
                    pass
                else:
                    exlcusividade = "Não"
                    pass
                    
                
                
                try:
                    
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    nomeCategoria = u'Sem Categoria'
                
                
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente, nomeCategoria, regime_exlusividade(docente), contract_end])
        pass
    
        
        
        
        
    
    paginator = Paginator(listaDocentes, 10)
    drange = range( 1, paginator.num_pages + 1)
    
    
    page = request.GET.get('page')
     
    try:
        docentes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        docentes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        docentes = paginator.page(paginator.num_pages)
        
    return render_to_response("recursosHumanos/listDocente.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

    
    
    
@login_required(redirect_field_name='Teste_home')
def listDocenteEdit_RecursosHumanos(request):
    
    allDocentes = Docente.objects.all()
    
    
    #nomesDepartamentos = {dep.nome for dep in allDepartamentos}
   
    listaDocentes = []
    actualState = ""
    #print "get - ", request.GET
    
    if "searchField" in request.GET or request.GET.get("actualState") == "searchField":
        
        keyword = request.GET.get("searchField")
        actualState = "actualState=searchField&searchField="
        actualState += str(keyword.encode('utf-8'))
        
        if keyword == None:
            keyword = ""
        
        if keyword == "":
            for docente in allDocentes:
            
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                
                exlcusividade = ""
                
                if docente.regime_exclusividade is True:
                    exlcusividade = "Sim"
                    pass
                else:
                    exlcusividade = "Não"
                    pass
                
                try:
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    nomeCategoria = "Sem Categoria"
                
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente, nomeCategoria, regime_exlusividade(docente), contract_end])
        else:
            finalkeyword = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
            listaTempoDocente = search_docente(finalkeyword,allDocentes, 0)
            listaTempoDep = search_depertamento(finalkeyword,allDocentes, 0)
            listaTempoCat = search_category(finalkeyword, allDocentes, 0)
            
            tempList = listaTempoDocente + listaTempoDep + listaTempoCat
            
            tempList = removeDuplicatedElements(tempList)
            
            if len(tempList) != 0:
                #listaTemp = search_docente(finalkeyword,allDocentes, listaDocentes)
                #listaDocentes.append(item for item in listaTemp)
                listaDocentes += tempList
      
               
                    
       
    elif "departamento" in request.GET or request.GET.get("actualState") == "departamento":
        keyword = request.GET.get("departamento")
        actualState = "actualState=departamento&departamento=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
       
          
        for docente in allDocentes:
              
            departamento_id = docente.departamento_id
            departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
            
            departamentoNome_final = unicodedata.normalize('NFKD', departamentoNome.lower()).encode('ASCII', 'ignore')
   
            exlcusividade = ""
                
            if docente.regime_exclusividade is True:
                exlcusividade = "Sim"
                pass
            else:
                exlcusividade = "Não"
                pass
   
            if departamentoNome_final == letter:
                
                id_Docente = docente.id
                try:
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    nomeCategoria = "Sem Categoria"
                    
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente, nomeCategoria,  regime_exlusividade(docente), contract_end])
        pass
    
    elif "category" in request.GET or request.GET.get("actualState") == "category":
        keyword = request.GET.get("category")
        actualState = "actualState=category&category=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
       
         
        for docente in allDocentes:
              
            departamento_id = docente.departamento_id
            departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
            
           
            exlcusividade = ""
                
            if docente.regime_exclusividade is True:
                exlcusividade = "Sim"
                pass
            else:
                exlcusividade = "Não"
                pass
            
                
            id_Docente = docente.id
            try:
                contrato = Contrato.objects.get(docente__id=id_Docente)
                contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                    #print contrato.categoria.id
                nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id).nome
                
            except ObjectDoesNotExist:
                nomeCategoria = u'Sem Categoria'
            
            nomeCategoria_final = unicodedata.normalize('NFKD', nomeCategoria.lower()).encode('ASCII', 'ignore')
                    
            if nomeCategoria_final == letter:
                    
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente, nomeCategoria,  regime_exlusividade(docente), contract_end])
        pass
        
        
    elif "letra" in request.GET or request.GET.get("actualState") == "letra":
        
        keyword = request.GET.get("letra")
        actualState = "actualState=letra&letra=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
        
          
        for docente in allDocentes:
                
            nomeDocente = unicodedata.normalize('NFKD', docente.nome_completo.lower()).encode('ASCII', 'ignore')
            if nomeDocente.startswith(letter):
              
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                
                exlcusividade = ""
                
                if docente.regime_exclusividade is True:
                    exlcusividade = "Sim"
                    pass
                else:
                    exlcusividade = "Não"
                    pass
                
                
                
                try:
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                    
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    nomeCategoria = u'Sem Categoria'
                    contract_end = u'---'
                    
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente, nomeCategoria,  regime_exlusividade(docente), contract_end])
        
        pass
    elif 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"
        for docente in allDocentes:
                
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                
                exlcusividade = ""
                
                if docente.regime_exclusividade is True:
                    exlcusividade = "Sim"
                    pass
                else:
                    exlcusividade = "Não"
                    pass
                    
                
                
                try:
                    
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    nomeCategoria = u'Sem Categoria'
                
                
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente, nomeCategoria, regime_exlusividade(docente), contract_end])
        pass
    
        
        
        
        
    
    paginator = Paginator(listaDocentes, 10)
    drange = range( 1, paginator.num_pages + 1)
    
    
    page = request.GET.get('page')
     
    try:
        docentes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        docentes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        docentes = paginator.page(paginator.num_pages)
        
    return render_to_response("recursosHumanos/listDocenteEdit.html",
        locals(),
        context_instance=RequestContext(request),
        )
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
    
def regime_exlusividade(docente):
    exlcusividade = ""
    if docente.regime_exclusividade is True:
        exlcusividade = "Sim"
    
        pass
    else:
        exlcusividade = "Não"
        pass
    
    return exlcusividade

def search_docente(search_word, allDocentes, isListContracts):
    
    lista = []
    id_Docente = 0
    departamentoNome = ""
    contract_end = None;
    departamento_id = 0
    
    for docente in allDocentes:
                
                nomeDocente = unicodedata.normalize('NFKD', docente.nome_completo.lower()).encode('ASCII', 'ignore')
                if nomeDocente.find(search_word) != -1:
                    
                    departamento_id = docente.departamento_id
                    departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                    id_Docente = docente.id
                    
                 
                
                    try:
                        contrato = Contrato.objects.get(docente__id=id_Docente)
                        contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
                        contract_end = contrato.data_fim.strftime("%d-%m-%Y")
                        contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                        percent = contrato.percentagem 
                        #print contrato.categoria.id
                        nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                    except ObjectDoesNotExist:
                            nomeCategoria = "Sem Categoria"
                    if isListContracts == 0:
                    
                        lista.append([docente.nome_completo, departamentoNome, id_Docente,  nomeCategoria, regime_exlusividade(docente), contract_end])
                    elif isListContracts == 1:
                        lista.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
    
    return lista                
    pass

def search_depertamento(search_word, allDocentes, isListContracts):
    lista = []
    
    for docente in allDocentes:
                
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                
                departamentoNomeFinal = unicodedata.normalize('NFKD', departamentoNome.lower()).encode('ASCII', 'ignore')
                if departamentoNomeFinal.find(search_word) != -1:
                    
                    
                    id_Docente = docente.id
                    try:
                        contrato = Contrato.objects.get(docente__id=id_Docente)
                        contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
                        contract_end = contrato.data_fim.strftime("%d-%m-%Y")
                        contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                        percent = contrato.percentagem 
                        #print contrato.categoria.id
                        nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                    except ObjectDoesNotExist:
                            nomeCategoria = "Sem Categoria"
                    if isListContracts == 0:
                    
                        lista.append([docente.nome_completo, departamentoNome, id_Docente,  nomeCategoria, regime_exlusividade(docente), contract_end])
                    elif isListContracts == 1:
                        lista.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
                    
    return lista                 
    pass

def search_category(search_word, allDocentes, isListContracts):
    
    lista = []
    id_Docente = 0
    departamentoNome = ""
    contract_end = None;
    departamento_id = 0
    
    for docente in allDocentes:
                
               
                
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                    
                 
                
                try:
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
                    contract_end = contrato.data_fim.strftime("%d-%m-%Y")
                    contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                    percent = contrato.percentagem 
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id).nome
                except ObjectDoesNotExist:
                        nomeCategoria = u"Sem Categoria"
                
                
                nomeCategoriaFinal = unicodedata.normalize('NFKD', nomeCategoria.lower()).encode('ASCII', 'ignore')
                
                
                        
                if nomeCategoriaFinal.find(search_word) != -1:
                    
                    
                    
                    if isListContracts == 0:
                        
                    
                        lista.append([docente.nome_completo, departamentoNome, id_Docente,  nomeCategoria, regime_exlusividade(docente), contract_end])
                    elif isListContracts == 1:
                        lista.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
    
    return lista                
    pass
    
@login_required(redirect_field_name='Teste_home')
def listContracts_RecursosHumanos(request):
    
    allDocentes = Docente.objects.all()
   
    listaContracts = []
    actualState = ""
    
    if "searchField" in request.GET or request.GET.get("actualState") == "searchField":
        
        keyword = request.GET.get("searchField")
        actualState = "actualState=searchField&searchField="
        actualState += str(keyword)
        
        if keyword == None:
            keyword = ""
        
        if keyword == "":
            for docente in allDocentes:
            
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                
                           
                try:
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
                    contract_end = contrato.data_fim.strftime("%d-%m-%Y")
                    contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                    percent = contrato.percentagem 
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    contract_start = "---"
                    contract_end = "---"
                    contract_type = "---"
                    percent = "---"
                    nomeCategoria = "Sem Categoria"
                    
                
                listaContracts.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
        else:
            finalkeyword = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
            listaTempoDocente = search_docente(finalkeyword,allDocentes, 1)
            listaTempoDep = search_depertamento(finalkeyword,allDocentes, 1)
            listaTempoCat = search_category(finalkeyword, allDocentes, 1)
            
            tempList = listaTempoDocente + listaTempoDep + listaTempoCat
            tempList.sort()
            
            tempList = list(tempList)
            
            if len(tempList) != 0:
                #listaTemp = search_docente(finalkeyword,allDocentes, listaDocentes)
                #listaDocentes.append(item for item in listaTemp)
                listaContracts += tempList
               
                    
       
    elif "departamento" in request.GET or request.GET.get("actualState") == "departamento":
        keyword = request.GET.get("departamento")
        actualState = "actualState=departamento&departamento=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
       
          
        for docente in allDocentes:
              
            departamento_id = docente.departamento_id
            departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
            
            departamentoNome_final = unicodedata.normalize('NFKD', departamentoNome.lower()).encode('ASCII', 'ignore')
   
        
   
            if departamentoNome_final == letter:
                
                id_Docente = docente.id
                try:
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
                    contract_end = contrato.data_fim.strftime("%d-%m-%Y")
                    contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                    percent = contrato.percentagem 
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    contract_start = "---"
                    contract_end = "---"
                    contract_type = "---"
                    percent = "---"
                    nomeCategoria = "Sem Categoria"
                    
                listaContracts.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
        pass
    
    elif "category" in request.GET or request.GET.get("actualState") == "category":
        keyword = request.GET.get("category")
        actualState = "actualState=category&category=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
       
         
        for docente in allDocentes:
              
            departamento_id = docente.departamento_id
            departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
            
           
            
                
            id_Docente = docente.id
            try:
                contrato = Contrato.objects.get(docente__id=id_Docente)
                contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
                contract_end = contrato.data_fim.strftime("%d-%m-%Y")
                contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                percent = contrato.percentagem 
                    #print contrato.categoria.id
                nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id).nome
                
            except ObjectDoesNotExist:
                contract_start = "---"
                contract_end = "---"
                contract_type = "---"
                percent = "---"
                nomeCategoria = u"Sem Categoria"
            
            nomeCategoria_final = unicodedata.normalize('NFKD', nomeCategoria.lower()).encode('ASCII', 'ignore')
            
            if nomeCategoria_final == letter:
                    
                listaContracts.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
        pass
        
        
    elif "letra" in request.GET or request.GET.get("actualState") == "letra":
        
        keyword = request.GET.get("letra")
        actualState = "actualState=letra&letra=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
       
          
        for docente in allDocentes:
                
            nomeDocente = unicodedata.normalize('NFKD', docente.nome_completo.lower()).encode('ASCII', 'ignore')
            if nomeDocente.startswith(letter):
              
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                
          
                try:
                    
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
                    contract_end = contrato.data_fim.strftime("%d-%m-%Y")
                    contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                    percent = contrato.percentagem 
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    contract_start = "---"
                    contract_end = "---"
                    contract_type = "---"
                    percent = "---"
                    nomeCategoria = "Sem Categoria"
                    
                listaContracts.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
        
        pass
    
    elif "data_inicio" in request.GET or request.GET.get("actualState") == "data_inicio":
        start_date = request.GET.get("date")
        radius = request.GET.get("number_increment")
        actualState = "actualState=data_inicio&date=" + start_date + "&number_increment=" + radius
       
        convertedDate = datetime.strptime(start_date, "%d-%m-%Y")
        
        interval = timedelta(int(radius))
      
        date_down = convertedDate - interval
        
        date_up = convertedDate + interval
        
        
        
        
        for docente in allDocentes:
            
            departamento_id = docente.departamento_id
            departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
            id_Docente = docente.id
                
                            
                
            try:
                    
                contrato = Contrato.objects.get(docente__id=id_Docente)
                contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
                contract_end = contrato.data_fim.strftime("%d-%m-%Y")
                contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                percent = contrato.percentagem 
                #print contrato.categoria.id
                nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
            except ObjectDoesNotExist:
                contract_start = "---"
                contract_end = "---"
                contract_type = "---"
                percent = "---"
                nomeCategoria = "Sem Categoria"
            if not(contract_end.startswith("---")):
                
                date_contract_start = datetime.strptime(contract_start, "%d-%m-%Y")
            
            #print type(date_contract_start)
            
                if date_contract_start > date_down and date_contract_start < date_up:
                        
                    listaContracts.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
        pass
    
    if "data_fim" in request.GET or request.GET.get("actualState") == "data_fim":
        end_date = request.GET.get("date")
        radius = request.GET.get("number_increment")
        actualState = "actualState=data_fim&date=" + end_date + "&number_increment=" + radius
       
        convertedDate = datetime.strptime(end_date, "%d-%m-%Y")
        
        interval = timedelta(int(radius))
      
        date_down = convertedDate - interval
        
        date_up = convertedDate + interval
        
        
        
        
        for docente in allDocentes:
            
            departamento_id = docente.departamento_id
            departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
            id_Docente = docente.id
                
                            
                
            try:
                    
                contrato = Contrato.objects.get(docente__id=id_Docente)
                contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
                contract_end = contrato.data_fim.strftime("%d-%m-%Y")
                contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                percent = contrato.percentagem 
                #print contrato.categoria.id
                nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
            except ObjectDoesNotExist:
                contract_start = "---"
                contract_end = "---"
                contract_type = "---"
                percent = "---"
                nomeCategoria = "Sem Categoria"
                
            if not(contract_end.startswith("---")):  
                date_contract_end = datetime.strptime(contract_end, "%d-%m-%Y")
            
                if date_contract_end > date_down and date_contract_end < date_up:    
                    listaContracts.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
                    pass
                pass
            pass
        pass
    
    if "data_fim_especial" in request.GET or request.GET.get("actualState") == "data_fim_especial":
        end_date = request.GET.get("date")
        radius = request.GET.get("number_increment")
        contractType = request.GET.get("type")
        actualState = "actualState=data_fim_especial&date=" + end_date + "&number_increment=" + radius
       
        convertedDate = datetime.strptime(end_date, "%d-%m-%Y")
        
        interval = timedelta(int(radius))
           
        date_up = convertedDate + interval
        
        for docente in allDocentes:
            
            departamento_id = docente.departamento_id
            departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
            id_Docente = docente.id
                
                            
                
            try:
                    
                contrato = Contrato.objects.get(docente__id=id_Docente)
                contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
                contract_end = contrato.data_fim.strftime("%d-%m-%Y")
                contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                percent = contrato.percentagem 
                #print contrato.categoria.id
                nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
            except ObjectDoesNotExist:
                contract_start = "---"
                contract_end = "---"
                contract_type = "---"
                percent = "---"
                nomeCategoria = "Sem Categoria"
            
            if not(contract_end.startswith("---")):
                date_contract_end = datetime.strptime(contract_end, "%d-%m-%Y")
                
                #print type(date_contract_start)
                
                if date_contract_end > convertedDate and date_contract_end < date_up:
                        if unicode(contractType).startswith("st"):
                            if unicode(contract_type).startswith("Sem Termo"):
                                listaContracts.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
                                pass
                            pass
                        elif unicode(contractType).startswith("ct"):
                            if unicode(contract_type).startswith("Termo Certo"):
                                listaContracts.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
                                pass
                            pass
                        pass
                pass          
        pass
            
    
        
    elif 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"
        for docente in allDocentes:
                
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                
                            
                
                try:
                    
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_start = contrato.data_inicio.strftime("%d-%m-%Y")
                    contract_end = contrato.data_fim.strftime("%d-%m-%Y")
                    contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                    percent = contrato.percentagem 
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    contract_start = "---"
                    contract_end = "---"
                    contract_type = "---"
                    percent = "---"
                    nomeCategoria = "Sem Categoria"
                
                
                listaContracts.append([docente.nome_completo, nomeCategoria, id_Docente, contract_type, percent, contract_start, contract_end])
        pass
    
    paginator = Paginator(listaContracts, 10)
    drange = range( 1, paginator.num_pages + 1)
    
    
    page = request.GET.get('page')
     
    try:
        docentes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        docentes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        docentes = paginator.page(paginator.num_pages)
    
    
    return render_to_response("recursosHumanos/listContracts.html",
        locals(),
        context_instance=RequestContext(request),
        )
    
    pass    

@login_required(redirect_field_name='Teste_home')
def indexRHInfoDocentes(request, id_docente):
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
    
    return render_to_response("recursosHumanos/infoDocente.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

@login_required(redirect_field_name='Teste_home')
def indexRHInfoDocentesContratos(request, id_docente):
    id_departamento = Docente.objects.get(id__exact=id_docente).departamento_id
    nome_Departamento = Departamento.objects.get(id__exact=id_departamento)
    nomeDocente = Docente.objects.get(id__exact=id_docente)
    escalao = Docente.objects.get(id__exact=id_docente).escalao
    regime_exclusividade = Docente.objects.get(id__exact=id_docente).regime_exclusividade
    
    try:
        contrato = Contrato.objects.get(docente__id=id_docente)
        categoria = Categoria.objects.get(id__exact = contrato.categoria.id)
        tipoContrato = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
        percentagem = Contrato.objects.get(docente_id__exact = id_docente).percentagem
        
        #para apresentar no template
        percentagem = str(percentagem) + "%"
        
        dataInicio = Contrato.objects.get(docente_id__exact = id_docente).data_inicio
        dataFim = Contrato.objects.get(docente_id__exact = id_docente).data_fim
    except ObjectDoesNotExist:
        categoria = "Sem Categoria"
        tipoContrato = "---"
        percentagem = "--- "
        dataInicio = "---"
        dataFim = "---"
        
    #atribuir regime exclusividade consoante se é True/False
    if regime_exclusividade == True :
        regimeExclusividade = "Sim"
        pass
    else:
        regimeExclusividade = "Não"
        pass
    
    return render_to_response("recursosHumanos/infoDocenteContrato.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass




@login_required(redirect_field_name='Teste_home')
def indexRH_EditarDocente(request, id_docente):
    return EditDocenteModelFormPreview(EditarDocenteForm)
    pass


@login_required(redirect_field_name='Teste_home')
def addDocenteRH(request):
    return AddDocenteModelFormPreview(AdicionarDocenteForm)
    pass

#ajuda
@login_required(redirect_field_name='Teste_home')
def ajudaRH(request, nr_video):
    
    return render_to_response("recursosHumanos/ajuda.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass


class AddDocenteModelFormPreview(FormPreview):
    preview_template = 'recursosHumanos/pageConfirForm.html'
    form_template = 'recursosHumanos/addDocente.html'
    def done(self, request, cleaned_data):
        a = 0
        estado = "add"
        
        if request.method == 'POST':
            form = AdicionarDocenteForm(request.POST)
            if form.is_valid():
                #passar a variavel nome_completo para o template
                nome_completo= form.cleaned_data['nome_completo']
                #verifica se o campo do regime de exclusividade é
                #verdadeiro ou Falso
                #regime exclusividade igual a verdadeiro
                if form.cleaned_data['regime_exclusividade']:
                    p = Docente(nome_completo = form.cleaned_data['nome_completo'],
                                departamento = form.cleaned_data['departamento'],
                                escalao = form.cleaned_data['escalao'],
                                email = form.cleaned_data['email'],
                                abreviatura = form.cleaned_data['abreviatura'],
                                regime_exclusividade = form.cleaned_data['regime_exclusividade'])
                    pass
                #regime exclusividade igual a falso
                else:
                    regimeExclusividade = False
                    p = Docente(nome_completo = form.cleaned_data['nome_completo'],
                                departamento = form.cleaned_data['departamento'],
                                escalao = form.cleaned_data['escalao'],
                                email = form.cleaned_data['email'],
                                abreviatura = form.cleaned_data['abreviatura'],
                                regime_exclusividade = regimeExclusividade)
                    pass
                
                p.save()   
                #return HttpResponseRedirect('/thanks/') # Redirect after POST
        else:
            form = AdicionarDocenteForm() # An unbound form
        
        return render_to_response("recursosHumanos/sucesso.html",
            locals(),
            context_instance=RequestContext(request),
            )
        pass
    pass
        



class EditDocenteModelFormPreview(FormPreview):
    
    id_docente = 0
    preview_template = 'recursosHumanos/pageConfirForm.html'
    form_template = 'recursosHumanos/editDocente.html'
    #a variavel estado informa a page de confirmação 
    #se está a editar os dados ou adicionar.
    estado = "Editar"
   
    def get_context(self, request, form):
        "Context for template rendering."
        
        return {
                'form': form,
                'stage_field': self.unused_name('stage'),
                'id_docente': self.state['id_docente'],
                'estado' : self.estado
                }
         
    def preview_get(self, request):
        "Displays the form"
        
        id_docente = self.state['id_docente']
        docenteEdit = Docente.objects.get(id=id_docente)
        form = EditarDocenteForm(instance=docenteEdit)
        
        
        try:
            modificacao = DocenteLogs.objects.filter(docente_id = id_docente)
            
            if(len(modificacao) != 0):
                
                modificacao = modificacao.reverse()[len(modificacao) - 1]
                userName = models.User.objects.get(id__exact= modificacao.id_user).username
                infoEdicao = 0         
                
            
        except ObjectDoesNotExist:
            modificacao = "O Docente ainda não foi alterado"
            infoEdicao = 1
    
            
         
        
        
        return render_to_response(self.form_template,
            locals(),
            context_instance=RequestContext(request))
    
    '''    
    def preview_post(self, request):
        "Validates the POST data. If valid, displays the preview page. Else, redisplays form."
        id_docente = self.id_docente
        b = Docente.objects.get(id=id_docente)
        form = EditarDocenteForm(instance=b)
        #context = self.get_context(request, f)
        return self.done(request, form)
    '''
    
    '''
    def preview_post(self, request):
        "Validates the POST data. If valid, displays the preview page. Else, redisplays form."
        id_docente = self.id_docente
        b = Docente.objects.get(id=id_docente)
        form = AddDocenteForm(request.POST)
        context = self.get_context(request, form)
        if form.is_valid():
            self.process_preview(request, form, context)
            context['hash_field'] = self.unused_name('hash')
            context['hash_value'] = self.security_hash(request, form)
            return render_to_response(self.preview_template, locals(), context_instance=RequestContext(request))
        else:
            return self.preview_post(request)
    
    
    def post_post(self, request):
        "Validates the POST data. If valid, calls done(). Else, redisplays form."
        id_docente = self.id_docente
        f = self.form(request.POST, auto_id=self.get_auto_id())
        if f.is_valid():
            if not self._check_security_hash(request.POST.get(self.unused_name('hash'), ''),
                                             request, f):
                return self.failed_hash(request) # Security hash failed.
            return self.done(request, f.cleaned_data)
        else:
            return render_to_response(self.form_template,
                locals(),
                context_instance=RequestContext(request))
           
            
    def parse_params(self, *args, **kwargs):
        self.id_docente =  kwargs['id_docente']
        pass
    '''
    '''
    def process_preview(self, request, form, context):
        """
        Given a validated form, performs any extra processing before displaying
        the preview page, and saves any extra data in context.
        """
        
        self.contador +=1
        print "contador = ", self.contador
        pass
    '''
    def parse_params(self, *args, **kwargs):
        """Handle captured args/kwargs from the URLconf"""
        # get the selected HI test
        try:
            self.state['id_docente'] = kwargs['id_docente']
        except Docente.DoesNotExist:
            raise Http404("Invalid")
        
    def done(self, request, cleaned_data):
        estado = "eddit"
        id_docente = self.state['id_docente']
        d = get_object_or_404(Docente, pk=id_docente)
        if request.method == 'POST':
            b = Docente.objects.get(id=id_docente)
            form = EditarDocenteForm(request.POST, instance=b)
            if form.is_valid():
                #passar a variavel nome_completo para o template
                nome_completo= form.cleaned_data['nome_completo']
                #verifica se o campo do regime de exclusividade é
                #verdadeiro ou Falso
                #regime exclusividade igual a verdadeiro
                if form.cleaned_data['regime_exclusividade']:
                    d.nome_completo = form.cleaned_data['nome_completo']
                    d.departamento = form.cleaned_data['departamento']
                    d.escalao = form.cleaned_data['escalao']
                    d.email = form.cleaned_data['email']
                    d.abreviatura = form.cleaned_data['abreviatura']
                    d.regime_exclusividade = form.cleaned_data['regime_exclusividade']
                    pass
                #regime exclusividade igual a falso
                else:
                    regimeExclusividade = False
                    d.nome_completo = form.cleaned_data['nome_completo']
                    d.departamento = form.cleaned_data['departamento']
                    d.escalao = form.cleaned_data['escalao']
                    d.email = form.cleaned_data['email']
                    d.abreviatura = form.cleaned_data['abreviatura']
                    d.regime_exclusividade = regimeExclusividade
                    pass
                
                '''
                print "Id do Docente ", id_docente
                print "DATA ", datetime.today()
                print "Id do User ", request.user.id
                
                '''
                docLogs = DocenteLogs(docente_id = id_docente,
                                    data_modificacao = datetime.today(),
                                    id_user = request.user.id
                                    )
                docLogs.save()
                d.save()
                self.contador = 0
                #return HttpResponseRedirect('/thanks/') # Redirect after POST
        else:
            
            b = Docente.objects.get(id=id_docente)
            form = EditarDocenteForm(instance=b)
        
        return render_to_response("recursosHumanos/sucesso.html",
            locals(),
            context_instance=RequestContext(request),
            )
        pass

        
def showSaveButton(request, id_docente):
    if request.is_ajax():
        return render_to_response("recursosHumanos/saveButton.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass    

def showSaveButton1(request):
    if request.is_ajax():
        return render_to_response("recursosHumanos/saveButtonAddDoc.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass 

'''
Fim das vistas dos Recursos Humanos
'''