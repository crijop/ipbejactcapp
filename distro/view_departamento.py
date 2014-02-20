# -*- coding: utf-8 -*-
'''
Created on 10 de Out de 2012

@author: admin1
'''

#Modulo de python com o nome view_departamento.py
#Modulo que trata de todas as views dos departamentos


from distro.forms_departamento import AdicionarServicoDocenteForm
from distro.models import Departamento, Turma, UnidadeCurricular, ServicoDocente, \
    Docente, TipoAula, Contrato, Categoria, Modulos, Curso
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.formtools.preview import FormPreview
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q
from django.http import Http404, QueryDict
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.datetime_safe import datetime
import unicodedata




DepUserTeste = user_passes_test(lambda u:u.groups.filter(Q(name='Departamento') | Q(name='Eng') | Q(name='B')).count(), login_url='/')

'''
Método responsavel por
colocar a combo box para o 
utilizaodr escolher um departamento
para delegar o modulo
'''
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def addComboToDelegate(request, *args, **kwargs):

    if request.is_ajax():

        depList = Departamento.objects.exclude(id__exact = request.session['dep_id'])
        
        
        return render_to_response("departamento/comboToDelegate.html",
        locals(),
        context_instance=RequestContext(request),
        )

'''
Metodo responsavel por tratar o pediodo AJAX de aparecimento do filtro de ordenação por
uma letra do alfabeto
presente na lista de docentes e lista de contratos
'''
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def filter_abc(request, *args, **kwargs):

    if request.is_ajax():

        alfabeto = map(chr , range(65, 91))
        return render_to_response("departamento/filter_abc.html",
        locals(),
        context_instance=RequestContext(request),
        )
        
'''
Metodo responsavel por tratar o pediodo AJAX de aparecimento do filtro de ordenação por
uma letra do alfabeto
presente na lista de docentes e lista de contratos.
Neste caso sem receber parametros do Url, a não ser o request
'''
def filter_abcd(request):


    if request.is_ajax():

        alfabeto = map(chr , range(65, 91))
        return render_to_response("departamento/filter_abc.html",
        locals(),
        context_instance=RequestContext(request),
        )
        
'''
Método responsavel por tratar o pedido ajax para o aparecimento da filtragem por categorias
'''
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def filter_cat(request):


    if request.is_ajax():

        allCategories = Categoria.objects.all()

        return render_to_response("departamento/filter_cat.html",
        locals(),
        context_instance=RequestContext(request),
        )
        
'''
Método responsavel por tratar o pedido ajax para o aparecimento da filtragem por cursos
'''
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def filter_curso(request, ano):

    if request.is_ajax():
        allCursos = []
        listTurmas = Turma.objects.filter(unidade_curricular__departamento_id__exact \
                                          = request.session['dep_id'], ano__exact=ano)
        for t in listTurmas:
            allCursos.append(t.unidade_curricular.curso)
            pass
        
        allCursos1 = removeRepetidosLista(allCursos)
        sorted(allCursos1)
        
        return render_to_response("departamento/filter_curso.html",
        locals(),
        context_instance=RequestContext(request),
        )
        
#Método responsável por remover elementos
#repetidos numa lista
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

#Método para definir o ano
#Se o mês actual for igual ou superior ao mẽs de Agosto
#vai devolver o ano seguinte ao da data actual.
def calcularAno():
    dateActual = datetime.today()
    mesActual = dateActual.month
    ano = dateActual.year
    if mesActual >= 8:
        ano += 1
        pass 
    return ano
        

'''
Inicio das vistas do Departamento
'''
#View da página index do departamento.
#só vai entrar nesta view se o utilizador estiver autenticado
#e se pertencer ao grupo de Departamento.
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def indexDepartamento(request):

    ano = calcularAno()
    
    id_Departamento = request.session['dep_id']
    
    MAXIMO_HORAS = 360
    MINIMO_HORAS = 180
    
    listaAnos = listarAnos(id_Departamento)
    listToSendSDoc = []
    listToSendCDoc = []
    
    listaServicoDocente = ServicoDocente.objects.filter(turma__unidade_curricular__departamento_id__exact = id_Departamento,\
                                                         turma__ano__exact = ano)
    
    for servico in listaServicoDocente:
        #Lista de Serviços sem docentes atribuidos
        modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).filter(docente_id__exact = None)
        if(len(modulos) != 0):
            modulos = modulos.reverse()[0]
            turma = Turma.objects.get(id__exact=servico.turma_id)
            unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
            tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
            id_servico = servico.id
            listToSendSDoc.append([unidade, id_servico, turma.turno, tipo_aula, servico.horas])
            pass
        
        #Lista de Serviços com docentes atribuidos
        modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).exclude(docente_id__exact = None)            
        if(len(modulos) != 0):
            modulos = modulos.reverse()[0]
            id_turma = servico.turma_id
            turma = Turma.objects.get(id__exact=servico.turma_id)
            unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
            
            tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
            listToSendCDoc.append([servico.id, unidade, turma.turno, tipo_aula, servico.horas, id_turma])
    
    sizeListSDoc = len(listToSendSDoc)        
    sizeListCDoc = len(listToSendCDoc)
    
    #Responsavel por ver os Docentes com excesso de horas
    #atribuidas e os docentes com nenhuma hora atribuida.
    
    listaDocentesDepartamento = Docente.objects.filter(departamento_id__exact = id_Departamento)
    
    horasTemp = 0 
    nrDocExcedHoras = 0
    
    nrDocSemHoras = 0
    for l in listaDocentesDepartamento:
        horasTemp = 0
            
        moduloTemp = Modulos.objects.filter(servico_docente__turma__ano__exact = ano)\
                                             .filter(docente_id__exact = l.id)
        print moduloTemp
        for m in moduloTemp:
            horasTemp += m.horas
            pass
        if horasTemp > MAXIMO_HORAS: 
            nrDocExcedHoras +=1
            pass
        elif horasTemp == 0:
            nrDocSemHoras +=1
            pass
        pass
            
    return render_to_response("departamento/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass


#view responsavel por filtrar as Turmas pertencentes ao
#Departamento que estiver autenticado.
#só vai entrar nesta view se o utilizador estiver autenticado
#e se pertencer ao grupo de Departamento.
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def listarTurmasDepart(request, ano):
    listaAnos = listarAnos(request.session['dep_id'])
    listaTurmas = []
    anoReferente = ano
    departamento = Departamento.objects.get(id__exact=request.session['dep_id']).nome

    listTurmas = Turma.objects.filter(unidade_curricular__departamento_id__exact = request.session['dep_id'], ano__exact=ano)

    if "searchField" in request.GET or request.GET.get("actualState") == "searchField":
        keyword = request.GET.get("searchField")
        actualState = "actualState=searchField&searchField="
        actualState += str(keyword.encode('utf-8'))

        if keyword == None:
            keyword = ""

        if keyword == "":
            for t in listTurmas:
                listaTurmas.append([t.unidade_curricular.nome, t.id, t.unidade_curricular.curso, t.horas, t.numero_alunos, t.tipo_aula, t.turno])

            listaTurmas.sort()
        else:
            finalkeyword = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
            listSplited = splitSearchPhrase(finalkeyword)
            print listSplited

            listaTempoUC = []
            listaTempoCurso = []
            search_unidadeCurricurlar(listSplited, listTurmas, listaTempoUC, ano)
            search_curso(listSplited, listTurmas, listaTempoUC, ano)

            tempList = listaTempoUC + listaTempoCurso


            tempList = removeDuplicatedElements(tempList)
            
            sizeList = len(tempList)

            if len(tempList) != 0:
                listaTurmas += tempList

            pass

    elif "letra" in request.GET or request.GET.get("actualState") == "letra":


        keyword = request.GET.get("letra")
        actualState = "actualState=letra&letra=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')




        for t in listTurmas:
            tumar_uc = unicodedata.normalize('NFKD', t.unidade_curricular.nome.lower()).encode('ASCII', 'ignore')


            if tumar_uc.startswith(letter):
                
                listaTurmas.append([t.unidade_curricular.nome, t.id, t.unidade_curricular.curso, t.horas, t.numero_alunos, t.tipo_aula, t.turno])
                pass
        
        sizeList = len(listaTurmas)


        pass
    elif "curso" in request.GET or request.GET.get("actualState") == "curso":


        keyword = request.GET.get("curso")
        actualState = "actualState=curso&curso=" + keyword
        courseName = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')


        for t in listTurmas:
            tumar_course = unicodedata.normalize('NFKD', t.unidade_curricular.curso.nome.lower()).encode('ASCII', 'ignore')


            if tumar_course == courseName:
                
                listaTurmas.append([t.unidade_curricular.nome, t.id, t.unidade_curricular.curso, t.horas, t.numero_alunos, t.tipo_aula, t.turno])
                pass
            
        sizeList = len(listaTurmas)


        pass      


    elif 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"

        for t in listTurmas:
            listaTurmas.append([t.unidade_curricular.nome, t.id, t.unidade_curricular.curso, t.horas, t.numero_alunos, t.tipo_aula, t.turno])

        listaTurmas.sort()
        sizeList = len(listaTurmas)

    paginator = Paginator(listaTurmas, 10)
    drange = range(1, paginator.num_pages + 1)


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
Divide o campo de pesquisa pelos espaços
'''
def splitSearchPhrase(keyword):

    listSplited = []

    keywordFinal = keyword.strip()

    listSplited = keywordFinal.split()

    return listSplited

'''
Metodo responsavel por fazer as pesquisas por docente do campo de procura
'''
def search_docente(search_List, allDocentes, listateste, count=0):


    listDocentes = []
    searchList = search_List

    countIncrements = count
    #print count
    if count < len(searchList):
        #print "entrei no ninho"
        for docente in allDocentes:

            nomeDocente = unicodedata.normalize('NFKD', docente.nome_completo.lower()).encode('ASCII', 'ignore')
            if nomeDocente.find(searchList[count]) != -1:

                listDocentes.append(docente)

        countIncrements += 1
        #print "vou chamar o metodo"
        search_docente(searchList, listDocentes, listateste, countIncrements)

    else:

        for docente in allDocentes:

            #listServicoTemp = ServicoDocente.objects.filter(docente_id__exact=docente.id)
            listServicoTemp = Modulos.objects.filter(docente_id__exact = docente.id)
            numberHoras = 0
            for h in listServicoTemp:
                numberHoras += h.horas
            listateste.append([docente.id, docente.nome_completo, len(listServicoTemp), numberHoras])


        #print "vou terminar o else"
        pass

    pass

'''
Metodo responsavel por fazer as pesquisas por unidade curricular do campo de procura
'''
def search_unidadeCurricurlar(search_List, allTurmas, lista, ano,count=0):


    listTurmas = []
    searchList = search_List

    countIncrements = count
    #print count
    if count < len(searchList):
        #print "entrei no ninho"

        for turmas in allTurmas:
            uCtoFind = unicodedata.normalize('NFKD', turmas.unidade_curricular.nome.lower()).encode('ASCII', 'ignore')
            if uCtoFind.find(searchList[count]) != -1:
                listTurmas.append(turmas)

        countIncrements += 1
        #print "vou chamar o metodo"
        search_unidadeCurricurlar(searchList, listTurmas, lista,ano, countIncrements)

    else:

        for turmas in allTurmas:
            lista.append([turmas.unidade_curricular.nome, turmas.id, turmas.unidade_curricular.curso, turmas.horas, turmas.numero_alunos, turmas.tipo_aula, turmas.turno])

        lista.sort()
        pass


'''
Metodo responsavel por fazer as pesquisas por curso do campo de procura
'''
def search_curso(search_List, allTurmas, lista, ano,count=0):


    listTurmas = []
    searchList = search_List

    countIncrements = count
    #print count
    if count < len(searchList):
        #print "entrei no ninho"


        for turmas in allTurmas:
            cursosToFind = unicodedata.normalize('NFKD', turmas.unidade_curricular.curso.nome.lower()).encode('ASCII', 'ignore')
            if cursosToFind.find(searchList[count]) != -1:
                listTurmas.append(turmas)


        countIncrements += 1
        #print "vou chamar o metodo"

        search_curso(searchList, listTurmas, lista,ano, countIncrements)

    else:

        for turmas in allTurmas:
            lista.append([turmas.unidade_curricular.nome, turmas.id, turmas.unidade_curricular.curso, turmas.horas, turmas.numero_alunos, turmas.tipo_aula, turmas.turno])
            
            
            
        lista.sort()
        pass

'''
listDocentes - Mostra todos os professores do departamento e as horas que ainda tem por atribuir
e o numero de turmas a que tão associados e o numero de horas que ja tem atribuidas
'''
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def listDocentes(request):
    id_Departamento = request.session['dep_id']
    listaAnos = listarAnos(id_Departamento)
    actualState = ""

    listToSend = []

    listDocentes = Docente.objects.filter(departamento_id__exact=request.session['dep_id'])

    if "searchField" in request.GET or request.GET.get("actualState") == "searchField":
        keyword = request.GET.get("searchField")
        actualState = "actualState=searchField&searchField="
        actualState += str(keyword.encode('utf-8'))

        if keyword == None:
            keyword = ""

        if keyword == "":
            for docente in listDocentes:
                listServicoTemp = ServicoDocente.objects.filter(docente_id__exact=docente.id)
                numberHoras = 0
                for h in listServicoTemp:
                    numberHoras += h.horas
                listToSend.append([docente.id, docente.nome_completo, len(listServicoTemp), numberHoras])
        else:
            finalkeyword = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
            listSplited = splitSearchPhrase(finalkeyword)
            print listSplited

            listaTempoDocente = []
            search_docente(listSplited, listDocentes, listaTempoDocente)

            tempList = listaTempoDocente


            tempList = removeDuplicatedElements(tempList)

            sizeList = len(tempList)
            
            if len(tempList) != 0:
                listToSend += tempList

            pass
        
    elif "category" in request.GET or request.GET.get("actualState") == "category":
        keyword = request.GET.get("category")
        actualState = "actualState=category&category=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')

        for docente in listDocentes:
            #listServicoTemp = ServicoDocente.objects.filter(docente_id__exact=docente.id)
            listServicoTemp = Modulos.objects.filter(docente_id__exact=docente.id)
        
            id_Docente = docente.id
            numberHoras = 0
            for h in listServicoTemp:
                numberHoras += h.horas
                pass
            try:
                contrato = Contrato.objects.get(docente__id=id_Docente)
                contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                nomeCategoria = Categoria.objects.get(id__exact=contrato.categoria.id).nome
            except ObjectDoesNotExist:
                nomeCategoria = u'Sem Categoria'

            nomeCategoria_final = unicodedata.normalize('NFKD', nomeCategoria.lower()).encode('ASCII', 'ignore')

            if nomeCategoria_final == letter:
                listToSend.append([docente.id, docente.nome_completo, len(listServicoTemp), numberHoras])
        sizeList = len(listToSend)
        pass


    elif "letra" in request.GET or request.GET.get("actualState") == "letra":

        keyword = request.GET.get("letra")
        actualState = "actualState=letra&letra=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')


        for docente in listDocentes:
            nomeDocente = unicodedata.normalize('NFKD', docente.nome_completo.lower()).encode('ASCII', 'ignore')

            if nomeDocente.startswith(letter):
                #listServicoTemp = ServicoDocente.objects.filter(docente_id__exact=docente.id)
                listServicoTemp = Modulos.objects.filter(docente_id__exact=docente.id)
                numberHoras = 0
                for h in listServicoTemp:
                    numberHoras += h.horas
                pass
                listToSend.append([docente.id, docente.nome_completo, len(listServicoTemp), numberHoras])
        sizeList = len(listToSend)
            

        pass
    
    elif "docExcedHours" in request.GET or request.GET.get("actualState") == "docExcedHours":
        chave = request.GET.get("docExcedHours")
        ano = request.GET.get("ano")
        actualState = "actualState=docExcedHours&docExcedHours=" + chave + "&ano=" + ano
        MAXIMO_HORAS = 360 
        listaDocentesDepartamento = Docente.objects.filter(departamento_id__exact = id_Departamento)
        horasTemp       = 0 
        nrDocExcedHoras = 0
        nrDocSemHoras   = 0
        
        if chave == "True":
            for l in listaDocentesDepartamento:
                horasTemp = 0
                listServicoTemp = Modulos.objects.filter(servico_docente__turma__ano__exact = ano)\
                                                     .filter(docente_id__exact = l.id)
                for m in listServicoTemp:
                    horasTemp += m.horas
                    pass
                if horasTemp == 0:
                    listToSend.append([l.id, l.nome_completo, len(listServicoTemp), horasTemp])
                    nrDocSemHoras +=1
                    pass
            pass
            
        elif chave == "False":
            for l in listaDocentesDepartamento:
                horasTemp = 0
                listServicoTemp = Modulos.objects.filter(servico_docente__turma__unidade_curricular__departamento_id__exact\
                                                     = id_Departamento, servico_docente__turma__ano__exact= ano)\
                                                     .filter(docente_id__exact = l.id)
                for m in listServicoTemp:
                    horasTemp += m.horas
                    pass
                if horasTemp > MAXIMO_HORAS: 
                    listToSend.append([l.id, l.nome_completo, len(listServicoTemp), horasTemp])
                    nrDocExcedHoras +=1
                    pass
            pass
        sizeList = len(listToSend)
        pass
    
    elif 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"

        for docente in listDocentes:
            listServicoTemp = Modulos.objects.filter(docente_id__exact=docente.id)
            numberHoras = 0
            for h in listServicoTemp:
                numberHoras += h.horas
            listToSend.append([docente.id, docente.nome_completo, len(listServicoTemp), numberHoras])
        sizeList = len(listToSend)


        pass

    paginator = Paginator(listToSend, 10)
    drange = range(1, paginator.num_pages + 1)


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


'''
Mostra todos os anos disponiveis para um dado departamento
'''
def listarAnos(id_departamento):
    listaAnos = []
    unidadesCurriculares = UnidadeCurricular.objects.filter(departamento_id__exact=id_departamento)
    for uC in unidadesCurriculares:
        turmas = Turma.objects.filter(unidade_curricular_id__exact=uC.id)
        for tur in turmas:
            listaAnos.append(tur.ano)

    listaAnos = removeDuplicatedElements(listaAnos)
    return listaAnos
    pass

'''
Responsavel por remover elementos duplicados na lista final da pesquisa
'''
def removeDuplicatedElements(dataList):
    templist = dataList
    if len(templist) != 0:
        templist.sort()
        last = templist[-1]
        for i in range(len(templist) - 2, -1, -1):
            if last == templist[i]:
                del templist[i]
            else:
                last = templist[i]
    return templist

#View responsavel por representar a informação de um 
#determinado docente. o metodo recebe o id_docente em questão
#só vai entrar nesta view se o utilizador estiver autenticado
#e se pertencer ao grupo de Departamento.
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def infoDocenteDep(request, id_docente):
    listaAnos = listarAnos(request.session['dep_id'])
    servicoDocente = Modulos.objects.filter(docente_id__exact=id_docente)
    unidadesCurriculares = UnidadeCurricular.objects.all()

    docente_name = Docente.objects.get(id__exact=id_docente).nome_completo

    lista = []
   
    horasTotal = 0
    for servDocente in servicoDocente:

        #nome da unidade curricular que o docente vai dar aulas.
        nomeUnidadeCurricular = UnidadeCurricular.objects.get(id__exact=servDocente.servico_docente.turma.unidade_curricular_id).nome
        turma = Turma.objects.get(id__exact=servDocente.servico_docente.turma_id)
        tipoAula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
        turno = turma.turno
        nomeCurso = UnidadeCurricular.objects.get(turma__id__exact=servDocente.servico_docente.turma_id).curso
        horasTotal += servDocente.horas
        lista.append((servDocente.docente_id, nomeUnidadeCurricular,
                           servDocente.horas, nomeCurso))
    
    return render_to_response("departamento/horasServico.html",
        locals(),
        context_instance=RequestContext(request),
        )


'''
Metodo responsavel por fazer as pesquisas por curso do campo de procura na area do serviço docente
'''
def search_curso_sd(search_List, allServicos, lista, count=0):


    listServicos = []
    searchList = search_List

    countIncrements = count
    #print count
    if count < len(searchList):
        #print "entrei no ninho"
        for servico in allServicos:
            modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).exclude(docente_id__exact = None)
            if(len(modulos) != 0):
                modulos = modulos.reverse()[0]
                
                nomeCurso = unicodedata.normalize('NFKD', modulos.servico_docente.turma.unidade_curricular.curso.nome.lower()).encode('ASCII', 'ignore')
                
                if nomeCurso.find(searchList[count]) != -1:
                    
                    listServicos.append(servico)
         
        countIncrements += 1
        #print "vou chamar o metodo"
    
        search_curso_sd(searchList, listServicos, lista, countIncrements)

    else:
        
        for servico in allServicos:
            modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).exclude(docente_id__exact = None)
            if(len(modulos) != 0):
                modulos = modulos.reverse()[0]
                id_turma = servico.turma_id
                turma = Turma.objects.get(id__exact=servico.turma_id)
                unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                    
                tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                             
                lista.append([servico.id, unidade, turma.turno, tipo_aula, servico.horas, id_turma])
                
            
            
        lista.sort()
        pass

'''
Metodo responsavel por fazer as pesquisas por curso do campo de procura na area do serviço docente sem atribuição
'''
def search_curso_nsd(search_List, allServicos, allDelegateModuls, lista, count=0):


    listServicos = []
    listDelgateModuls = []
    searchList = search_List

    countIncrements = count
    #print count
    if count < len(searchList):
        #print "entrei no ninho"
        for servico in allServicos:
            modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).filter(docente_id__exact = None)
            if(len(modulos) != 0):
                modulos = modulos.reverse()[0]
                
                nomeCurso = unicodedata.normalize('NFKD', modulos.servico_docente.turma.unidade_curricular.curso.nome.lower()).encode('ASCII', 'ignore')
                
                if nomeCurso.find(searchList[count]) != -1:
                    
                    listServicos.append(servico)
        
        for lm in allDelegateModuls:
                nomeCurso = unicodedata.normalize('NFKD', lm.servico_docente.turma.unidade_curricular.curso.nome.lower()).encode('ASCII', 'ignore')
                if nomeCurso.find(searchList[count]) != -1:
                    listDelgateModuls.append(lm)
         
        countIncrements += 1
        #print "vou chamar o metodo"
        
       
        search_curso_nsd(searchList, listServicos, listDelgateModuls, lista, countIncrements)

    else:
        
        for servico in allServicos:
           
            id_turma = servico.turma_id
            turma = Turma.objects.get(id__exact=servico.turma_id)
            unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                    
            tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                             
            lista.append([servico.id, unidade, turma.turno, tipo_aula, servico.horas, id_turma])
        
        for lm in allDelegateModuls:
            lista.append([lm.servico_docente.id, lm.servico_docente.turma.unidade_curricular.nome, lm.servico_docente.turma.turno, lm.servico_docente.turma.tipo_aula.tipo, lm.servico_docente.horas, lm.servico_docente.turma.id])
            print lista
                
            
            
        lista.sort()
        pass

'''
Metodo responsavel por fazer as pesquisas por unidade curricular do campo de procura 
na lista de serviços docente já atribuidos
'''
def search_unidadeCurricurlar_sd(search_List, allServicos, lista, count=0):
    
    listServicos = []
    searchList = search_List

    countIncrements = count
    #print count
    if count < len(searchList):
        #print "entrei no ninho"
        for servico in allServicos:
            modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).exclude(docente_id__exact = None)
            
            if(len(modulos) != 0):
                modulos = modulos.reverse()[0]
                
                nomeUC = unicodedata.normalize('NFKD', modulos.servico_docente.turma.unidade_curricular.nome.lower()).encode('ASCII', 'ignore')
                
                if nomeUC.find(searchList[count]) != -1:
                   
                    listServicos.append(servico)
         
        countIncrements += 1
        #print "vou chamar o metodo"
        
       
        search_unidadeCurricurlar_nsd(searchList, listServicos, lista, countIncrements)

    else:
        
        for servico in allServicos:
           
            id_turma = servico.turma_id
            turma = Turma.objects.get(id__exact=servico.turma_id)
            unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                    
            tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                             
            lista.append([servico.id, unidade, turma.turno, tipo_aula, servico.horas, id_turma])
            print lista
                
            
            
        lista.sort()
        pass

'''
Metodo responsavel por fazer as pesquisas por unidade curricular do campo de 
procura na lista de serviços docente por atribuir
'''
def search_unidadeCurricurlar_nsd(search_List, allServicos, allDelegateModuls, lista, count=0):
    
    

    listServicos = []
    listDelgateModuls = []
    searchList = search_List

    countIncrements = count
    #print count
    if count < len(searchList):
        #print "entrei no ninho"
        for servico in allServicos:
            modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).filter(docente_id__exact = None)
            
            if(len(modulos) != 0):
                modulos = modulos.reverse()[0]
                
                nomeUC = unicodedata.normalize('NFKD', modulos.servico_docente.turma.unidade_curricular.nome.lower()).encode('ASCII', 'ignore')
                
                if nomeUC.find(searchList[count]) != -1:
                   
                    listServicos.append(servico)
        
        for lm in allDelegateModuls:
                nomeUC = unicodedata.normalize('NFKD', lm.servico_docente.turma.unidade_curricular.nome.lower()).encode('ASCII', 'ignore')
                if nomeUC.find(searchList[count]) != -1:
                    listDelgateModuls.append(lm)
         
        countIncrements += 1
        #print "vou chamar o metodo"
        
       
        search_unidadeCurricurlar_nsd(searchList, listServicos,listDelgateModuls, lista, countIncrements)

    else:
        
        for servico in allServicos:
           
            id_turma = servico.turma_id
            turma = Turma.objects.get(id__exact=servico.turma_id)
            unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                    
            tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                             
            lista.append([servico.id, unidade, turma.turno, tipo_aula, servico.horas, id_turma])
            
        for lm in allDelegateModuls:
            lista.append([lm.servico_docente.id, lm.servico_docente.turma.unidade_curricular.nome, lm.servico_docente.turma.turno, lm.servico_docente.turma.tipo_aula.tipo, lm.servico_docente.horas, lm.servico_docente.turma.id])
            
            print lista
                
            
            
        lista.sort()
        pass

'''
Lista todas os serviços de docente já atribuidos
recebendo para isso o ano
'''
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def  listServicoDocente(request, ano):
    id_Departamento = request.session['dep_id']
    listaAnos = listarAnos(id_Departamento)

    listToSend = []
    
    
    listaServicoDocente = ServicoDocente.objects.filter(turma__unidade_curricular__departamento_id__exact = id_Departamento, turma__ano__exact = ano )
    
    if "searchField" in request.GET or request.GET.get("actualState") == "searchField":
        keyword = request.GET.get("searchField")
        actualState = "actualState=searchField&searchField="
        actualState += str(keyword.encode('utf-8'))

        if keyword == None:
            keyword = ""

        if keyword == "":
            for servico in listaServicoDocente:
                modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).exclude(docente_id__exact = None)
            
                if(len(modulos) != 0):
                    modulos = modulos.reverse()[0]
                    id_turma = servico.turma_id
                    turma = Turma.objects.get(id__exact=servico.turma_id)
                    unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                    
                    tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                    
        
                    listToSend.append([servico.id, unidade, turma.turno, tipo_aula, servico.horas, id_turma])
        else:
            finalkeyword = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
            listSplited = splitSearchPhrase(finalkeyword)
            print listSplited

            listaTempoCurso = []
            search_curso_sd(listSplited, listaServicoDocente, listaTempoCurso)
            listaTempoUC = []
            search_unidadeCurricurlar_sd(listSplited, listaServicoDocente, listaTempoUC)
           
            
            tempList = listaTempoCurso + listaTempoUC


            tempList = removeDuplicatedElements(tempList)
            
            
            sizeList = len(tempList)
            
            if len(tempList) != 0:
                listToSend += tempList

            pass
        
    
    elif "letra" in request.GET or request.GET.get("actualState") == "letra":

        keyword = request.GET.get("letra")
        actualState = "actualState=letra&letra=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
       
        for servico in listaServicoDocente:
            modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).exclude(docente_id__exact = None)
            #nomeUnidadeCurricular = servico.turma.unidade_curricular.nome
            nomeUnidadeCurricular = unicodedata.normalize('NFKD', servico.turma.unidade_curricular.nome.lower()).encode('ASCII', 'ignore')
            
            if nomeUnidadeCurricular.startswith(letter):
                if(len(modulos) != 0):
                    modulos = modulos.reverse()[0]
                    id_turma = servico.turma_id
                    turma = Turma.objects.get(id__exact=servico.turma_id)
                    unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                    
                    tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                    
        
                    listToSend.append([servico.id, unidade, turma.turno, tipo_aula, servico.horas, id_turma])
        sizeList = len(listToSend)
            
    elif "curso" in request.GET or request.GET.get("actualState") == "curso":
        keyword = request.GET.get("curso")
        actualState = "actualState=curso&curso=" + keyword
        cursos = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
        for servico in listaServicoDocente:
            modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).exclude(docente_id__exact = None)
            if(len(modulos) != 0):
                modulos = modulos.reverse()[0]
                
                nomeCurso = unicodedata.normalize('NFKD', modulos.servico_docente.turma.unidade_curricular.curso.nome.lower()).encode('ASCII', 'ignore')
            
                if nomeCurso == cursos:
                    #modulos = modulos.reverse()[0]
                    id_turma = servico.turma_id
                    turma = Turma.objects.get(id__exact=servico.turma_id)
                    unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                    
                    tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                    
                    listToSend.append([servico.id, unidade, turma.turno, tipo_aula, servico.horas, id_turma])
            sizeList = len(listToSend)
            
        pass
        
    elif 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"
        
        
        
        for servico in listaServicoDocente:
            modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).exclude(docente_id__exact = None)
            
            if(len(modulos) != 0):
                modulos = modulos.reverse()[0]
                id_turma = servico.turma_id
                turma = Turma.objects.get(id__exact=servico.turma_id)
                unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                
                tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                
    
                listToSend.append([servico.id, unidade, turma.turno, tipo_aula, servico.horas, id_turma])
                
        
        sizeList = len(listToSend)
        
    
    
    paginator = Paginator(listToSend, 10)
    drange = range(1, paginator.num_pages + 1)


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
Informação por Modulos pertencente ao Docente 
'''    
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def infoModulosDocente(request, id_docente, ano):
    nomeDocente = Docente.objects.get(id__exact = id_docente)
    return render_to_response("departamento/infoModulosDocente.html",
        locals(),
        context_instance=RequestContext(request),
        )
    
'''
Informação por Modulos pertencente a cada turma 
já com serviço de Docente atribuido em cada ano
'''    
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def infoModulosTurma(request, id_servico, ano):
    id_Departamento = request.session['dep_id']
    listaAnos = listarAnos(id_Departamento)
    
    listInfo = []
    
    modulos = Modulos.objects.filter(servico_docente_id__exact = id_servico)
    servico = ServicoDocente.objects.get(id__exact=id_servico)
    
    nomeTurma = servico.turma.unidade_curricular.nome
    turno = servico.turma.turno
    tipoAula = servico.turma.tipo_aula.tipo
    
    horasTotal = 0
    for m in modulos:
        if m.docente != None:
            horasTotal += m.horas
            listInfo.append([m.docente.id, m.docente.nome_completo, m.horas, "", ""])
        else:
            horasTotal += m.horas
            listInfo.append(["", "Sem Docente Atribuido", m.horas, "", ""])
        pass
    
    
    return render_to_response("departamento/infoModulosTurma.html",
        locals(),
        context_instance=RequestContext(request),
        )
     
    
'''
Método responsavel por listar todos os serviços docente que ainda nao tem todos os docentes atribuidos
nos seus modulos
'''
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def addServicoDocenteDepart(request, ano):
   
    id_Departamento = request.session['dep_id']
    listaAnos = listarAnos(id_Departamento)
    listToSend = []
    
    listRepetidos = []
    
    listaServicoDocente = ServicoDocente.objects.filter(turma__unidade_curricular__departamento_id__exact = id_Departamento, turma__ano__exact = ano)
    listModulosDelegados = Modulos.objects.filter(servico_docente__turma__ano__exact = ano, departamento_id__exact = id_Departamento).filter(docente_id__exact = None).filter(aprovacao__exact = 1)
    listServicosDelegados = ServicoDocente.objects.filter(turma__ano__exact = ano)
        
    #print listModulosDelegados
    '''
    Lista pela pesquisa efectuada
    '''    
    if "searchField" in request.GET or request.GET.get("actualState") == "searchField":
        keyword = request.GET.get("searchField")
        actualState = "actualState=searchField&searchField="
        actualState += str(keyword.encode('utf-8'))

        if keyword == None:
            keyword = ""

        if keyword == "":
            for servico in listaServicoDocente:
                modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).filter(docente_id__exact = None).filter(departamento_id__exact = None)
            
                if(len(modulos) != 0):
                    modulos = modulos.reverse()[0]
                    id_turma = servico.turma_id
                    turma = Turma.objects.get(id__exact=servico.turma_id)
                    unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                    
                    tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                    
                    
                    listToSend.append([servico.id, unidade, turma.turno, tipo_aula, servico.horas, id_turma])
           
            for lm in listModulosDelegados:
                if verify_List_Have_Value(lm.servico_docente.id, listRepetidos) == False:
                    listRepetidos.append(lm.servico_docente.id)                
                    listToSend.append([lm.servico_docente.id, lm.servico_docente.turma.unidade_curricular.nome, lm.servico_docente.turma.turno, lm.servico_docente.turma.tipo_aula.tipo, lm.servico_docente.horas, lm.servico_docente.turma.id])
                
        else:
            finalkeyword = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
            listSplited = splitSearchPhrase(finalkeyword)
            print listSplited

            listaTempoCurso = []
            search_curso_nsd(listSplited, listaServicoDocente, listModulosDelegados, listaTempoCurso)
            listaTempoUC = []
            search_unidadeCurricurlar_nsd(listSplited, listaServicoDocente, listModulosDelegados,  listaTempoUC)
           
            tempList = listaTempoCurso + listaTempoUC


            tempList = removeDuplicatedElements(tempList)
            
            
            sizeList = len(tempList)
            
            if len(tempList) != 0:
                listToSend += tempList

            pass
        
    
    elif "letra" in request.GET or request.GET.get("actualState") == "letra":
        '''
        Lista pelaletra do alfabeto
        '''
        keyword = request.GET.get("letra")
        actualState = "actualState=letra&letra=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
       
        for servico in listaServicoDocente:
            modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).filter(docente_id__exact = None).filter(departamento_id__exact = None)
            #nomeUnidadeCurricular = servico.turma.unidade_curricular.nome
            nomeUnidadeCurricular = unicodedata.normalize('NFKD', servico.turma.unidade_curricular.nome.lower()).encode('ASCII', 'ignore')
            
            if nomeUnidadeCurricular.startswith(letter):
                if(len(modulos) != 0):
                    modulos = modulos.reverse()[0]
                    turma = Turma.objects.get(id__exact=servico.turma_id)
                    unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                    tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                    id_servico = servico.id
                    listToSend.append([id_servico, unidade,  turma.turno, tipo_aula, servico.horas])
                    
        for lm in listModulosDelegados:
                nomeUnidadeCurricular = unicodedata.normalize('NFKD', lm.servico_docente.turma.unidade_curricular.nome.lower()).encode('ASCII', 'ignore')
                if nomeUnidadeCurricular.startswith(letter):
                    if verify_List_Have_Value(lm.servico_docente.id, listRepetidos) == False:                    
                        listRepetidos.append(lm.servico_docente.id) 
                        listToSend.append([lm.servico_docente.id, lm.servico_docente.turma.unidade_curricular.nome, lm.servico_docente.turma.turno, lm.servico_docente.turma.tipo_aula.tipo, lm.servico_docente.horas, lm.servico_docente.turma.id])
        sizeList = len(listToSend)
         
    elif "curso" in request.GET or request.GET.get("actualState") == "curso":
        '''
        Lista pelo curso
        '''   
        keyword = request.GET.get("curso")
        actualState = "actualState=curso&curso=" + keyword
        cursos = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
        
        for servico in listaServicoDocente:
            modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).filter(docente_id__exact = None).filter(departamento_id__exact = None)
            if(len(modulos) != 0):
                modulos = modulos.reverse()[0]
                
                nomeCurso = unicodedata.normalize('NFKD', modulos.servico_docente.turma.unidade_curricular.curso.nome.lower()).encode('ASCII', 'ignore')
                if nomeCurso == cursos:      
                    turma = Turma.objects.get(id__exact=servico.turma_id)
                    unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                    tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                    id_servico = servico.id
                    listToSend.append([id_servico, unidade, turma.turno, tipo_aula, servico.horas])
                    
        for lm in listModulosDelegados:
                nomeCurso = unicodedata.normalize('NFKD', lm.servico_docente.turma.unidade_curricular.curso.nome.lower()).encode('ASCII', 'ignore')
                if nomeCurso == cursos:
                    if verify_List_Have_Value(lm.servico_docente.id, listRepetidos) == False:
                        listRepetidos.append(lm.servico_docente.id) 
                        listToSend.append([lm.servico_docente.id, lm.servico_docente.turma.unidade_curricular.nome, lm.servico_docente.turma.turno, lm.servico_docente.turma.tipo_aula.tipo, lm.servico_docente.horas, lm.servico_docente.turma.id])
                
        sizeList = len(listToSend)
        
        pass
    elif 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"
    
        for servico in listaServicoDocente:
            modulos = Modulos.objects.filter(servico_docente_id__exact = servico.id).filter(docente_id__exact = None).filter(departamento_id__exact = None)
            if(len(modulos) != 0):
                
                modulos = modulos.reverse()[0]
                turma = Turma.objects.get(id__exact=servico.turma_id)
                unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                id_servico = servico.id
                
                listToSend.append([id_servico, unidade, turma.turno, tipo_aula, servico.horas])
        
        for lm in listModulosDelegados:
            #sDocente = ServicoDocente.objects.get(id__exact = lm.servico_docente.id)
            if verify_List_Have_Value(lm.servico_docente.id, listRepetidos) == False:
                listRepetidos.append(lm.servico_docente.id) 
                #listToSend.append([lm.id, lm.turma.unidade_curricular.nome, lm.turma.turno, lm.turma.tipo_aula.tipo, lm.horas, lm.turma.id])
                listToSend.append([lm.servico_docente.id, lm.servico_docente.turma.unidade_curricular.nome, lm.servico_docente.turma.turno, lm.servico_docente.turma.tipo_aula.tipo, lm.servico_docente.horas, lm.servico_docente.turma.id])
       
        print    listRepetidos  
        sizeList = len(listToSend)
    
    listToSend.sort()
    paginator = Paginator(listToSend, 10)
    drange = range(1, paginator.num_pages + 1)

    page = request.GET.get('page')

    try:
        listInfo = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        listInfo = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        listInfo = paginator.page(paginator.num_pages)
    return render_to_response("departamento/turmasSemServicoDocente.html",
        locals(),
        context_instance=RequestContext(request),
        )
    #return AtribuirServicoDocenteFormPreview(AdicionarServicoDocenteForm)
    pass

def verify_List_Have_Value(id_servico, listaValores):
    
    exist = True
    
    if(len(listaValores) != 0):
        for i in listaValores:
            
            if(i == id_servico):
               
                exist = True
            elif i != id_servico:
               
                exist = False
    else:
        
        
        exist = False
        
    return exist
    
    pass   
#Metodo responsavel por tratar o pediodo AJAX do aparecimento
#do Butão para adicionar o Serviço Docente.
def showSaveButton(request, id_servico, id_Departamento, ano):
    if request.is_ajax():

        return render_to_response("departamento/saveButton.html",
                                                        locals(),
                                                        context_instance=RequestContext(request),)
        pass
    pass


#View responsavél por atribuir o serviço docente
#Responsavel por apresentar o formulario ao utilizador.
#só vai entrar nesta view se o utilizador estiver autenticado
#e se pertencer ao grupo de Departamento.
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def viewFormClass(request, *args, **kwargs):
    view = AtribuirServicoDocenteFormPreview(AdicionarServicoDocenteForm)
    return view(request, *args, **kwargs)
    pass


#Class Criada para tratar do formulario
#atribuir o serviço docente.
#mais propriamente para fazer a confirmação dos dados do
#formulário a enviar.
class AtribuirServicoDocenteFormPreview(FormPreview):
    preview_template = 'departamento/pageConfirForm.html'
    form_template = 'departamento/adicionarServicoDocente.html'
  
    def get_context(self, request, form, docentesID, listaAnos, lModulos, listaDocentes, erro, depList, id_departamento):

        "Context for template rendering."

        return {
                'form': form,
                'stage_field': self.unused_name('stage'),
                'id_servico': self.state['id_servico'],
                'docentesID' : docentesID,
                'listaAnos' : listaAnos,
                'lModulos': lModulos,
                'listaDocentes': listaDocentes,
                'erro': erro,
                'depList': depList,
                'id_departamento': id_departamento
                }

    def preview_get(self, request):
        "Displays the form"
        id_departamento = request.session['dep_id']
        listaAnos = listarAnos(id_departamento)
        id_servico = self.state['id_servico']
        nomeTurma = ServicoDocente.objects.get(id__exact = id_servico).turma.unidade_curricular.nome
        f = self.form(auto_id=self.get_auto_id(), initial=self.get_initial(request))
        modulosID  = None
        docentesID = None
        
        depEspecial = ServicoDocente.objects.get(id__exact = id_servico)
        if(depEspecial.turma.unidade_curricular.departamento.id == id_departamento):
            listaModuls = Modulos.objects.filter(servico_docente_id__exact = id_servico)
            #cont = 0 
            lModulos = []
            for lm in listaModuls:
                
                if(lm.docente_id != None):
                    nomeDocente = Docente.objects.get(id__exact = lm.docente_id).nome_completo
                    
                    try:
                        lModulos.append([lm.id, lm.horas, lm.docente_id, lm.servico_docente_id, nomeDocente, "", lm.departamento])
                    except Departamento.DoesNotExist:
                        lModulos.append([lm.id, lm.horas, lm.docente_id, lm.servico_docente_id, nomeDocente, "", None])
                    #cont +=1 
                else:
                    try:
                        lModulos.append([lm.id, lm.horas, lm.docente_id, lm.servico_docente_id, "", "", lm.departamento])
                    except Departamento.DoesNotExist:
                        lModulos.append([lm.id, lm.horas, lm.docente_id, lm.servico_docente_id, "", "", None])
                        
                    #cont +=1
                pass
            
            print lModulos
            
            listaDocentes = Docente.objects.filter(departamento_id__exact = id_departamento)
            lista_docentesFinal = None
        else:
            listaModuls = Modulos.objects.filter(servico_docente_id__exact = id_servico, departamento_id__exact = id_departamento, aprovacao__exact = 1)
            
            print "fsdfdf ",listaModuls
            #cont = 0 
            lModulos = []
            for lm in listaModuls:
                
                if(lm.docente_id != None):
                    nomeDocente = Docente.objects.get(id__exact = lm.docente_id).nome_completo
                    
                    lModulos.append([lm.id, lm.horas, lm.docente_id, lm.servico_docente_id, nomeDocente, "", lm.departamento])
                    #cont +=1 
                else:
                    try:
                        lModulos.append([lm.id, lm.horas, lm.docente_id, lm.servico_docente_id, "", "", lm.departamento])
                    except Departamento.DoesNotExist:
                        lModulos.append([lm.id, lm.horas, lm.docente_id, lm.servico_docente_id, "", "", None])
                        
                    #cont +=1
                pass
            
            print lModulos
            
            listaDocentes = Docente.objects.filter(departamento_id__exact = id_departamento)
            lista_docentesFinal = None
        
        return render_to_response(self.form_template,
            locals(),
            context_instance=RequestContext(request))
   
    def parse_params(self, *args, **kwargs):
        """Handle captured args/kwargs from the URLconf"""
        # get the selected HI test
        try:
            self.state['id_servico'] = kwargs['id_servico']
            self.state['id_Departamento'] = kwargs['id_Departamento']
            self.state['ano'] = kwargs['ano']
        except Docente.DoesNotExist:
            raise Http404("Invalid")
        pass

    
    def preview_post(self, request):
        id_departamento = request.session['dep_id']
        listaAnos = listarAnos(id_departamento)
        "Validates the POST data. If valid, displays the preview page. Else, redisplays form."
        id_servico = self.state['id_servico']
        
        erro = "Um ou mais Modulos não tem docente atribuido"
       
        #Adiciona se os dois arrays vindos do POST 
        modulosID = dict(request.POST)[u'moduloID[]']
        
      
        
        docentesID = dict(request.POST)[u'docenteID[]']
        
        depDelegated = dict(request.POST)[u'delegateDep[]']
        
        print "delegação - ",depDelegated
        
        nomeTurma = ServicoDocente.objects.get(id__exact = id_servico).turma.unidade_curricular.nome
        #precorre se o array de ID de docente faz-se uma consulta pelo seu ID para se obter o Nome e 
        #horas que o deocente realizou e depois guarda se na lista seguinte
        lista_docentesFinal = []
        if(docentesID != None):
        
            for l in docentesID:
                if(l != ''):
                
                    nome = Docente.objects.get(id__exact = l).nome_completo
                    horas = "";
                    lista_docentesFinal.append([nome, horas])
                    pass
                else:
                    lista_docentesFinal.append(['', ''])
                    pass
        depEspecial = ServicoDocente.objects.get(id__exact = id_servico)
        if(depEspecial.turma.unidade_curricular.departamento.id == id_departamento):
            #Aqui criamos uma lista que vai receber os dados a serem mostrados no template entre eles os dados do array criado em cima
            listaModuls = Modulos.objects.filter(servico_docente_id__exact = id_servico)
            cont = 0 
            print "posição - ", depDelegated[cont]
            lModulos = []
            for lm in listaModuls:
                if depDelegated[cont] == 0:
                    lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], lm.departamento, 0])
                else:
                    try:
                        lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], lm.departamento, int(depDelegated[cont])])
                    except Departamento.DoesNotExist:
                        lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], None, int(depDelegated[cont])])
                    
                cont +=1 
                pass
        else:
            listaModuls = Modulos.objects.filter(servico_docente_id__exact = id_servico, departamento_id__exact = id_departamento, aprovacao__exact = 1)
            cont = 0 
            print "posição - ", depDelegated[cont]
            lModulos = []
            for lm in listaModuls:
                if depDelegated[cont] == 0:
                    lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], lm.departamento, 0])
                else:
                    try:
                        lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], lm.departamento, int(depDelegated[cont])])
                    except Departamento.DoesNotExist:
                        lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], None, int(depDelegated[cont])])
                cont +=1 
                pass
        
        depList = Departamento.objects.exclude(id__exact = id_departamento)
        
        
      
        
        listaDocentes = Docente.objects.filter(departamento_id__exact = id_departamento)
        
        b = ServicoDocente.objects.get(id=id_servico)
        
        f = AdicionarServicoDocenteForm(request.POST, instance=b)
        context = self.get_context(request, f, docentesID, listaAnos, lModulos, listaDocentes, erro, depList, id_departamento)
        if f.is_valid(modulosID, docentesID):
             
            self.process_preview(request, f, context)
            context['hash_field'] = self.unused_name('hash')
            context['hash_value'] = self.security_hash(request, f)
            return render_to_response(self.preview_template, context, context_instance=RequestContext(request))
        else:
            return render_to_response(self.form_template, context, context_instance=RequestContext(request))
    
    
    def post_post(self, request):
        "Validates the POST data. If valid, calls done(). Else, redisplays form."

        id_departamento = request.session['dep_id']
        listaAnos = listarAnos(id_departamento)
        id_servico = self.state['id_servico']
        erro = "Um ou mais Modulos não tem docente atribuido"
       
        #Adiciona se os dois arrays vindos do POST 
        modulosID = dict(request.POST)[u'moduloID[]']
        
      
        
        docentesID = dict(request.POST)[u'docenteID[]']
        
        depDelegated = dict(request.POST)[u'delegateDep[]']
        
        
        nomeTurma = ServicoDocente.objects.get(id__exact = id_servico).turma.unidade_curricular.nome
        #precorre se o array de ID de docente faz-se uma consulta pelo seu ID para se obter o Nome e 
        #horas que o deocente realizou e depois guarda se na lista seguinte
        lista_docentesFinal = []
        if(docentesID != None):
        
            for l in docentesID:
                if(l != ''):
                
                    nome = Docente.objects.get(id__exact = l).nome_completo
                    horas = "";
                    lista_docentesFinal.append([nome, horas])
                    pass
                else:
                    lista_docentesFinal.append(['', ''])
                    pass
        
        depEspecial = ServicoDocente.objects.get(id__exact = id_servico)
        if(depEspecial.turma.unidade_curricular.departamento.id == id_departamento):
            #Aqui criamos uma lista que vai receber os dados a serem mostrados no template entre eles os dados do array criado em cima
            listaModuls = Modulos.objects.filter(servico_docente_id__exact = id_servico)
            cont = 0 
            lModulos = []
            for lm in listaModuls:
                
                if depDelegated[cont] == 0:
                    lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], lm.departamento, 0])
                else:
                    try:
                        lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], lm.departamento, int(depDelegated[cont])])
                    except Departamento.DoesNotExist:
                        lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], None, int(depDelegated[cont])])
                cont +=1  
                pass
        else:
            listaModuls = Modulos.objects.filter(servico_docente_id__exact = id_servico, departamento_id__exact = id_departamento, aprovacao__exact = 1)
            cont = 0 
            lModulos = []
            for lm in listaModuls:
                
                if depDelegated[cont] == 0:
                    lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], lm.departamento, 0])
                else:
                    try:
                        lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], lm.departamento, int(depDelegated[cont])])
                    except Departamento.DoesNotExist:
                        lModulos.append([lm.id, lm.horas, docentesID[cont], lm.servico_docente_id, lista_docentesFinal[cont][0], lista_docentesFinal[cont][1], None, int(depDelegated[cont])])
                cont +=1  
                pass
           
        
      
        
        listaDocentes = Docente.objects.filter(departamento_id__exact = id_departamento)
        
        b = ServicoDocente.objects.get(id=id_servico)
        
        f = AdicionarServicoDocenteForm(request.POST, instance=b)
        
        if f.is_valid(modulosID, docentesID):

            if not self._check_security_hash(request.POST.get(self.unused_name('hash'), ''),
                                             request, f):
                return self.failed_hash(request) # Security hash failed.
            return self.done(request)
        else:
            return render_to_response(self.form_template,
                locals(),
                context_instance=RequestContext(request))

    
    def done(self, request):
        listaAnos = listarAnos(request.session['dep_id'])
        id_servico = self.state['id_servico']
        ano = self.state['ano']
        turma = ServicoDocente.objects.filter(id__exact = id_servico)
        
        #Adiciona se os dois arrays vindos do POST 
        modulosID = dict(request.POST)[u'moduloID[]']
        
      
        
        docentesID = dict(request.POST)[u'docenteID[]']
        
        depDelegated = dict(request.POST)[u'delegateDep[]']
        listaModuls = Modulos.objects.filter(servico_docente_id__exact = id_servico)
        
        if request.method == 'POST':

            b = ServicoDocente.objects.get(id=id_servico)
            f = AdicionarServicoDocenteForm(request.POST, instance=b)
            
            if f.is_valid(modulosID, docentesID):
                
                count = 0
                for m in modulosID:
                    p = Modulos(id = m,
                                horas = Modulos.objects.get(id__exact = m).horas,
                                servico_docente_id = id_servico,
                                docente_id = docentesID[count],
                                departamento_id = depDelegated[count],
                                aprovacao = Modulos.objects.get(id__exact = m).aprovacao)
                    p.save()
                    count += 1

        else:
            b = ServicoDocente.objects.get(id=id_servico)

            form = AdicionarServicoDocenteForm(instance=b, id_Departamento = self.state['id_Departamento'],
                                                                                ano = self.state['ano'])

        return render_to_response("departamento/sucesso.html",

            locals(),
            context_instance=RequestContext(request),
            )
        pass

    pass

'''
Fim das vistas do Departamento
'''
