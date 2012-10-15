# -*- coding: utf-8 -*-
'''
Created on 10 de Out de 2012

@author: admin1
'''
from distro.forms_departamento import AdicionarServicoDocenteForm
from distro.models import Departamento, Turma, UnidadeCurricular, ServicoDocente, \
	Docente, TipoAula
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.formtools.preview import FormPreview
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext





DepUserTeste = user_passes_test(lambda u:u.groups.filter(Q(name='Departamento') | Q(name='Eng')).count())

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
    departamento = Departamento.objects.get(id__exact = request.session['dep_id']).nome
    
    unidadesCurriculares = UnidadeCurricular.objects.filter(departamento_id__exact = request.session['dep_id'])
    
    for uC in unidadesCurriculares:
        turmasFilter = Turma.objects.filter(unidade_curricular_id__exact = uC.id, ano__exact = ano)
        
        for t in turmasFilter:    
            listaTurmas.append([t.unidade_curricular.nome, t.id, t.unidade_curricular.curso, t.horas, t.numero_alunos, t.tipo_aula, t.turno])
    
    listaTurmas.sort()

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
   
    listToSend = []
    unidadesCurriculares = UnidadeCurricular.objects.filter(departamento_id__exact = request.session['dep_id'])
    
    for uC in unidadesCurriculares:
        turmasFilter = Turma.objects.filter(unidade_curricular_id__exact = uC.id, ano__exact = ano)
        
        for t in turmasFilter:
            listaServicoDocente = ServicoDocente.objects.filter(turma_id__exact = t.id).exclude(docente_id__exact = None)
    
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
    
@login_required(redirect_field_name='login_redirectUsers')
@DepUserTeste
def addServicoDocenteDepart(request, ano):
    listaAnos = listarAnos(request.session['dep_id'])
    listToSend = []
    unidadesCurriculares = UnidadeCurricular.objects.filter(departamento_id__exact = request.session['dep_id'])
    
    for uC in unidadesCurriculares:
        turmasFilter = Turma.objects.filter(unidade_curricular_id__exact = uC.id, ano__exact = ano)
        for t in turmasFilter:
            listaServicoDocente = ServicoDocente.objects.filter(turma_id__exact = t.id).filter(docente_id__exact = None)
            for servico in listaServicoDocente:
                turma = Turma.objects.get(id__exact = servico.turma_id)
                unidade = UnidadeCurricular.objects.get(id__exact = turma.unidade_curricular_id).nome        
                tipo_aula = TipoAula.objects.get(id__exact = turma.tipo_aula_id).tipo
        
                listToSend.append([unidade, servico.id, turma.turno, tipo_aula, servico.horas])
        
    listToSend.sort()    
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
    return render_to_response("departamento/turmasSemServicoDocente.html",
        locals(),
        context_instance=RequestContext(request),
        )
    #return AtribuirServicoDocenteFormPreview(AdicionarServicoDocenteForm)
    pass   
    
    
class AtribuirServicoDocenteFormPreview(FormPreview):
    preview_template = 'recursosHumanos/pageConfirForm.html'
    form_template = 'departamento/addServicoDocente.html'
    
    estado = "Editar"
    
    def get_context(self, request, form):
        "Context for template rendering."
        
        return {
                'form': form,
                'stage_field': self.unused_name('stage'),
                'id_servico': self.state['id_servico'],
                'estado' : self.estado
                }
        
        
    def preview_get(self, request):
        "Displays the form"
        
        id_servico = self.state['id_servico']
        print "xsxxxxxxxxxxxxxxxxxxxxxxxxxxxx ", id_servico
        b = ServicoDocente.objects.get(id=id_servico)
        form = AdicionarServicoDocenteForm(request.POST, instance=b)
            
        
        return render_to_response(self.form_template,
            locals(),
            context_instance=RequestContext(request))
    
    def parse_params(self, *args, **kwargs):
        """Handle captured args/kwargs from the URLconf"""
        # get the selected HI test
        try:
            self.state['id_servico'] = kwargs['id_servico']
        except Docente.DoesNotExist:
            raise Http404("Invalid")
        pass
       
    def done(self, request, cleaned_data):
        id_servico = self.state['id_servico']
        d = get_object_or_404(ServicoDocente, pk=id_servico)
        if request.method == 'POST':
            b = ServicoDocente.objects.get(id=id_servico)
            form = AdicionarServicoDocenteForm(request.POST, instance=b)
            if form.is_valid():
                '''
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
                '''
                print "Id do Docente ", id_docente
                print "DATA ", datetime.today()
                print "Id do User ", request.user.id
                
                '''
                '''
                docLogs = DocenteLogs(docente_id = id_docente,
                                    data_modificacao = datetime.today(),
                                    id_user = request.user.id
                                    )
                docLogs.save()
                d.save()
                self.contador = 0
                '''
                #return HttpResponseRedirect('/thanks/') # Redirect after POST
        else:
            b = ServicoDocente.objects.get(id=id_servico)
            form = AdicionarServicoDocenteForm(instance=b)
            
        return render_to_response("recursosHumanos/sucesso.html",
            locals(),
            context_instance=RequestContext(request),
            )
        pass
      
    pass    

'''
Fim das vistas do Departamento
''' 
