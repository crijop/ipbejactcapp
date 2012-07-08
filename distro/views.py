# -*- coding: utf-8 -*-

# Create your views here.
from django.http import HttpResponse
from django import forms

from distro.models import Curso
from distro.models import Turma
from distro.models import UnidadeCurricular
from distro.models import TipoAula
from distro.models import ServicoDocente

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
