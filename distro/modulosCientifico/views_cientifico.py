# -*- coding: utf-8 -*-
'''
Created on 23/04/2014

@author: Carlos Rijo Palma
@author: António Urbano Baião
'''
from distro.Forms.form_extra import ComboxAno
from distro.models import CursosAno, Ano, UC_Ano, Curso, Turma, Departamento, \
    UnidadeCurricular, Categoria, Docente, Modulos, Contrato, TipoAula
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query_utils import Q
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

# Informação de um determinado Curso
@login_required(redirect_field_name = 'login_redirectUsers')
@cientificoUserTeste
def informacao_Curso(request, *args, **kwargs):
    curso_id = kwargs['curso']
    curso = Curso.objects.get(id = curso_id)
    return render_to_response("cientifico_new/info_curso.html",
        locals(),
        context_instance = RequestContext(request),
        )

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


# Informação de uma determinada Unidade Curricular
@login_required(redirect_field_name = 'login_redirectUsers')
@cientificoUserTeste
def informacao_UC(request, *args, **kwargs):
    uc_id = kwargs['uc_id']
    uc = UnidadeCurricular.objects.get(id = uc_id)
    
    return render_to_response("cientifico_new/info_uc.html",
        locals(),
        context_instance = RequestContext(request),
        )
    
    

'''
listDocentes - Mostra todos os Docentes e as horas que ainda tem por atribuir
e o numero de turmas a que tão associados e o numero de horas que ja tem atribuidas
'''
@login_required(redirect_field_name = 'login_redirectUsers')
@cientificoUserTeste
def listDocentes(request, *args, **kwargs):
    
    listaAnos = Ano.objects.all()  # listarAnos(id_Departamento)
    allCategories = Categoria.objects.all()
    actualState = ""

    listToSend = []

    listDocentes = Docente.objects.all()

    if "category" in request.GET or request.GET.get("actualState") == "category":
        keyword = request.GET.get("category")
        actualState = "actualState=category&category=" + keyword
        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
         
        for docente in listDocentes:
            # listServicoTemp = ServicoDocente.objects.filter(docente_id__exact=docente.id)
            listServicoTemp = Modulos.objects.filter(docente_id__exact = docente.id)
             
            id_Docente = docente.id
            numberHoras = 0
            for h in listServicoTemp:
                numberHoras += h.horas
            try:
                contrato = Contrato.objects.get(docente__id = id_Docente)
                contract_end = contrato.data_fim.strftime("%d/%m/%Y")
                nomeCategoria = Categoria.objects.get(id__exact = contrato.categoria.id).nome
            except ObjectDoesNotExist:
                nomeCategoria = u'Sem Categoria'
             
            nomeCategoria_final = unicodedata.normalize('NFKD', nomeCategoria.lower()).encode('ASCII', 'ignore')
  
            if nomeCategoria_final == letter:
                listToSend.append([docente.id, docente.nome_completo, len(listServicoTemp), numberHoras])
        sizeList = len(listToSend)


#  
#     elif "letra" in request.GET or request.GET.get("actualState") == "letra":
#  
#        keyword = request.GET.get("letra")
#        actualState = "actualState=letra&letra=" + keyword
#        letter = unicodedata.normalize('NFKD', keyword.lower()).encode('ASCII', 'ignore')
#  
#  
#        for docente in listDocentes:
#            nomeDocente = unicodedata.normalize('NFKD', docente.nome_completo.lower()).encode('ASCII', 'ignore')
#  
#            if nomeDocente.startswith(letter):
#                # listServicoTemp = ServicoDocente.objects.filter(docente_id__exact=docente.id)
#                listServicoTemp = Modulos.objects.filter(docente_id__exact = docente.id)
#                numberHoras = 0
#                for h in listServicoTemp:
#                    numberHoras += h.horas
#                pass
#                listToSend.append([docente.id, docente.nome_completo, len(listServicoTemp), numberHoras])
#        sizeList = len(listToSend)
#              
#  
#        pass
#      
#     elif "docExcedHours" in request.GET or request.GET.get("actualState") == "docExcedHours":
#        chave = request.GET.get("docExcedHours")
#        ano = request.GET.get("ano")
#        actualState = "actualState=docExcedHours&docExcedHours=" + chave + "&ano=" + ano
#        MAXIMO_HORAS = 360 
#        listaDocentesDepartamento = Docente.objects.filter(departamento_id__exact = id_Departamento)
#        horasTemp = 0 
#        nrDocExcedHoras = 0
#        nrDocSemHoras = 0
#          
#        if chave == "True":
#            for l in listaDocentesDepartamento:
#                horasTemp = 0
#                listServicoTemp = Modulos.objects.filter(servico_docente__turma__ano__exact = ano)\
#                                                     .filter(docente_id__exact = l.id)
#                for m in listServicoTemp:
#                    horasTemp += m.horas
#                    pass
#                if horasTemp == 0:
#                    listToSend.append([l.id, l.nome_completo, len(listServicoTemp), horasTemp])
#                    nrDocSemHoras += 1
#                    pass
#            pass
#              
#        elif chave == "False":
#            for l in listaDocentesDepartamento:
#                horasTemp = 0
#                listServicoTemp = Modulos.objects.filter(servico_docente__turma__unidade_curricular__departamento_id__exact\
# = id_Departamento, servico_docente__turma__ano__exact = ano)\
#                                                     .filter(docente_id__exact = l.id)
#                for m in listServicoTemp:
#                    horasTemp += m.horas
#                    pass
#                if horasTemp > MAXIMO_HORAS: 
#                    listToSend.append([l.id, l.nome_completo, len(listServicoTemp), horasTemp])
#                    nrDocExcedHoras += 1
#                    pass
#            pass
#        sizeList = len(listToSend)
#        pass
#===============================================================================
    
    if 'show' in request.GET or request.GET == {} or request.GET.get("actualState") == "show":
        actualState = "actualState=show"

        for docente in listDocentes:
            print docente.nome_completo
            listServicoTemp = Modulos.objects.filter(docente_id__exact = docente.id)
            numberHoras = 0
            for h in listServicoTemp:
                numberHoras += h.horas
            listToSend.append([docente.id, docente.nome_completo, len(listServicoTemp), numberHoras])
        sizeList = len(listToSend)

    
    print sizeList
    print listToSend
    return render_to_response("cientifico_new/listarDocentes.html",
        locals(),
        context_instance = RequestContext(request),
        )


# View responsavel por representar a informação de um 
# determinado docente. o metodo recebe o id_docente em questão
# só vai entrar nesta view se o utilizador estiver autenticado
# e se pertencer ao grupo de Departamento.
@login_required(redirect_field_name = 'login_redirectUsers')
@cientificoUserTeste
def infoDocente_cientifico(request, *args, **kwargs):
    id_docente = kwargs['id_docente']
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
    
    servicoDocente = Modulos.objects.filter(Q(docente_id__exact = id_docente), Q(servico_docente__turma__ucAno__cursosAno__ano__id__exact = ano_selected))
    
    unidadesCurriculares = UnidadeCurricular.objects.all()

    docente_name = Docente.objects.get(id__exact = id_docente).nome_completo

    lista = []
   
    horasTotal = 0
    for servDocente in servicoDocente:

        print "#################################"
        print servDocente.servico_docente.turma.ucAno.cursosAno.ano.id
        print servDocente.servico_docente.turma.unidade_curricular_id
        print "#################################"
        # nome da unidade curricular que o docente vai dar aulas.
        nomeUnidadeCurricular = UnidadeCurricular.objects.get(id__exact = servDocente.servico_docente.turma.unidade_curricular_id).nome
        turma = Turma.objects.get(id__exact = servDocente.servico_docente.turma_id)
        tipoAula = TipoAula.objects.get(id__exact = turma.tipo_aula_id).tipo
        turno = turma.turno
        nomeCurso = UnidadeCurricular.objects.get(turma__id__exact = servDocente.servico_docente.turma_id).curso
        horasTotal += servDocente.horas
        lista.append((servDocente.docente_id, nomeUnidadeCurricular,
                           servDocente.horas, nomeCurso))
    
    return render_to_response("cientifico_new/horasServico.html",
        locals(),
        context_instance = RequestContext(request),
        )
