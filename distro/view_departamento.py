# -*- coding: utf-8 -*-
'''
Created on 10 de Out de 2012

@author: admin1
'''


#Modulo de python com o nome view_departamento.py
#Modulo que trata de todas as views dos departamentos


from distro.forms_departamento import AdicionarServicoDocenteForm
from distro.models import Departamento, Turma, UnidadeCurricular, ServicoDocente, \
        Docente, TipoAula, Contrato, Categoria
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.formtools.preview import FormPreview
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
import unicodedata




DepUserTeste = user_passes_test(lambda u:u.groups.filter(Q(name='Departamento') | Q(name='Eng')).count(), login_url='/')

'''
Metodo responsavel por tratar o pediodo AJAX de aparecimento do filtro de ordenação por
uma letra do alfabeto
presente na lista de docentes e lista de contratos
'''
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def filter_abc(request):


    if request.is_ajax():

        alfabeto = map(chr , range(65, 91))

        return render_to_response("recursosHumanos/filter_abc.html",
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

        return render_to_response("recursosHumanos/filter_cat.html",
        locals(),
        context_instance=RequestContext(request),
        )

'''
Inicio das vistas do Departamento
'''
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def indexDepartamento(request):
    listaAnos = listarAnos(request.session['dep_id'])

    return render_to_response("departamento/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass


@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def listarTurmasDepart(request, ano):
    listaAnos = listarAnos(request.session['dep_id'])
    listaTurmas = []
    anoReferente = ano
    departamento = Departamento.objects.get(id__exact=request.session['dep_id']).nome

    #unidadesCurriculares = UnidadeCurricular.objects.filter(departamento_id__exact=request.session['dep_id'])

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

            if len(tempList) != 0:
                listaTurmas += tempList

            pass



    elif 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"

        for t in listTurmas:
            listaTurmas.append([t.unidade_curricular.nome, t.id, t.unidade_curricular.curso, t.horas, t.numero_alunos, t.tipo_aula, t.turno])

        listaTurmas.sort()

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

            listServicoTemp = ServicoDocente.objects.filter(docente_id__exact=docente.id)
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
    listaAnos = listarAnos(request.session['dep_id'])
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

            if len(tempList) != 0:
                listToSend += tempList

            pass
    elif "category" in request.GET or request.GET.get("actualState") == "category":
        keyword = request.GET.get("category")
        actualState = "actualState=category&category=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')

        for docente in listDocentes:
            listServicoTemp = ServicoDocente.objects.filter(docente_id__exact=docente.id)
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
        pass


    elif "letra" in request.GET or request.GET.get("actualState") == "letra":

        keyword = request.GET.get("letra")
        actualState = "actualState=letra&letra=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')


        for docente in listDocentes:
            nomeDocente = unicodedata.normalize('NFKD', docente.nome_completo.lower()).encode('ASCII', 'ignore')

            if nomeDocente.startswith(letter):
                print docente.id
                listServicoTemp = ServicoDocente.objects.filter(docente_id__exact=docente.id)
                numberHoras = 0
                for h in listServicoTemp:
                    numberHoras += h.horas
                pass
                listToSend.append([docente.id, docente.nome_completo, len(listServicoTemp), numberHoras])
                pass

        pass
    elif 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"

        for docente in listDocentes:
            listServicoTemp = ServicoDocente.objects.filter(docente_id__exact=docente.id)
            numberHoras = 0
            for h in listServicoTemp:
                numberHoras += h.horas
            listToSend.append([docente.id, docente.nome_completo, len(listServicoTemp), numberHoras])


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


@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def infoDocenteDep(request, id_docente):
    listaAnos = listarAnos(request.session['dep_id'])
    servicoDocente = ServicoDocente.objects.filter(docente_id__exact=id_docente)
    unidadesCurriculares = UnidadeCurricular.objects.all()

    docente_name = Docente.objects.get(id__exact=id_docente).nome_completo

    lista = []
    #numero total de horas que o docente tem de serviço
    numeroTotalHoras = 0
    for servDocente in servicoDocente:

        #nome da unidade curricular que o docente vai dar aulas.
        nomeUnidadeCurricular = UnidadeCurricular.objects.get(turma__id__exact=servDocente.turma_id).nome
        tipoAula = Turma.objects.get(id__exact=servDocente.turma_id).tipo_aula
        turno = Turma.objects.get(id__exact=servDocente.turma_id).turno
        nomeCurso = UnidadeCurricular.objects.get(turma__id__exact=servDocente.turma_id).curso
        numeroTotalHoras += servDocente.horas
        lista.append((servDocente.docente_id, nomeUnidadeCurricular,
                           servDocente.horas, nomeCurso))

    return render_to_response("departamento/horasServico.html",
        locals(),
        context_instance=RequestContext(request),
        )

'''
Lista todas os serviços de docente já atribuidos
recebendo para isso o ano
'''
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def  listServicoDocente(request, ano):
    listaAnos = listarAnos(request.session['dep_id'])

    listToSend = []
    unidadesCurriculares = UnidadeCurricular.objects.filter(departamento_id__exact=request.session['dep_id'])

    for uC in unidadesCurriculares:
        turmasFilter = Turma.objects.filter(unidade_curricular_id__exact=uC.id, ano__exact=ano)

        for t in turmasFilter:
            listaServicoDocente = ServicoDocente.objects.filter(turma_id__exact=t.id).exclude(docente_id__exact=None)

            for servico in listaServicoDocente:
                turma = Turma.objects.get(id__exact=servico.turma_id)
                
                id_turma = servico.turma_id

                unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome

                docente = Docente.objects.get(id__exact=servico.docente_id).nome_completo

                id_docente = servico.docente_id
                
                tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo
                
                
                listToSend.append([servico.id, docente, unidade, turma.turno, tipo_aula, servico.horas, id_turma, id_docente])

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
já com serviço de Docente atribuido em cada ano
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
Informação por Modulos pertencente ao Docente 
já com serviço de Docente atribuido em cada ano
'''    
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def infoModulosTurma(request, id_turma, ano):
    nomeTurma = Turma.objects.get(id__exact = id_turma).unidade_curricular.nome
    tipoAula = Turma.objects.get(id__exact = id_turma).tipo_aula
    turno = Turma.objects.get(id__exact = id_turma).turno
    return render_to_response("departamento/infoModulosTurma.html",
        locals(),
        context_instance=RequestContext(request),
        )      
    

@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def addServicoDocenteDepart(request, ano):
    id_Departamento = request.session['dep_id']
    listaAnos = listarAnos(id_Departamento)
    listToSend = []
    unidadesCurriculares = UnidadeCurricular.objects.filter(departamento_id__exact=request.session['dep_id'])

    for uC in unidadesCurriculares:
        turmasFilter = Turma.objects.filter(unidade_curricular_id__exact=uC.id, ano__exact=ano)
        for t in turmasFilter:
            listaServicoDocente = ServicoDocente.objects.filter(turma_id__exact=t.id).filter(docente_id__exact=None)
            for servico in listaServicoDocente:
                turma = Turma.objects.get(id__exact=servico.turma_id)
                unidade = UnidadeCurricular.objects.get(id__exact=turma.unidade_curricular_id).nome
                tipo_aula = TipoAula.objects.get(id__exact=turma.tipo_aula_id).tipo

                listToSend.append([unidade, servico.id, turma.turno, tipo_aula, servico.horas])

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


def showSaveButton(request, id_servico, id_Departamento, ano):
    if request.is_ajax():

        return render_to_response("departamento/saveButton.html",
                                                        locals(),
                                                        context_instance=RequestContext(request),)
        pass
    pass



class AtribuirServicoDocenteFormPreview(FormPreview):
    preview_template = 'departamento/pageConfirForm.html'
    form_template = 'departamento/addServicoDocente.html'

    estado = "Editar"


    def get_context(self, request, form, nomeTurma, listaAnos):

        "Context for template rendering."

        return {
                'form': form,
                'stage_field': self.unused_name('stage'),
                'id_servico': self.state['id_servico'],
                'nomeTurma' : nomeTurma,
                'listaAnos' : listaAnos
                }

    def preview_get(self, request):
        "Displays the form"
        listaAnos = listarAnos(request.session['dep_id'])
        id_servico = self.state['id_servico']
        nomeTurma = ServicoDocente.objects.get(id__exact = id_servico).turma.unidade_curricular.nome

        b = ServicoDocente.objects.get(id=id_servico)
        form = AdicionarServicoDocenteForm(instance=b,
                                    id_Departamento = self.state['id_Departamento'],
                                    ano = self.state['ano'])


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
        listaAnos = listarAnos(request.session['dep_id'])
        "Validates the POST data. If valid, displays the preview page. Else, redisplays form."
        id_servico = self.state['id_servico']
        nomeTurma = ServicoDocente.objects.get(id__exact = id_servico).turma.unidade_curricular.nome
        b = ServicoDocente.objects.get(id=id_servico)
        f = AdicionarServicoDocenteForm(request.POST, instance=b,
                            id_Departamento = self.state['id_Departamento'],
                            ano = self.state['ano'])
        context = self.get_context(request, f, nomeTurma, listaAnos)
        if f.is_valid():
            self.process_preview(request, f, context)
            context['hash_field'] = self.unused_name('hash')
            context['hash_value'] = self.security_hash(request, f)
            return render_to_response(self.preview_template, context, context_instance=RequestContext(request))
        else:
            return render_to_response(self.form_template, context, context_instance=RequestContext(request))

    def post_post(self, request):
        "Validates the POST data. If valid, calls done(). Else, redisplays form."
        listaAnos = listarAnos(request.session['dep_id'])
        id_servico = self.state['id_servico']
        nomeTurma = ServicoDocente.objects.get(id__exact = id_servico).turma.unidade_curricular.nome
        b = ServicoDocente.objects.get(id=id_servico)
        f = AdicionarServicoDocenteForm(request.POST, instance=b,
                            id_Departamento = self.state['id_Departamento'],
                            ano = self.state['ano'])
        if f.is_valid():
            if not self._check_security_hash(request.POST.get(self.unused_name('hash'), ''),
                                             request, f):
                return self.failed_hash(request) # Security hash failed.
            return self.done(request, f.cleaned_data)
        else:
            return render_to_response(self.form_template,
                self.get_context(request, f, nomeTurma, listaAnos),
                context_instance=RequestContext(request))


    def done(self, request, cleaned_data):
        listaAnos = listarAnos(request.session['dep_id'])
        id_servico = self.state['id_servico']
        ano = self.state['ano']
        turma = ServicoDocente.objects.filter(id__exact = id_servico)
        d = get_object_or_404(ServicoDocente, pk=id_servico)
        if request.method == 'POST':

            b = ServicoDocente.objects.get(id=id_servico)
            form = AdicionarServicoDocenteForm(request.POST, instance=b,
                                                                            id_Departamento = self.state['id_Departamento'],
                                                                            ano = ano)
            if form.is_valid():
                d.turma_id = id_servico
                d.docente_id = form.cleaned_data['docente']
                d.horas = form.cleaned_data['horas']

                d.save()


                #return HttpResponseRedirect('/thanks/') # Redirect after POST
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
