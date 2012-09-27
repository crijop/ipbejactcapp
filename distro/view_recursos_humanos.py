# -*- coding: utf-8 -*-

'''
Created on 25 de Set de 2012

@author: António
'''
from distro.forms import EditarDocenteForm, AddDocenteForm
from distro.models import Departamento, Docente, Contrato, Categoria, \
    TipoContrato
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.preview import FormPreview
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from pydoc import Doc
import unicodedata

'''
Inicio das vistas dos Recursos Humanos


''' 

def filter_abc(request):

    if request.is_ajax():
       
        alfabeto = map(chr , range(65, 91))
        
        return render_to_response("recursosHumanos/filter_abc.html",
        locals(),
        context_instance=RequestContext(request),
        )
        
def filter_dep(request):

    if request.is_ajax():
       
        allDepartamentos = Departamento.objects.all()
        
        return render_to_response("recursosHumanos/filter_dep.html",
        locals(),
        context_instance=RequestContext(request),
        )

def filter_cat(request):

    if request.is_ajax():
       
        allCategories = Categoria.objects.all()
        
        return render_to_response("recursosHumanos/filter_cat.html",
        locals(),
        context_instance=RequestContext(request),
        )
        

def filter_date_start(request):

    if request.is_ajax():
       
        
        
        return render_to_response("recursosHumanos/filter_date_start.html",
        locals(),
        context_instance=RequestContext(request),
        )

def ajax(request):

    if request.is_ajax():
       
        
        
        return render_to_response("recursosHumanos/index.html",
        locals(),
        context_instance=RequestContext(request),
        )

@login_required(redirect_field_name='Teste_home')
def indexRecursosHumanos(request):
    
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
        actualState += str(keyword)
        
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
            listaTempoDocente = search_docente(finalkeyword,allDocentes)
            listaTempoDep = search_depertamento(finalkeyword,allDocentes)
            if len(listaTempoDocente) != 0:
                #listaTemp = search_docente(finalkeyword,allDocentes, listaDocentes)
                #listaDocentes.append(item for item in listaTemp)
                listaDocentes += listaTempoDocente
            elif len(listaTempoDep) != 0:
                listaDocentes += listaTempoDep
               
                    
       
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


def regime_exlusividade(docente):
    exlcusividade = ""
    if docente.regime_exclusividade is True:
        exlcusividade = "Sim"
    
        pass
    else:
        exlcusividade = "Não"
        pass
    
    return exlcusividade

def search_docente(search_word, allDocentes):
    
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
                        contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                        #print contrato.categoria.id
                        nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                    except ObjectDoesNotExist:
                            nomeCategoria = "Sem Categoria"
                    
                    lista.append([docente.nome_completo, departamentoNome, id_Docente,  nomeCategoria, regime_exlusividade(docente), contract_end])
                    
    
    return lista                
    pass

def search_depertamento(search_word, allDocentes):
    lista = []
    
    for docente in allDocentes:
                
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                
                departamentoNome = unicodedata.normalize('NFKD', departamentoNome.lower()).encode('ASCII', 'ignore')
                if departamentoNome.find(search_word) != -1:
                    
                    
                    id_Docente = docente.id
                    lista.append([docente.nome_completo, departamentoNome, id_Docente])
                    
    return lista                 
    pass


    
@login_required(redirect_field_name='Teste_home')
def listContracts_RecursosHumanos(request):
    
    allDocentes = Docente.objects.all()
   
    listaContracts = []
    actualState = ""
    
    if 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"
        for docente in allDocentes:
                
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                
                            
                
                try:
                    
                    contrato = Contrato.objects.get(docente__id=id_Docente)
                    contract_start = contrato.data_inicio.strftime("%d/%m/%Y")
                    contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                    contract_type = TipoContrato.objects.get(id__exact = contrato.tipo_contrato_id)
                    percent = contrato.percentagem 
                        #print contrato.categoria.id
                    nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id)
                except ObjectDoesNotExist:
                    nomeCategoria = u'Sem Categoria'
                
                
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
    a = id_docente
    #atribuir regime exclusividade consoante se é True/False
    if regime_exclusividade == True:
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
def indexRH_EditarDocente(request, id_docente):
    return EditDocenteModelFormPreview(EditarDocenteForm)
    pass






@login_required(redirect_field_name='Teste_home')
def addDocenteRH(request):
    return DocenteModelFormPreview(AddDocenteForm)
    pass


class DocenteModelFormPreview(FormPreview):
    preview_template = 'recursosHumanos/pageConfirForm.html'
    form_template = 'recursosHumanos/addDocente.html'
    def done(self, request, cleaned_data):
        a = 0
        if request.method == 'POST':
            form = AddDocenteForm(request.POST)
            if form.is_valid():
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
            form = AddDocenteForm() # An unbound form
        
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


    def get_context(self, request, form):
        "Context for template rendering."
        return {'form': form, 'stage_field': self.unused_name('stage'), 'id_docente': self.state['id_docente']}
         
    def preview_get(self, request):
        "Displays the form"
        
        print "GETTTTTTTTTTTTTTTTTTTTTTTT"
        id_docente = self.state['id_docente']
        b = Docente.objects.get(id=id_docente)
        form = EditarDocenteForm(instance=b)
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
    
    def parse_params(self, *args, **kwargs):
        """Handle captured args/kwargs from the URLconf"""
        # get the selected HI test
        try:
            self.state['id_docente'] = kwargs['id_docente']
        except Docente.DoesNotExist:
            raise Http404("Invalid HI test id: '%s'")
    '''  
    def done(self, request):
        """save the results of the form and return an HttpResponseRedirect"""
        self.state['ss_formset'].save(self.state['gene_form'])
        return HttpResponseRedirect('recursosHumanos/sucesso.html')
    '''
    def done(self, request, cleaned_data):
        print "DONEEEEEEEEEEEEEEEEEEEEEE"
        id_docente = self.state['id_docente']
        
        p = get_object_or_404(Docente, pk=id_docente)
        if request.method == 'POST':
            b = Docente.objects.get(id=id_docente)
            form = EditarDocenteForm(request.POST, instance=b)
            if form.is_valid():
                #verifica se o campo do regime de exclusividade é
                #verdadeiro ou Falso
                #regime exclusividade igual a verdadeiro
                if form.cleaned_data['regime_exclusividade']:
                    p.nome_completo = form.cleaned_data['nome_completo']
                    p.departamento = form.cleaned_data['departamento']
                    p.escalao = form.cleaned_data['escalao']
                    p.email = form.cleaned_data['email']
                    p.abreviatura = form.cleaned_data['abreviatura']
                    p.regime_exclusividade = form.cleaned_data['regime_exclusividade']
                    pass
                #regime exclusividade igual a falso
                else:
                    regimeExclusividade = False
                    p.nome_completo = form.cleaned_data['nome_completo']
                    p.departamento = form.cleaned_data['departamento']
                    p.escalao = form.cleaned_data['escalao']
                    p.email = form.cleaned_data['email']
                    p.abreviatura = form.cleaned_data['abreviatura']
                    p.regime_exclusividade = regimeExclusividade
                    pass
                
                p.save()   
                #return HttpResponseRedirect('/thanks/') # Redirect after POST
        else:
            
            b = Docente.objects.get(id=id_docente)
            form = EditarDocenteForm(instance=b)
        
        return render_to_response("recursosHumanos/sucesso.html",
            locals(),
            context_instance=RequestContext(request),
            )
        pass

        
    



'''
Fim das vistas dos Recursos Humanos
'''