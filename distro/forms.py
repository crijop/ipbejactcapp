# -*- coding: utf-8 -*-
'''
Created on 20 de Set de 2012


@author: admin1
'''




from distro.models import Departamento, Docente
from django import forms
from django.contrib.formtools.preview import FormPreview
from django.core.context_processors import request
from django.forms.models import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.defaultfilters import default


class AddDocenteForm(forms.Form):
    nome_completo     = forms.CharField(max_length=300, label=u'Nome Completo')
                                         
    
    departamento      = forms.ModelChoiceField(queryset=Departamento.objects.all())


    # escalao de vencimento do docente
    escalao           = forms.IntegerField(required=False, initial= 100)


    regime_exclusividade = forms.BooleanField(required=False, initial = True)


    email = forms.EmailField(required = False, label=u'Email Institucional')
    
    abreviatura       = forms.CharField()


    # foto = forms.ImageField()
    
    
class EditarDocenteForm(ModelForm):
    nome_completo     = forms.CharField(max_length=300, label=u'Nome Completo')
    email = forms.EmailField(required = False, label=u'Email Institucional')
    abreviatura       = forms.CharField()
    class Meta:
        model = Docente
        
        def save(self, commit=True):
            docente = super(EditarDocenteForm, self).save(commit=False)    
            if commit:
                docente.save()
    
            return docente
            
