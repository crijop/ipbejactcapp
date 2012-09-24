# -*- coding: utf-8 -*-
'''
Created on 20 de Set de 2012


@author: admin1
'''




from distro.models import Departamento, Docente
from django import forms
from django.forms.models import ModelForm
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
    class Meta:
        model = Docente
