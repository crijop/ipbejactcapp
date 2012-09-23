# -*- coding: utf-8 -*-
'''
Created on 20 de Set de 2012


@author: admin1
'''




from distro.models import Departamento, Docente
from django import forms
from django.forms.models import ModelForm


class AddDocenteForm(forms.Form):
    nome_completo     = forms.CharField(max_length=300)
                                         
    
    departamento      = forms.ModelChoiceField(queryset=Departamento.objects.all())


    # escalao de vencimento do docente
    escalao           = forms.IntegerField()


    regime_exclusividade = forms.BooleanField(required=False)


    email = forms.EmailField()
    
    abreviatura       = forms.CharField()


    # foto = forms.ImageField()
    
    
class EditarDocenteForm(ModelForm):
    class Meta:
        model = Docente
