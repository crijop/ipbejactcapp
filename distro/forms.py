# -*- coding: utf-8 -*-
'''
Created on 20 de Set de 2012


@author: admin1
'''
from distro.models import Departamento, Docente
from django import forms
from django.forms.models import ModelForm
from django.forms.widgets import Widget



class AddDocenteForm(forms.Form):
    nome_completo     = forms.CharField(max_length=300, label=u'Nome Completo')
    departamento      = forms.ModelChoiceField(queryset=Departamento.objects.all())
    escalao           = forms.IntegerField(required=False, initial= 100)
    regime_exclusividade = forms.BooleanField(required=False, initial = True)
    email = forms.EmailField(required = False, label=u'Email Institucional')
    abreviatura       = forms.CharField()

#Class que apresenta o formulário para
#adicionar o docente
class AdicionarDocenteForm(ModelForm):
    #widget=forms.TextInput(attrs={ 'required': 'true' })
    nome_completo     = forms.CharField(max_length=300, label=u'Nome Completo')
    email = forms.EmailField(required = False, label=u'Email Institucional')
    abreviatura       = forms.CharField()
    
    class Meta:
        model = Docente

#Class que apresenta o formulário para
#editar o docente
class EditarDocenteForm(ModelForm):
    nome_completo     = forms.CharField(max_length=300, label=u'Nome Completo')
    email = forms.EmailField(required = False, label=u'Email Institucional')
    abreviatura       = forms.CharField()
    
    #Para evitar que o django faça a 
    #validação do formulario aos campos que são unicos
    #No formulário para editar o docente
    #essa validação não faz sentido, porque podemos editar 
    #o docente sem alterar os campos unique
    def validate_unique(self):        
        pass
    
    
    class Meta:
        model = Docente
        
        '''
        def save(self, commit=True):
            docente = super(EditarDocenteForm, self).save(commit=False)    
            if commit:
                docente.save()
    
            return docente
        '''
