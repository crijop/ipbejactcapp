# -*- coding: utf-8 -*-
'''
Created on 15 de Out de 2012

@author: admin1
'''
from django import forms
from distro.models import Departamento, ServicoDocente
from django.forms.models import ModelForm



class AdicionarServicoDocenteForm(ModelForm):
    #widget=forms.TextInput(attrs={ 'required': 'true' })
    '''
    nome_completo     = forms.CharField(max_length=300, label=u'Nome Completo')
    email = forms.EmailField(required = False, label=u'Email Institucional')
    abreviatura       = forms.CharField()
    
    departamento = forms.ModelChoiceField(Departamento.objects.all(),
                                          widget = forms.Select(attrs = {'onchange':'testeSearch();'}))

    regime_exclusividade = forms.BooleanField(required=False, initial = True, 
                                              widget=forms.CheckboxInput(attrs={'onchange':'testeSearch();'}))
    '''
    class Meta:
        model = ServicoDocente
    pass