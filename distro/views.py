# -*- coding: utf-8 -*-

# Create your views here.
from distro.models import Curso, Docente, ServicoDocente, TipoAula, Turma, \
    UnidadeCurricular, ReducaoServicoDocente, Reducao, Departamento
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from distro.forms import AddDocenteForm

import unicodedata



#login_required - só entra nesta vista se
#o utilizador estiver autênticado
#vista para a Página Home
@login_required
def Teste_home(request):
    
    name_group = Group.objects.get(name="Cientifico")
    name_group1 = Group.objects.get(name="CoordenadoresCursos")
    name_group2 = Group.objects.get(name="Departamento")
    name_group3 = Group.objects.get(name = "DirectoresEscola")
    name_group4 = Group.objects.get(name="Docente")
    name_group5 = Group.objects.get(name = "RecusosHumanos")
    name_group6 = Group.objects.get(name = "servicosPlaneamento")
    
    #verifica se o utlizador pertence ao grupo do Cientifico
    if name_group in request.user.groups.all():
        return redirect(indexCientifico)
        pass
    #verifica se o utlizador pertence ao grupo dos Coordenadores Cursos
    if name_group1 in request.user.groups.all():
        return redirect(indexCoordCursos)
        pass
    #verifica se o utlizador pertence ao grupo do Departamento
    elif name_group2 in request.user.groups.all():
        return redirect(indexDepartamento)
        pass
    #verifica se o utlizador pertence ao grupo dos Directores de Escolas
    elif name_group3 in request.user.groups.all():
        return redirect(indexDirectoresEscola)
        pass
    #verifica se o utlizador pertence ao grupo do Docente
    elif name_group4 in request.user.groups.all():
        '''return render_to_response("docentes/index.html",
        locals(),
        context_instance=RequestContext(request),
        )'''
        docentes = Docente.objects.all()
        for docente in docentes:
            if docente.abreviatura == request.user.username:
                request.session['nomeDocente'] = docente.nome_completo
                request.session['nr_Docente'] = docente.id
                return redirect(indexDocente)
                pass
            else:
                pass
            
        return False
    #verifica se o utlizador pertence ao grupo dos recursos Humanos
    elif name_group5 in request.user.groups.all():
        return redirect(indexRecursosHumanos)
        pass
    #verifica se o utlizador pertence ao grupo dos servicosPlaneamento
    elif name_group6 in request.user.groups.all():
        return redirect(indexServicoPlaneamento)
        pass
    
    #Se as condições anteriores não se verificarem, 
    #é mostrado o conteudo da Página Teste_home.html
    else:
        return render_to_response("Teste_home.html",
            locals(),
            context_instance=RequestContext(request),
            )
        pass
    pass


'''
Inicio das vistas do Ciêntifico
'''
@login_required(redirect_field_name='Teste_home')
def indexCientifico(request):
    return render_to_response("cientifico/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass
'''
Fim das vistas do Ciêntifico
'''

'''
Inicio das vistas dos Coordenadores Cursos
'''
#Falta a tabela para definir os Coordenadores...............................
#Falta fazer o url's
@login_required(redirect_field_name='Teste_home')
def indexCoordCursos(request):
    return render_to_response("CoordCursos/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

'''
Fim das vistas dos Coordenadores Cursos
'''

'''
Inicio das vistas do Departamento
''' 
@login_required(redirect_field_name='Teste_home')
def indexDepartamento(request):
    return render_to_response("departamento/index.html",
        locals(),
        context_instance=RequestContext(request),
        )

'''
Fim das vistas do Departamento
''' 
    
'''
Inicio das vistas dos Directores de Escola
''' 
@login_required(redirect_field_name='Teste_home')
def indexDirectoresEscola(request):
    return render_to_response("directoresEscola/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

'''
Fim das vistas dos Directores de Escola
'''
    

'''
Inicio das vistas dos docentes
''' 
#Página Inicial do utilizador Docente
@login_required(redirect_field_name='Teste_home')
def indexDocente(request):
    nomeDocente = request.session['nomeDocente']
    nrDocente = request.session['nr_Docente']
    servicoDocente = ServicoDocente.objects.all()
    lista = []
    #numero total de horas que o docente tem de serviço
    numeroTotalHoras = 0
    horasServico = 0
    reducaoHoras = 0
    for servDocente in servicoDocente:
        if servDocente.docente_id ==  nrDocente:
            #nome da unidade curricular que o docente vai dar aulas.
            nomeUnidadeCurricular = UnidadeCurricular.objects.get(turma__id__exact=servDocente.turma_id).nome
            #todas a reduções de serviço referentes ao docente
            reducao = ReducaoServicoDocente.objects.filter(docente_id__exact=nrDocente)
            #se o tamanho for 0 é porque nao existem reduções
            if len(reducao) == 0 :
                #nao faz nada
                pass
            else:
                #obtem o ID da redução
                reducaoId = ReducaoServicoDocente.objects.get(docente_id__exact=nrDocente).reducao_id
                #print "reducao id - ", reducaoId
                #obtem o numero de horas de redução
                reducaoHoras = Reducao.objects.get(id__exact=reducaoId).horas
                pass
            
            #print "docente_n _ ", reducao
            #incrementa as horas de serviço
            horasServico += servDocente.horas
            numeroTotalHoras = horasServico + reducaoHoras
            lista.append((servDocente.docente_id, nomeUnidadeCurricular,
                           servDocente.horas, reducaoHoras))
    numeroTotalTurmas = len(lista)   
    #print "dsfdf - ", reducaoHoras
    return render_to_response("docentes/index.html",
        locals(),
        context_instance=RequestContext(request),
        )

    
#Página de apresentação das turmas a que os Docentes pertencem
@login_required(redirect_field_name='Teste_home')
def turmasDocentes(request):    
    nomeDocente = request.session['nomeDocente']
    nrDocente = request.session['nr_Docente']
    servicoDocente = ServicoDocente.objects.all()
    unidadesCurriculares = UnidadeCurricular.objects.all()
    lista = []
    for servDocente in servicoDocente:
        if servDocente.docente_id ==  nrDocente:
            #nome da unidade curricular que o docente vai dar aulas.
            nomeUnidadeCurricular = UnidadeCurricular.objects.get(turma__id__exact=servDocente.turma_id).nome
            nomeCurso = UnidadeCurricular.objects.get(turma__id__exact=servDocente.turma_id).curso       
            lista.append((servDocente.docente_id, nomeUnidadeCurricular, nomeCurso))
    return render_to_response("docentes/turmaDocente.html",
        locals(),
        context_instance=RequestContext(request),
        )    
    
#Página de apresentação das horas de serviço pertencente a cada Docente
@login_required(redirect_field_name='Teste_home')
def horasServico(request):
    nomeDocente = request.session['nomeDocente']
    nrDocente = request.session['nr_Docente']  
    servicoDocente = ServicoDocente.objects.all()
    unidadesCurriculares = UnidadeCurricular.objects.all()
    lista = []
    #numero total de horas que o docente tem de serviço
    numeroTotalHoras = 0
    for servDocente in servicoDocente:
        if servDocente.docente_id ==  nrDocente:
            #nome da unidade curricular que o docente vai dar aulas.
            nomeUnidadeCurricular = UnidadeCurricular.objects.get(turma__id__exact=servDocente.turma_id).nome
            nomeCurso = UnidadeCurricular.objects.get(turma__id__exact=servDocente.turma_id).curso
            numeroTotalHoras +=servDocente.horas       
            lista.append((servDocente.docente_id, nomeUnidadeCurricular,
                           servDocente.horas, nomeCurso))
              
    return render_to_response("docentes/horasServico.html",
        locals(),
        context_instance=RequestContext(request),
        )
    
'''
Fim das vistas dos docentes
'''    


'''
Inicio das vistas dos Recursos Humanos
''' 
@login_required(redirect_field_name='Teste_home')
def indexRecursosHumanos(request):
    
    allDocentes = Docente.objects.all()
    listaDocentes = []
    actualState = ""
    print "get - ", request.GET
    
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
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente])
        else:
            finalkeyword = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
          
            for docente in allDocentes:
                
                nomeDocente = unicodedata.normalize('NFKD', docente.nome_completo.lower()).encode('ASCII', 'ignore')
                if nomeDocente.find(finalkeyword) != -1:
                    
                    departamento_id = docente.departamento_id
                    departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                    id_Docente = docente.id
                    listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente])
                    
                else:
                    pass 
    elif "departamento" in request.GET:
        
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
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente])
        
        pass
    elif 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"
        for docente in allDocentes:
                
                departamento_id = docente.departamento_id
                departamentoNome = Departamento.objects.get(id__exact=departamento_id).nome
                id_Docente = docente.id
                listaDocentes.append([docente.nome_completo, departamentoNome, id_Docente])
        pass
    
        
        
        
        
    
    paginator = Paginator(listaDocentes, 10)
    drange = range( 1, paginator.num_pages + 1)
    alfabeto = map(chr , range(65, 91))
    
    page = request.GET.get('page')
     
    try:
        docentes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        docentes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        docentes = paginator.page(paginator.num_pages)
        
    return render_to_response("recursosHumanos/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass



@login_required(redirect_field_name='Teste_home')
def indexRHInfoDocentes(request, id_docente):
    docenteX = Docente.objects.get(id__exact=id_docente)
    print "DOCENTE ---", docenteX
    
    return render_to_response("recursosHumanos/infoDocente.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass



@login_required(redirect_field_name='Teste_home')
def addDocenteRH(request):
    if request.method == 'POST': # If the form has been submitted...
        form = AddDocenteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = AddDocenteForm() # An unbound form
    
    return render_to_response("recursosHumanos/addDocente.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass


'''
Fim das vistas dos Recursos Humanos
'''

'''
Inicio das vistas dos Serviços de Planeamento
''' 
@login_required(redirect_field_name='Teste_home')
def indexServicoPlaneamento(request):
    return render_to_response("servicosPlaneamento/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

'''
Fim das vistas dos Serviços de Planeamento
'''


# vista para a criação automática de todas as distribuições
# de serviço docente iniciais para um determinado ano lectivo
def apagar_turmas(request, ano):
    Turma.objects.all().delete()
    return HttpResponse("Apagar {0}".format(ano))
    

# vista para a criação automática de todas as distribuições
# de serviço docente iniciais para um determinado ano lectivo
def criar_turmas(request, ano):
    '''
    criar o serviço docente para um determinado ano
    '''
    # formar um dicionário de objetos e tipos de aula
    dict_tipos_aula = dict()
    tipos = TipoAula.objects.all()

    for tipo in tipos:
        dict_tipos_aula[tipo.tipo] = tipo
        pass

    # com o ano seleccionado devemos criar as turmas
    # para todos os cursos
    # em primeiro lugar deve buscar-se a lista de cursos
    # todos_os_cursos = Curso.objects.all()

    tudo = 'YEP'
     
    unidades_curriculares = UnidadeCurricular.objects.all()
    for uc in unidades_curriculares:
        tipos_aula = []
        if uc.horas_lei_tp > 0.0:
            tipos_aula.append((dict_tipos_aula['TP'],
                               uc.horas_lei_tp))
            pass
        if uc.horas_lei_t > 0.0:
            tipos_aula.append((dict_tipos_aula['T'],
                               uc.horas_lei_t))
            pass
        if uc.horas_lei_pl > 0.0:
            tipos_aula.append((dict_tipos_aula['PL'],
                               uc.horas_lei_pl))
            pass
        if uc.horas_lei_tc > 0.0:
            tipos_aula.append((dict_tipos_aula['TC'],
                               uc.horas_lei_tc))
            pass
        if uc.horas_lei_s > 0.0:
            tipos_aula.append((dict_tipos_aula['S'],
                               uc.horas_lei_s))
            pass
        if uc.horas_lei_e > 0.0:
            tipos_aula.append((dict_tipos_aula['E'],
                               uc.horas_lei_e))
            pass
        if uc.horas_lei_ot > 0.0:
            tipos_aula.append((dict_tipos_aula['OT'],
                               uc.horas_lei_ot))
            pass
        if uc.horas_lei_o > 0.0:
            tipos_aula.append((dict_tipos_aula['O'],
                               uc.horas_lei_o))
            pass
        
        for tipo_aula, horas in tipos_aula:
            nova_turma = Turma(ano=ano,
                               turno='A',
                               unidade_curricular=uc,
                               tipo_aula=tipo_aula,
                               horas=horas)
            
            nova_turma.save()
            pass
        pass
    
    return HttpResponse("Criar turmas {0} {1}".format(ano, tudo))
                                                     
# vista para a criação automática de todas as distribuições
# de serviço docente iniciais para um determinado ano lectivo
def criar_servico(request, ano):
    turmas = Turma.objects.all()
    nada = ''
    lista_servicos = []
    
    for turma in turmas:
        if turma.tipo_aula.tipo == 'PL':
            novo_servico = ServicoDocente(turma=turma,
                                          horas=turma.unidade_curricular.horas_lei_pl)
            #nada += 'PL '
            pass
        if turma.tipo_aula.tipo == 'TP':
            novo_servico = ServicoDocente(turma=turma,
                                          horas=turma.unidade_curricular.horas_lei_tp)
            #nada += 'TP '
            pass
        if turma.tipo_aula.tipo == 'T':
            novo_servico = ServicoDocente(turma=turma,
                                          horas=turma.unidade_curricular.horas_lei_t)
            #nada += 'T '
            pass
        if turma.tipo_aula.tipo == 'TC':
            novo_servico = ServicoDocente(turma=turma,
                                          horas=turma.unidade_curricular.horas_lei_tc)
            #nada += 'TC '
            pass
        if turma.tipo_aula.tipo == 'E':
            novo_servico = ServicoDocente(turma=turma,
                                          horas=turma.unidade_curricular.horas_lei_e)
            #nada += 'E '
            pass
        if turma.tipo_aula.tipo == 'OT':
            novo_servico = ServicoDocente(turma=turma,
                                          horas=turma.unidade_curricular.horas_lei_ot)
            #nada += 'OT '
            pass
        if turma.tipo_aula.tipo == 'S':
            novo_servico = ServicoDocente(turma=turma,
                                          horas=turma.unidade_curricular.horas_lei_s)
            #nada += 'S '
            pass
        if turma.tipo_aula.tipo == 'O':
            novo_servico = ServicoDocente(turma=turma,
                                          horas=turma.unidade_curricular.horas_lei_o)
            #nada += 'O '
            pass
        lista_servicos.append(novo_servico)
        
        pass

    for servico in lista_servicos:
        servico.save()
        pass
    nada = str(len(lista_servicos))
    return HttpResponse("Criar serviços {0} {1}".format(ano, nada))

def apagar_servico(request, ano):
    ServicoDocente.objects.all().delete()
    return HttpResponse("Apagar {0}".format(ano))

def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
        pass
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

# código experimental
def search_form(request):
    return render_to_response('search_form.html')

def search(request):
    error = False
    if 'q' in request.GET: # and request.GET['q']:
        q = request.GET['q']
        if not q:
            error = True
        else:
            docentes = Docente.objects.filter(nome_completo__icontains=q)
            contagem = len(docentes)
            return render_to_response('search_results.html',
                                      {'docentes': docentes, 
                                       'query': q,
                                       'contagem': contagem})
        pass

    return render_to_response('search_form.html',
                              {'error': error})

# código para experimentar posteriormente
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form
        pass

    return render_to_response('contact.html', {
                'form': form,
                })

