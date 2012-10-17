# -*- coding: utf-8 -*-
'''
Created on 15 de Out de 2012

@author: admin1
'''
from distro.models import Turma, ServicoDocente, Docente, UnidadeCurricular
from django import forms
from django.core.context_processors import request
from django.forms.models import ModelForm



class AdicionarServicoDocenteForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        id_D = kwargs.pop('id_Departamento')
        ano = kwargs.pop('ano')
        super(AdicionarServicoDocenteForm, self).__init__(*args, **kwargs)
        
        
        #self.fields['turma'] = forms.ModelChoiceField(
        #                Turma.objects.filter(unidade_curricular__departamento_id__exact = id_Departamento).filter(ano = ano)
        #                )
        self.fields['docente'] = forms.ModelChoiceField(Docente.objects.filter(departamento_id__exact = id_D),
                                          widget = forms.Select(attrs = {'onchange':'testeSearch();'}))
        self.fields['horas'] = forms.CharField(widget=forms.TextInput(attrs={ 'readonly': 'readonly' }))
        

    class Meta:
        model = ServicoDocente
        exclude = ('turma',)
    pass